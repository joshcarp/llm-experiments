import datasets


def combine_columns(example):
    combined_input = " ".join([
        example['input-text'],
        example['input-evy'],
        example['input-python']
    ])

    combined_output = " ".join([
        example['output-text'],
        example['output-evy']
    ])
    inp = f"""
{example['input-text']}
"""
    if example['input-evy'] != "":
        inp += f"""```evy
    {example['input-evy']}
        ```"""

    out = f"""```evy
{example['output-evy']}     
```"""
    if example['input-python'] != "":
        inp = f"""Can you convert this to evy for me?
```python
{example['input-python']}
```"""
    return {'input': inp, 'output': out}


if __name__ == "__main__":
    dataset1 = datasets.load_dataset("joshcarp/evy-dataset")
    # dataset1["train"].to_csv("out.csv")
    dataset = dataset1["train"].filter(lambda x: x["output-evy"] != "")
    dataset = dataset.map(combine_columns)

    # Remove original columns
    dataset = dataset.remove_columns(
        ['input-text', 'input-evy', 'input-python', 'output-text', 'output-evy', 'id'])
    dataset = dataset.filter(lambda x: len(x["output"]) < 5000)

    # Write the new dataset to a csv file
    dataset.to_csv("gemini.csv")