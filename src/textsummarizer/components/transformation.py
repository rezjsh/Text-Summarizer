from dataclasses import dataclass
from pathlib import Path
import os
from datasets import load_dataset, load_from_disk
from transformers import AutoTokenizer
from textsummarizer.logging import logger

@dataclass()
class DataTransformation:
    root_dir: Path
    data_path: Path
    tokenizer_name: str

    def __post_init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_name)


    def preprocess_function(self,example_batch):
            input_encodings = self.tokenizer(example_batch['dialogue'] , max_length = 1024, truncation = True )
            
            with self.tokenizer.as_target_tokenizer():
                target_encodings = self.tokenizer(example_batch['summary'], max_length = 128, truncation = True )
                
            return {
                'input_ids' : input_encodings['input_ids'],
                'attention_mask': input_encodings['attention_mask'],
                'labels': target_encodings['input_ids']
            }
        

    def convert(self):
        dataset_samsum = load_from_disk(self.data_path)
        dataset_samsum_pt = dataset_samsum.map(self.preprocess_function, batched = True)
        dataset_samsum_pt.save_to_disk(os.path.join(self.root_dir,"samsum_dataset"))