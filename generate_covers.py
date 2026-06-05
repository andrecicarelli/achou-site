#!/usr/bin/env python3
"""Generate branded cover images for Agência Achou blog posts.

Outputs both JPG (quality=92) and WebP (quality=85) for each post.
Run from the site root: python3 generate_covers.py
"""

from PIL import Image, ImageDraw, ImageFont
import os

SITE_DIR   = os.path.dirname(os.path.abspath(__file__))
COVERS_DIR = os.path.join(SITE_DIR, "src", "assets", "covers")
os.makedirs(COVERS_DIR, exist_ok=True)

# Brand colors
BLUE       = (15, 43, 91)      # #0F2B5B — cor principal
BLUE_MID   = (26, 63, 128)     # #1A3F80 — hover / gradiente
ORANGE     = (245, 158, 11)    # #F59E0B — accent
DARK_STRIP = (8, 25, 55)       # footer strip
WHITE      = (255, 255, 255)
MUTED      = (180, 196, 220)   # texto secundário sobre azul

W, H = 1200, 630

FONT_PATH = "/System/Library/Fonts/Avenir Next.ttc"
# Avenir Next TTC indices: 0=Regular, 2=Medium, 4=DemiBold, 6=Bold, 8=Heavy
FONT_IDX_BOLD   = 6
FONT_IDX_MEDIUM = 2
FONT_IDX_REG    = 0

posts = [
    ("por-que-seu-negocio-nao-aparece-no-google",
     "Por que seu negócio não aparece no Google"),
    ("google-meu-negocio-guia-completo",
     "Google Meu Negócio: o guia completo"),
    ("como-aparecer-google-maps",
     "Como aparecer no Google Maps"),
    ("seo-local-o-que-e",
     "SEO local: o que é e por que importa"),
    ("5-erros-que-tornam-negocio-invisivel-google",
     "5 erros que tornam seu negócio invisível no Google"),
    ("avaliacoes-google-como-conseguir-mais",
     "Avaliações no Google: como conseguir mais"),
    ("site-profissional-diferenca",
     "Site profissional vs. site amador"),
    ("google-ads-vs-seo-qual-melhor",
     "Google Ads vs. SEO: qual é melhor?"),
    ("como-dentistas-conseguem-mais-pacientes-google",
     "Como dentistas conseguem mais pacientes pelo Google"),
    ("como-fisioterapeutas-atraem-pacientes",
     "Como fisioterapeutas atraem pacientes pela internet"),
    ("como-mecanicos-conseguem-clientes-google",
     "Como mecânicos conseguem clientes pelo Google"),
    ("como-saloes-beleza-atraem-clientes-google",
     "Como salões de beleza atraem clientes pelo Google"),
    ("como-nutricionistas-atraem-clientes-online",
     "Como nutricionistas atraem clientes online"),
    ("como-personal-trainers-conseguem-alunos-google",
     "Como personal trainers conseguem alunos pelo Google"),
    ("como-pet-shops-conseguem-clientes-google",
     "Como pet shops e veterinários conseguem clientes"),
    ("como-restaurantes-aparecem-google-maps",
     "Como restaurantes aparecem no Google Maps"),
    ("eletricistas-encanadores-aparecem-google",
     "Como eletricistas e encanadores conseguem serviços"),
    ("quanto-custa-site-pequena-empresa",
     "Quanto custa ter um site profissional"),
    ("o-que-e-dominio-proprio-por-que-precisa",
     "O que é domínio próprio e por que precisa"),
    ("site-no-celular-por-que-importa",
     "Por que 80% dos seus clientes pesquisam pelo celular"),
    ("por-que-instagram-nao-e-suficiente",
     "Por que só ter Instagram não é suficiente"),
    ("por-que-concorrente-aparece-antes",
     "Por que seu concorrente aparece antes de você"),
    ("metricas-pequeno-negocio-acompanhar-site",
     "Métricas que todo pequeno negócio deve acompanhar"),
    ("diferenca-google-maps-google-search",
     "Google Maps vs. Google Search: qual a diferença?"),
    ("google-ads-local-vale-a-pena",
     "Google Ads local: vale a pena para pequenos negócios?"),
    ("google-meu-negocio-fotos-e-posts",
     "Como usar fotos e posts no Google Meu Negócio"),
    ("como-transformar-visitantes-em-clientes",
     "Como transformar visitantes do site em clientes"),
    ("o-que-clientes-pesquisam-antes-contratar",
     "O que os clientes pesquisam antes de contratar"),
    ("7-perguntas-que-clientes-pesquisam-antes",
     "7 perguntas que seus clientes pesquisam no Google"),
    ("presenca-digital-pequeno-negocio-por-onde-comecar",
     "Presença digital para pequenos negócios: por onde começar"),
]


def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] > max_width and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines


def make_cover(slug, title):
    img  = Image.new("RGB", (W, H), BLUE)
    draw = ImageDraw.Draw(img)

    # Subtle gradient overlay (darker bottom-right)
    for y in range(H):
        alpha = int(y / H * 30)
        draw.line([(0, y), (W, y)], fill=(
            max(0, BLUE[0] - alpha // 3),
            max(0, BLUE[1] - alpha // 3),
            max(0, BLUE[2] - alpha // 3),
        ))

    # Orange top accent bar
    draw.rectangle([(0, 0), (W, 8)], fill=ORANGE)

    # Orange left sidebar accent
    draw.rectangle([(0, 0), (6, H)], fill=ORANGE)

    # "achou" logo — wordmark
    font_logo = ImageFont.truetype(FONT_PATH, 32, index=FONT_IDX_BOLD)
    logo_x, logo_y = 50, 44
    draw.text((logo_x, logo_y), "achou", fill=WHITE, font=font_logo)

    # Orange dot after "achou"
    bbox_logo = draw.textbbox((logo_x, logo_y), "achou", font=font_logo)
    dot_x = bbox_logo[2] + 4
    dot_y = logo_y + (bbox_logo[3] - bbox_logo[1]) // 2 - 5
    draw.ellipse([(dot_x, dot_y), (dot_x + 10, dot_y + 10)], fill=ORANGE)

    # Divider under logo
    draw.rectangle([(50, 96), (210, 98)], fill=(255, 255, 255, 40))

    # Title — auto-size to fit
    max_title_w = W - 120
    for size in (62, 52, 44, 38, 32):
        font_title = ImageFont.truetype(FONT_PATH, size, index=FONT_IDX_BOLD)
        lines = wrap_text(title, font_title, max_title_w, draw)
        if len(lines) <= 3:
            break

    line_h  = int(size * 1.28)
    total_h = len(lines) * line_h
    # Center vertically with slight downward bias
    y_start = max(130, (H - total_h) // 2 + 20)

    for i, line in enumerate(lines):
        draw.text((50, y_start + i * line_h), line, fill=WHITE, font=font_title)

    # Bottom strip
    draw.rectangle([(0, H - 60), (W, H)], fill=DARK_STRIP)

    # Domain text
    font_url = ImageFont.truetype(FONT_PATH, 18, index=FONT_IDX_REG)
    draw.text((66, H - 38), "achouagencia.com.br", fill=MUTED, font=font_url)

    # Orange dot before domain
    draw.ellipse([(50, H - 32), (60, H - 22)], fill=ORANGE)

    # Save JPG
    jpg_path = os.path.join(COVERS_DIR, f"{slug}.jpg")
    img.save(jpg_path, "JPEG", quality=92, optimize=True)

    # Save WebP
    webp_path = os.path.join(COVERS_DIR, f"{slug}.webp")
    img.save(webp_path, "WEBP", quality=85, method=6)

    print(f"  ✓ {slug}")


if __name__ == "__main__":
    print("Generating cover images for Agência Achou...\n")
    for slug, title in posts:
        make_cover(slug, title)
    print(f"\nDone. {len(posts)} posts → {len(posts) * 2} images in src/assets/covers/")
