# Testing fine tuning process with base model with Alpaca dataset

## Details

- Runtime: Google Colab with T4 GPU
- Model selected: [Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B)
- Dataset: [alpaca-cleaned](https://huggingface.co/datasets/yahma/alpaca-cleaned)
- About the dataset: The Alpaca dataset is a collection of instruction-following examples designed to fine-tune language models for better performance on various tasks.
- Method: LoRA
- Process: Follow the steps in the notebook.

>**NOTE:** This is another way to do instruction fine tuning, compared to the previous experiment. However, in this method we changes the data format we input to the model. This can cause the model to be confused sometimes, and then it outputs gibberish or answers in improper format.
