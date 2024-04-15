from dataclasses import dataclass
from pathlib import Path
import os
from transformers import TrainingArguments, Trainer
from transformers import DataCollatorForSeq2Seq
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from datasets import  load_from_disk
import torch

@dataclass(frozen=True)
class ModelTrainer:
    """
    Configuration for the model trainer.

    Attributes:
    - root_dir (Path): The root directory for the model trainer.
    - data_path (Path): The path to the data.
    - model_ckpt (str): The model checkpoint.
    - num_train_epochs (int): Number of training epochs.
    - warmup_steps (int): Number of warmup steps.
    - per_device_train_batch_size (int): Batch size per device for training.
    - per_device_eval_batch_size (int): Batch size per device for evaluation.
    - weight_decay (float): Weight decay for the optimizer.
    - logging_steps (int): Log training metrics at this interval.
    - evaluation_strategy (str): Strategy for evaluation (e.g., "steps" or "epoch").
    - eval_steps (int): Evaluation steps.
    - save_steps (float): Save model checkpoint at this interval.
    - gradient_accumulation_steps (int): Number of steps for gradient accumulation.
    """

    root_dir: Path 
    data_path: Path
    model_ckpt: str
    num_train_epochs: int = 1
    warmup_steps: int = 500
    per_device_train_batch_size: int = 1
    per_device_eval_batch_size: int = 1
    weight_decay: float = 0.01
    logging_steps: int = 10
    evaluation_strategy: str = 'steps'
    eval_steps: int = 500
    save_steps: float = 1e6
    gradient_accumulation_steps: int = 16

    def train(self):
        """
        Train the model using the specified configuration.

        This method loads the tokenizer and model, configures the trainer arguments, initializes the trainer,
        starts the training, and saves the trained model and tokenizer.
        
        """
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(self.model_ckpt)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.model_ckpt).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)

        # Load dataset
        dataset_samsum_pt = load_from_disk(self.data_path)

        # Configure trainer arguments
        trainer_args = TrainingArguments(
            output_dir=self.root_dir,
            num_train_epochs=self.num_train_epochs,
            warmup_steps=self.warmup_steps,
            per_device_train_batch_size=self.per_device_train_batch_size,
            per_device_eval_batch_size=self.per_device_train_batch_size,
            weight_decay=self.weight_decay, logging_steps=self.logging_steps,
            evaluation_strategy=self.evaluation_strategy,
            eval_steps=self.eval_steps, save_steps=1e6,
            gradient_accumulation_steps=self.gradient_accumulation_steps
        ) 

        # Initialize trainer
        trainer = Trainer(model=model_pegasus, args=trainer_args,
                  tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                  train_dataset=dataset_samsum_pt["train"], 
                  eval_dataset=dataset_samsum_pt["validation"])
        
        # Start training
        trainer.train()

        # Save trained model and tokenizer
        model_pegasus.save_pretrained(os.path.join(self.root_dir,"pegasus-samsum-model"))
        tokenizer.save_pretrained(os.path.join(self.root_dir,"tokenizer"))
