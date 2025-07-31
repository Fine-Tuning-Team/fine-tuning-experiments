import json
import os
import re
from pprint import pprint
import regex_patterns 

from utils import get_most_recent_file_with_prefix


class DatasetFormatter:
    """Class for formatting already **curated** code datasets in `raw` directory into blocks and ChatML format."""

    def __init__(self, source_dir=None, output_dir=None, chatml_dir=None, enable_split=False):
        """Initialize the DatasetFormatter with directory paths and configuration."""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Set default paths if not provided
        self.source_dir = source_dir or os.path.normpath(os.path.join(script_dir, '..', 'data', 'raw'))
        self.output_dir = output_dir or os.path.normpath(os.path.join(script_dir, '..', 'data', 'block-formatted'))
        self.chatml_dir = chatml_dir or os.path.normpath(os.path.join(script_dir, '..', 'data', 'chatML'))
        self.enable_train_val_test_split = enable_split
        
        self.dataset_input_file = None
        self.train_input_file = None
        self.val_input_file = None
        self.test_input_file = None

    def prompt_confirmation(self):
        """Ask for user confirmation before proceeding."""
        prompt = f"""
Source directory: {self.source_dir}
Output directory: {self.output_dir}
train_val_test split: {self.enable_train_val_test_split}

Proceed? (y/n): """

        if input(prompt).strip().lower() != 'y':
            print("Exiting...")
            return False
        return True

    def setup_directories(self):
        """Check and create necessary directories."""
        # Check if the source directory exists
        if not os.path.exists(self.source_dir):
            raise FileNotFoundError(f"The directory {self.source_dir} does not exist.")

        # Check if the directory is empty
        if not os.listdir(self.source_dir):
            raise ValueError(f"The directory {self.source_dir} is empty.")

        # Create output directories if they don't exist
        for directory in [self.output_dir, self.chatml_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)

    def load_input_files(self):
        """Load the most recent dataset file paths."""
        print("=== Loading the most recent dataset files ===")
        self.dataset_input_file = get_most_recent_file_with_prefix(self.source_dir, 'dataset_')
        self.train_input_file = get_most_recent_file_with_prefix(self.source_dir, 'train_')
        self.val_input_file = get_most_recent_file_with_prefix(self.source_dir, 'val_')
        self.test_input_file = get_most_recent_file_with_prefix(self.source_dir, 'test_')

        # Validate file availability based on chosen mode
        if self.enable_train_val_test_split:
            if not (self.train_input_file and self.val_input_file and self.test_input_file):
                raise ValueError("Train, validation, and test files are required for splitting.")
        elif not self.dataset_input_file:
            raise ValueError("Dataset file is required for processing.")

    @staticmethod
    def extract_code_blocks(content):
        combined_pattern = regex_patterns.pattern
        blocks = re.findall(combined_pattern, content, re.DOTALL)
        return blocks

    @staticmethod
    def create_completion_pairs(code_blocks):
        """Generate input-output pairs for code completion."""
        pairs = []
        for block in code_blocks:
            lines = block.split('\n')
            # Take the first 1-2 lines as partial code (input)
            partial_code = '\n'.join(lines[:1]).strip()
            full_code = block.strip()
            pairs.append({
                "input": partial_code,
                "output": full_code
            })
        return pairs

    @staticmethod
    def format_chatml(pairs, output_file):
        """Convert input-output pairs to ChatML format and save as JSONL."""
        with open(output_file, 'w') as f:
            for pair in pairs:
                chatml_entry = {
                    "messages": [
                        {"role": "system", "content": "You are a Ballerina code completion assistant."},
                        {"role": "user", "content": f"Complete this Ballerina code:\n```ballerina\n{pair['input']}\n```"},
                        {"role": "assistant", "content": f"```ballerina\n{pair['output']}\n```"}
                    ]
                }
                f.write(json.dumps(chatml_entry) + '\n')

    def process_dataset(self):
        """Process the dataset based on configuration."""
        print("=== Extracting code blocks ===")
        
        if self.enable_train_val_test_split:
            # Process train/val/test files separately
            with open(self.train_input_file, 'r', encoding='utf-8') as f:
                train_data = f.read()
            with open(self.val_input_file, 'r', encoding='utf-8') as f:
                val_data = f.read()
            with open(self.test_input_file, 'r', encoding='utf-8') as f:
                test_data = f.read()
                
            raise NotImplementedError("Train, validation, and test files handling are not yet implemented.")
        else:
            # Process single dataset file
            return self._process_single_dataset()
            
    def _process_single_dataset(self):
        """Process a single dataset file and generate formatted outputs."""
        # Load and process the dataset file
        with open(self.dataset_input_file, 'r', encoding='utf-8') as f:
            all_data = f.read()
            all_data_blocks = self.extract_code_blocks(all_data)
            print(f"Total code blocks found: {len(all_data_blocks)}")

        # Save extracted code blocks
        print("=== Writing the extracted code blocks to file ===")
        blocks_filename = f'blocks_{os.path.basename(self.dataset_input_file)}.txt'
        blocks_output_file = os.path.join(self.output_dir, blocks_filename)
        with open(blocks_output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_data_blocks))
        print("=== Finished writing code blocks ===")

        # Create and save input-output pairs
        input_output_pairs = self.create_completion_pairs(all_data_blocks)
        print(f"Total input-output pairs created: {len(input_output_pairs)}")

        print("=== Writing the input-output pairs to file ===")
        chatml_filename = f'chat_{os.path.basename(self.dataset_input_file)}.jsonl'
        chatml_output_file = os.path.join(self.chatml_dir, chatml_filename)
        self.format_chatml(input_output_pairs, chatml_output_file)
        print("=== Finished writing input-output pairs ===")
        
        return {
            "blocks_file": blocks_output_file,
            "chatml_file": chatml_output_file,
            "block_count": len(all_data_blocks),
            "pair_count": len(input_output_pairs)
        }

    def run(self):
        """Execute the complete formatting pipeline."""
        if not self.prompt_confirmation():
            return False
            
        try:
            self.setup_directories()
            self.load_input_files()
            result = self.process_dataset()
            return result
        except Exception as e:
            print(f"Error processing dataset: {e}")
            return False


def main():
    """Main entry point for the script."""
    formatter = DatasetFormatter()
    result = formatter.run()
    
    if result:
        print("\n=== Processing Summary ===")
        print(f"Code blocks extracted: {result['block_count']}")
        print(f"Input-output pairs created: {result['pair_count']}")
        print(f"Blocks file: {result['blocks_file']}")
        print(f"ChatML file: {result['chatml_file']}")
        print("=== Process completed successfully ===")


if __name__ == "__main__":
    main()
