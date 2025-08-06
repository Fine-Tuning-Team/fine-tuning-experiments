# Run 005 - Qwen2.5 - Choreo Docs

This is an experimentation run for Choreo Docs domain knowledge adaptation using the `Qwen2.5-Instruct` model on Kaggle with T4 GPU.

## Information

- **Model :** unsloth/Qwen2.5-7B-Instruct-unsloth-bnb-4bit
- **Fine-tuning method :** Low Rank Adaptation (LoRA)
- **Library Used :** Unsloth
- **Dataset used :** [train](https://huggingface.co/datasets/rtweera/simple_implicit_n_qa_results_v2), [test1](https://huggingface.co/datasets/rtweera/fmt-q-and-a-together-part-14-76qty), [test2](https://huggingface.co/datasets/rtweera/fmt-q-and-a-together-part-13-114qty), [test3](https://huggingface.co/datasets/rtweera/user_centric_results_v1), [test4](https://huggingface.co/datasets/rtweera/user_centric_results_v2)
- **Inference results**:
  - [Base model results for test1](https://huggingface.co/datasets/rtweera/2025-Jun-12_23-15-06_b1_outputof_Qwen2.5-7B-Instruct-unsloth-bnb-4bit)
  - [Base model results for test2](https://huggingface.co/datasets/rtweera/2025-Jun-12_23-22-20_b2_outputof_Qwen2.5-7B-Instruct-unsloth-bnb-4bit)
  - [Base model results for test3](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-55-51_b3_outputof_Qwen2.5-7B-Instruct-unsloth-bnb-4bit)
  - [Base model results for test4](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-58-03_b4_outputof_Qwen2.5-7B-Instruct-unsloth-bnb-4bit)
  - [Fine-tuned model results for test1](https://huggingface.co/datasets/rtweera/2025-Jun-12_16-09-59_s1_outputof_2025-Jun-12_15-31-29_Qwen2.5-7B-Instruct-unsloth-bnb-4bit_LoRA)
  - [Fine-tuned model results for test2](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-35-35_s2_outputof_2025-Jun-12_15-31-29_Qwen2.5-7B-Instruct-unsloth-bnb-4bit_LoRA)
  - [Fine-tuned model results for test3](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-42-43_s3_outputof_2025-Jun-12_15-31-29_Qwen2.5-7B-Instruct-unsloth-bnb-4bit_LoRA)
  - [Fine-tuned model results for test4](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-44-16_s4_outputof_2025-Jun-12_15-31-29_Qwen2.5-7B-Instruct-unsloth-bnb-4bit_LoRA)
  - [Choreo copilot results for test1](https://huggingface.co/datasets/rtweera/copilot-answers-dataset-part-14-76qty)
  - [Choreo copilot results for test2](https://huggingface.co/datasets/rtweera/copilot-answers-dataset-part-13-114qty)
  - [Choreo copilot results for test3](https://huggingface.co/datasets/rtweera/copilot-answers-user_centric_results_v1)
  - [Choreo copilot results for test4](https://huggingface.co/datasets/rtweera/copilot-answers-user_centric_results_v2)
- **HF Model Card :** https://huggingface.co/rtweera/2025-Jun-04_14-52-53_Qwen2.5-7B-Instruct-unsloth-bnb-4bit_LoRA

## Instructions

- **Works in Kaggle with T4 GPU**

- **Use the `Run 003` notebook** to run the fine-tuning & inferencing process. Only change is the datasets.

- **Update secrets in the Kaggle environment:**
  - Set your Hugging Face token.
  - Set your Weights & Biases (wandb) organization name and API token.

- **Model Versioning:**  
    Ensure you properly version fine-tuned models before pushing them to Hugging Face.
