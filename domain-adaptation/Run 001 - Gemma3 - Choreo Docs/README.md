# Run 001 - Gemma3 - Choreo Docs

This is an experimentation run for Choreo Docs domain knowledge adaptation using the `gemma3-4b-it` model on Google Colab.

## Information
- **Model :** unsloth/gemma-3-4b-it | google/gemma-3-4b-it
- **Fine-tuning method :** Low Rank Adaptation (LoRA)
- **Library Used :** Unsloth
- **Dataset used :** rtweera/simple_implicit_n_qa_results_v2
- **Dataset Size :** 194
- **HF Model Card :** lukepramo221/lukepramo221/gemma-3-4b-finetuned_choreo-qna_full_v0.1

## Instructions

- **Use only with Google Colab.**  
    Not supported with Kaggle.

- **Update environment variables in the Colab environment:**
    - Set your Hugging Face token.
    - Set your Weights & Biases (wandb) organization name and API token.

- **Model Versioning:**  
    Ensure you properly version fine-tuned models before pushing them to Hugging Face.

- **RAGAS Evaluator:**
    You can run RAGAS evaluator code on any VM without GPU. Make sure to put the environment variables as needed.

## Evaluation results

All evaluation results for Gemma3 based fine tuning rns are available in the following Google Sheet.

Link : [Google Sheets](https://docs.google.com/spreadsheets/d/1KZn_YtTTuxMAKvPhgGUCArjlBMRYK7k-hgWdNCtvhhM/edit?usp=sharing)