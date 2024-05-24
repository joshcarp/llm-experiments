import os
import re
from collections import defaultdict

file_pattern = re.compile(r"^(?P<id>\S+)-(?P<rowname>output-evy|output-text|input-python|input-text|input-evy|source)\.(?P<extension>\w*)$")


def iterate_files(directory_path):
    rows = defaultdict(dict)
    todo = []
    for root, dirs, files in os.walk(directory_path):
        for filename in files:
            match = file_pattern.match(filename)
            if match:
                with open(os.path.join(root, filename), 'r') as file:
                    data = file.read()
                id, rowname = match.group('id'), match.group('rowname')
                rows[id]["id"] = id
                rows[id][rowname] = data
            else:
                todo.append(os.path.join(root, filename))
    return rows, todo

def process_todos(todos):
    renames = {}
    for elem in todos:
        if ".evy" in elem:
            id = elem.removesuffix(".evy")
            renames[elem] = f"{id}-output-evy.evy"
        elif ".py" in elem:
            id = elem.removesuffix(".py")
            renames[elem] = f"{id}-input-python.py"
    return renames


from datasets import Dataset

def standardize_row(row, all_attributes):
    standardized_row = {attr: row.get(attr, "") for attr in all_attributes}
    return standardized_row

<<<<<<< Updated upstream
=======
def combine_columns(example):
    combined_input = " ".join([example['input-text'], example['input-evy'], example['input-python']])
    combined_output = " ".join([example['output-text'], example['output-evy']])
    return {'Combined Input': combined_input, 'Combined Output': combined_output}

>>>>>>> Stashed changes
if __name__ == "__main__":
    directory_paths = "../processed"
    rows, todo = iterate_files(directory_paths)
    attrs = {k for row in rows.values() for k in row}
    rows = [standardize_row(row, attrs) for row in rows.values()]

    dataset = Dataset.from_list(rows)
    # dataset.push_to_hub("joshcarp/evy-dataset")
    dataset.save_to_disk("temp_dataset")
    dataset.load_from_disk("temp_dataset")
<<<<<<< Updated upstream
    dataset.push_to_hub("joshcarp/evy-dataset3")
=======
    dataset.push_to_hub("joshcarp/evy-dataset")
>>>>>>> Stashed changes
    dataset.to_csv("evy-dataset.csv")
    renames = process_todos(todo)
    for orig, new in renames.items():
        old = os.path.join(directory_paths, orig)
        new = os.path.join(directory_paths, new)
        os.system(f"mv {old} {new}")
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
