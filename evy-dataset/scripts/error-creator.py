import hashlib
import os
import re
import subprocess
from random import random


def run_evy(filename, timeout=None):  # Add timeout parameter (default=None for no timeout)
    """Runs the `evy run` command with an optional timeout and returns stdout/stderr."""

    try:
        process = subprocess.Popen(
            ["evy", "run", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        outs, errs = process.communicate(timeout=timeout)  # Communicate with timeout

        # Check return code even with timeout, as communicate() doesn't raise errors on its own
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, process.args, output=outs, stderr=errs)

        return outs, errs

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: 'evy' command not found. Is it installed and in your PATH?")

    except subprocess.TimeoutExpired:
        process.kill()  # Terminate the process if it times out
        outs, errs = process.communicate()  # Get any partial output
        raise TimeoutError(f"'evy run' timed out after {timeout} seconds") from None

    except subprocess.CalledProcessError as e:
        return "", e.stderr

def hash_prompt(prompt_text):
    """Hashes a prompt using SHA256."""
    return hashlib.sha256(prompt_text.encode()).hexdigest()[:8]

def newfile(orig, root):
    id = hash_prompt(orig)
    bad = corrupt_code(orig, len(orig))

    badfilepath = os.path.join(root, f"{id}-input-evy-bad.evy")
    with open(badfilepath, "w") as f:
        f.write(bad)
    stdout, stderr = run_evy(badfilepath)
    if stderr == "":
        os.remove(badfilepath)
        return
    with open(os.path.join(root, f"{id}-output-evy.evy"), "w") as f:
        f.write(orig)
    if stdout != "":
        with open(os.path.join(root, f"{id}-input-stdout"), "w") as f:
            f.write(stdout)
    if stderr != "":
        with open(os.path.join(root, f"{id}-input-stderr"), "w") as f:
            f.write(stderr)

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
                with open(filepath) as f:
                    good = f.read()
                newfile(good, root)

if __name__ == "__main__":
    main()
