# 6. hafta: e-Devlet — farklı kurumların hizmetlerine tek giriş.
# Kullanım: python3 diyagram_betikleri/diagram-edevlet.py
# Çıktı:    hafta-06-internet-eposta-edevlet/gorseller/diagram-edevlet.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8): başlık ders notunda şekil
# altyazısı, sunuda slayt başlığıdır.

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-06-internet-eposta-edevlet" / "gorseller"

LAC = "#1F3864"     # lacivert
ACIK = "#DCE7F5"    # açık mavi kutu
ZEMIN = "#EDF2F9"   # zemin bandı
GRI = "#595959"     # alt yazı

plt.rcParams["font.family"] = "DejaVu Sans"


def kutu(ax, x, y, w, h, metin, fc=ACIK, ec=LAC, fs=11, tc=LAC, bold=False):
    b = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                       linewidth=1.6, edgecolor=ec, facecolor=fc, zorder=2)
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2, metin, ha="center", va="center",
            fontsize=fs, color=tc, zorder=3,
            fontweight="bold" if bold else "normal", wrap=True)
    return (x, y, w, h)


def ok(ax, p1, p2, cift=False, etiket=None, renk=LAC):
    a = FancyArrowPatch(p1, p2, arrowstyle="-|>", mutation_scale=14,
                        linewidth=1.5, color=renk, zorder=1,
                        shrinkA=2, shrinkB=2)
    ax.add_patch(a)
    if cift:
        a2 = FancyArrowPatch(p2, p1, arrowstyle="-|>", mutation_scale=14,
                             linewidth=1.5, color=renk, zorder=1,
                             shrinkA=2, shrinkB=2)
        ax.add_patch(a2)
    if etiket:
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        ax.text(mx, my + 0.09, etiket, ha="center", va="bottom",
                fontsize=8.5, color=GRI, zorder=4)


fig, ax = plt.subplots(figsize=(8.6, 3.2), dpi=170)
ax.set_xlim(0, 10)
ax.set_ylim(0, 4.2)
ax.axis("off")

ax.add_patch(FancyBboxPatch((0.25, 0.2), 9.5, 3.7,
             boxstyle="round,pad=0.02,rounding_size=0.12",
             linewidth=0, facecolor=ZEMIN, zorder=0))

# sol: kullanıcı
kutu(ax, 0.7, 1.55, 2.0, 1.0, "Kullanıcı\n(tek giriş)", fc="#FFFFFF", fs=11, bold=True)
# orta: e-Devlet kapısı
kutu(ax, 3.7, 1.3, 2.3, 1.5, "e-Devlet\nKapısı", fc=LAC, tc="#FFFFFF", fs=13, bold=True)
# sag: kurumlar
kurumlar = ["Belge talebi", "Başvuru", "Sorgulama", "Ödeme"]
ys = [2.9, 2.15, 1.4, 0.65]
for k, y in zip(kurumlar, ys):
    kutu(ax, 7.1, y, 2.2, 0.62, k, fc=ACIK, fs=10)

ok(ax, (2.7, 2.05), (3.7, 2.05), cift=True, etiket="giriş /\nsonuç")
for y in ys:
    ok(ax, (6.0, 2.05), (7.1, y + 0.31))

fig.tight_layout(pad=0.35)
cikti = HEDEF / "diagram-edevlet.png"
fig.savefig(cikti, dpi=170, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
