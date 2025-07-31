# Fine tuning for reasoning

## Details

- Runtime: Run on colab with T4
- Model selected: [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B)
- Dataset: [Reasoning dataset](https://huggingface.co/datasets/unsloth/OpenMathReasoning-mini), [None reasoning dataset](https://huggingface.co/datasets/mlabonne/FineTome-100k)
- About the dataset: The reasoning dataset is a collection of math problems and their solutions with reasoning `<think>` blocks, while the None reasoning dataset contains various programming and other questions without reasoning steps.
- Method: LoRA
- Process: This notebook shows how to fine-tune a reasonining capable model with reasoning and non-reasoning datasets. By training on both datasets, we can turn the reasoning on or off (by passing an argument to the model when generating the inference) and get the model to work in both modes.
