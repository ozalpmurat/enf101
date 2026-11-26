# 10. hafta: adres çubuğunda güvenli (https + kilit) ve şüpheli bağlantı.
# İki satır: doğru ve yanlış adres çubuğu örneği. Markasız, temsilî çizimdir.
#
# Kullanım:
#   python3 diyagram_betikleri/diagram-guvenli-baglanti.py            # PNG üretir
#   python3 diyagram_betikleri/diagram-guvenli-baglanti.py --kontrol  # taşma denetimi
#
# Çıktı: hafta-10-bilgi-guvenligi/gorseller/diagram-guvenli-baglanti.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8). Gerçek bir tarayıcı ekran
# görüntüsü değil, kavramı gösteren kendi çizimimizdir.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Circle, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-10-bilgi-guvenligi" / "gorseller"

LAC = "#1F3864"
GRI = "#595959"
YESIL = "#2E6B3E"
KIRMIZI = "#A93A3A"
RULE = "#C9D3E0"

plt.rcParams["font.family"] = "DejaVu Sans"

G, Y = 18.0, 6.2
BAR_X, BAR_W, BAR_H = 0.7, 11.6, 1.5
ETIKET_X = 12.9

ADRES_FS, BASLIK_FS, ALT_FS = 10, 10.5, 9

# (y0, adres, renk, güvenli mi, etiket, açıklama)
SATIRLAR = [
    (3.55, "https://www.ornek-banka.com.tr", YESIL, True,
     "Güvenli bağlantı", "https ve kilit simgesi var"),
    (1.15, "http://ornek-banka-giris.com", KIRMIZI, False,
     "Şüpheli bağlantı", "https ve kilit yok;\nadres kuruma benzemiyor"),
]


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def kilit(ax, cx, cy, renk):
    """küçük asma kilit simgesi: gövde + kavis."""
    bw, bh = 0.44, 0.34
    ax.add_patch(FancyBboxPatch((cx - bw / 2, cy - bh / 2), bw, bh,
                 boxstyle="round,pad=0.005,rounding_size=0.06",
                 linewidth=1.6, edgecolor=renk, facecolor="white", zorder=4))
    ax.add_patch(Arc((cx, cy + bh / 2), 0.30, 0.34, theta1=0, theta2=180,
                 linewidth=1.6, edgecolor=renk, zorder=4))


def uyari(ax, cx, cy, renk):
    """küçük ünlem: kırmızı daire içinde '!'."""
    ax.add_patch(Circle((cx, cy), 0.20, linewidth=1.6, edgecolor=renk,
                        facecolor="white", zorder=4))
    ax.text(cx, cy, "!", ha="center", va="center", fontsize=10,
            color=renk, fontweight="bold", zorder=5)


def kur():
    fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, G)
    ax.set_ylim(0, Y)
    ax.axis("off")
    for y0, adres, renk, guvenli, etiket, aciklama in SATIRLAR:
        cy = y0 + BAR_H / 2
        ax.add_patch(FancyBboxPatch((BAR_X, y0), BAR_W, BAR_H,
                     boxstyle="round,pad=0.02,rounding_size=0.10",
                     linewidth=1.6, edgecolor=RULE, facecolor="white", zorder=2))
        if guvenli:
            kilit(ax, BAR_X + 0.55, cy, renk)
        else:
            uyari(ax, BAR_X + 0.55, cy, renk)
        ax.text(BAR_X + 1.05, cy, adres, ha="left", va="center",
                fontsize=ADRES_FS, color=LAC, zorder=5)
        ax.text(ETIKET_X, cy + 0.35, etiket, ha="left", va="center",
                fontsize=BASLIK_FS, color=renk, fontweight="bold", zorder=5)
        ax.text(ETIKET_X, cy - 0.32, aciklama, ha="left", va="center",
                fontsize=ALT_FS, color=GRI, linespacing=1.4, zorder=5)
    return fig, ax


def kontrol(fig, ax):
    sorun = 0
    adres_sinir = BAR_W - 1.25
    etiket_sinir = G - ETIKET_X - 0.2
    for _, adres, _, _, etiket, aciklama in SATIRLAR:
        g = metin_olc(fig, ax, adres, ADRES_FS, False)
        if g > adres_sinir:
            print(f"TAŞIYOR  adres: {g:.2f} > {adres_sinir:.2f}  ({adres})")
            sorun += 1
        for metin, fs, bold in [(etiket, BASLIK_FS, True),
                                *[(s, ALT_FS, False) for s in aciklama.split("\n")]]:
            g = metin_olc(fig, ax, metin, fs, bold)
            if g > etiket_sinir:
                print(f"TAŞIYOR  etiket: {g:.2f} > {etiket_sinir:.2f}  ({metin})")
                sorun += 1
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig, ax = kur()
if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-guvenli-baglanti.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
