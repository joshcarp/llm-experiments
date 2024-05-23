import csv
import os
import re
import ast
import tokenize
import subprocess
from collections import defaultdict

def is_valid_python_string(line):
    """Checks if a line represents a valid Python string literal."""
    try:
        ast.parse(line)
        return True
    except SyntaxError:
        return False
    return False  # It's either not Python or not a string


def is_valid_evy_string(param):
    result = subprocess.run(["evy","run", "-"], input=param, capture_output=True, text=True)
    return result.returncode == 0
    idents = ["func", "[]num", "{}any", "end\n"]
    for ident in idents:
        if ident in param:
            return True
    return False



def process_string(input_string, ignore_python=False):
    """Processes a string, extracting code blocks and text into a dictionary."""
    result = defaultdict(str)
    current_block = "text"
    evy_start = re.compile(r"^`evy\s*$")
    python_start = re.compile(r"^```python\s*$")
    lines = input_string.splitlines()
    for i, line in enumerate(lines):
        if current_block == "text":
            if evy_start.match(line) or is_valid_evy_string("\n".join(lines[i:])):
                current_block = "evy"
            elif python_start.match(line) or is_valid_python_string("\n".join(lines[i:])):
                if ignore_python is False:
                    current_block = "python"
                else:
                    current_block = "evy"
        #elif line.startswith("```"):  # Detect the end of any code block
        #    current_block = "text"
        result[current_block] += f"{line}\n"
    for block, content in result.items():
        result[block] = result[block].lstrip("```python")
        result[block] = result[block].lstrip("```evy")
        result[block] = result[block].lstrip("```\n")
    return result


def process_csv_to_files(csv_file_path, output_directory):
    """Reads a CSV, creates files based on rows and columns."""

    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            id_part = ""
            if "id" in row:
                id_part = row['id']
            else:
                id_part = f"{i}"
            if "#START:PROMPT" in row.__str__() or "check(candidate)" in row.__str__():
                continue
            for field_name in reader.fieldnames:
                if field_name != 'id':
                    content = process_string(row[field_name], field_name=="output")
                    file_type = field_name.split('-')[0] # 'input' or 'output'

                    ext = field_name.split('.')[-1]       # File extension
                    filename = f"{id_part}-{file_type}.{ext}"
                    filepath = os.path.join(output_directory, filename)
                    if field_name == "prompt":
                        t = "input"
                    elif field_name == "output":
                        t = "output"


                    # Create output directory if it doesn't exist
                    os.makedirs(output_directory, exist_ok=True)
                    field_name_mapping = {"prompt": "input", "output": "output"}
                    tpe = field_name_mapping[field_name]

                    if 'evy' in content:
                        # Asking to fix some code
                        with open(os.path.join(output_directory, f"{id_part}-{tpe}-evy.evy"), "w") as f:
                            f.write(content["evy"])
                    if "text" in content.keys():
                        with open(os.path.join(output_directory, f"{id_part}-{tpe}-text.txt"), "w") as f:
                            f.write(content["text"])
                    if "python" in content.keys():
                        # Asking to convert code from python to evy
                        with open(os.path.join(output_directory, f"{id_part}-{tpe}-python.py"), "w") as f:
                            f.write(content["python"])




                    # with open(filepath, 'w') as outfile:
                    #     outfile.write(content)

if __name__ == "__main__":
    csv_file_path = "../gemini-import.csv"
    output_directory = "../export"
    os.system("rm ../export/* || true")
    process_csv_to_files(csv_file_path, output_directory)
