import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from html import escape
from pathlib import Path

OUTPUT_DIR = Path("output")


def clean_filename(name: str) -> str:
    name = re.sub(r"[^a-zA-Z0-9_-]+", "_", name.strip().lower())
    return name or "resume"


def load_data(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def p(value) -> str:
    return escape(str(value or ""))


def find_browser() -> str | None:
    candidates = ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "msedge"]
    for c in candidates:
        found = shutil.which(c)
        if found:
            return found
    return None


def render_html(data: dict, template: str = "ats") -> str:
    accent = "#1f4e79" if template == "pro" else "#111111"
    bg = "#ffffff"
    border = "#a0a0a0"
    css = f"""
    @page {{ size: A4; margin: 14mm 14mm; }}
    * {{ box-sizing: border-box; }}
    body {{
      font-family: Arial, Helvetica, sans-serif;
      background: {bg}; color: #111; line-height: 1.36;
      font-size: 11.2px; margin: 0;
    }}
    .page {{ max-width: 800px; margin: 0 auto; }}
    h1 {{ text-align: center; color: {accent}; font-size: 25px; margin: 0 0 2px; letter-spacing: .2px; }}
    .title {{ text-align: center; font-size: 12px; margin-bottom: 3px; }}
    .contact {{ text-align: center; font-size: 10.5px; margin-bottom: 10px; word-break: break-word; }}
    h2 {{ color: {accent}; border-bottom: 1px solid {border}; font-size: 13px; margin: 12px 0 5px; padding-bottom: 2px; letter-spacing: .4px; }}
    p {{ margin: 3px 0; }}
    ul {{ margin: 3px 0 6px 17px; padding: 0; }}
    li {{ margin: 2px 0; }}
    .row {{ display: flex; justify-content: space-between; gap: 18px; align-items: flex-start; }}
    .left {{ font-weight: 700; }}
    .right {{ white-space: nowrap; font-size: 10.5px; }}
    .item {{ margin-bottom: 6px; page-break-inside: avoid; }}
    a {{ color: #111; text-decoration: none; }}
    .skill-line b {{ color: #111; }}
    """

    html = ["<!doctype html><html><head><meta charset='utf-8'>",
            f"<title>{p(data.get('name', 'Resume'))} Resume</title>",
            "<style>", css, "</style></head><body><main class='page'>"]

    html.append(f"<h1>{p(data.get('name', 'Your Name'))}</h1>")
    if data.get("title"):
        html.append(f"<div class='title'>{p(data['title'])}</div>")
    contacts = " | ".join([p(x) for x in [
        data.get("email"), data.get("phone"), data.get("location"),
        data.get("linkedin"), data.get("github"), data.get("portfolio")
    ] if x])
    html.append(f"<div class='contact'>{contacts}</div>")

    def section(title: str):
        html.append(f"<h2>{p(title.upper())}</h2>")

    if data.get("summary"):
        section("Professional Summary")
        html.append(f"<p>{p(data['summary'])}</p>")

    if data.get("skills"):
        section("Skills")
        for category, skills in data["skills"].items():
            html.append(f"<p class='skill-line'><b>{p(category)}:</b> {p(', '.join(skills))}</p>")

    if data.get("experience"):
        section("Experience")
        for job in data["experience"]:
            html.append("<div class='item'>")
            html.append(f"<div class='row'><div class='left'>{p(job.get('role'))} - {p(job.get('company'))}, {p(job.get('location'))}</div><div class='right'>{p(job.get('start'))} - {p(job.get('end'))}</div></div>")
            html.append("<ul>")
            for bullet in job.get("bullets", []):
                html.append(f"<li>{p(bullet)}</li>")
            html.append("</ul></div>")

    if data.get("projects"):
        section("Projects")
        for project in data["projects"]:
            html.append("<div class='item'>")
            line = f"<b>{p(project.get('name'))}</b>"
            if project.get("link"):
                line += f" - {p(project.get('link'))}"
            html.append(f"<p>{line}</p><ul>")
            for bullet in project.get("bullets", []):
                html.append(f"<li>{p(bullet)}</li>")
            html.append("</ul></div>")

    if data.get("education"):
        section("Education")
        for edu in data["education"]:
            html.append("<div class='item'>")
            html.append(f"<div class='row'><div class='left'>{p(edu.get('degree'))} - {p(edu.get('school'))}, {p(edu.get('location'))}</div><div class='right'>{p(edu.get('start'))} - {p(edu.get('end'))}</div></div>")
            html.append("</div>")

    if data.get("certifications"):
        section("Certifications")
        html.append("<ul>")
        for cert in data["certifications"]:
            html.append(f"<li>{p(cert)}</li>")
        html.append("</ul>")

    if data.get("languages"):
        section("Languages")
        html.append(f"<p>{p(', '.join(data['languages']))}</p>")

    html.append("</main></body></html>")
    return "".join(html)


def save_html(data: dict, output_path: Path, template: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_html(data, template), encoding="utf-8")


def html_to_pdf(html_path: Path, pdf_path: Path):
    browser = find_browser()
    if not browser:
        raise RuntimeError("Chromium/Chrome not found. Install Chromium or Google Chrome to export PDF.")
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_path.resolve()}",
        str(html_path.resolve())
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "PDF export failed")


def main():
    parser = argparse.ArgumentParser(description="ATS Friendly Resume Maker - PDF and HTML Generator")
    parser.add_argument("--data", default="resume_data.json", help="Path to resume JSON file")
    parser.add_argument("--template", choices=["ats", "pro"], default="ats", help="Resume style")
    parser.add_argument("--format", choices=["pdf", "html", "both"], default="both", help="Output format")
    args = parser.parse_args()

    data = load_data(args.data)
    base = clean_filename(data.get("name", "resume")) + f"_{args.template}"
    html_path = OUTPUT_DIR / f"{base}.html"
    pdf_path = OUTPUT_DIR / f"{base}.pdf"

    if args.format in ["html", "both", "pdf"]:
        save_html(data, html_path, args.template)
        if args.format in ["html", "both"]:
            print(f"HTML created: {html_path}")

    if args.format in ["pdf", "both"]:
        html_to_pdf(html_path, pdf_path)
        print(f"PDF created: {pdf_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
