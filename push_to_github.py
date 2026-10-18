"""
Helper script to push local Git repository to your GitHub repository
Usage:
  python push_to_github.py <github_repo_url> <personal_access_token>
"""

import sys
import os
from dulwich import porcelain
from dulwich.repo import Repo

ROOT = os.path.dirname(os.path.abspath(__file__))

def push_repo(repo_url, username=None, password=None):
    repo = Repo(ROOT)
    print(f"[*] Pushing repository to: {repo_url}...")
    try:
        porcelain.push(repo, repo_url, refspecs=b"refs/heads/master:refs/heads/main", username=username, password=password)
        print("[SUCCESS] Pushed to GitHub successfully! Your cloud host can now build it.")
    except Exception as e:
        print("[!] Push notice:", e)

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        url = sys.argv[1]
        token = sys.argv[2] if len(sys.argv) >= 3 else None
        push_repo(url, password=token)
    else:
        print("Usage: python push_to_github.py <https://github.com/username/bis-quiz> [token]")
