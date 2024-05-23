import os
import git
import pandas as pd
import shutil
import re

def clone_or_update_repo(repos, local_dir):
    shutil.rmtree(local_dir)
    for repo in repos:
        repo = repo["repo"]
        branch = repo["branch"] if "branch" in repo else None
        git.Repo.clone_from(repo, local_dir + "/" + repo.replace("https://", ""), b=branch)

if __name__ == "__main__":
    repo_urls = [
        {"repo": "https://github.com/evylang/evy.git", "branch": "learn-seed"},
        {"repo": "https://github.com/joshcarp/evy-leetcode.git"},
        {"repo": "https://github.com/evylang/evy.wiki.git"},
        {"repo": "https://github.com/joshcarp/humaneval-evy/"},
    ]
    local_dir = "../unprocessed"
    clone_or_update_repo(repo_urls, local_dir)
