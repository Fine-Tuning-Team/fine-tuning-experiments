# Run 003 - Qwen2.5 - Choreo Docs

This is an experimentation run for Choreo Docs domain knowledge adaptation using the `Qwen2.5-Instruct` model on Kaggle with T4 GPU.

## Information
- **Model :** unsloth/Qwen2.5-7B-Instruct-unsloth-bnb-4bit
- **Fine-tuning method :** Low Rank Adaptation (LoRA)
- **Library Used :** Unsloth
- **Dataset used :** https://huggingface.co/datasets/rtweera/choreo-dataset-fixed-leakage
- **HF Model Card :** https://huggingface.co/rtweera/2025-May-22_12-10-49_Qwen2.5-3B-Instruct-unsloth-bnb-4bit_LoRA

## Instructions

- **Works in Kaggle**

- **Update secrets in the Kaggle environment:**
    - Set your Hugging Face token.
    - Set your Weights & Biases (wandb) organization name and API token.

- **Model Versioning:**  
    Ensure you properly version fine-tuned models before pushing them to Hugging Face.
