# Run 006 - Qwen2.5 - Choreo Docs

This is an experimentation run for Choreo Docs domain knowledge adaptation using the `Qwen2.5-Instruct` model on Kaggle with T4 GPU.

## Information

- **Model :** unsloth/Qwen2.5-7B-Instruct-unsloth-bnb-4bit
- **Fine-tuning method :** Low Rank Adaptation (LoRA)
- **Library Used :** Unsloth
- **Dataset used :** [train](https://huggingface.co/datasets/rtweera/simple_implicit_n_qa_results_v2), [test1](https://huggingface.co/datasets/rtweera/user_centric_results_v1), [test2](https://huggingface.co/datasets/rtweera/user_centric_results_v2)
- **Inference results**:
  - [Base model results for test1](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-55-51_b3_outputof_Qwen2.5-7B-Instruct-unsloth-bnb-4bit)
  - [Base model results for test2](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-58-03_b4_outputof_Qwen2.5-7B-Instruct-unsloth-bnb-4bit)
  - [Fine-tuned model results for test1](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-42-43_s3_outputof_2025-Jun-12_15-31-29_Qwen2.5-7B-Instruct-unsloth-bnb-4bit_LoRA)
  - [Fine-tuned model results for test2](https://huggingface.co/datasets/rtweera/2025-Jun-12_22-44-16_s4_outputof_2025-Jun-12_15-31-29_Qwen2.5-7B-Instruct-unsloth-bnb-4bit_LoRA)
  - [Choreo copilot results for test1](https://huggingface.co/datasets/rtweera/copilot-answers-user_centric_results_v1)
  - [Choreo copilot results for test2](https://huggingface.co/datasets/rtweera/copilot-answers-user_centric_results_v2)
- **HF Model Card :** https://huggingface.co/rtweera/2025-Jun-04_14-52-53_Qwen2.5-7B-Instruct-unsloth-bnb-4bit_LoRA
- **Evaluation results**: All results are in the xlsx files. Refer to the following mapping:
  - `test1` direct domain questions -> `[FineTuning][AITeamsMeeting] Fine-Tuning SLMs - Column chart 1.xlsx`
  - `test2` scenario based questions-> `[FineTuning][AITeamsMeeting] Fine-Tuning SLMs - Column chart 2.xlsx`

## Instructions

- **Works in Kaggle with T4 GPU**

- **Use the `Run 003` notebook** to run the fine-tuning & inferencing process. Only change is the datasets.

- **Update secrets in the Kaggle environment:**
  - Set your Hugging Face token.
  - Set your Weights & Biases (wandb) organization name and API token.

- **Model Versioning:**  
    Ensure you properly version fine-tuned models before pushing them to Hugging Face.

- Evaluation was done using the `Ragas` library.

## Additional Context

In the new test datasets, testset 1 directly checks the domain knowledge: like 'How to search in Choreo marketplace?'. The testset 2 is a scenario-based one where the user is faced with a certain scenario and asks the model to how to solve it, such as: 'I need the service X in my application, how can I find this in Choreo marketplace?'.

This run is a continuation of the previous run (005). Here, we are using the same inferenced output from previous run, but in addtion to semantic similarity we use factual correctness, answer accuracy, rouge score to evaluate. With those metrics, we can see a clear domain knowledge adaptation in the model. Refer to `png` files to see the evaluation results in graphical format. Refer to the `xlsx` files for detailed evaluation results in numerical format. Row by row evaluation was not performed in this run; only the overall evaluation was done.
