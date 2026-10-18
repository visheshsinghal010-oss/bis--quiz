import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
CSS_FILE = os.path.join(ROOT, "static", "css", "style.css")

with open(CSS_FILE, "r", encoding="utf-8") as f:
    dark_css = f.read()

# -------------------------------------------------------------
# 1. UPDATE HOST.HTML
# -------------------------------------------------------------
host_path = os.path.join(ROOT, "templates", "host.html")
with open(host_path, "r", encoding="utf-8") as f:
    host_html = f.read()

# Replace embedded CSS
host_html = re.sub(r'<style id="embedded_css">.*?</style>', f'<style id="embedded_css">\n{dark_css}\n</style>', host_html, flags=re.DOTALL)

# Add Upside Down Panel if not present
host_panel_html = '''
  <!-- Smooth Upside Down Host Control Deck -->
  <div class="panel-backdrop-overlay" id="hostPanelBackdrop" onclick="toggleUpsideDownPanel()"></div>
  <div class="upside-down-panel" id="hostUpsideDownPanel">
    <div class="panel-inner">
      <div class="panel-header-bar">
        <h3><span>⚡ Host Command Deck & Quick Controls</span></h3>
        <button type="button" class="panel-close-btn" onclick="toggleUpsideDownPanel()" title="Close Panel">✕</button>
      </div>

      <div class="panel-grid-cards">
        <div class="panel-card-item">
          <span class="item-title">📲 Candidate Quiz Join URL</span>
          <span class="item-value" style="font-size:13px; word-break:break-all; color:#93c5fd;" id="deckJoinUrl">{{ host_join_url }}</span>
          <div style="margin-top:10px; display:flex; gap:8px;">
            <button type="button" class="btn-secondary" style="font-size:12px; padding:6px 12px;" onclick="copyJoinLink()">📋 Copy Candidate Link</button>
            <button type="button" class="btn-secondary" style="font-size:12px; padding:6px 12px;" onclick="showLargeQR()">🔍 Enlarge QR</button>
          </div>
        </div>

        <div class="panel-card-item">
          <span class="item-title">👑 Co-Host Dashboard URL</span>
          <span class="item-value" style="font-size:13px; word-break:break-all; color:#60a5fa;" id="deckPublicHostUrl">{{ public_host_url }}</span>
          <div style="margin-top:10px; display:flex; gap:8px;">
            <button type="button" class="btn-secondary" style="font-size:12px; padding:6px 12px;" onclick="copyPublicHostLink()">📋 Copy Host Link</button>
            <button type="button" class="btn-secondary" style="font-size:12px; padding:6px 12px;" onclick="showCoHostQR()">📲 Host QR</button>
          </div>
        </div>

        <div class="panel-card-item">
          <span class="item-title">📊 Live Session Snapshot</span>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
            <div>
              <div style="font-size:11px; color:#94a3b8;">Registered</div>
              <div style="font-size:22px; font-weight:800; color:#38bdf8;" id="deckRegCount">0</div>
            </div>
            <div>
              <div style="font-size:11px; color:#94a3b8;">Completed</div>
              <div style="font-size:22px; font-weight:800; color:#34d399;" id="deckCompCount">0</div>
            </div>
            <div>
              <div style="font-size:11px; color:#94a3b8;">Top Score</div>
              <div style="font-size:22px; font-weight:800; color:#fbbf24;" id="deckTopScore">0</div>
            </div>
          </div>
        </div>

        <div class="panel-card-item">
          <span class="item-title">📁 Quick Export & Controls</span>
          <div style="margin-top:10px; display:flex; flex-direction:column; gap:8px;">
            <a href="/api/export-csv" class="btn-export" style="font-size:12px; padding:7px 12px; justify-content:center;">📥 Download Scores (.CSV)</a>
            <button type="button" class="btn-secondary" style="font-size:12px; padding:6px 12px; justify-content:center;" onclick="copyHostSummaryText()">📋 Copy Formatted Summary</button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Pull-Down Trigger Tab -->
  <div class="panel-toggle-tab" onclick="toggleUpsideDownPanel()" id="hostPanelTab">
    <span>⚡ Quick Host Deck</span>
    <span class="tab-chevron">▼</span>
  </div>
'''

if 'id="hostUpsideDownPanel"' not in host_html:
    host_html = host_html.replace('<body>', '<body>\n' + host_panel_html)

# Update light inline styling to dark theme
host_html = host_html.replace('color:#1e293b;', 'color:#f8fafc;')
host_html = host_html.replace('background:#f0fdf4; border:1.5px solid #86efac;', 'background:rgba(6, 78, 59, 0.25); border:1.5px solid rgba(16, 185, 129, 0.45);')
host_html = host_html.replace('color:#15803d;', 'color:#34d399;')
host_html = host_html.replace('color:#1e40af;', 'color:#60a5fa;')
host_html = host_html.replace('background:#eff6ff; border:1.5px solid #93c5fd;', 'background:rgba(30, 58, 138, 0.25); border:1.5px solid rgba(59, 130, 246, 0.45);')
host_html = host_html.replace('color:#1d4ed8;', 'color:#93c5fd;')
host_html = host_html.replace('background:#f1f5f9; padding:10px 14px; border-radius:6px; font-size:12px; color:#475569;', 'background:rgba(30, 41, 59, 0.6); padding:10px 14px; border-radius:6px; font-size:12px; color:#94a3b8; border:1px solid rgba(255,255,255,0.08);')
host_html = host_html.replace('style="white-space:nowrap; background:#ffffff;"', 'style="white-space:nowrap; background:#1e293b; color:#e2e8f0; border:1px solid rgba(255,255,255,0.15);"')
host_html = host_html.replace('background:#f8fafc;', 'background:#1e293b;')

# Add JS toggle handler to host.html
host_js_addon = '''
function toggleUpsideDownPanel() {
  const panel = document.getElementById("hostUpsideDownPanel");
  const backdrop = document.getElementById("hostPanelBackdrop");
  const tab = document.getElementById("hostPanelTab");
  if (!panel) return;
  const isOpen = panel.classList.contains("open");
  if (isOpen) {
    panel.classList.remove("open");
    if (backdrop) backdrop.classList.remove("open");
    if (tab) tab.querySelector(".tab-chevron").style.transform = "rotate(0deg)";
  } else {
    panel.classList.add("open");
    if (backdrop) backdrop.classList.add("open");
    if (tab) tab.querySelector(".tab-chevron").style.transform = "rotate(180deg)";
  }
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const panel = document.getElementById("hostUpsideDownPanel");
    if (panel && panel.classList.contains("open")) toggleUpsideDownPanel();
  }
});
'''

if 'function toggleUpsideDownPanel' not in host_html:
    host_html = host_html.replace('let hostParticipants = [];', host_js_addon + '\nlet hostParticipants = [];')

# Also sync deck stats in fetchHostData
host_html = host_html.replace(
    'document.getElementById("statAvgScore").textContent = (hostStats.avg_score || 0) + " pts";',
    '''document.getElementById("statAvgScore").textContent = (hostStats.avg_score || 0) + " pts";
      const deckReg = document.getElementById("deckRegCount"); if (deckReg) deckReg.textContent = hostStats.total_registered || 0;
      const deckComp = document.getElementById("deckCompCount"); if (deckComp) deckComp.textContent = hostStats.total_completed || 0;
      const deckTop = document.getElementById("deckTopScore"); if (deckTop) deckTop.textContent = hostStats.top_score || 0;'''
)

with open(host_path, "w", encoding="utf-8") as f:
    f.write(host_html)
print("[*] host.html updated successfully with dark theme & upside-down panel!")


# -------------------------------------------------------------
# 2. UPDATE INDEX.HTML
# -------------------------------------------------------------
index_path = os.path.join(ROOT, "templates", "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    index_html = f.read()

index_html = re.sub(r'<style id="embedded_css">.*?</style>', f'<style id="embedded_css">\n{dark_css}\n</style>', index_html, flags=re.DOTALL)

cand_panel_html = '''
  <!-- Smooth Upside Down Guidelines Deck -->
  <div class="panel-backdrop-overlay" id="candPanelBackdrop" onclick="toggleCandidatePanel()"></div>
  <div class="upside-down-panel" id="candUpsideDownPanel">
    <div class="panel-inner">
      <div class="panel-header-bar">
        <h3><span>📌 Official BIS Quiz Exam Guidelines & Rules</span></h3>
        <button type="button" class="panel-close-btn" onclick="toggleCandidatePanel()" title="Close Panel">✕</button>
      </div>

      <div class="panel-grid-cards">
        <div class="panel-card-item">
          <span class="item-title">⏱️ Strict Countdown Timer</span>
          <span class="item-value" style="font-size:15px; color:#60a5fa;">20:00 Minutes (1200s)</span>
          <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Once you click Start, the timer counts down. The exam automatically submits when time expires.</p>
        </div>

        <div class="panel-card-item">
          <span class="item-title">⚡ Speed Bonus Scoring</span>
          <span class="item-value" style="font-size:15px; color:#fbbf24;">Earn Up to +1500 Bonus Points</span>
          <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Each correct answer earns 100 base points. Finishing faster awards massive bonus points on the live leaderboard!</p>
        </div>

        <div class="panel-card-item">
          <span class="item-title">📝 30 BIS Multiple Choice Questions</span>
          <span class="item-value" style="font-size:15px; color:#34d399;">Randomized & Secure</span>
          <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Covers BIS Acts, ISI mark, Hallmarking, Compulsory Registration Scheme (CRS), and National Standards.</p>
        </div>

        <div class="panel-card-item">
          <span class="item-title">🔒 Fair Play Policy</span>
          <span class="item-value" style="font-size:15px; color:#f472b6;">Single Attempt Session</span>
          <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Do not reload or close your browser tab during the exam. Questions can be reviewed and changed anytime before submitting.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Pull-Down Trigger Tab -->
  <div class="panel-toggle-tab" onclick="toggleCandidatePanel()" id="candPanelTab">
    <span>📌 Exam Guidelines & Speed Rules</span>
    <span class="tab-chevron">▼</span>
  </div>
'''

if 'id="candUpsideDownPanel"' not in index_html:
    index_html = index_html.replace('<body>', '<body>\n' + cand_panel_html)

# Update badge & error styles
index_html = index_html.replace('background:#e0f2fe; color:#0369a1;', 'background:rgba(59, 130, 246, 0.18); color:#93c5fd; border:1px solid rgba(59, 130, 246, 0.35);')
index_html = index_html.replace(
    'style="display:none; color:#dc2626; background:#fee2e2; padding:12px; border-radius:8px; margin-bottom:16px; font-size:14px; text-align:center;"',
    'style="display:none; color:#fca5a5; background:rgba(239, 68, 68, 0.2); border:1px solid rgba(239, 68, 68, 0.4); padding:12px; border-radius:8px; margin-bottom:16px; font-size:14px; text-align:center;"'
)

cand_js_addon = '''
function toggleCandidatePanel() {
  const panel = document.getElementById("candUpsideDownPanel");
  const backdrop = document.getElementById("candPanelBackdrop");
  const tab = document.getElementById("candPanelTab");
  if (!panel) return;
  const isOpen = panel.classList.contains("open");
  if (isOpen) {
    panel.classList.remove("open");
    if (backdrop) backdrop.classList.remove("open");
    if (tab) tab.querySelector(".tab-chevron").style.transform = "rotate(0deg)";
  } else {
    panel.classList.add("open");
    if (backdrop) backdrop.classList.add("open");
    if (tab) tab.querySelector(".tab-chevron").style.transform = "rotate(180deg)";
  }
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const panel = document.getElementById("candUpsideDownPanel");
    if (panel && panel.classList.contains("open")) toggleCandidatePanel();
  }
});
'''

if 'function toggleCandidatePanel' not in index_html:
    index_html = index_html.replace('<script>', '<script>\n' + cand_js_addon)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_html)
print("[*] index.html updated successfully with dark theme & upside-down panel!")


# -------------------------------------------------------------
# 3. UPDATE QUIZ.HTML
# -------------------------------------------------------------
quiz_path = os.path.join(ROOT, "templates", "quiz.html")
with open(quiz_path, "r", encoding="utf-8") as f:
    quiz_html = f.read()

quiz_html = re.sub(r'<style id="embedded_css">.*?</style>', f'<style id="embedded_css">\n{dark_css}\n</style>', quiz_html, flags=re.DOTALL)

quiz_panel_html = '''
  <!-- Smooth Upside Down Exam Overview Deck -->
  <div class="panel-backdrop-overlay" id="quizPanelBackdrop" onclick="toggleQuizPanel()"></div>
  <div class="upside-down-panel" id="quizUpsideDownPanel">
    <div class="panel-inner">
      <div class="panel-header-bar">
        <h3><span>📊 Exam Overview & Real-Time Status</span></h3>
        <button type="button" class="panel-close-btn" onclick="toggleQuizPanel()" title="Close Panel">✕</button>
      </div>

      <div class="panel-grid-cards">
        <div class="panel-card-item">
          <span class="item-title">👤 Candidate Information</span>
          <span class="item-value" style="font-size:16px; color:#f8fafc;">{{ participant.name }}</span>
          <span style="font-size:12px; color:#94a3b8; margin-top:4px;">College ID: <strong style="color:#60a5fa;">{{ participant.college_id }}</strong></span>
        </div>

        <div class="panel-card-item">
          <span class="item-title">📝 Progress Overview</span>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
            <div>
              <div style="font-size:11px; color:#94a3b8;">Answered</div>
              <div style="font-size:22px; font-weight:800; color:#34d399;" id="deckAnswered">0</div>
            </div>
            <div>
              <div style="font-size:11px; color:#94a3b8;">Remaining</div>
              <div style="font-size:22px; font-weight:800; color:#f87171;" id="deckRemaining">30</div>
            </div>
            <div>
              <div style="font-size:11px; color:#94a3b8;">Marked Review</div>
              <div style="font-size:22px; font-weight:800; color:#c084fc;" id="deckReview">0</div>
            </div>
          </div>
        </div>

        <div class="panel-card-item">
          <span class="item-title">⚡ Speed Bonus Gauge</span>
          <span class="item-value" style="font-size:15px; color:#fbbf24;">Dynamic Speed Points Active</span>
          <p style="font-size:12px; color:#94a3b8; margin-top:4px;">Finishing with more time remaining awards extra points. Double-check marked answers before finishing.</p>
        </div>

        <div class="panel-card-item">
          <span class="item-title">✓ Ready to Finish?</span>
          <div style="margin-top:8px;">
            <button type="button" class="btn-submit-exam" style="width:100%; justify-content:center;" onclick="toggleQuizPanel(); openSubmitModal();">
              ✓ Open Submit Review
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Pull-Down Trigger Tab -->
  <div class="panel-toggle-tab" onclick="toggleQuizPanel()" id="quizPanelTab">
    <span>📊 Exam Status & Guidelines</span>
    <span class="tab-chevron">▼</span>
  </div>
'''

if 'id="quizUpsideDownPanel"' not in quiz_html:
    quiz_html = quiz_html.replace('<body>', '<body>\n' + quiz_panel_html)

quiz_js_addon = '''
function toggleQuizPanel() {
  const panel = document.getElementById("quizUpsideDownPanel");
  const backdrop = document.getElementById("quizPanelBackdrop");
  const tab = document.getElementById("quizPanelTab");
  if (!panel) return;
  const isOpen = panel.classList.contains("open");
  if (isOpen) {
    panel.classList.remove("open");
    if (backdrop) backdrop.classList.remove("open");
    if (tab) tab.querySelector(".tab-chevron").style.transform = "rotate(0deg)";
  } else {
    // Update live deck stats
    const answeredCount = Object.keys(answers).length;
    const revCount = reviewMarks.size;
    const elAns = document.getElementById("deckAnswered"); if (elAns) elAns.textContent = answeredCount;
    const elRem = document.getElementById("deckRemaining"); if (elRem) elRem.textContent = questions.length - answeredCount;
    const elRev = document.getElementById("deckReview"); if (elRev) elRev.textContent = revCount;

    panel.classList.add("open");
    if (backdrop) backdrop.classList.add("open");
    if (tab) tab.querySelector(".tab-chevron").style.transform = "rotate(180deg)";
  }
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const panel = document.getElementById("quizUpsideDownPanel");
    if (panel && panel.classList.contains("open")) toggleQuizPanel();
  }
});
'''

if 'function toggleQuizPanel' not in quiz_html:
    quiz_html = quiz_html.replace('let questions = [];', quiz_js_addon + '\nlet questions = [];')

with open(quiz_path, "w", encoding="utf-8") as f:
    f.write(quiz_html)
print("[*] quiz.html updated successfully with dark theme & upside-down panel!")


# -------------------------------------------------------------
# 4. UPDATE LEADERBOARD.HTML
# -------------------------------------------------------------
lb_path = os.path.join(ROOT, "templates", "leaderboard.html")
with open(lb_path, "r", encoding="utf-8") as f:
    lb_html = f.read()

lb_html = re.sub(r'<style id="embedded_css">.*?</style>', f'<style id="embedded_css">\n{dark_css}\n</style>', lb_html, flags=re.DOTALL)

lb_panel_html = '''
  <!-- Smooth Upside Down Leaderboard Highlights Deck -->
  <div class="panel-backdrop-overlay" id="lbPanelBackdrop" onclick="toggleLbPanel()"></div>
  <div class="upside-down-panel" id="lbUpsideDownPanel">
    <div class="panel-inner">
      <div class="panel-header-bar">
        <h3><span>🏆 Leaderboard Scoring & Host Deck</span></h3>
        <button type="button" class="panel-close-btn" onclick="toggleLbPanel()" title="Close Panel">✕</button>
      </div>

      <div class="panel-grid-cards">
        <div class="panel-card-item">
          <span class="item-title">🥇 Official Ranking Formula</span>
          <span class="item-value" style="font-size:14px; color:#fbbf24;">Total Points = Base Points + Speed Bonus</span>
          <p style="font-size:12px; color:#94a3b8; margin-top:4px;">In case of tied points, the participant who completed the exam in less time ranks higher.</p>
        </div>

        <div class="panel-card-item">
          <span class="item-title">👑 Host Dashboard Navigation</span>
          <span class="item-value" style="font-size:14px; color:#60a5fa;">Admin Control Center</span>
          <div style="margin-top:10px;">
            <a href="/" class="btn-secondary" style="font-size:12px; padding:6px 14px; display:inline-flex;">📊 Open Host Dashboard</a>
          </div>
        </div>

        <div class="panel-card-item">
          <span class="item-title">📱 Candidate Quiz Access</span>
          <span class="item-value" style="font-size:14px; color:#34d399;">Register New Participant</span>
          <div style="margin-top:10px;">
            <a href="/candidate" class="btn-secondary" style="font-size:12px; padding:6px 14px; display:inline-flex;">📱 Candidate Portal</a>
          </div>
        </div>

        <div class="panel-card-item">
          <span class="item-title">🔄 Live Auto-Refresh</span>
          <span class="item-value" style="font-size:14px; color:#38bdf8;">Synchronized Every 5s</span>
          <p style="font-size:12px; color:#94a3b8; margin-top:4px;">New exam submissions and rank changes update automatically without page reloading.</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Pull-Down Trigger Tab -->
  <div class="panel-toggle-tab" onclick="toggleLbPanel()" id="lbPanelTab">
    <span>🏆 Highlights & Host Deck</span>
    <span class="tab-chevron">▼</span>
  </div>
'''

if 'id="lbUpsideDownPanel"' not in lb_html:
    lb_html = lb_html.replace('<body>', '<body>\n' + lb_panel_html)

lb_html = lb_html.replace('background:#ecfdf5; color:#065f46;', 'background:rgba(16, 185, 129, 0.18); color:#34d399; border:1px solid rgba(16, 185, 129, 0.35);')

lb_js_addon = '''
function toggleLbPanel() {
  const panel = document.getElementById("lbUpsideDownPanel");
  const backdrop = document.getElementById("lbPanelBackdrop");
  const tab = document.getElementById("lbPanelTab");
  if (!panel) return;
  const isOpen = panel.classList.contains("open");
  if (isOpen) {
    panel.classList.remove("open");
    if (backdrop) backdrop.classList.remove("open");
    if (tab) tab.querySelector(".tab-chevron").style.transform = "rotate(0deg)";
  } else {
    panel.classList.add("open");
    if (backdrop) backdrop.classList.add("open");
    if (tab) tab.querySelector(".tab-chevron").style.transform = "rotate(180deg)";
  }
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    const panel = document.getElementById("lbUpsideDownPanel");
    if (panel && panel.classList.contains("open")) toggleLbPanel();
  }
});
'''

if 'function toggleLbPanel' not in lb_html:
    lb_html = lb_html.replace('let leaderboardData = [];', lb_js_addon + '\nlet leaderboardData = [];')

with open(lb_path, "w", encoding="utf-8") as f:
    f.write(lb_html)
print("[*] leaderboard.html updated successfully with dark theme & upside-down panel!")

print("\n[ALL COMPLETE] Dark theme & Smooth Upside-Down Panels applied to all 4 pages!")
