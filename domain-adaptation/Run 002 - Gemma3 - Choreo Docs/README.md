# Run 001 - Gemma3 - Choreo Docs

This is an experimentation run for Choreo Docs domain knowledge adaptation using the `gemma3-4b-it` model on Google Colab.

## Information
- **Model :** unsloth/gemma-3-4b-it | google/gemma-3-4b-it
- **Fine-tuning method :** Low Rank Adaptation (LoRA)
- **Library Used :** Unsloth
- **Dataset used :** lukepramo221/choreo_concepts_docs_qna_trainset_conversation_formatted_pqt_v1.0
- **HF Model Card :** lukepramo221/choreo-qna-finetuned-gemma-3-qna-v0.6

## Instructions

- **Fine-tuner and inferencer is optimized for Google Colab only.**  
    No support for Kaggle.

- **Update environment variables in the Colab environment:**
    - Set your Hugging Face token.
    - Set your Weights & Biases (wandb) organization name and API token.

- **Model Versioning:**  
    Ensure you properly version fine-tuned models before pushing them to Hugging Face.
    
- **RAGAS Evaluator:**
    You can run RAGAS evaluator code on any VM without GPU. Make sure to put the environment variables as needed.
