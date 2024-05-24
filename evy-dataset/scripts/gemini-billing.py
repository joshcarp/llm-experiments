"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai
import os

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = []

model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

import pandas as pd

# Load the CSV file
df = pd.read_csv('gemini.csv')

# Create lists of input and output parts
input_parts = df['input'].tolist()
output_parts = df['output'].tolist()
prompt_parts = []
# Printing or further processing here (optional)
for inp, out in zip(input_parts, output_parts):
    prompt_parts.extend([f"input {inp}", f"output {out}"])

prompt_parts.append("input write fizzbuzz for me in evy")
prompt_parts.append("output ")

response = model.generate_content(prompt_parts)
print(response.text)

if __name__ == "__main__":
    pass