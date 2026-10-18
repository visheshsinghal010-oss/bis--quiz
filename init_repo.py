import os
from dulwich.repo import Repo
from dulwich import porcelain

ROOT = os.path.dirname(os.path.abspath(__file__))

# 1. Create .gitignore
gitignore_path = os.path.join(ROOT, ".gitignore")
with open(gitignore_path, "w", encoding="utf-8") as f:
    f.write("""cloudflared.exe
__pycache__/
*.pyc
public_url.txt
response_debug.html
*.zip
.git/
""")

print("[*] .gitignore created.")

# 2. Init Git Repo
git_dir = os.path.join(ROOT, ".git")
if not os.path.exists(git_dir):
    repo = Repo.init(ROOT)
    print("[*] Initialized Git repository at:", ROOT)
else:
    repo = Repo(ROOT)
    print("[*] Using existing Git repo at:", ROOT)

# 3. Add and Commit files
files_to_add = [
    "app.py",
    "questions.py",
    "wsgi.py",
    "requirements.txt",
    "Procfile",
    "Dockerfile",
    "README.md",
    ".gitignore",
    os.path.join("templates", "index.html"),
    os.path.join("templates", "quiz.html"),
    os.path.join("templates", "leaderboard.html"),
    os.path.join("templates", "host.html"),
    os.path.join("static", "css", "style.css"),
    os.path.join("static", "js", "quiz.js"),
    os.path.join("static", "js", "leaderboard.js"),
    os.path.join("static", "js", "host.js"),
]

for rel_path in files_to_add:
    full_path = os.path.join(ROOT, rel_path)
    if os.path.exists(full_path):
        porcelain.add(repo, rel_path)

try:
    commit_id = porcelain.commit(
        repo,
        message=b"Initial commit: BIS Quiz 2026 full-stack web application (24/7 cloud ready)",
        author=b"BIS Quiz Host <host@bis-quiz.local>",
        committer=b"BIS Quiz Host <host@bis-quiz.local>"
    )
    print("[*] Committed successfully! Commit ID:", commit_id.decode('ascii'))
except Exception as e:
    print("Commit notice:", e)

print("[SUCCESS] Local Git Repository is fully generated and ready!")
