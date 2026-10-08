# 📄 CV Web & Exportable a PDF - Gonzalo Bartual

Este repositorio contiene la versión web oficial de tu Currículum Vitae, diseñada con fidelidad milimétrica a tu diseño original, optimizada para **exportación directa a PDF (A4)** y preparada para que cualquier **agente de IA** pueda modificarlo, mejorarlo o adaptarlo a ofertas específicas al instante.

---

## 🚀 Archivos del Proyecto

| Archivo | Descripción |
| :--- | :--- |
| **`index.html`** | Página web del CV. Incluye barra de herramientas flotante, modo interactivo de edición en vivo y estilos CSS de impresión A4 (`@media print`). |
| **`cv-data.json`** | Todos los datos del CV en formato JSON estructurado. Es la fuente ideal para que una IA lea y edite los contenidos fácilmente. |
| **`render.py`** | Script en Python que toma `cv-data.json` y actualiza automáticamente `index.html`. |
| **`export_pdf.py`** | Genera el archivo PDF sin abrir el navegador manualmente, usando Microsoft Edge / Chrome en segundo plano (`headless`). |
| **`export-pdf.ps1`** | Script de PowerShell para exportar el PDF con un solo comando. |
| **`profile.jpg`** | Fotografía original extraída del documento en alta calidad, enmarcada con CSS circular. |

---

## 🖨️ Cómo Exportar a PDF

Tienes dos formas sencillas de exportar:

### 1. Desde el navegador (Visual & Rápido)
1. Abre [`index.html`](file:///c:/Users/gonza/Documents/CurriculumGonzalo/index.html) en tu navegador (Edge, Chrome, Brave, etc.).
2. Haz clic en el botón flotante superior **"Exportar a PDF"** (o presiona `Ctrl + P`).
3. En la ventana de impresión:
   - **Destino:** *Guardar como PDF*
   - **Diseño:** *Vertical*
   - **Tamaño de papel:** *A4*
   - **Márgenes:** *Ninguno* (o *Predeterminado*)
   - **Gráficos de fondo:** *Activado* (para ver el fondo gris de la barra lateral).

### 2. Desde la terminal (Automático por script o IA)
- **Formato estándar (2 páginas):**
  ```powershell
  python export_pdf.py
  # Genera: Gonzalo_Bartual_CV.pdf
  ```
- **Formato compacto (1 página completa):**
  ```powershell
  python export_pdf.py --1page
  # Genera: Gonzalo_Bartual_CV_1Page.pdf
  ```

---

## 🤖 Guía para Agentes de IA (Prompts recomendados)

Puedes pedirle a cualquier agente de IA (como Antigravity, Claude, ChatGPT, etc.) que modifique tu CV usando estos ejemplos de prompts:

### 1. Adaptar el CV a una oferta de trabajo específica
> *"Tengo esta oferta de trabajo: [pegar descripción del empleo]. Por favor, actualiza `cv-data.json` para destacar mis proyectos en RAG, microservicios y LLMs relevantes para esta oferta, ejecuta `python render.py` y luego `python export_pdf.py`."*

### 2. Traducir el CV al inglés
> *"Por favor traduce todo el contenido de `cv-data.json` al inglés profesional (ej: 'Software Engineer', 'Work Experience', etc.), actualiza `index.html` con `python render.py` y genera el PDF en inglés con `python export_pdf.py Gonzalo_Bartual_CV_EN.pdf`."*

### 3. Mejorar redacción de experiencias con métricas (Fórmula STAR/XYZ)
> *"Revisa las descripciones de mis puestos en `cv-data.json` y reescríbelas aplicando la metodología STAR (Situación, Tarea, Acción, Resultado) con un tono de alto impacto para un perfil de AI Engineer. Luego sincroniza el HTML y compila el PDF."*

### 4. Añadir o actualizar un puesto
> *"Añade una nueva experiencia laboral a `cv-data.json` como 'Senior AI Engineer' en [Empresa] de [Fecha], sincroniza `index.html` y reexporta."*

---

## ✏️ Modo de Edición en Vivo en el Navegador
Si quieres ajustar una palabra rápidamente sin tocar código:
1. Abre `index.html`.
2. Pulsa en el botón superior **"Editar texto"**.
3. Haz clic directamente sobre cualquier texto o fecha en la pantalla para editarlo como si fuera Word.
4. Pulsa **"Exportar a PDF"** para guardar el resultado.
