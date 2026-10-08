import json
import re
from pathlib import Path

def load_data():
    with open('cv-data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_skills_html(skills):
    items = []
    for s in skills:
        items.append(f'            <li>\n              <strong>{s["category"]}:</strong> {s["items"]}\n            </li>')
    return '\n'.join(items)

def generate_idiomas_html(idiomas):
    items = []
    for lang in idiomas:
        items.append(f'          <div class="lang-item"><strong>{lang["language"]}</strong> – {lang["level"]}</div>')
    return '\n'.join(items)

def generate_experience_html(experiencia):
    articles = []
    for exp in experiencia:
        articles.append(f'''            <!-- Job -->
            <article class="cv-item">
              <div class="item-header">
                <h3 class="item-title">{exp["role"]}</h3>
                <span class="item-date">{exp["period"]}</span>
              </div>
              <div class="item-subtitle">{exp["company"]}</div>
              <p class="item-desc">
                {exp["description"]}
              </p>
            </article>''')
    return '\n\n'.join(articles)

def generate_education_html(educacion):
    articles = []
    for edu in educacion:
        desc_paragraphs = '\n'.join([f'                <p>{p.strip()}</p>' for p in edu["description"].split('\n') if p.strip()])
        articles.append(f'''            <!-- Degree -->
            <article class="cv-item">
              <div class="item-header">
                <h3 class="item-title">{edu["degree"]}</h3>
                <span class="item-date">{edu["period"]}</span>
              </div>
              <div class="item-subtitle">{edu["institution"]}</div>
              <div class="item-desc">
{desc_paragraphs}
              </div>
            </article>''')
    return '\n\n'.join(articles)

def generate_courses_html(cursos):
    articles = []
    for c in cursos:
        articles.append(f'''            <article class="course-item">
              <div class="item-header">
                <h3 class="item-title">{c["title"]}</h3>
                <span class="item-date">{c["year"]}</span>
              </div>
              <div class="item-subtitle">{c["institution"]}</div>
            </article>''')
    return '\n\n'.join(articles)

def update_html():
    data = load_data()
    html_path = Path('index.html')
    if not html_path.exists():
        print("index.html not found.")
        return

    content = html_path.read_text(encoding='utf-8')

    # Update personal
    content = re.sub(r'(<h1 class="header-name">)(.*?)(</h1>)', rf'\g<1>{data["personal"]["name"].upper()}\g<3>', content)
    content = re.sub(r'(<div class="header-title">)(.*?)(</div>)', rf'\g<1>{data["personal"]["title"]}\g<3>', content)
    content = re.sub(r'(<a href="tel:[^"]*" class="contact-val">)(.*?)(</a>)', rf'<a href="tel:{data["personal"]["phone"].replace(" ", "")}" class="contact-val">{data["personal"]["phone"]}</a>', content)
    content = re.sub(r'(<a href="mailto:[^"]*" class="contact-val">)(.*?)(</a>)', rf'<a href="mailto:{data["personal"]["email"]}" class="contact-val">{data["personal"]["email"]}</a>', content)

    # Update perfil
    content = re.sub(
        r'(<section class="sidebar-section" id="section-perfil">.*?<p class="sidebar-text">)(.*?)(</p>.*?</section>)',
        rf'\g<1>\n            {data["perfil"]}\n          \g<3>',
        content,
        flags=re.DOTALL
    )

    # Update skills
    skills_html = generate_skills_html(data["skills"])
    content = re.sub(
        r'(<ul class="sidebar-list">)(.*?)(</ul>)',
        rf'\g<1>\n{skills_html}\n          \g<3>',
        content,
        flags=re.DOTALL
    )

    # Update idiomas
    idiomas_html = generate_idiomas_html(data["idiomas"])
    content = re.sub(
        r'(<section class="sidebar-section" id="section-idiomas">.*?<h2 class="sidebar-title">Idiomas</h2>)(.*?)(</section>)',
        rf'\g<1>\n{idiomas_html}\n        \g<3>',
        content,
        flags=re.DOTALL
    )

    # Update experiencia
    exp_html = generate_experience_html(data["experiencia"])
    content = re.sub(
        r'(<section class="main-section" id="section-experiencia">.*?<div class="item-group">)(.*?)(</div>\s*</section>)',
        rf'\g<1>\n{exp_html}\n          \g<3>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Update educacion
    edu_html = generate_education_html(data["educacion"])
    content = re.sub(
        r'(<section class="main-section" id="section-educacion">.*?<div class="item-group">)(.*?)(</div>\s*</section>)',
        rf'\g<1>\n{edu_html}\n          \g<3>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Update educacion page 1 (if present for compact mode)
    content = re.sub(
        r'(<section class="main-section" id="section-educacion-page1"[^>]*>.*?<div class="item-group">)(.*?)(</div>\s*</section>)',
        rf'\g<1>\n{edu_html}\n          \g<3>',
        content,
        count=1,
        flags=re.DOTALL
    )

    # Update cursos (Page 2)
    courses_html = generate_courses_html(data["cursos"])
    content = re.sub(
        r'(<section class="main-section" id="section-cursos">.*?<div class="item-group">)(.*?)(</div>\s*</section>)',
        rf'\g<1>\n{courses_html}\n          \g<3>',
        content,
        count=1,
        flags=re.DOTALL
    )

    html_path.write_text(content, encoding='utf-8')
    print("Successfully updated index.html from cv-data.json")

if __name__ == '__main__':
    update_html()
