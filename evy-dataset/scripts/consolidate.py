import os
import re
import pandas as pd
import hashlib


def filter(filepath)-> bool:
    if "examples/human-eval" in filepath:
        return False
    return True
def find_evy_files(directory):
    evy_files = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            source = filepath.lstrip(directory)
            if not filter(filepath):
                continue
            if file.endswith('.md'):
                with open(filepath, 'r') as f:
                    content = f.read()
                    if "type: question" in content:
                        continue
                    id = hashlib.sha256(content.encode()).hexdigest()[:10]
                    evy_code_blocks = re.findall(r"```evy\n([^`]+)```", content)
                    for block in evy_code_blocks:
                        evy_files[id] = {
                            'id': id,
                            'filename': file,
                            'output-evy.evy': block,
                            'input-evy.evy': block,
                            "proj": source.split("/")[2]
                        }
            elif file.endswith('.evy'):
                id = file.rstrip(".evy")
                with open(filepath, 'r') as f:
                    content = f.read()

                row = {'filename': file, 'output-evy.evy': content, "id": id, "proj": source.split("/")[2], "source": source}
                pythonfile = filepath.replace(".evy", ".py")
                pythonfile = pythonfile.replace("/evy/", "/python/")
                if os.path.exists(pythonfile):
                    with open(pythonfile) as file:
                        row["input-python.py"] = file.read()
                else:
                    row['input-evy.evy'] = content
                evy_files[id] = row
    return evy_files

evy_files = find_evy_files("../unprocessed")

evy_files

for example in evy_files.values():
    proj_dir = os.path.join("../processed", example["proj"])
    os.makedirs(proj_dir, exist_ok=True)
    for attr in example.keys():
        if attr in ["proj", "filename", "id"]:
            continue
        filename = f"{example['id']}-{attr}"
        with open(os.path.join(proj_dir, filename), "w") as f:
            f.write(example[attr])



if __name__ == "__main__":
    pass