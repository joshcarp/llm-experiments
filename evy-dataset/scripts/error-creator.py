import hashlib
import os
import re
import subprocess
from random import random


def run_evy(filename):
    """Runs the `evy run` command on the given file and returns stdout."""

    try:
        result = subprocess.run(
            ["evy", "run", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,               # Capture output as text
            check=True               # Raise an error if the command fails
        )
        return result.stdout, result.stderr
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: 'evy' command not found. Is it installed and in your PATH?")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error running evy on {filename}: {e.stderr}")

def hash_prompt(prompt_text):
    """Hashes a prompt using SHA256."""
    return hashlib.sha256(prompt_text.encode()).hexdigest()

def newfile(dict: {}, root: str):
    id = hash_prompt(dict.__str__())
    for key, val in dict.items():
        if val == "":
            continue
        filename = f"{id[:8]}-{key}"
        with open(os.path.join(root, filename), "w") as f:
            f.write(val)

import random
from string import punctuation, whitespace

def corrupt_code(code_str, seed):
    random.seed(seed)  # Ensure deterministic behavior based on seed
    corruption_options = [
        lambda s: s.replace(":[]num", ":= []num", 1),
        lambda s: s.replace(":[]num", ":= []num", 1),
        lambda s: s.replace(":", ";", 1),
        lambda s: s + random.choice(punctuation),
        lambda s: s[:-1] + random.choice(whitespace),
        lambda s: s[:2] + s[2:].upper(),
        lambda s: s + "\n.", # should always fail on this one
    ]
    for i in range(seed, seed + len(corruption_options)):
        opt = i % len(corruption_options)
        corruption_func = corruption_options[opt]
        new_code = corruption_func(code_str)
        if new_code != code_str:
            return new_code
    assert False # something should've been corrupted by now


def main():
    target_directory = "../processed"
    filename_pattern = re.compile(r"^(?P<id>\S+)-(?P<rowname>output-evy)\.(?P<extension>\w*)$")

    for root, _, files in os.walk(target_directory):
        for file in files:
            match = filename_pattern.match(file)
            if match:
                filepath = os.path.join(root, file)  # Get the full file path
                stdout, stderr = run_evy(filepath)
                with open(filepath) as f:
                    good = f.read()
                newfile({"input-evy-error.evy": corrupt_code(good, len(good)), "input-stdout": stdout, "input-stderr": stderr, "output-evy": good, "input-text.txt": "Can you fix this evy code for me?"}, root)

if __name__ == "__main__":
    main()
