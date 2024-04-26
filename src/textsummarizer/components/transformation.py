from dataclasses import dataclass
from pathlib import Path
import os
from datasets import load_dataset, load_from_disk
from transformers import AutoTokenizer
from textsummarizer.logging import logger

@dataclass(frozen=True)
class DataTransformation:
    root_dir: Path
    data_path: Path
    tokenizer_name: str
    do_train: bool = True
    do_eval: bool =  True
    do_predict: bool = True
    text_column: str = "dialogue"
    summary_column: str = "summary"
    max_source_length: int = 1024
    max_target_length: int = 128
    padding: bool = False
    ignore_pad_token_for_loss: bool = False

    def convert(self):
        samsum_dataset = load_from_disk(self.data_path)
        column_names = samsum_dataset.column_names
        if self.do_train:
            train_dataset = samsum_dataset["train"]
            tokenized_train_datasets  = train_dataset.map(
                            self.preprocess_function,
                            batched=True,
                            remove_columns=column_names['train'],
                            desc="Running tokenizer on train dataset",
                        )
            tokenized_train_datasets.save_to_disk(os.path.join(self.root_dir,"train"))

        if self.do_eval:
            validation_dataset = samsum_dataset["validation"]
            tokenized_val_datasets  = validation_dataset.map(
                self.preprocess_function,
                batched=True,
                remove_columns=column_names['validation'],
                desc="Running tokenizer on validation dataset",
            )
            tokenized_val_datasets.save_to_disk(os.path.join(self.root_dir,"validation"))

        if self.do_predict:
            test_dataset = samsum_dataset["test"]
            tokenized_test_datasets  = test_dataset.map(
                self.preprocess_function,
                batched=True,
                remove_columns=column_names['test'],
                desc="Running tokenizer on test dataset",
            )
            tokenized_test_datasets.save_to_disk(os.path.join(self.root_dir,"test"))

    def preprocess_function(self, examples):
        # remove pairs where at least one record is None
        tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)

        inputs, targets = [], []
        for i in range(len(examples[self.text_column])):
            if examples[self.text_column][i] and examples[self.summary_column][i]:
                inputs.append(examples[self.text_column][i])
                targets.append(examples[self.summary_column][i])

        model_inputs = tokenizer(inputs, max_length=self.max_source_length, padding=self.padding, truncation=True)

        # Tokenize targets with the `text_target` keyword argument
        labels = tokenizer(text_target=targets, max_length=self.max_target_length, padding=self.padding, truncation=True)

        # If we are padding here, replace all tokenizer.pad_token_id in the labels by -100 when we want to ignore
        # padding in the loss.
        if self.padding == "max_length" and self.ignore_pad_token_for_loss:
            labels["input_ids"] = [
                [(l if l != tokenizer.pad_token_id else -100) for l in label] for label in labels["input_ids"]
            ]

        model_inputs["labels"] = labels["input_ids"]
        return model_inputs
    