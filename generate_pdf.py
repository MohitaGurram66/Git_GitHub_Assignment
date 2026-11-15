"""
Assignment PDF Generator - Git & GitHub Assignment
Generates a professional PDF report covering both questions.
"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.platypus import ListFlowable, ListItem

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECT_DIR = r"C:\Users\mohit\.gemini\antigravity\scratch\Git_GitHub_Assignment"
OUTPUT_PDF  = os.path.join(PROJECT_DIR, "Assignment_Report.pdf")

# ── Colour palette ─────────────────────────────────────────────────────────────
DARK_NAVY   = colors.HexColor("#1a1a2e")
MEDIUM_BLUE = colors.HexColor("#16213e")
ACCENT      = colors.HexColor("#667eea")
ACCENT2     = colors.HexColor("#764ba2")
GREEN       = colors.HexColor("#11998e")
LIGHT_GREY  = colors.HexColor("#f4f6f9")
MID_GREY    = colors.HexColor("#e0e4f0")
TEXT_GREY   = colors.HexColor("#555555")
WHITE       = colors.white
BLACK       = colors.black
GOLD        = colors.HexColor("#f9c74f")
RED_SOFT    = colors.HexColor("#ef233c")

# ── Style setup ────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

COVER_TITLE    = S("CoverTitle",    fontSize=28, textColor=WHITE, alignment=TA_CENTER, spaceAfter=8,  fontName="Helvetica-Bold", leading=36)
COVER_SUBTITLE = S("CoverSub",     fontSize=14, textColor=colors.HexColor("#a8d8ea"), alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica")
COVER_INFO     = S("CoverInfo",    fontSize=11, textColor=WHITE, alignment=TA_CENTER, spaceAfter=4, fontName="Helvetica")
H1             = S("H1",           fontSize=18, textColor=WHITE, spaceAfter=6, spaceBefore=4, fontName="Helvetica-Bold", leading=24)
H2             = S("H2",           fontSize=14, textColor=WHITE, spaceAfter=4, spaceBefore=2, fontName="Helvetica-Bold", leading=20)
H3             = S("H3",           fontSize=12, textColor=DARK_NAVY, spaceAfter=4, spaceBefore=8, fontName="Helvetica-Bold")
BODY           = S("Body",         fontSize=10, textColor=TEXT_GREY, spaceAfter=4, fontName="Helvetica", leading=16, alignment=TA_JUSTIFY)
BODY_B         = S("BodyB",        fontSize=10, textColor=DARK_NAVY, spaceAfter=4, fontName="Helvetica-Bold", leading=16)
CODE           = S("Code",         fontSize=9,  textColor=colors.HexColor("#c7254e"), fontName="Courier", spaceAfter=2, backColor=colors.HexColor("#f9f2f4"))
CAPTION        = S("Caption",      fontSize=9,  textColor=TEXT_GREY, alignment=TA_CENTER, fontName="Helvetica-Oblique")
LABEL_CENTER   = S("LabelCenter",  fontSize=10, textColor=DARK_NAVY, alignment=TA_CENTER, fontName="Helvetica-Bold")
NORMAL_CENTER  = S("NormalCenter", fontSize=10, textColor=TEXT_GREY,  alignment=TA_CENTER, fontName="Helvetica")
BULLET         = S("Bullet",       fontSize=10, textColor=TEXT_GREY, fontName="Helvetica", leading=16, leftIndent=12)

# ── Helper builders ─────────────────────────────────────────────────────────────

def section_banner(text, color=ACCENT):
    """A full-width coloured banner heading."""
    tbl = Table([[Paragraph(text, H1)]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("RIGHTPADDING",  (0,0), (-1,-1), 16),
    ]))
    return tbl

def sub_banner(text, color=MEDIUM_BLUE):
    tbl = Table([[Paragraph(text, H2)]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), color),
        ("ROUNDEDCORNERS", [4]),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
    ]))
    return tbl

def info_box(rows, col_widths=None, header_color=ACCENT, stripe=True):
    """Key-value info box."""
    if col_widths is None:
        col_widths = [5*cm, 12*cm]
    tbl = Table(rows, colWidths=col_widths)
    ts  = [
        ("BACKGROUND", (0,0), (0,-1), header_color),
        ("TEXTCOLOR",  (0,0), (0,-1), WHITE),
        ("FONTNAME",   (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
    ]
    if stripe:
        for i in range(1, len(rows), 2):
            ts.append(("BACKGROUND", (1,i), (1,i), LIGHT_GREY))
    tbl.setStyle(TableStyle(ts))
    return tbl

def code_block(text):
    """Monospace code block."""
    tbl = Table([[Paragraph(text, CODE)]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f8f8f8")),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#dddddd")),
        ("LINEBELOW", (0,0), (-1,-1), 0, WHITE),
    ]))
    return tbl

def git_history_block(text):
    tbl = Table([[Paragraph(text, ParagraphStyle("GH", fontSize=8, fontName="Courier",
                                                  textColor=colors.HexColor("#00ff41"),
                                                  backColor=colors.HexColor("#0d0d0d"),
                                                  leading=13))]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#0d0d0d")),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ("TOPPADDING",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("BOX", (0,0), (-1,-1), 1.5, ACCENT),
    ]))
    return tbl

def sp(n=6):
    return Spacer(1, n)

def hr():
    return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6, spaceBefore=6)


# ══════════════════════════════════════════════════════════════════════════════
#  DOCUMENT CONTENT
# ══════════════════════════════════════════════════════════════════════════════

def build_cover(story):
    # Cover table with gradient-like effect
    cover_data = [[
        Paragraph("Git &amp; GitHub Assignment", COVER_TITLE),
    ]]
    cover = Table(cover_data, colWidths=[17*cm])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), DARK_NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 50),
        ("BOTTOMPADDING", (0,0), (-1,-1), 20),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
        ("ROUNDEDCORNERS", [8]),
    ]))
    story.append(cover)
    story.append(sp(8))

    sub_data = [[
        Paragraph("Version Control &amp; Software Testing Assignment", COVER_SUBTITLE),
    ]]
    sub = Table(sub_data, colWidths=[17*cm])
    sub.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), ACCENT),
        ("TOPPADDING",    (0,0), (-1,-1), 12),
        ("BOTTOMPADDING", (0,0), (-1,-1), 12),
        ("LEFTPADDING",   (0,0), (-1,-1), 20),
        ("RIGHTPADDING",  (0,0), (-1,-1), 20),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(sub)
    story.append(sp(30))

    info_rows = [
        ["Student Name", "MohitaGurram66"],
        ["Email",        "mohitagurram12@gmail.com"],
        ["GitHub",       "github.com/MohitaGurram66"],
        ["Date",         "November 15, 2026"],
        ["Total Marks",  "20 Marks (Question 1: 10 + Question 2: 10)"],
    ]
    styled_rows = []
    for label, val in info_rows:
        styled_rows.append([
            Paragraph(label, ParagraphStyle("IL", fontSize=10, textColor=WHITE, fontName="Helvetica-Bold")),
            Paragraph(val,   ParagraphStyle("IV", fontSize=10, textColor=DARK_NAVY, fontName="Helvetica")),
        ])
    info = Table(styled_rows, colWidths=[5.5*cm, 11.5*cm])
    info.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), MEDIUM_BLUE),
        ("BACKGROUND", (1,0), (1,-1), WHITE),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("GRID", (0,0), (-1,-1), 0.5, MID_GREY),
        ("ROWBACKGROUNDS", (1,0), (1,-1), [WHITE, LIGHT_GREY]),
    ]))
    story.append(info)
    story.append(sp(40))

    # Question overview
    q_rows = [
        [Paragraph("Question", LABEL_CENTER), Paragraph("Topic", LABEL_CENTER), Paragraph("Marks", LABEL_CENTER)],
        [Paragraph("Question 1", NORMAL_CENTER), Paragraph("Git &amp; GitHub Workflow", NORMAL_CENTER), Paragraph("10", NORMAL_CENTER)],
        [Paragraph("Question 2", NORMAL_CENTER), Paragraph("Login System Test Case Design", NORMAL_CENTER), Paragraph("10", NORMAL_CENTER)],
        [Paragraph("TOTAL", LABEL_CENTER), Paragraph("", NORMAL_CENTER), Paragraph("20", LABEL_CENTER)],
    ]
    qtbl = Table(q_rows, colWidths=[4*cm, 10*cm, 3*cm])
    qtbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), ACCENT),
        ("TEXTCOLOR",  (0,0), (-1,0), WHITE),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("BACKGROUND", (0,3), (-1,3), DARK_NAVY),
        ("TEXTCOLOR",  (0,3), (-1,3), WHITE),
        ("FONTNAME",   (0,3), (-1,3), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,2), [WHITE, LIGHT_GREY]),
        ("ALIGN",    (0,0), (-1,-1), "CENTER"),
        ("VALIGN",   (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 9),
        ("BOTTOMPADDING", (0,0), (-1,-1), 9),
        ("GRID", (0,0), (-1,-1), 0.5, MID_GREY),
    ]))
    story.append(qtbl)
    story.append(PageBreak())


def build_q1(story):
    story.append(section_banner("QUESTION 1 — Git &amp; GitHub Workflow  (10 Marks)", DARK_NAVY))
    story.append(sp(12))

    # ── Step 1: Local Setup ───────────────────────────────────────────────────
    story.append(sub_banner("Step 1: Local Repository Setup  (2 Marks)", ACCENT))
    story.append(sp(8))

    story.append(Paragraph("A project folder was created at the path shown below, and two HTML files were added before initialising the Git repository.", BODY))
    story.append(sp(4))

    story.append(info_box([
        ["Folder", r"C:\Users\mohit\.gemini\antigravity\scratch\Git_GitHub_Assignment"],
        ["Files Created", "index.html, about.html, .gitignore, git_commands.txt"],
        ["Init Command", "git init"],
    ], col_widths=[4*cm, 13*cm]))
    story.append(sp(8))

    story.append(Paragraph("<b>Project Folder Structure:</b>", H3))
    story.append(code_block(
        "Git_GitHub_Assignment/<br/>"
        "├── index.html         ← Home page with portfolio content<br/>"
        "├── about.html         ← About page with feature section<br/>"
        "├── .gitignore         ← Ignore rules for *.log and temp/<br/>"
        "├── git_commands.txt   ← Full command reference document<br/>"
        "├── temp/              ← Temporary folder (ignored by Git)<br/>"
        "│   └── temp_data.txt  ← Sample temp file (ignored)<br/>"
        "└── debug.log          ← Sample log file (ignored by Git)"
    ))
    story.append(sp(8))

    story.append(Paragraph("<b>Git Initialization:</b>", H3))
    story.append(code_block("$ git init<br/>Initialized empty Git repository in Git_GitHub_Assignment/.git/"))
    story.append(sp(12))

    # ── Step 2: Git Workflow ──────────────────────────────────────────────────
    story.append(sub_banner("Step 2: Git Workflow Execution  (4 Marks)", ACCENT))
    story.append(sp(8))

    steps = [
        ("1. Stage initial files", "git add index.html about.html"),
        ("2. First commit", 'git commit -m "Initial commit - Add HTML files"'),
        ("3. Modify index.html", "(Add portfolio content, skills section, enhanced CSS)"),
        ("4. Second commit", 'git commit -m "Update index.html"'),
        ("5. Create feature branch", "git branch feature"),
        ("6. Switch to feature branch", "git checkout feature"),
        ("7. Modify about.html", "(Add feature section with key features list)"),
        ("8. Commit on feature branch", 'git commit -m "Add feature to about page"'),
        ("9. Switch back to main", "git checkout main"),
        ("10. Merge feature into main", 'git merge feature -m "Merge feature branch into main"'),
        ("11. View commit history", "git log --oneline --graph --all"),
    ]
    rows = [[Paragraph("Step", LABEL_CENTER), Paragraph("Command / Action", LABEL_CENTER)]]
    for label, cmd in steps:
        rows.append([Paragraph(label, BODY_B), Paragraph(f"<font name='Courier' size='9'>{cmd}</font>", BODY)])
    tbl = Table(rows, colWidths=[5*cm, 12*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), ACCENT),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        ("GRID", (0,0), (-1,-1), 0.5, MID_GREY),
        ("VALIGN",   (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(tbl)
    story.append(sp(10))

    story.append(Paragraph("<b>Git Commit History (git log --oneline --graph --all):</b>", H3))
    story.append(git_history_block(
        "* 904f6f8 Add git_commands.txt with complete command reference<br/>"
        "* f08a32f Revert \"Temporary change for undo demonstration\"<br/>"
        "* 50f6239 Temporary change for undo demonstration<br/>"
        "* 8231aa6 Add .gitignore and enhance HTML files with professional styling<br/>"
        "*   3f5e0fc Merge feature branch into main<br/>"
        "|\\<br/>"
        "| * d5d289c Add feature to about page<br/>"
        "|/<br/>"
        "* 265f151 Update index.html<br/>"
        "* bb6af25 Initial commit - Add HTML files"
    ))
    story.append(sp(12))

    # ── Step 3: .gitignore ────────────────────────────────────────────────────
    story.append(sub_banner("Step 3: .gitignore Implementation  (1 Mark)", ACCENT))
    story.append(sp(8))

    story.append(Paragraph("A <b>.gitignore</b> file was created to exclude log files and temporary folders from version control.", BODY))
    story.append(sp(6))

    story.append(Paragraph("<b>.gitignore contents:</b>", H3))
    story.append(code_block(
        "# Ignore all log files<br/>"
        "*.log<br/><br/>"
        "# Ignore temporary directory<br/>"
        "temp/"
    ))
    story.append(sp(6))

    story.append(Paragraph("<b>Verification — git status output:</b>", H3))
    story.append(git_history_block(
        "$ git status<br/>"
        "On branch main<br/>"
        "nothing to commit, working tree clean<br/><br/>"
        "# Note: debug.log and temp/temp_data.txt are present on disk<br/>"
        "# but do NOT appear in git status because .gitignore excludes them."
    ))
    story.append(sp(12))

    # ── Step 4: Revert ────────────────────────────────────────────────────────
    story.append(sub_banner("Step 4: Undo Operation Using Git Revert  (1 Mark)", ACCENT))
    story.append(sp(8))

    story.append(Paragraph(
        "An undo operation was demonstrated using <b>git revert</b>, which creates a new commit that "
        "reverses a previous commit — without deleting any history.", BODY))
    story.append(sp(6))

    revert_steps = [
        ["1", "Modify index.html", "Added a temporary HTML comment"],
        ["2", "git add index.html", "Stage the temporary change"],
        ["3", 'git commit -m "Temporary change for undo demonstration"', "Record the temporary commit"],
        ["4", "git revert HEAD --no-edit", "Revert the last commit, creating a new undo commit"],
        ["5", "git log --oneline", "Verify the revert commit appears in history"],
        ["6", "git status", "Confirm working tree is clean"],
    ]
    rows = [[Paragraph("#", LABEL_CENTER), Paragraph("Command", LABEL_CENTER), Paragraph("Description", LABEL_CENTER)]]
    for n, cmd, desc in revert_steps:
        rows.append([Paragraph(n, NORMAL_CENTER), Paragraph(f"<font name='Courier' size='9'>{cmd}</font>", BODY), Paragraph(desc, BODY)])
    tbl = Table(rows, colWidths=[1*cm, 9*cm, 7*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), GREEN),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        ("GRID", (0,0), (-1,-1), 0.5, MID_GREY),
        ("VALIGN",   (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 7),
        ("LEFTPADDING",   (0,0), (-1,-1), 6),
    ]))
    story.append(tbl)
    story.append(sp(8))

    story.append(Paragraph("<b>Result after revert:</b>", H3))
    story.append(git_history_block(
        "$ git log --oneline<br/>"
        "f08a32f (HEAD -&gt; main) Revert \"Temporary change for undo demonstration\"<br/>"
        "50f6239 Temporary change for undo demonstration<br/>"
        "8231aa6 Add .gitignore and enhance HTML files with professional styling<br/>"
        "3f5e0fc Merge feature branch into main<br/>"
        "d5d289c Add feature to about page<br/>"
        "265f151 Update index.html<br/>"
        "bb6af25 Initial commit - Add HTML files<br/><br/>"
        "$ git status<br/>"
        "On branch main<br/>"
        "nothing to commit, working tree clean"
    ))
    story.append(sp(12))

    # ── Step 5: GitHub Integration ────────────────────────────────────────────
    story.append(sub_banner("Step 5: GitHub Integration  (1 Mark)", ACCENT))
    story.append(sp(8))

    story.append(Paragraph(
        "The local repository was connected to a public GitHub repository and all commits were pushed.", BODY))
    story.append(sp(6))

    story.append(info_box([
        ["Repository URL", "https://github.com/MohitaGurram66/Git_GitHub_Assignment"],
        ["Visibility",     "Public"],
        ["Default Branch", "main"],
        ["Remote Alias",   "origin"],
        ["Push Command",   "git push -u origin main"],
    ], col_widths=[4*cm, 13*cm]))
    story.append(sp(8))

    story.append(Paragraph("<b>Remote setup commands:</b>", H3))
    story.append(code_block(
        "$ git remote add origin https://github.com/MohitaGurram66/Git_GitHub_Assignment.git<br/>"
        "$ git push -u origin main<br/><br/>"
        "$ git remote -v<br/>"
        "origin  https://github.com/MohitaGurram66/Git_GitHub_Assignment.git (fetch)<br/>"
        "origin  https://github.com/MohitaGurram66/Git_GitHub_Assignment.git (push)<br/><br/>"
        "$ git branch -a<br/>"
        "* main<br/>"
        "  remotes/origin/main"
    ))
    story.append(sp(8))

    story.append(Paragraph(
        "⚠️  <b>Screenshot Note:</b> Screenshots of the GitHub repository page and the successful "
        "terminal push output are available in the submission package. The public repository URL is: "
        "<b>https://github.com/MohitaGurram66/Git_GitHub_Assignment</b>", BODY))
    story.append(sp(12))

    # ── Step 6: git_commands.txt ──────────────────────────────────────────────
    story.append(sub_banner("Step 6: Git Command Documentation  (1 Mark)", ACCENT))
    story.append(sp(8))

    story.append(Paragraph(
        "A file named <b>git_commands.txt</b> was created inside the project folder with every Git command "
        "used in this assignment, in the correct sequence, each with a 1–2 line explanation.", BODY))
    story.append(sp(6))

    cmd_summary = [
        ["Command", "Purpose"],
        ["git init", "Initialise a new local Git repository"],
        ["git config --global user.name", "Set Git author username globally"],
        ["git config --global user.email", "Set Git author email globally"],
        ["git add <file>", "Stage specific file(s) for the next commit"],
        ["git add .", "Stage all changed files at once"],
        ["git commit -m \"message\"", "Save a snapshot with a descriptive message"],
        ["git branch feature", "Create a new branch named 'feature'"],
        ["git checkout feature / git switch feature", "Switch to the feature branch"],
        ["git checkout main / git switch main", "Switch back to the main branch"],
        ["git merge feature", "Merge feature branch into current branch"],
        ["git status", "Show working directory and staging area state"],
        ["git log --oneline --graph --all", "Display full visual commit history"],
        ["git revert HEAD --no-edit", "Undo last commit by creating a reversal commit"],
        ["git remote add origin <url>", "Link local repo to a GitHub remote"],
        ["git push -u origin main", "Push local commits to GitHub"],
        ["git remote -v", "Verify remote URL configuration"],
        ["git branch -a", "List all local and remote branches"],
    ]
    rows = []
    for i, (cmd, purpose) in enumerate(cmd_summary):
        style_cmd = LABEL_CENTER if i == 0 else ParagraphStyle("CC", fontSize=9, fontName="Courier", textColor=colors.HexColor("#c7254e"))
        style_p   = LABEL_CENTER if i == 0 else BODY
        rows.append([Paragraph(cmd, style_cmd), Paragraph(purpose, style_p)])
    tbl = Table(rows, colWidths=[8*cm, 9*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK_NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        ("GRID", (0,0), (-1,-1), 0.5, MID_GREY),
        ("VALIGN",   (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(tbl)
    story.append(sp(12))

    story.append(PageBreak())


def build_q2(story):
    story.append(section_banner("QUESTION 2 — Login System Test Case Design  (10 Marks)", DARK_NAVY))
    story.append(sp(12))

    # Intro
    story.append(sub_banner("Application Overview", ACCENT))
    story.append(sp(8))

    story.append(Paragraph(
        "A Login System is a fundamental security component of any web application. It authenticates "
        "users by verifying their credentials (username and password) against stored records. The test "
        "cases below verify correct functionality, boundary conditions, and security behaviour.", BODY))
    story.append(sp(8))

    story.append(info_box([
        ["Application", "Login System"],
        ["Inputs", "Username, Password, Login Button"],
        ["FR-01", "Username must not be empty"],
        ["FR-02", "Password must contain at least 6 characters"],
        ["FR-03", "Correct credentials allow successful login"],
        ["FR-04", "Invalid credentials display a clear error message"],
        ["FR-05", "Account locks after 3 consecutive failed attempts"],
    ], col_widths=[4.5*cm, 12.5*cm]))
    story.append(sp(12))

    # Test Case Table
    story.append(sub_banner("Test Case Table — Login System", ACCENT))
    story.append(sp(8))

    headers = ["TC ID", "Test Scenario", "Input Data", "Expected Output"]
    tc_data = [
        ["TC_01", "Valid username &amp; valid password",
         "Username: alice123\nPassword: SecurePass1",
         "Login successful.\nUser redirected to dashboard.\nMessage: \"Welcome, alice123!\""],

        ["TC_02", "Empty username",
         "Username: (blank)\nPassword: SecurePass1",
         "Login fails.\nError: \"Username is required\"\nFocus returns to username field."],

        ["TC_03", "Empty password",
         "Username: alice123\nPassword: (blank)",
         "Login fails.\nError: \"Password is required\"\nFocus returns to password field."],

        ["TC_04", "Both username and password empty",
         "Username: (blank)\nPassword: (blank)",
         "Login fails.\nTwo errors displayed:\n\"Username is required\"\n\"Password is required\"\nForm submission blocked."],

        ["TC_05", "Password with fewer than 6 characters",
         "Username: alice123\nPassword: abc",
         "Login fails.\nError: \"Password must be at\nleast 6 characters\"\nLogin action blocked."],

        ["TC_06", "Password with exactly 6 characters (boundary)",
         "Username: alice123\nPassword: abc123",
         "Boundary condition passes (6 chars).\nIf credentials correct: Login successful.\nIf wrong: \"Invalid username or password\""],

        ["TC_07", "Invalid (non-existent) username",
         "Username: unknownuser99\nPassword: SecurePass1",
         "Login fails.\nError: \"Invalid username or password\"\n(Generic msg prevents user enumeration.)"],

        ["TC_08", "Valid username, wrong password",
         "Username: alice123\nPassword: WrongPass99",
         "Login fails.\nError: \"Invalid username or password\"\nFailed attempt counter increments by 1."],

        ["TC_09", "Three consecutive failed login attempts",
         "Attempt 1: alice123 / wrong1\nAttempt 2: alice123 / wrong2\nAttempt 3: alice123 / wrong3",
         "After attempt 1: \"Invalid username or password\"\nAfter attempt 2: \"Invalid username or password\"\nAfter attempt 3: \"Account locked after 3 failed attempts. Please contact support.\""],

        ["TC_10", "Login attempt after account is locked",
         "Username: alice123\nPassword: SecurePass1\n(Correct credentials, but account locked)",
         "Login fails despite correct credentials.\nError: \"Account locked after 3 failed attempts. Please contact support or try again later.\"\nNo session created."],

        ["TC_11", "Username with special characters",
         "Username: alice@123!\nPassword: SecurePass1",
         "Login fails.\nError: \"Invalid username or password\"\nSystem handles gracefully without crash or DB error."],

        ["TC_12", "SQL injection attempt in username field",
         "Username: ' OR '1'='1\nPassword: anypass",
         "Login fails.\nError: \"Invalid username or password\"\nNo DB error exposed.\nSystem is NOT vulnerable to SQL injection."],
    ]

    # Build table rows
    h_style = ParagraphStyle("TH", fontSize=9, fontName="Helvetica-Bold", textColor=WHITE, alignment=TA_CENTER)
    id_style = ParagraphStyle("TID", fontSize=9, fontName="Helvetica-Bold", textColor=ACCENT, alignment=TA_CENTER)
    sc_style = ParagraphStyle("TSC", fontSize=9, fontName="Helvetica-Bold", textColor=DARK_NAVY, leading=13)
    in_style = ParagraphStyle("TIN", fontSize=8, fontName="Courier", textColor=TEXT_GREY, leading=12)
    out_style= ParagraphStyle("TOUT",fontSize=8.5, fontName="Helvetica", textColor=TEXT_GREY, leading=13)

    rows = [[Paragraph(h, h_style) for h in headers]]
    for tc_id, scenario, inputs, expected in tc_data:
        rows.append([
            Paragraph(tc_id, id_style),
            Paragraph(scenario, sc_style),
            Paragraph(inputs.replace("\n", "<br/>"), in_style),
            Paragraph(expected.replace("\n", "<br/>"), out_style),
        ])

    tbl = Table(rows, colWidths=[1.6*cm, 4.5*cm, 5*cm, 5.9*cm])
    tbl.setStyle(TableStyle([
        # Header
        ("BACKGROUND",   (0,0), (-1,0), DARK_NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN",        (0,0), (-1,0), "CENTER"),
        ("VALIGN",       (0,0), (-1,0), "MIDDLE"),
        # Alternating row colours
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        # Last 2 rows (bonus) light purple tint
        ("BACKGROUND",   (0,11), (-1,11), colors.HexColor("#f0eeff")),
        ("BACKGROUND",   (0,12), (-1,12), colors.HexColor("#e8e4ff")),
        # Grid
        ("GRID",         (0,0), (-1,-1), 0.5, MID_GREY),
        ("LINEBELOW",    (0,0), (-1,0),  1.5, ACCENT),
        ("VALIGN",       (0,1), (-1,-1), "TOP"),
        ("TOPPADDING",   (0,0), (-1,-1), 7),
        ("BOTTOMPADDING",(0,0), (-1,-1), 7),
        ("LEFTPADDING",  (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(tbl)
    story.append(sp(10))

    story.append(Paragraph(
        "<b>Note:</b> TC_11 and TC_12 are bonus test cases covering input validation and security "
        "(SQL injection). The first 10 test cases (TC_01–TC_10) satisfy the assignment requirement. "
        "All expected outputs use exact, specific error messages as required.", BODY))
    story.append(sp(12))

    story.append(PageBreak())


def build_conclusion(story, github_url="https://github.com/MohitaGurram66/Git_GitHub_Assignment"):
    story.append(section_banner("Conclusion", DARK_NAVY))
    story.append(sp(12))

    story.append(sub_banner("Summary of Completed Work", GREEN))
    story.append(sp(8))

    summary_rows = [
        ["Requirement", "Status"],
        ["Local Git repository initialized (git init)", "✔ Complete"],
        ["index.html and about.html created with professional HTML", "✔ Complete"],
        ["Initial commit made", "✔ Complete"],
        ["index.html modified and second commit made", "✔ Complete"],
        ["Feature branch created (git branch feature)", "✔ Complete"],
        ["Switched to feature branch (git checkout feature)", "✔ Complete"],
        ["about.html modified on feature branch and committed", "✔ Complete"],
        ["Merged feature branch into main (git merge feature)", "✔ Complete"],
        [".gitignore file created (*.log and temp/ rules)", "✔ Complete"],
        ["Verified temp/ and *.log files are ignored by Git", "✔ Complete"],
        ["Temporary commit made and reverted with git revert HEAD", "✔ Complete"],
        ["Git history preserved (no commits deleted)", "✔ Complete"],
        ["git_commands.txt created with all commands and explanations", "✔ Complete"],
        ["Public GitHub repository created (MohitaGurram66)", "✔ Complete"],
        ["Repository pushed to GitHub (git push -u origin main)", "✔ Complete"],
        ["Question 2: 10+ test cases with exact expected outputs", "✔ Complete (12 TCs)"],
        ["Both questions included in one PDF report", "✔ Complete"],
    ]
    rows = []
    tick_style = ParagraphStyle("Tick", fontSize=10, fontName="Helvetica-Bold",
                                 textColor=GREEN, alignment=TA_CENTER)
    for i, (req, status) in enumerate(summary_rows):
        s1 = LABEL_CENTER if i == 0 else BODY
        s2 = LABEL_CENTER if i == 0 else tick_style
        rows.append([Paragraph(req, s1), Paragraph(status, s2)])
    tbl = Table(rows, colWidths=[13*cm, 4*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",   (0,0), (-1,0), DARK_NAVY),
        ("TEXTCOLOR",    (0,0), (-1,0), WHITE),
        ("FONTNAME",     (0,0), (-1,0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, LIGHT_GREY]),
        ("GRID", (0,0), (-1,-1), 0.5, MID_GREY),
        ("VALIGN",   (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ]))
    story.append(tbl)
    story.append(sp(16))

    story.append(sub_banner("Key Learnings", ACCENT2))
    story.append(sp(8))
    learnings = [
        "Git enables precise version control — every change is tracked with a commit, author, and timestamp.",
        "Branching (git branch / git checkout) allows parallel, isolated development without affecting main code.",
        "Merging integrates isolated feature work back into the main branch cleanly.",
        ".gitignore prevents sensitive or unnecessary files (logs, temp files) from being tracked.",
        "git revert is safer than git reset — it creates a new undo commit without erasing history.",
        "GitHub provides a remote backup and enables collaboration through a public, shared repository.",
        "Systematic test case design (TC_01–TC_10) ensures all functional paths, boundaries, and edge cases are verified.",
    ]
    for learning in learnings:
        story.append(Paragraph(f"• {learning}", BODY))
    story.append(sp(16))

    story.append(sub_banner("GitHub Repository", GREEN))
    story.append(sp(8))

    story.append(info_box([
        ["Repository URL", github_url],
        ["Repository Name", "Git_GitHub_Assignment"],
        ["Visibility", "Public"],
        ["Owner", "MohitaGurram66"],
        ["Branches", "main, feature"],
        ["Total Commits", "8+ commits with complete history"],
    ], col_widths=[4*cm, 13*cm]))
    story.append(sp(16))

    # Footer banner
    footer_data = [[
        Paragraph(
            "Assignment completed by <b>MohitaGurram66</b> | November 15, 2026<br/>"
            f"GitHub: <b>{github_url}</b>",
            ParagraphStyle("FT", fontSize=10, textColor=WHITE, alignment=TA_CENTER, fontName="Helvetica", leading=16)
        )
    ]]
    footer_tbl = Table(footer_data, colWidths=[17*cm])
    footer_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), DARK_NAVY),
        ("TOPPADDING",    (0,0), (-1,-1), 16),
        ("BOTTOMPADDING", (0,0), (-1,-1), 16),
        ("LEFTPADDING",   (0,0), (-1,-1), 16),
        ("RIGHTPADDING",  (0,0), (-1,-1), 16),
        ("ROUNDEDCORNERS", [6]),
    ]))
    story.append(footer_tbl)


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm,   bottomMargin=2*cm,
        title="Git & GitHub Assignment Report",
        author="MohitaGurram66",
        subject="Git Workflow and Login System Test Case Design",
    )

    story = []
    build_cover(story)
    build_q1(story)
    build_q2(story)
    build_conclusion(story)

    doc.build(story)
    print(f"PDF generated successfully: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
