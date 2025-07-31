# Fine tuning a code completion model for Ballerina

## Details

- Runtime: Run locally the data preparation and then use Google Colab with TPU (Tensor Processing Units) for training
- Model selected: [Qwen/Qwen2.5-Coder-0.5B](https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B)
- Dataset: [Several Repos from the Ballerina-Platform](https://github.com/orgs/ballerina-platform/repositories)
- About the dataset: The dataset consists of various code snippets and examples from the Ballerina programming language repositories, aimed at improving code completion tasks.
- Method: LoRA
- Process: Follow the steps in the notebook.

> **NOTE**: `curate_dataset.py` was used to create a dataset from the ballerina files. `format_dataset.py` was used to format the curated dataset into the format we need for training. Other two `.py` files are supporting files for these two scripts.