# Copilot Instructions for DWQ Codebase

## Project Overview
This is a static website for Dragon Wisdom Qigong (DWQ), consisting of multiple HTML pages, images, videos, and stylesheets. There is no backend or build system; all content is served as static files.

## Directory Structure
- `index.html`, `home.html`, etc.: Main site pages. Each page is standalone and may link to others.
- `styles/`: Contains CSS files (e.g., `elements.css`).
- `Images/`: Contains image assets (e.g., diagrams, photos).
- `videos/`: Contains video files for embedding.
- `Healers/`: Contains information about healers (currently text files).

## Key Patterns & Conventions
- **Navigation:** Most pages use standard HTML navigation links. Ensure consistency in navigation menus across all pages.
- **Styling:** All CSS is in `styles/elements.css`. Add new styles here unless a new stylesheet is justified.
- **Media:** Reference images from `Images/` and videos from `videos/` using relative paths.
- **Content Updates:** To add new pages, copy the structure of an existing HTML file and update navigation links as needed.
- **Accessibility:** Use semantic HTML tags (`<header>`, `<nav>`, `<main>`, `<footer>`) for better accessibility and SEO.

## Developer Workflow
- **No build step:** Directly edit HTML, CSS, and media files. No compilation or bundling required.
- **Preview:** Open HTML files in a browser to preview changes. No local server is required unless using advanced features.
- **Debugging:** Use browser developer tools for inspecting layout, styles, and media.

## Integration Points
- **External dependencies:** None detected. All resources are local.
- **Extending:** To add new features (e.g., JavaScript interactivity), create a new JS file in a `scripts/` directory and link it in the relevant HTML files.

## Examples
- To add a new instructor profile:
  1. Create a new HTML file (e.g., `instructor-jane.html`).
  2. Add a link to it in `instructors.html` and navigation menus.
  3. Place any images in `Images/` and reference them with relative paths.

- To update site-wide styles:
  1. Edit `styles/elements.css`.
  2. Preview changes in multiple pages to ensure consistency.

## Important Files
- `index.html`: Main landing page.
- `styles/elements.css`: Central stylesheet.
- `Images/`, `videos/`: Media asset directories.

## Project-Specific Advice
- Keep navigation menus synchronized across all pages.
- Use relative paths for all internal links and media references.
- Maintain semantic HTML for accessibility and search engine optimization.

---
For questions or unclear conventions, review existing HTML files for examples or ask for clarification.
