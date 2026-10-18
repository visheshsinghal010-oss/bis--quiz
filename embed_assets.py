import os

ROOT = os.path.dirname(os.path.abspath(__file__))

css_path = os.path.join(ROOT, "static", "css", "style.css")
with open(css_path, "r", encoding="utf-8") as f:
    css_content = f.read()

quiz_js_path = os.path.join(ROOT, "static", "js", "quiz.js")
with open(quiz_js_path, "r", encoding="utf-8") as f:
    quiz_js = f.read()

lb_js_path = os.path.join(ROOT, "static", "js", "leaderboard.js")
with open(lb_js_path, "r", encoding="utf-8") as f:
    lb_js = f.read()

host_js_path = os.path.join(ROOT, "static", "js", "host.js")
with open(host_js_path, "r", encoding="utf-8") as f:
    host_js = f.read()

# Enhance quiz_js to immediately use INITIAL_QUESTIONS if provided
enhanced_quiz_js = quiz_js.replace(
    'document.addEventListener("DOMContentLoaded", async () => {',
    '''document.addEventListener("DOMContentLoaded", async () => {
  // If questions are already injected by server, load instantly!
  if (typeof INITIAL_QUESTIONS !== "undefined" && Array.isArray(INITIAL_QUESTIONS) && INITIAL_QUESTIONS.length > 0) {
    questions = INITIAL_QUESTIONS;
    renderPalette();
    renderQuestion(0);
    startTimer();
  }'''
)

# 1. Update index.html
index_path = os.path.join(ROOT, "templates", "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

if "<style id=\"embedded_css\">" not in index_html:
    index_html = index_html.replace(
        '<link rel="stylesheet" href="/static/css/style.css">',
        f'<style id="embedded_css">\n{css_content}\n</style>'
    )
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_html)
    print("[*] index.html updated with embedded CSS.")

# 2. Update quiz.html
quiz_path = os.path.join(ROOT, "templates", "quiz.html")
with open(quiz_path, "r", encoding="utf-8") as f:
    quiz_html = f.read()

quiz_html = quiz_html.replace(
    '<link rel="stylesheet" href="/static/css/style.css">',
    f'<style id="embedded_css">\n{css_content}\n</style>'
)
quiz_html = quiz_html.replace(
    '<script src="/static/js/quiz.js"></script>',
    f'<script>\nconst INITIAL_QUESTIONS = {{{{ questions_json | safe if questions_json is defined else "[]" }}}};\n{enhanced_quiz_js}\n</script>'
)
with open(quiz_path, "w", encoding="utf-8") as f:
    f.write(quiz_html)
print("[*] quiz.html updated with embedded CSS and instant question renderer.")

# 3. Update leaderboard.html
lb_path = os.path.join(ROOT, "templates", "leaderboard.html")
with open(lb_path, "r", encoding="utf-8") as f:
    lb_html = f.read()

lb_html = lb_html.replace(
    '<link rel="stylesheet" href="/static/css/style.css">',
    f'<style id="embedded_css">\n{css_content}\n</style>'
)
lb_html = lb_html.replace(
    '<script src="/static/js/leaderboard.js"></script>',
    f'<script>\n{lb_js}\n</script>'
)
with open(lb_path, "w", encoding="utf-8") as f:
    f.write(lb_html)
print("[*] leaderboard.html updated with embedded CSS and JS.")

# 4. Update host.html
host_path = os.path.join(ROOT, "templates", "host.html")
with open(host_path, "r", encoding="utf-8") as f:
    host_html = f.read()

host_html = host_html.replace(
    '<link rel="stylesheet" href="/static/css/style.css">',
    f'<style id="embedded_css">\n{css_content}\n</style>'
)
host_html = host_html.replace(
    '<script src="/static/js/host.js"></script>',
    f'<script>\n{host_js}\n</script>'
)
with open(host_path, "w", encoding="utf-8") as f:
    f.write(host_html)
print("[*] host.html updated with embedded CSS and JS.")

print("\n[SUCCESS] All 4 templates are now 100% self-contained and bulletproof!")
