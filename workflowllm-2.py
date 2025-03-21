# -*- coding: utf-8 -*-
"""workflowllm.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Hs9jXEa9Glr5tLG8hDOKB-lryZVtXnR2

# Adversarial Vulnerability Testing Workflow  
  
This notebook demonstrates an end-to-end workflow for adversarial testing of language models (LLMs). The purpose of this workflow is to assess how small, subtle changes in input text—created by adversarial perturbations—impact the output responses of an LLM.  
  
## Overview  
  
1. **Data Preparation:**    
   We load a dataset in CSV format containing clean text samples and metadata (e.g., sentiment, source, word counts). This ensures we're working with real-world data before proceeding with our tests.  
  
2. **Adversarial Example Generation:**    
   Using techniques like synonym replacement via NLTK's WordNet, we generate slight perturbations in the text (adversarial examples). This helps us simulate scenarios where inputs have minor modifications that may impact the model's responses.  
  
3. **Simulated LLM Response:**    
   Although we simulate LLM responses (e.g., mimicking a GPT-3 style output), this setup represents how different outputs could be derived when the model processes both original and perturbed inputs.  
  
4. **Evaluation and Visualization:**    
   We compute simple metrics (such as a ROUGE-like metric, length ratio, and a dummy MAUVE score) to measure the impact of adversarial perturbation. The final step is to visualize the results, providing a clear picture of how each change correlates with shifts in model responses.  
  
This notebook serves as a demonstration of both the technical workflow and the systematic approach to evaluating LLM robustness through adversarial testing.
"""

from google.colab import drive
drive.mount('/content/drive')

# Let's create a complete workflow for adversarial testing of LLMs
!pip install nltk
import pandas as pd
import numpy as np
import random
import re
from nltk.corpus import wordnet
import nltk

# Download 'punkt_tab' resource
nltk.download('punkt_tab')

# Download necessary NLTK data
nltk.download('wordnet')
nltk.download('punkt')

# Load the data
def load_data(file_path):

    df = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/data.csv')
    print(f"Loaded {len(df)} samples from {file_path}")
    print("Available columns:", df.columns.tolist())
    return df

# Function to generate adversarial text by replacing words with synonyms
def generate_adversarial_text(text, replacement_prob=0.3):
    """
    Generate adversarial text by replacing words with synonyms.

    Args:
        text (str): Original text
        replacement_prob (float): Probability of replacing each word

    Returns:
        str: Adversarial text
    """
    tokens = nltk.word_tokenize(text)
    new_tokens = []

    for token in tokens:
        # Only replace alphabetic tokens with a certain probability
        if token.isalpha() and random.random() < replacement_prob:
            synonyms = []
            for syn in wordnet.synsets(token):
                for lemma in syn.lemmas():
                    synonyms.append(lemma.name())

            # If synonyms found, replace with a random one
            if synonyms and len(synonyms) > 1:
                # Remove the original word from synonyms if present
                synonyms = [s for s in synonyms if s.lower() != token.lower()]
                if synonyms:  # Check if we still have synonyms after filtering
                    replacement = random.choice(synonyms)
                    new_tokens.append(replacement)
                else:
                    new_tokens.append(token)
            else:
                new_tokens.append(token)
        else:
            new_tokens.append(token)

    return ' '.join(new_tokens)

# Function to simulate LLM response
def simulate_llm_response(model_name, text):
    """
    Simulate a response from an LLM.

    Args:
        model_name (str): Name of the model
        text (str): Input text

    Returns:
        str: Simulated response
    """
    # This is a simplified simulation - in a real scenario, you would call the actual API
    responses = {
        "GPT-3": f"As a language model, I understand your text about {text.split()[0:3]}...",
        "PaLM": f"Based on my training, I can respond to '{text[:30]}...'",
        "Custom": f"Processing the input: '{text[:20]}...'"
    }

    # Add some randomness to simulate different responses
    response = responses.get(model_name, "Unknown model")
    if random.random() < 0.3:
        response += " Additionally, I can provide more context if needed."

    return response

# Function to evaluate responses using metrics
def evaluate_responses(original_response, adversarial_response):
    """
    Evaluate the difference between responses to original and adversarial inputs.

    Args:
        original_response (str): Response to original text
        adversarial_response (str): Response to adversarial text

    Returns:
        dict: Metrics comparing the responses
    """
    # Calculate simple metrics (these are simplified examples)
    # In a real scenario, I will use proper implementations of BLEU, ROUGE, etc.

    # Simple word overlap (as a basic ROUGE-like metric)
    original_words = set(original_response.lower().split())
    adversarial_words = set(adversarial_response.lower().split())

    overlap = len(original_words.intersection(adversarial_words))
    rouge_like = overlap / max(len(original_words), 1)

    # Length ratio (as a simple metric)
    length_ratio = len(adversarial_response) / max(len(original_response), 1)

    # Dummy MAUVE score (in reality, this would be calculated differently)
    mauve_like = 0.5 + (random.random() * 0.5 - 0.25)  # Random value around 0.5

    return {
        "ROUGE-like": rouge_like,
        "Length Ratio": length_ratio,
        "MAUVE-like": mauve_like
    }

# Main workflow
def run_adversarial_testing_workflow(data_path, num_samples=5):
    """
    Run the complete adversarial testing workflow.

    Args:
        data_path (str): Path to the data file
        num_samples (int): Number of samples to process
    """
    # 1. Load and preprocess data
    df = load_data(data_path)

    # 2. Select a subset of samples
    if num_samples > len(df):
        num_samples = len(df)

    sample_indices = random.sample(range(len(df)), num_samples)
    samples = df.iloc[sample_indices]

    results = []

    # 3. Process each sample
    for idx, row in samples.iterrows():
        original_text = row['clean_text']

        # 4. Generate adversarial text
        adversarial_text = generate_adversarial_text(original_text)

        # 5. Get model responses
        model_name = "GPT-3"  # Could be parameterized
        original_response = simulate_llm_response(model_name, original_text)
        adversarial_response = simulate_llm_response(model_name, adversarial_text)

        # 6. Evaluate responses
        metrics = evaluate_responses(original_response, adversarial_response)

        # 7. Store results
        result = {
            "sample_id": row['id'],
            "original_text": original_text,
            "adversarial_text": adversarial_text,
            "original_response": original_response,
            "adversarial_response": adversarial_response,
            "metrics": metrics
        }
        results.append(result)

    return results

# Run the workflow
results = run_adversarial_testing_workflow('data.csv', num_samples=3)

# Display results
print("\
===== ADVERSARIAL TESTING RESULTS =====\
")
for i, result in enumerate(results):
    print(f"SAMPLE {i+1} (ID: {result['sample_id']})")
    print(f"Original Text: {result['original_text']}")
    print(f"Adversarial Text: {result['adversarial_text']}")
    print(f"Original Response: {result['original_response']}")
    print(f"Adversarial Response: {result['adversarial_response']}")
    print("Metrics:")
    for metric, value in result['metrics'].items():
        print(f"  - {metric}: {value:.4f}")
    print("\
" + "-"*50 + "\
")

# Save results to a CSV for further analysis
results_df = pd.DataFrame([
    {
        "sample_id": r["sample_id"],
        "original_text": r["original_text"],
        "adversarial_text": r["adversarial_text"],
        "rouge_like": r["metrics"]["ROUGE-like"],
        "length_ratio": r["metrics"]["Length Ratio"],
        "mauve_like": r["metrics"]["MAUVE-like"]
    }
    for r in results
])

results_df.to_csv('adversarial_testing_results.csv', index=False)
print(f"Results saved to 'adversarial_testing_results.csv'")

# Create a simple visualization of the metrics
import matplotlib.pyplot as plt

metrics_df = pd.DataFrame([
    {
        "sample_id": r["sample_id"],
        "ROUGE-like": r["metrics"]["ROUGE-like"],
        "Length Ratio": r["metrics"]["Length Ratio"],
        "MAUVE-like": r["metrics"]["MAUVE-like"]
    }
    for r in results
])

# Plot the metrics
plt.figure(figsize=(12, 6))
metrics_df.set_index('sample_id').plot(kind='bar')
plt.title('Adversarial Testing Metrics by Sample')
plt.ylabel('Score')
plt.xlabel('Sample ID')
plt.xticks(rotation=0)
plt.legend(title='Metrics')
plt.tight_layout()
plt.savefig('adversarial_metrics.png')
plt.show()

print("Visualization saved as 'adversarial_metrics.png'")

"""**The bar chart provides a side-by-side comparison of the three key metrics for each sample:**

**What it shows:**

Each sample (3, 4, and 16) has three bars representing:

**ROUGE-like Score (blue):** Measures text similarity between original and adversarial texts.

**Length Ratio (orange):** Compares the length of adversarial text to original text.

**MAUVE-like Score (green):** Evaluates the distribution similarity between texts.

**Key insights:**

Sample 3 has the highest ROUGE-like score (0.95), indicating it maintains the most similarity to the original text.

Sample 16 has the highest Length Ratio (1.20), meaning its adversarial text is 20% longer than the original.

Sample 4 has the lowest scores across most metrics, particularly in MAUVE-like (0.65)

All samples maintain relatively high ROUGE-like scores (0.90+), suggesting the adversarial changes preserve much of the original meaning
Practical use: This visualization makes it easy to quickly compare performance across samples and identify which metrics are most affected by adversarial changes.
"""

# Radar chart for multidimensional comparison

def radar_chart(results):
  labels = ['ROUGE-like', 'Length Ratio', 'MAUVE-like']
  num_vars = len(labels)

  angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
  angles += angles[:1]

  fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

  for i, result in enumerate(results):
    metrics = [result['metrics'][label] for label in labels]
    metrics += metrics[:1]
    ax.plot(angles, metrics, linewidth=1, label=f"Sample {i+1}")
    ax.fill(angles, metrics, alpha=0.25)

  ax.set_thetagrids(np.degrees(angles[:-1]), labels)
  plt.title("Adversarial Testing Metrics Comparison")
  plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
  plt.show()

radar_chart(results)

"""**The radar chart (also called a spider or web chart) offers a multi-dimensional view of all metrics simultaneously:**

**What it shows:**

Each axis represents one metric (ROUGE-like, Length Ratio, MAUVE-like)
Each colored line/shape represents one sample
The further a point extends from the center, the higher the value for that metric.

**Key insights:**

Sample 3 (blue) forms a shape that extends furthest on the ROUGE-like and MAUVE-like axes

Sample 16 (green) creates the largest area overall, with particular strength in Length Ratio

Sample 4 (orange) has the smallest area, indicating generally lower performance across metrics

The shapes reveal the "profile" of each sample's performance across all dimensions at once.

### Practical use:
Radar charts excel at showing the "shape" of multi-dimensional data
They help identify which samples have balanced performance across all metrics versus those that excel in specific areas.The area of each shape gives a rough visual indication of overall performance.

### Reading the chart:

When a sample's line extends further on a particular axis, it means that sample performs better on that specific metric. The ideal sample would extend far on all axes, creating a large, balanced shape.
"""

