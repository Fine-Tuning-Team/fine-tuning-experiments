# KTO Training for alignment with human feedback

## Details

- Runtime: Run on google colab with T4 GPU
- Model selected: [Qwen2.5-1.5B-Instruct](https://huggingface.co/unsloth/Qwen2.5-1.5B-Instruct)
- Dataset: [KTO-MIX](https://huggingface.co/datasets/trl-lib/kto-mix-14k)
- About the dataset: The dataset is a mix of 14k binary human feedback data, which includes various types of instructions and responses. For each question and response, there is a binary label indicating whether the response is good or bad. The dataset is designed to train models to align with human feedback.
- Method: LoRA with KTO training
- Process: Follow the steps in the notebook.
