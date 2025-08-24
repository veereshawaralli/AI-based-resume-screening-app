import flask
import spacy
import re
import PyPDF2
from spacy.matcher import PhraseMatcher

app = flask.Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def classify_resume(text):
    text_lower = text.lower()
    category_keywords = {
        "Software Engineer": ["developer", "software", "python", "flask", "java", "backend", "frontend", "api", "django"],
        "Full Stack Developer": ["full stack", "frontend", "backend", "react", "node.js", "angular", "express"],
        "Data Scientist": ["machine learning", "data", "pandas", "numpy", "analysis", "statistics", "deep learning"],
        "AI/ML Engineer": ["deep learning", "tensorflow", "pytorch", "computer vision", "mlops", "bert", "transformers"],
        "DevOps Engineer": ["ci/cd", "jenkins", "docker", "kubernetes", "infrastructure", "aws", "ansible"],
        "UI/UX Designer": ["figma", "wireframe", "prototyping", "user research", "adobe xd", "interaction design"],
        "Marketing": ["seo", "content", "marketing", "branding", "social media", "adwords", "digital strategy"],
        "Finance": ["accounting", "finance", "tax", "audit", "investment", "budgeting"],
        "HR": ["recruitment", "payroll", "human resource", "employee engagement", "interview scheduling"],
        "Mechanical Engineer": ["mechanical", "solidworks", "autocad", "cad", "catia"],
        "Electrical Engineer": ["electrical", "pcb", "microcontroller", "power systems", "proteus"],
        "Civil Engineer": ["civil", "construction", "site", "structural", "estimation"],
        "Educator": ["teaching", "teacher", "curriculum", "lesson plan", "pedagogy"],
        "Project Manager": ["scrum", "agile", "timeline", "milestones", "pmp", "kanban"],
        "Business Analyst": ["requirement", "stakeholder", "gap analysis", "process modeling", "business case"],
        "Sales Executive": ["crm", "cold calling", "negotiation", "lead generation", "pitching"],
        "Legal Advisor": ["contract", "litigation", "legal", "compliance", "case law"],
        "Healthcare Professional": ["patient", "medical", "clinical", "nursing", "diagnosis", "healthcare"],
        "Content Writer": ["content writing", "copywriting", "blogs", "proofreading", "editing", "seo writing"]
    }
    for category, keywords in category_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    return "Other"

def extract_skills(text, skills_list):
    doc = nlp(text.lower())
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    patterns = [nlp.make_doc(skill.lower()) for skill in skills_list]
    matcher.add("Skills", patterns)
    matches = matcher(doc)
    return list(set([doc[start:end].text for match_id, start, end in matches]))

def extract_info(text):
    doc = nlp(text)
    name = next((ent.text for ent in doc.ents if ent.label_ == "PERSON"), "N/A")
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    phone_match = re.search(r"\+?\d[\d\s\-\(\)]{8,}\d", text)
    edu_keywords = ["b.tech", "m.tech", "bachelor", "master", "mba", "phd", "engineering", "science", "commerce"]
    education = next((sent.text for sent in doc.sents if any(k in sent.text.lower() for k in edu_keywords)), "N/A")
    return {
        "name": name,
        "email": email_match.group(0) if email_match else "N/A",
        "phone": phone_match.group(0) if phone_match else "N/A",
        "education": education
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        uploaded_file = flask.request.files["resume"]
        if uploaded_file.filename.endswith(".txt"):
            resume_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.filename.endswith(".pdf"):
            reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in reader.pages:
                resume_text += page.extract_text() or ""
        else:
            return "Unsupported file format. Please upload .txt or .pdf", 400

        predicted_category = classify_resume(resume_text)
        skills_map = {
            "Software Engineer": ["Python", "Java", "C++", "Git", "Flask", "SQL", "JavaScript", "REST API", "OOP"],
            "Full Stack Developer": ["React", "Node.js", "Express", "MongoDB", "HTML", "CSS", "Redux"],
            "Data Scientist": ["Pandas", "NumPy", "Scikit-learn", "NLP", "Deep Learning", "TensorFlow", "Matplotlib", "Seaborn"],
            "AI/ML Engineer": ["TensorFlow", "PyTorch", "Keras", "CNN", "RNN", "Transformer", "MLOps", "Computer Vision"],
            "DevOps Engineer": ["Docker", "Kubernetes", "CI/CD", "AWS", "Terraform", "Jenkins", "GitHub Actions"],
            "UI/UX Designer": ["Figma", "Adobe XD", "Sketch", "Prototyping", "Wireframing", "User Research"],
            "Marketing": ["SEO", "Content Writing", "Google Analytics", "Campaign Management", "Social Media", "Email Marketing"],
            "Finance": ["Accounting", "Excel", "Tax", "Budgeting", "Financial Modeling", "Investment Analysis"],
            "HR": ["Recruitment", "Payroll", "Employee Engagement", "Interviewing", "Training"],
            "Mechanical Engineer": ["SolidWorks", "AutoCAD", "Ansys", "CAD", "Thermodynamics"],
            "Electrical Engineer": ["PCB", "Microcontroller", "Circuit", "Proteus", "Power Systems"],
            "Civil Engineer": ["AutoCAD", "Construction", "Structural Analysis", "Project Estimation"],
            "Educator": ["Teaching", "Curriculum Design", "Lesson Planning", "Assessment"],
            "Project Manager": ["Agile", "Scrum", "Leadership", "Risk Management", "Planning", "Jira"],
            "Business Analyst": ["Requirement Gathering", "SQL", "Data Visualization", "Gap Analysis", "UML"],
            "Sales Executive": ["CRM", "Sales Pitch", "Negotiation", "Lead Generation", "Cold Calling"],
            "Legal Advisor": ["Contract Drafting", "Compliance", "Litigation", "Legal Research"],
            "Healthcare Professional": ["Clinical", "Diagnosis", "Patient Care", "Medical Records"],
            "Content Writer": ["Copywriting", "Proofreading", "Editing", "SEO Writing", "Creative Writing"]
        }
        skill_list = skills_map.get(predicted_category, [])
        matched_skills = extract_skills(resume_text, skill_list)
        info = extract_info(resume_text)
        score = int((len(matched_skills) / len(skill_list)) * 100) if skill_list else 0

        return flask.render_template(
            "result.html",
            predicted_category=predicted_category,
            recommended_job=predicted_category,
            name=info["name"],
            phone=info["phone"],
            email=info["email"],
            education=info["education"],
            matched=matched_skills,
            score=score
        )
    return flask.render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
