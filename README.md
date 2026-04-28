# Resume Maker Pro - ATS Friendly PDF Resume Generator

A clean GitHub-ready Python project that creates professional **ATS-friendly resumes** in PDF and HTML format.

## Why this project is useful

Many resume builders create fancy designs that look good but fail in ATS systems. This project focuses on:

- Clean ATS-readable layout
- Simple PDF export
- Professional resume structure
- Easy JSON-based editing
- Beginner-friendly Python code
- No paid API required
- Good for job applications, internships, freshers, and professionals

## Features

- ATS-friendly resume template
- Professional colored template
- PDF export
- HTML preview export
- Easy resume editing using `resume_data.json`
- Sections included:
  - Professional Summary
  - Skills
  - Experience
  - Projects
  - Education
  - Certifications
  - Languages
- GitHub-ready folder structure

## Folder Structure

```text
resume-maker-pro/
├── main.py
├── resume_data.json
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── output/
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/resume-maker-pro.git
cd resume-maker-pro
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

## How to use

### Step 1: Edit your resume details

Open this file:

```text
resume_data.json
```

Replace the sample details with your own details.

### Step 2: Generate ATS-friendly resume

```bash
python main.py --template ats --format pdf
```

Your PDF will be saved inside:

```text
output/
```

### Step 3: Generate professional resume

```bash
python main.py --template pro --format pdf
```

### Step 4: Generate both PDF and HTML

```bash
python main.py --template ats --format both
```

## Commands

| Command | Use |
|---|---|
| `python main.py --template ats --format pdf` | Create ATS-friendly PDF |
| `python main.py --template pro --format pdf` | Create professional PDF |
| `python main.py --template ats --format html` | Create HTML preview |
| `python main.py --template pro --format both` | Create PDF and HTML |

## ATS Resume Tips

For best ATS results:

- Use simple section headings
- Avoid tables with too much design
- Avoid images and icons
- Use standard fonts
- Use keywords from the job description
- Save and send as PDF unless the company asks for DOCX
- Keep fresher resumes to 1 page if possible

## Best Resume Bullet Format

Use this format:

```text
Action Verb + What You Did + Tool/Skill Used + Result/Impact
```

Example:

```text
Performed vulnerability scanning using Nmap and documented open ports, services, risks, and remediation steps.
```

## Example Cybersecurity Fresher Skills

You can include skills like:

- Nmap
- Kali Linux
- Burp Suite
- Metasploit
- Linux Basics
- Web Vulnerability Testing
- OWASP Top 10
- Report Writing
- GitHub
- Python Basics

## Disclaimer

This project creates resume files locally. It does not guarantee job selection. Resume quality depends on your real skills, projects, keywords, and experience.

## License

MIT License
