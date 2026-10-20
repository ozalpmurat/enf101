# 7. hafta: iyi tablo biçimlendirmesi — "her hücre çerçeveli" ile "az çizgili" karşılaştırması.
# Kullanım: python3 diyagram_betikleri/diagram-tablo-ornek.py [--kontrol]
#           --kontrol : yazıların hücrelere sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-07-kelime-islemci/gorseller/diagram-tablo-ornek.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8); başlık slaytta/ders notunda
# altyazıdır. Panellerin üstündeki kısa etiketler paneli tanımlar.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

LAC = "#1F3864"
MAVI = "#2E74B5"
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"

# birim = cm
G, Y = 18.8, 7.4
KOLONLAR = ["Ad", "Vize", "Final", "Ortalama"]
SATIRLAR = [
    ["Ayşe", "70", "85", "79"],
    ["Mehmet", "60", "55", "57"],
    ["Zeynep", "90", "95", "93"],
]
HUCRE_FS = 10.5
ETIKET_FS = 9.5

PANEL_W = 8.8
PANEL_H = 4.6
PANEL_Y0 = 0.9
SOLD_X = 0.4
SAG_X = 9.8


def metin_olc(fig, ax, metin, fs, bold):
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def kontrol(fig, ax):
    sorun = 0
    kolon_w = PANEL_W / len(KOLONLAR)
    sinir = kolon_w - 0.4
    for satir in [KOLONLAR] + SATIRLAR:
        for hucre in satir:
            g = metin_olc(fig, ax, hucre, HUCRE_FS, False)
            if g > sinir:
                print(f"TAŞIYOR  hücre: {g:.2f} > {sinir:.2f}  ({hucre})")
                sorun += 1
    for etiket in ("Her hücre çerçeveli", "Az çizgili (önerilen)"):
        if metin_olc(fig, ax, etiket, ETIKET_FS, False) > PANEL_W:
            print(f"TAŞIYOR  etiket: {etiket}")
            sorun += 1
    print(f"şema: panel {PANEL_W:.1f} cm, kolon {kolon_w:.2f} cm, eksen {G} cm")
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


def tablo(ax, x0, tam_izgara):
    satir_h = PANEL_H / (len(SATIRLAR) + 1)
    kolon_w = PANEL_W / len(KOLONLAR)

    for i, satir in enumerate([KOLONLAR] + SATIRLAR):
        y = PANEL_Y0 + PANEL_H - (i + 0.5) * satir_h
        for j, hucre in enumerate(satir):
            x = x0 + j * kolon_w
            ortak = dict(va="center", fontsize=HUCRE_FS, color=LAC, zorder=3)
            if j == 0:
                ax.text(x + 0.18, y, hucre, ha="left",
                        fontweight="bold" if i == 0 else "normal", **ortak)
            else:
                ax.text(x + kolon_w - 0.18, y, hucre, ha="right",
                        fontweight="bold" if i == 0 else "normal", **ortak)

    ust = PANEL_Y0 + PANEL_H
    if tam_izgara:
        for i in range(len(SATIRLAR) + 2):
            y = ust - i * satir_h
            ax.plot([x0, x0 + PANEL_W], [y, y], color=GRI, linewidth=0.8, zorder=2)
        for j in range(len(KOLONLAR) + 1):
            x = x0 + j * kolon_w
            ax.plot([x, x], [PANEL_Y0, ust], color=GRI, linewidth=0.8, zorder=2)
    else:
        ax.plot([x0, x0 + PANEL_W], [ust, ust], color=LAC, linewidth=1.6, zorder=2)
        ax.plot([x0, x0 + PANEL_W], [ust - satir_h, ust - satir_h],
                color=LAC, linewidth=1.0, zorder=2)
        ax.plot([x0, x0 + PANEL_W], [PANEL_Y0, PANEL_Y0], color=LAC, linewidth=1.6, zorder=2)


fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, G)
ax.set_ylim(0, Y)
ax.axis("off")

for x0, etiket, tam in (
    (SOLD_X, "Her hücre çerçeveli", True),
    (SAG_X, "Az çizgili (önerilen)", False),
):
    ax.text(x0, PANEL_Y0 + PANEL_H + 0.75, etiket, ha="left", va="center",
            fontsize=ETIKET_FS, color=MAVI if tam else LAC, fontweight="bold", zorder=3)
    tablo(ax, x0, tam)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-tablo-ornek.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
