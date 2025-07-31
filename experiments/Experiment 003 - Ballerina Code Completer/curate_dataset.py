import datetime
import os
import random
import numpy as np
from sklearn.model_selection import train_test_split


class DatasetCurator:
    """Class to handle the curation of **raw** dataset files from `bal` files in `data-bal-files` directory."""

    def __init__(self):
        """Initialize paths, filenames, and configuration."""
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.repo_dir = os.path.normpath(os.path.join(self.script_dir, '..', 'data-bal-files'))
        self.output_dir = os.path.normpath(os.path.join(self.script_dir, '..', 'data', 'raw'))
        
        # Get the current date and time for unique filenames
        self.current_date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Output filenames
        self.dataset_output_file = f'dataset_{self.current_date_time}.txt'
        self.train_output_file = f'train_{self.current_date_time}.txt'
        self.val_output_file = f'val_{self.current_date_time}.txt'
        self.test_output_file = f'test_{self.current_date_time}.txt'
        
        # Configuration
        self.enable_train_val_test_split = False
        self.train_size = 0.8
        self.val_size = 0.1
        self.test_size = 0.1
        self.random_seed = 42

    def get_user_confirmation(self):
        """Get confirmation from the user before proceeding."""
        confirmation = input(f"""
Source directory: {self.repo_dir}
Output directory: {self.output_dir}
train_val_test split: {self.enable_train_val_test_split}

Proceed? (y/n): """).strip().lower()
        
        if confirmation != 'y':
            print("Exiting...")
            return False
        return True

    def validate_split_ratios(self):
        """Validate that the split ratios are valid."""
        if not (0 <= self.train_size <= 1 and 0 <= self.test_size <= 1 and 0 <= self.val_size <= 1):
            raise ValueError("Sizes must be between 0 and 1.")
        if round(self.train_size + self.test_size + self.val_size, 10) != 1.0:
            raise ValueError("Train, test, and validation sizes must add up to 1.")

    def set_random_seeds(self):
        """Set random seeds for reproducibility."""
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)

    def collect_bal_files(self):
        """Collect all .bal files from the repository."""
        print("=== Collecting all .bal files ===")
        bal_files = []
        for root, dirs, files in os.walk(self.repo_dir):
            for file in files:
                if file.endswith('.bal'):
                    bal_files.append(os.path.join(root, file))
        print(f"Total .bal files found: {len(bal_files)}")
        print("=== Finished collecting .bal files ===")
        return bal_files

    def split_dataset(self, bal_files):
        """Split the dataset into train, validation, and test sets."""
        print("=== Balancing the dataset ===")
        if self.enable_train_val_test_split:
            train_files, temp_files = train_test_split(bal_files, train_size=self.train_size, random_state=self.random_seed)
            val_files, test_files = train_test_split(temp_files, test_size=self.test_size/(self.test_size + self.val_size), random_state=self.random_seed)
        else:
            train_files = bal_files
            val_files = []
            test_files = []
            
        return train_files, val_files, test_files

    def read_files(self, file_list):
        """Read the contents of all files in the list."""
        return [open(file, 'r', encoding='utf-8').read() for file in file_list]

    def process_dataset(self):
        """Process the dataset: collect files, split, and read contents."""
        # Check if directories exist
        if not os.path.exists(self.repo_dir):
            raise FileNotFoundError(f"The directory {self.repo_dir} does not exist.")

        if not os.listdir(self.repo_dir):
            raise ValueError(f"The directory {self.repo_dir} is empty.")

        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Collect files
        bal_files = self.collect_bal_files()
        
        # Split dataset
        train_files, val_files, test_files = self.split_dataset(bal_files)
        
        # Read file contents
        print("=== Reading the dataset files ===")
        train_data = self.read_files(train_files)
        val_data = self.read_files(val_files)
        test_data = self.read_files(test_files)
        print("=== Finished reading the dataset files ===")
        
        if self.enable_train_val_test_split:
            print(f"Training files: {len(train_files)}, Validation files: {len(val_files)}, Test files: {len(test_files)}")
        else:
            print(f"Dataset files: {len(train_files)}")
            
        return train_data, val_data, test_data

    def save_datasets(self, train_data, val_data, test_data):
        """Save the datasets to output files."""
        print("=== Started writing the dataset ===")
        if self.enable_train_val_test_split:
            # Save the datasets to text files
            with open(os.path.join(self.output_dir, self.train_output_file), 'w', encoding='utf-8') as f:
                f.write('\n'.join(train_data))
            with open(os.path.join(self.output_dir, self.val_output_file), 'w', encoding='utf-8') as f:
                f.write('\n'.join(val_data))
            with open(os.path.join(self.output_dir, self.test_output_file), 'w', encoding='utf-8') as f:
                f.write('\n'.join(test_data))
        else:
            # Save the dataset to a single text file
            with open(os.path.join(self.output_dir, self.dataset_output_file), 'w', encoding='utf-8') as f:
                f.write('\n'.join(train_data))
        print("=== Finished writing the dataset ===")

    def run(self):
        """Main method to execute the dataset curation process."""
        # Get user confirmation
        if not self.get_user_confirmation():
            return
        
        # Validate split ratios
        self.validate_split_ratios()
        
        # Set random seeds
        self.set_random_seeds()
        
        # Process dataset
        train_data, val_data, test_data = self.process_dataset()
        
        # Save datasets
        self.save_datasets(train_data, val_data, test_data)


def main():
    """Entry point of the script."""
    curator = DatasetCurator()
    curator.run()


if __name__ == "__main__":
    main()
