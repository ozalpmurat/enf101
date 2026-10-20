# 7. hafta: sayfa düzeni şeması — A4 dikey sayfa üzerinde üstbilgi, metin alanı,
# kenar boşlukları ve altbilgi.
# Kullanım: python3 diyagram_betikleri/diagram-sayfa-duzeni.py [--kontrol]
#           --kontrol : yazıların alanlarına sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-07-kelime-islemci/gorseller/diagram-sayfa-duzeni.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8); başlık slaytta/ders notunda
# altyazıdır. Eski PNG'nin (866×456, yatay) kaynak betiği depoda yoktu; şema
# A4 dikey oranına uygun olarak bu betikle yeniden çizildi.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

LAC = "#1F3864"
MAVI = "#2E74B5"
ACIK = "#EDF2F9"
GRI = "#595959"

plt.rcParams["font.family"] = "DejaVu Sans"

# birim = cm; figür oranı A4 dikeye yakın (0,706)
G, Y = 12.0, 17.0

SAYFA = (1.2, 1.7, 9.6, 13.6)      # x, y, w, h  (9,6 / 13,6 = 0,706)
KENAR = 1.0                        # iç kenar boşluğu
METIN = (SAYFA[0] + KENAR, SAYFA[1] + KENAR,
         SAYFA[2] - 2 * KENAR, SAYFA[3] - 2 * KENAR)


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
    sinir = METIN[2] - 0.3
    for metin, fs, bold in (
        ("METİN ALANI", 13, True),
        ("ÜSTBİLGİ (başlık)", 9.5, True),
        ("ALT BİLGİ", 10, True),
        ("(sayfa numarası)", 8.5, False),
    ):
        g = metin_olc(fig, ax, metin, fs, bold)
        if g > sinir:
            print(f"TAŞIYOR  {metin}: {g:.2f} > {sinir:.2f}")
            sorun += 1
    print(f"şema: sayfa {SAYFA[2]:.1f} × {SAYFA[3]:.1f} cm (oran {SAYFA[2]/SAYFA[3]:.3f}), "
          f"figür {G} × {Y} cm")
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, G)
ax.set_ylim(0, Y)
ax.axis("off")

# sayfa
ax.add_patch(Rectangle((SAYFA[0], SAYFA[1]), SAYFA[2], SAYFA[3],
                       linewidth=1.8, edgecolor=LAC, facecolor="white", zorder=2))

# metin alanı
ax.add_patch(Rectangle((METIN[0], METIN[1]), METIN[2], METIN[3],
                       linewidth=1.0, edgecolor=MAVI, facecolor=ACIK, zorder=3))
ax.text(METIN[0] + METIN[2] / 2, METIN[1] + METIN[3] / 2, "METİN ALANI",
        ha="center", va="center", fontsize=13, color=LAC, fontweight="bold", zorder=4)

# üstbilgi
ust_y = METIN[1] + METIN[3] + KENAR / 2
ax.plot([METIN[0], METIN[0] + METIN[2]], [METIN[1] + METIN[3] + 0.08] * 2,
        color=LAC, linewidth=0.9, zorder=3)
ax.text(METIN[0] + METIN[2] / 2, ust_y + 0.18, "ÜSTBİLGİ (başlık)",
        ha="center", va="center", fontsize=9.5, color=GRI, zorder=4)

# altbilgi — iki satır
ax.plot([METIN[0], METIN[0] + METIN[2]], [METIN[1] - 0.04] * 2,
        color=LAC, linewidth=0.9, zorder=3)
ax.text(METIN[0] + METIN[2] / 2, METIN[1] - 0.25, "ALT BİLGİ",
        ha="center", va="center", fontsize=10, color=LAC, fontweight="bold", zorder=4)
ax.text(METIN[0] + METIN[2] / 2, METIN[1] - 0.58, "(sayfa numarası)",
        ha="center", va="center", fontsize=8.5, color=GRI, zorder=4)

# kenar boşluğu oku (sol)
ok_y0, ok_y1 = METIN[1] + 1.2, METIN[1] + METIN[3] - 1.2
ax.add_patch(FancyArrowPatch((SAYFA[0] + 0.15, ok_y0), (SAYFA[0] + 0.15, ok_y1),
                             arrowstyle="<->", mutation_scale=11,
                             linewidth=1.2, color=MAVI, zorder=4))
ax.text(SAYFA[0] + 0.55, (ok_y0 + ok_y1) / 2, "kenar boşlukları",
        ha="center", va="center", rotation=90, fontsize=8.5, color=MAVI, zorder=4)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-sayfa-duzeni.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
