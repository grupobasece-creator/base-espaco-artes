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



# ---------- Modelos elaborados ----------
import math, random

def _confete(d, W, H, seed, cores, n=38, area=None):
    rnd = random.Random(seed)
    for _ in range(n):
        x, y = rnd.randint(0, W), rnd.randint(0, H)
        if area and area[0] < x < area[2] and area[1] < y < area[3]: continue
        r = rnd.randint(6, 16); c = rnd.choice(cores); t = rnd.random()
        if t < 0.4: d.ellipse([x - r, y - r, x + r, y + r], fill=c)
        elif t < 0.7:
            a = rnd.random() * math.pi
            d.line([(x - r * math.cos(a), y - r * math.sin(a)), (x + r * math.cos(a), y + r * math.sin(a))], fill=c, width=6)
        else: d.rectangle([x - r // 2, y - r // 2, x + r // 2, y + r // 2], fill=c)

def _moldura(foto, w, h, raio=48):
    im = recorte(foto, w, h).convert("RGBA")
    m = Image.new("L", (w, h), 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, w, h], radius=raio, fill=255)
    im.putalpha(m); return im

def arte_foto_card(it, W, H):
    """Foto em moldura arredondada + faixa de texto separada (texto NÃO fica em cima da foto)."""
    im = Image.new("RGBA", (W, H), (*ESCURO, 255)); d = ImageDraw.Draw(im)
    d.ellipse([W - 420, -260, W + 260, 420], fill=(*AMBAR, 255))
    d.ellipse([W - 220, H - 260, W + 240, H + 200], outline=AMBAR, width=10)
    l = logo(230); im.alpha_composite(l, (60, 55))
    fh = int(H * (0.56 if H < 1500 else 0.55)); fw = W - 120
    fy = 170 if H < 1500 else 260
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle(
        [72, fy + 18, 72 + fw, fy + 18 + fh], radius=48, fill=(0, 0, 0, 120)); im.alpha_composite(sh)
    im.alpha_composite(_moldura(it["foto"], fw, fh), (60, fy))
    y = fy + fh + 60
    d.rectangle([60, y, 160, y + 10], fill=AMBAR); y += 40
    for ln in quebrar(d, it["titulo"], fonte("Bold", 76), W - 120):
        d.text((60, y), ln, font=fonte("Bold", 76), fill=BRANCO); y += 86
    if it.get("subtitulo"):
        d.text((60, y + 14), it["subtitulo"], font=fonte("Medium", 40), fill=AMBAR)
    return im

def arte_festa(it, W, H):
    """Frase com confetes, círculos e selo — para bom dia, datas e dicas."""
    amb = it.get("fundo") == "ambar"
    fundo = AMBAR if amb else ESCURO; cor_t = ESCURO if amb else BRANCO
    cores = [ESCURO, BRANCO, (255, 120, 80)] if amb else [AMBAR, BRANCO, (255, 120, 80), (90, 200, 250)]
    im = Image.new("RGBA", (W, H), (*fundo, 255)); d = ImageDraw.Draw(im)
    d.ellipse([-200, -200, 380, 380], fill=(*(ESCURO if amb else AMBAR), 255))
    d.ellipse([W - 260, H - 300, W + 220, H + 180], outline=(ESCURO if amb else AMBAR), width=14)
    cx, cy = W // 2, H // 2
    _confete(d, W, H, it.get("seed", 1), cores, area=(80, cy - 360, W - 80, cy + 360))
    ft = fonte("Bold", 92 if len(it["titulo"]) <= 40 else 74); fs = fonte("Medium", 44)
    ht = altura(d, it["titulo"], ft, W - 200) + (36 + altura(d, it.get("subtitulo", ""), fs, W - 240, 1.3) if it.get("subtitulo") else 0)
    pad = 70; top = cy - ht // 2 - pad; bot = cy + ht // 2 + pad
    d.rounded_rectangle([90, top, W - 90, bot], radius=50, fill=(*(BRANCO if amb else (28, 34, 56)), 255))
    if it.get("selo"):
        fsel = fonte("Bold", 34); tw = d.textlength(it["selo"], font=fsel)
        d.rounded_rectangle([cx - tw / 2 - 30, top - 32, cx + tw / 2 + 30, top + 32], radius=32, fill=(ESCURO if amb else AMBAR))
        d.text((cx, top), it["selo"], font=fsel, fill=(AMBAR if amb else ESCURO), anchor="mm")
    y = bloco(d, it["titulo"], ft, cx, cy - ht // 2, W - 200, ESCURO if amb else BRANCO)
    if it.get("subtitulo"): bloco(d, it["subtitulo"], fs, cx, y + 36, W - 240, (ESCURO if amb else AMBAR), 1.3)
    if amb: d.text((cx, H - 100), "BASE ESPAÇO DE EVENTOS", font=fonte("Bold", 36), fill=ESCURO, anchor="mm")
    else:
        l = logo(260); im.alpha_composite(l, ((W - l.width) // 2, H - 150))
    return im

def arte_mosaico(it, W, H):
    """Colagem de 3 fotos + título — tour do espaço / chamada."""
    im = Image.new("RGBA", (W, H), (*ESCURO, 255)); d = ImageDraw.Draw(im)
    fotos = it["fotos"][:3]; g = 20; top = 170
    alto = int(H * 0.58); w1 = int((W - 3 * g) * 0.58); w2 = W - 3 * g - w1; h2 = (alto - g) // 2
    im.alpha_composite(_moldura(fotos[0], w1, alto, 36), (g, top))
    im.alpha_composite(_moldura(fotos[1], w2, h2, 36), (2 * g + w1, top))
    im.alpha_composite(_moldura(fotos[2], w2, h2, 36), (2 * g + w1, top + h2 + g))
    l = logo(230); im.alpha_composite(l, (40, 55))
    if it.get("selo"):
        fsel = fonte("Bold", 32); tw = d.textlength(it["selo"], font=fsel)
        d.rounded_rectangle([W - 60 - tw - 50, 58, W - 60, 118], radius=30, fill=AMBAR)
        d.text((W - 60 - 25, 88), it["selo"], font=fsel, fill=ESCURO, anchor="rm")
    y = top + alto + 55
    for ln in quebrar(d, it["titulo"], fonte("Bold", 72), W - 100):
        d.text((W // 2, y), ln, font=fonte("Bold", 72), fill=BRANCO, anchor="mt"); y += 82
    d.rounded_rectangle([170, y + 30, W - 170, y + 130], radius=50, fill=AMBAR)
    d.text((W // 2, y + 80), WHATS, font=fonte("Bold", 42), fill=ESCURO, anchor="mm")
    return im

_TIPOS_EXTRA = {"foto_card": arte_foto_card, "festa": arte_festa, "mosaico": arte_mosaico}

def main(plano):
    itens = json.load(open(plano, encoding="utf-8"))
    tipos = {"frase": arte_frase, "foto": arte_foto, "chamada": arte_chamada, **_TIPOS_EXTRA}
    for it in itens:
        W, H = TAM[it.get("formato", "feed")]
        im = tipos[it["tipo"]](it, W, H)
        destino = os.path.join(BASE, it["arquivo"]); os.makedirs(os.path.dirname(destino), exist_ok=True)
        im.convert("RGB").save(destino, quality=90); print("ok", it["arquivo"])

if __name__ == "__main__":
    main(sys.argv[1])
