---
name: ui-theme
description: Visual theme and style guide for the DesertoAI frontend (8-bit African savannah). Use whenever creating or changing UI in templates/ or static/, including pages, panels, headers, colours, fonts, icons or art.
---

# UI theme: 8-bit African savannah

All UI in `templates/` and `static/` follows this theme. Keep it simple and consistent.

## Look and feel
- Retro 8-bit / pixel-art style. Hard edges, no gradients, no soft shadows.
- Chunky 2-4px borders. Square corners (`border-radius: 0`).
- Use `image-rendering: pixelated` on any pixel art.

## Palette
Define as CSS variables in `static/style.css` and only use these:

| Variable | Colour | Use |
|---|---|---|
| `--sand` | `#e8c872` | page background |
| `--dust` | `#c98f3c` | panels, secondary surfaces |
| `--acacia` | `#3b6b2f` | headers, positive accents |
| `--sunset` | `#d9531e` | highlights, buttons, alerts |
| `--earth` | `#5a3a1e` | borders, body text |
| `--night` | `#1e1b2e` | dark surfaces, header text bg |

## Typography
- Pixel font for headings and labels, e.g. "Press Start 2P" (Google Fonts). Fallback `monospace`.
- Readable monospace for body text at 14px or larger.

## Page structure
- Every distinct element on the page gets a clear header (map, region info, event detail, etc.).
- Headers use the pixel font, `--acacia` background, a 4px `--earth` border.

## Art
- Prefer real pixel art from `static/img/` (check `static/img/CREDITS.md` for licence).
- Where there is no image yet, use ASCII art in a `<pre>` block. Keep it small (under ~12 lines) and in the theme (acacia tree, lion, sun, elephant, grass).
- Every image needs `alt` text. ASCII art gets `aria-hidden="true"` if decorative.

## Rules
- Keep contrast readable (dark text on light surfaces, light on dark).
- Don't add a framework or build step. Plain HTML, CSS and JS only.
- Keep CSS in `static/style.css` and JS in `static/app.js`, no inline styles.
- Don't restyle Leaflet internals beyond colours and borders.
