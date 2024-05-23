import csv
import os
def pythonPrompt(s):
    return f"""Can you convert this python to evy for me?
```python
{s}
```"""
def create_csv_from_pairs(directory, output_csv="file_pairs.csv"):
    """Creates a CSV file listing file pairs with their contents.

    Args:
        directory: The directory to search for file pairs.
        output_csv: The name of the output CSV file.
    """

    file_pairs = []
    for filename in os.listdir(directory):
        base_name, extension = os.path.splitext(filename)
        if extension == ".evy":
            py_filename = base_name + ".py"
            if os.path.isfile(os.path.join(directory, py_filename)):
                with open(os.path.join(directory, filename), "r") as evy_file:
                    evy_content = evy_file.read()
                with open(os.path.join(directory, py_filename), "r") as py_file:
                    py_content = py_file.read()
                    if py_content == "":
                        continue
                file_pairs.append((evy_content, pythonPrompt(py_content)))

    with open(output_csv, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["evy", "python"])
        for evy_content, py_content in file_pairs:
            writer.writerow([evy_content, py_content])

directory_to_search = "raw"
create_csv_from_pairs(directory_to_search, output_csv="gemini.csv")
