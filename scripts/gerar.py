"""Gera artes do @baseespacodeeventos a partir de um JSON.

Uso: python3 scripts/gerar.py plano.json
Cada item do JSON: {"arquivo": "artes/2026-11-23/feed-seg.jpg", "formato": "feed"|"story",
  "tipo": "frase"|"foto"|"chamada", "titulo": "...", "subtitulo": "...", "foto": "fotos/x.jpg",
  "fundo": "escuro"|"ambar"}
- "frase": arte só com texto (bom dia, dica, data comemorativa), sem foto.
- "foto": foto do espaço tratada, SEM texto por cima (só o logo pequeno).
- "chamada": card escuro com título e WhatsApp.
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AMBAR = (255, 191, 0); ESCURO = (14, 18, 32); BRANCO = (255, 255, 255)
WHATS = "WhatsApp (85) 99156-0403"
TAM = {"feed": (1080, 1350), "story": (1080, 1920)}

def fonte(peso, tam):
    return ImageFont.truetype(os.path.join(BASE, "fonts", f"Poppins-{peso}.ttf"), tam)

def logo(larg):
    l = Image.open(os.path.join(BASE, "marca", "logo-base.png")).convert("RGBA")
    l.thumbnail((larg, larg)); return l

def quebrar(d, texto, f, larg_max):
    linhas = []
    for par in texto.split("\n"):
        atual = ""
        for p in par.split():
            t = (atual + " " + p).strip()
            if d.textlength(t, font=f) <= larg_max: atual = t
            else: linhas.append(atual); atual = p
        linhas.append(atual)
    return linhas

def bloco(d, texto, f, cx, y, larg_max, cor, esp=1.15):
    for l in quebrar(d, texto, f, larg_max):
        d.text((cx, y), l, font=f, fill=cor, anchor="mt"); y += int(f.size * esp)
    return y

def altura(d, texto, f, larg_max, esp=1.15):
    return len(quebrar(d, texto, f, larg_max)) * int(f.size * esp)

def recorte(caminho, W, H):
    im = Image.open(os.path.join(BASE, caminho)).convert("RGB")
    w, h = im.size; r = W / H
    if w / h > r: cw, ch = h * r, h
    else: cw, ch = w, w / r
    x, y = (w - cw) / 2, (h - ch) / 2
    im = im.crop((int(x), int(y), int(x + cw), int(y + ch))).resize((W, H), Image.LANCZOS)
    im = ImageEnhance.Brightness(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.15)
    return ImageEnhance.Contrast(im).enhance(1.05)

def arte_frase(it, W, H):
    amb = it.get("fundo") == "ambar"
    fundo, cor_t, cor_s = (AMBAR, ESCURO, ESCURO) if amb else (ESCURO, BRANCO, AMBAR)
    im = Image.new("RGBA", (W, H), (*fundo, 255)); d = ImageDraw.Draw(im)
    if not amb:
        l = logo(300); im.alpha_composite(l, ((W - l.width) // 2, 90))
    else:
        d.text((W // 2, 120), "BASE ESPAÇO DE EVENTOS", font=fonte("Bold", 34), fill=ESCURO, anchor="mt")
    ft = fonte("Bold", 96 if len(it["titulo"]) <= 40 else 76); fs = fonte("Medium", 44)
    sub = it.get("subtitulo", "")
    ht = altura(d, it["titulo"], ft, W - 160) + (40 + altura(d, sub, fs, W - 200, 1.3) if sub else 0)
    y = (H - ht) // 2
    d.rectangle([W // 2 - 60, y - 50, W // 2 + 60, y - 40], fill=(cor_s if not amb else ESCURO))
    y = bloco(d, it["titulo"], ft, W // 2, y, W - 160, cor_t)
    if sub: bloco(d, sub, fs, W // 2, y + 40, W - 200, cor_s if not amb else ESCURO, 1.3)
    d.text((W // 2, H - 110), "@baseespacodeeventos", font=fonte("Medium", 36),
           fill=(cor_s if not amb else ESCURO), anchor="mm")
    return im

def arte_foto(it, W, H):
    im = recorte(it["foto"], W, H).convert("RGBA")
    sombra = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sombra)
    for i in range(220): d.line([(0, i), (W, i)], fill=(*ESCURO, int(140 * (1 - i / 220) ** 1.8)))
    im = Image.alpha_composite(im, sombra); im.alpha_composite(logo(220), (50, 45))
    return im

def arte_chamada(it, W, H):
    im = Image.new("RGBA", (W, H), (*ESCURO, 255)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 16], fill=AMBAR)
    l = logo(560); im.alpha_composite(l, ((W - l.width) // 2, int(H * 0.17)))
    y = int(H * 0.38)
    y = bloco(d, it["titulo"], fonte("Bold", 84), W // 2, y, W - 160, BRANCO)
    if it.get("subtitulo"):
        y = bloco(d, it["subtitulo"], fonte("Medium", 44), W // 2, y + 30, W - 200, AMBAR, 1.3)
    y = max(y + 80, int(H * 0.72))
    d.rounded_rectangle([130, y, W - 130, y + 120], radius=60, fill=AMBAR)
    d.text((W // 2, y + 60), WHATS, font=fonte("Bold", 48), fill=ESCURO, anchor="mm")
    d.text((W // 2, y + 200), "Av. Pasteur, 271 · Cristo Redentor", font=fonte("Medium", 38),
           fill=(210, 210, 210), anchor="mm")
    return im

def main(plano):
    itens = json.load(open(plano, encoding="utf-8"))
    for it in itens:
        W, H = TAM[it.get("formato", "feed")]
        im = {"frase": arte_frase, "foto": arte_foto, "chamada": arte_chamada}[it["tipo"]](it, W, H)
        destino = os.path.join(BASE, it["arquivo"]); os.makedirs(os.path.dirname(destino), exist_ok=True)
        im.convert("RGB").save(destino, quality=90); print("ok", it["arquivo"])

if __name__ == "__main__":
    main(sys.argv[1])
