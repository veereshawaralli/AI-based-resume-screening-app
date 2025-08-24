# AI-based-resume-screening-app
An NLP-powered Resume Screening System that automates the initial phase of recruitment by classifying resumes into job categories and extracting candidate information such as name, contact details, education, and key skills.

##Features:
Upload resumes in PDF or TXT format

Text extraction using PyPDF2

Preprocessing with spaCy (tokenization, cleaning, keyword matching)

Resume classification into predefined job roles (12 categories)

Skill extraction using spaCy PhraseMatcher

User-friendly Flask web interface (HTML/CSS templates)

Lightweight, transparent, and does not require training datasets

###System Architecture :
User uploads a resume (PDF/TXT)

Text extracted with PyPDF2

Preprocessing with spaCy (tokenization, lowercasing)

Keyword-based classification into job roles

Skill extraction using PhraseMatcher

Results displayed in a web interface (Flask)

####Tech Stack
Language: Python 3.x

Backend: Flask

Frontend: HTML/CSS

Libraries: spaCy, PyPDF2

NLP Model: en_core_web_sm

#Future Enhancements :
Support for DOCX and image-based resumes (OCR)

Semantic classification using ML/Transformers (e.g., BERT)

Expanded skill/keyword database

Extract companies, certifications, projects

Cloud deployment for HR teams

Integration with Applicant Tracking Systems (ATS)
