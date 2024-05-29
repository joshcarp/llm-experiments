from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import numpy as np

# Load pre-trained GPT-2 model and tokenizer
model_name = "gpt2"  # You can try other models like "gpt2-medium"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

def perplexity(prompt):
    """Calculates the perplexity of a given prompt using GPT-2."""
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        loss = outputs[0]
    return torch.exp(loss).item()

def perplexity_per_word(prompt):
    """Calculates perplexity normalized by the number of words."""
    ppx = perplexity(prompt)
    num_words = len(prompt.split())  # Count words
    return ppx / num_words

def perplexity_bits_per_char(prompt):
    """Calculates perplexity in bits per character (BPC)."""
    ppx = perplexity(prompt)
    num_chars = len(prompt)  # Count characters
    return np.log2(ppx) / num_chars

# Example usage
prompts = [
    "The quick brown fox jumps over the lazy dog.",
    "What is the meaning of life?",
    "Explain quantum physics in simple terms."
]

for p in prompts:
    ppx = perplexity(p)
    ppx_per_word = perplexity_per_word(p)
    ppx_bpc = perplexity_bits_per_char(p)

    print(f"\nPrompt: '{p}'")
    print(f"  Perplexity: {ppx:.2f}")
    print(f"  Perplexity per Word: {ppx_per_word:.2f}")
    print(f"  Perplexity (BPC): {ppx_bpc:.2f}")

# Sort by normalized perplexity (you can choose either method)
# perplexities = [(p, perplexity_per_word(p)) for p in prompts]
perplexities = [(p, perplexity_bits_per_char(p)) for p in prompts]
perplexities.sort(key=lambda x: x[1])

print("\nSorted by Normalized Perplexity (lower is better):")
for prompt, ppx in perplexities:
    print(f"Prompt: '{prompt}' - Perplexity: {ppx:.2f}")

def pairwise_perplexity_ranking(prompts):
    """Ranks prompts based on pairwise perplexity decrease."""
    results = {}
    for i, prompt_a in enumerate(prompts):
        decreases = []
        for j, prompt_b in enumerate(prompts):
            if i != j:
                ppx_a = perplexity(prompt_a)
                ppx_ab = perplexity(prompt_a + prompt_b)
                decrease = ppx_a - ppx_ab
                decreases.append(decrease)
        results[prompt_a] = sum(decreases) / len(decreases)  # Average decrease
    return sorted(results.items(), key=lambda x: x[1], reverse=True)  # Sort by decrease


# Example usage:
prompts = [
    "The quick brown fox jumps over the lazy dog.",
    "What is the meaning of life?",
    "Explain quantum physics in simple terms."
]

ranking = pairwise_perplexity_ranking(prompts)
print("\nPairwise Perplexity Ranking (higher decrease is better):")
for prompt, avg_decrease in ranking:
    print(f"Prompt: '{prompt}' - Avg. Decrease: {avg_decrease:.2f}")

if __name__ == "__main__":
    pass