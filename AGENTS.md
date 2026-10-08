# 🤖 AGENTS.MD - Guía de Operación para Agentes de IA

Este documento define las directrices, estructura y procedimientos estándar para que cualquier **Agente de IA** (Antigravity, Cursor, Claude Code, Copilot, Aider, etc.) pueda leer, modificar, adaptar y compilar nuevas versiones del Currículum Vitae de **Gonzalo Bartual**.

---

## 🏗️ Arquitectura del Proyecto

El proyecto sigue una arquitectura desacoplada de datos, plantilla y compilación:

```
cv-data.json (Fuente de datos)
      │
      ▼ (python render.py)
  index.html  (Plantilla web HTML/CSS con estilos A4 @media print)
      │
      ▼ (python export_pdf.py)
Gonzalo_Bartual_CV.pdf (Resultado final exportable)
```

### Mapa de Archivos
* **[`cv-data.json`](file:///c:/Users/gonza/Documents/CurriculumGonzalo/cv-data.json)**: **Fuente única de la verdad**. Contiene toda la información del CV en formato JSON estructurado. Modifica preferentemente este archivo.
* **[`render.py`](file:///c:/Users/gonza/Documents/CurriculumGonzalo/render.py)**: Script que lee `cv-data.json` y sincroniza las secciones correspondientes en `index.html`.
* **[`index.html`](file:///c:/Users/gonza/Documents/CurriculumGonzalo/index.html)**: Documento web responsivo, optimizado para impresión A4 milimétrica. Contiene CSS y SVG inline.
* **[`export_pdf.py`](file:///c:/Users/gonza/Documents/CurriculumGonzalo/export_pdf.py)**: Compilador headless (vía Edge/Chrome) que genera el archivo PDF final.
* **[`export-pdf.ps1`](file:///c:/Users/gonza/Documents/CurriculumGonzalo/export-pdf.ps1)**: Wrapper PowerShell opcional para ejecutar la exportación.
* **[`profile.jpg`](file:///c:/Users/gonza/Documents/CurriculumGonzalo/profile.jpg)**: Foto de perfil oficial.

---

## 📋 Protocolo de Ejecución Paso a Paso (SOP)

Cuando un usuario solicite cualquier cambio ("añade una experiencia", "adapta el CV a esta oferta", "traduce a inglés", "mejora los bullets"), el agente debe seguir obligatoriamente este flujo:

### 1. Leer el estado actual
Leer [`cv-data.json`](file:///c:/Users/gonza/Documents/CurriculumGonzalo/cv-data.json) para comprender el contexto actual y los campos existentes.

### 2. Aplicar las modificaciones en `cv-data.json`
Editar `cv-data.json` respetando el esquema (ver sección [Esquema de Datos](#-esquema-de-datos)).

### 3. Sincronizar la plantilla HTML
Ejecutar el script de renderizado:
```powershell
python render.py
```
*Si has añadido estilos nuevos o modificado la maquetación estructural, edita directamente `index.html`.*

### 4. Compilar el nuevo PDF
Ejecutar el comando de exportación según el formato deseado:

- **Formato estándar de 2 páginas (por defecto):**
  ```powershell
  python export_pdf.py
  # Genera: Gonzalo_Bartual_CV.pdf
  ```

- **Formato compacto de 1 página:**
  ```powershell
  python export_pdf.py --1page
  # Genera: Gonzalo_Bartual_CV_1Page.pdf
  ```

- **Archivo con nombre personalizado (ej. versión en inglés o para empresa específica):**
  ```powershell
  python export_pdf.py "Gonzalo_Bartual_CV_Google.pdf"
  ```

### 5. Verificar la salida
Verificar que el PDF generado existe y que el comando terminó con código de salida `0`.

---

## 🗂️ Esquema de Datos (`cv-data.json`)

El archivo JSON cuenta con las siguientes claves principales:

```json
{
  "personal": {
    "name": "Gonzalo Bartual",
    "title": "AI Engineer & Data Analyst",
    "phone": "+34 693 28 46 02",
    "email": "gonzalo.bartual.fernandez2@gmail.com",
    "links": {
      "linkedin": { "label": "Linkedin", "url": "https://..." },
      "github": { "label": "Github", "url": "https://..." },
      "portfolio": { "label": "Portfolio personal", "url": "http://..." }
    },
    "photo": "profile.jpg"
  },
  "perfil": "Texto descriptivo del perfil profesional...",
  "skills": [
    {
      "category": "Nombre de categoría",
      "items": "Tecnología 1, Tecnología 2, ..."
    }
  ],
  "idiomas": [
    { "language": "Español", "level": "Nativo" }
  ],
  "experiencia": [
    {
      "role": "Título del puesto",
      "company": "Empresa",
      "period": "mes. AAAA - mes. AAAA",
      "description": "Descripción del rol, logros y stack utilizado..."
    }
  ],
  "educacion": [
    {
      "degree": "Nombre del título",
      "institution": "Universidad / Institución",
      "period": "AAAA - AAAA",
      "description": "Detalles del grado, mención, TFG..."
    }
  ],
  "cursos": [
    {
      "title": "Nombre del curso / certificación",
      "institution": "Entidad emisora",
      "year": "AAAA"
    }
  ]
}
```

---

## 🛠️ Tareas Típicas y Cómo Proceder

### A. Añadir una nueva Experiencia Laboral
1. En `cv-data.json`, inserta un nuevo objeto al **principio** de la lista `"experiencia"`:
   ```json
   {
     "role": "Senior AI Engineer",
     "company": "Nombre Empresa",
     "period": "jun. 2026 - Presente",
     "description": "Liderazgo en el desarrollo de arquitecturas multi-agente..."
   }
   ```
2. Ejecuta:
   ```powershell
   python render.py
   python export_pdf.py
   ```

### B. Adaptar el CV a una Oferta de Empleo (Targeting ATS)
1. Analizar los requisitos clave de la oferta (keywords de tecnologías, metodologías, certificaciones).
2. Modificar en `cv-data.json`:
   - `"title"`: Ajustar el subtítulo profesional si aplica (ej. `Senior Machine Learning Engineer` o `AI Solutions Architect`).
   - `"perfil"`: Reenfocar las 3-4 líneas iniciales destacando el valor específico para esa empresa.
   - `"skills"`: Priorizar las tecnologías requeridas por la oferta en las primeras posiciones.
   - `"experiencia"`: Enfatizar logros y tecnologías afines a la vacante usando verbos de acción.
3. Ejecutar `python render.py` y `python export_pdf.py "Gonzalo_Bartual_CV_[Empresa].pdf"`.

### C. Aplicar Metodología STAR / XYZ a los Logros
Al redactar descripciones de experiencia, aplicar la fórmula:
> **Logré [X], medido por [Y], realizando [Z].**

*Ejemplo de mejora:*
- **Antes:** *"Responsable de sistemas de IA conversacional (RAG) para automatizar el soporte."*
- **Después:** *"Diseñé y desplegué un sistema de IA conversacional RAG que redujo los tiempos de resolución del soporte corporativo en un 40%, integrando Azure AI Search y Power Platform."*

### D. Añadir Cursos o Certificaciones
1. Añadir el nuevo objeto a `"cursos"` en `cv-data.json`:
   ```json
   {
     "title": "AWS Certified Machine Learning - Specialty",
     "institution": "Amazon Web Services",
     "year": "2026"
   }
   ```
2. Sincronizar y compilar:
   ```powershell
   python render.py
   python export_pdf.py
   ```

---

## ⚠️ Reglas y Restricciones Técnicas

1. **No alterar los IDs y delimitadores HTML clave** en `index.html` (`#section-perfil`, `#section-skills`, `#section-experiencia`, etc.), ya que `render.py` utiliza patrones de expresiones regulares sobre estos marcadores para inyectar los datos.
2. **Dimensiones A4 Estrictas**:
   - Si añades mucho contenido y utilizas el modo de 1 página (`--1page`), asegúrate de que el texto sea conciso para evitar desbordamientos visuales.
   - En el formato de 2 páginas, las experiencias se distribuyen de forma que la educación y cursos queden balanceados limpiamente.
3. **Imágenes y Recursos**: La imagen de perfil referenciada debe mantenerse en `profile.jpg` o actualizarse conservando la misma ruta relativa.
4. **Entorno de Ejecución**: En Windows PowerShell, los scripts de python se invocan directamente con `python render.py` y `python export_pdf.py`. No uses comandos de cambio de directorio innecesarios si ya te encuentras en el directorio de trabajo.
