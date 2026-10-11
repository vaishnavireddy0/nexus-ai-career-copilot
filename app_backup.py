
from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

SKILLS = [
    "python", "java", "javascript", "html", "css",
    "sql", "flask", "django", "react", "node.js",
    "machine learning", "data analysis", "git",
    "github", "excel", "communication", "leadership",
    "problem solving", "project management", "aws",
    "docker", "c++", "typescript", "api"
]

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NEXUS AI | Resume Intelligence</title>
<style>
* { box-sizing: border-box; }
body {
  margin: 0; background: #080b14; color: #edf0ff;
  font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;
}
nav {
  padding: 22px 7%; border-bottom: 1px solid #25283b;
  color: #a78bfa; font-weight: bold; letter-spacing: 3px;
}
main { max-width: 950px; margin: 55px auto; padding: 0 22px; }
.tag { color: #67e8f9; letter-spacing: 3px; font-size: 12px; }
h1 { font-size: clamp(36px, 6vw, 60px); margin: 14px 0; }
h1 span { color: #a78bfa; }
p { color: #a8b0ca; line-height: 1.7; }
.panel {
  background: #111626; border: 1px solid #292e46;
  border-radius: 20px; padding: 25px; margin-top: 30px;
}
label { display: block; margin: 18px 0 9px; font-weight: 600; }
textarea {
  width: 100%; min-height: 150px; padding: 15px;
  border: 1px solid #333952; border-radius: 12px;
  background: #090d19; color: white; font: inherit;
  resize: vertical;
}
textarea:focus { outline: 1px solid #a78bfa; }
button {
  margin-top: 20px; padding: 14px 22px; width: 100%;
  border: 0; border-radius: 10px; background: #8b5cf6;
  color: white; font-weight: bold; font-size: 16px;
  cursor: pointer;
}
button:hover { background: #7042dc; }
.results { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.metric {
  background: #0a1020; padding: 18px; border-radius: 12px;
  border: 1px solid #292e46;
}
.number { font-size: 30px; color: #67e8f9; font-weight: bold; }
.chip {
  display: inline-block; margin: 5px; padding: 7px 10px;
  border-radius: 20px; background: #24203c; color: #c4b5fd;
  font-size: 13px;
}
footer { text-align: center; padding: 35px; color: #747d99; }
@media(max-width: 560px) {
  .results { grid-template-columns: 1fr; }
  main { margin-top: 35px; }
}
</style>
</head>
<body>
<nav>NEXUS AI <span style="color:white">/ CAREER COPILOT</span></nav>
<main>
  <div class="tag">CAREER INTELLIGENCE SYSTEM</div>
  <h1>Your career.<br><span>Decoded.</span></h1>
  <p>Analyze your resume, discover your skills, and compare your profile with a target job.</p>

  <form class="panel" method="POST">
    <label for="resume">Your resume text</label>
    <textarea id="resume" name="resume" required
      placeholder="Paste your resume text here...">{{ resume }}</textarea>
    <label for="job">Target job description (optional)</label>
    <textarea id="job" name="job"
      placeholder="Paste the job description here...">{{ job }}</textarea>
    <button type="submit">Analyze My Resume ↗</button>
  </form>

  {% if result %}
  <section class="panel">
    <div class="tag">ANALYSIS COMPLETE</div>
    <h2>Your resume insights</h2>
    <div class="results">
      <div class="metric">
        <div class="number">{{ result.skill_count }}</div>
        <p>Recognized skills</p>
      </div>
      <div class="metric">
        <div class="number">{{ result.match }}%</div>
        <p>Target job keyword coverage</p>
      </div>
    </div>
    <h3>Skills identified</h3>
    {% if result.skills %}
      {% for skill in result.skills %}
        <span class="chip">{{ skill }}</span>
      {% endfor %}
    {% else %}
      <p>No listed skills were detected. Try adding more resume details.</p>
    {% endif %}
    {% if result.missing %}
      <h3>Job keywords not detected</h3>
      {% for skill in result.missing %}
        <span class="chip">{{ skill }}</span>
      {% endfor %}
      <p>Check whether these skills genuinely match your experience before adding them to your resume.</p>
    {% endif %}
    <p>This is a basic keyword-based estimate, not an AI judgement or a prediction of hiring success.</p>
  </section>
  {% endif %}
</main>
<footer> NEXUS AI · YOUR CAREER COPILOT </footer>
</body>
</html>
"""


def find_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS:
        pattern = r"(?<![a-z0-9+#.])" + re.escape(skill) + r"(?![a-z0-9+#.])"
        if re.search(pattern, text):
            found.append(skill)
    return found


@app.route("/", methods=["GET", "POST"])
def home():
    resume = ""
    job = ""
    result = None

    if request.method == "POST":
        resume = request.form.get("resume", "")[:20000]
        job = request.form.get("job", "")[:10000]

        resume_skills = find_skills(resume)
        job_skills = find_skills(job)

        if job_skills:
            matched = [s for s in job_skills if s in resume_skills]
            missing = [s for s in job_skills if s not in resume_skills]
            score = round(len(matched) / len(job_skills) * 100)
        else:
            score = 0
            missing = []

        result = {
            "skills": resume_skills,
            "skill_count": len(resume_skills),
            "match": score,
            "missing": missing
        }

    return render_template_string(
        PAGE, resume=resume, job=job, result=result
    )


if __name__ == "__main__":
    app.run(debug=True)
