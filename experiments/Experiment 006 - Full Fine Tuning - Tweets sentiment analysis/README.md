# Sentiment analysis of tweets with Full Fine tuning

## Details

- Model selected: [Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B)
- Dataset: [tweet_sentiment_extraction](https://huggingface.co/datasets/mteb/tweet_sentiment_extraction)
- About the dataset: The dataset contains tweets with sentiment labels (positive, negative, neutral) and the corresponding text to extract the sentiment from. It is used for training models to perform sentiment analysis on tweets.
- Method: Full Fine tuning
- Runtime: Google Colab with T4 GPU
- Process:
  - Load the dataset
  - Preprocess the data
  - Load the model with a classification head attached and tokenizer
  - Fine-tune the model on the dataset
  - Evaluate the model

> **NOTE**: This experiment shows that full fine tuning enables the LLMs/SLMs to be effective classifiers, even with a limited amount of training time.
