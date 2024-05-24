import os
import subprocess
import hashlib
import google.generativeai as genai

def hash_prompt(prompt_text):
    """Hashes a prompt using SHA256."""
    return hashlib.sha256(prompt_text.encode()).hexdigest()

def run_evy(filename):
    """Runs the evy command and returns True if successful."""
    try:
        result = subprocess.run(["evy", "run", filename], capture_output=True, text=True, check=True)
        print(f"Output for {filename}:\n{result.stdout}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running {filename}:\n{e.stderr}")
        return False, e.stderr

def prompt_gemini(prompt):
    # genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    # Set up the model
    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 0,
        "max_output_tokens": 8192,
    }
    safety_settings = []
    model = genai.GenerativeModel(model_name="tunedModels/evy24may-c8ek8ggror37",
                                  generation_config=generation_config,
                                  safety_settings=safety_settings)
    out = model.generate_content([f"input: {prompt} in the evy programming language:"])
    txt = out.text
    txt = txt.lstrip("output:")
    txt = txt.lstrip("```evy")
    txt = txt.rstrip("```")
    txt = txt.rstrip("'")
    txt = txt.lstrip("'")
    if "func test" in txt and "\ntest" not in txt:
        txt += "\ntest\n"
    return txt

def process_prompts(input_file="prompts.txt", output_dir="output", passed_dir="passed"):
    """Reads prompts, runs evy, and manages files."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(passed_dir, exist_ok=True)

    with open(input_file, "r") as prompts:
        for prompt_text in prompts:
            prompt_text = prompt_text.strip()
            if prompt_text:
                prompt_hash = hash_prompt(prompt_text)
                prompt_id = prompt_hash[:8]  # Use first 8 chars for shorter ID

                output_filename = os.path.join(output_dir, f"{prompt_id}-output-evy.evy")
                output_passed_filename = output_filename.replace("output/", "../processed/synthetic/")

                stdout_filename = os.path.join(output_dir, f"{prompt_id}-output-stdout.txt")

                prompt_filename = os.path.join(output_dir, f"{prompt_id}-input-text.txt")
                prompt_passed_filename = prompt_filename.replace("output/", "../processed/synthetic/")

                if os.path.exists(prompt_passed_filename) and prompt_passed_filename:
                    continue

                evy_code = prompt_gemini(prompt_text)
                with open(output_filename, "w") as outfile, open(prompt_filename, "w") as promptfile:
                    outfile.write(evy_code)
                    promptfile.write(prompt_text)
                ok, out = run_evy(output_filename)
                if ok:
                    os.rename(output_filename, output_passed_filename)
                    os.rename(prompt_filename, prompt_passed_filename)
                else:
                    with open(stdout_filename, "w") as f:
                        f.write(out)



if __name__ == "__main__":
    process_prompts()
