# 6. hafta: etkili arama — dört adım ve geri dönüş.
# Kullanım: python3 diyagram_betikleri/diagram-arama.py [--kontrol]
#           --kontrol : yazıların kutulara sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-06-internet-eposta-edevlet/gorseller/diagram-arama.png
#
# Adımlar tek turda bitmez: sonuç yeterli değilse başa dönülür. Şemada bu,
# kartların altından 4. adımdan 1. adıma giden geri okuyla gösterilir.
# Okun etiketi yoktur; döngüyü ders notundaki metin ve sunudaki alt cümle anlatır.
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8): başlık ders notunda şekil
# altyazısı, sunuda slayt başlığıdır.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.path as mpath
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-06-internet-eposta-edevlet" / "gorseller"

LAC = "#1F3864"     # lacivert
MAVI = "#2E74B5"    # vurgu (oklar)
ACIK = "#DCE7F5"    # açık mavi kutu
ZEMIN = "#EDF2F9"   # zemin bandı
GRI = "#595959"     # alt yazı

plt.rcParams["font.family"] = "DejaVu Sans"

# eksen birimi cinsinden kart ölçüleri
X0, KART_W, ARALIK = 0.34, 2.12, 0.28
KART_Y, KART_H = 0.95, 1.90
DÖNÜŞ_Y = 0.55       # geri okun kartların altından geçtiği yükseklik
DIŞ_PAY = 0.12       # şeridin sağ/sol kenarında kalan pay
İÇ_PAY = 0.16        # kutu içinde iki yandan bırakılacak pay

ADIMLAR = [
    ("1", "SORUYU\nNETLEŞTİR", "ne arıyorum?"),
    ("2", "ANAHTAR\nKELİME", "kısa ve öz"),
    ("3", "SINIRLA", "site, tarih, tür"),
    ("4", "DOĞRULA", "kaynağa bak"),
]


def kart_x(i):
    return X0 + i * (KART_W + ARALIK)


def metin_olc(fig, ax, metin, fs, bold):
    """metnin eksen birimindeki genişlik ve yüksekliği."""
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, y1), (x2, y2) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1, y2 - y1


def kontrol(fig, ax):
    """yazılar kutuya sığıyor mu; sığmıyorsa eksi değer yazılır."""
    sorun = 0
    for i, (no, baslik, alt) in enumerate(ADIMLAR):
        for etiket, metin, fs, bold in [
            ("no", no, 10.5, False),
            ("başlık", baslik, 10.5, True),
            ("alt", alt, 9.5, False),
        ]:
            gen, _ = metin_olc(fig, ax, metin, fs, bold)
            # sola yaslı rakamda soldaki yerleşim boşluğu da paydan düşülür
            pay = KART_W - (0.24 if etiket == "no" else İÇ_PAY)
            if gen > pay:
                sat = max(metin.split("\n"), key=len)
                print(f"TAŞIYOR  kart {i + 1} {etiket}: {gen:.2f} > {pay:.2f}  ({sat})")
                sorun += 1
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


def kutu(ax, x, y, w, h, fc):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.10",
                 linewidth=1.6, edgecolor=LAC, facecolor=fc, zorder=2))


fig, ax = plt.subplots(figsize=(8.0, 3.0), dpi=200)
SAG = kart_x(len(ADIMLAR) - 1) + KART_W      # son kartın sağ kenarı
XMAX = SAG + X0                              # simetri: sağa da X0 kadar pay
ax.set_xlim(0, XMAX)
ax.set_ylim(0, 3.12)
ax.axis("off")

ax.add_patch(FancyBboxPatch((DIŞ_PAY, 0.15), XMAX - 2 * DIŞ_PAY, 2.85,
             boxstyle="round,pad=0.02,rounding_size=0.14",
             linewidth=0, facecolor=ZEMIN, zorder=0))

for i, (no, baslik, alt) in enumerate(ADIMLAR):
    x = kart_x(i)
    kutu(ax, x, KART_Y, KART_W, KART_H, ACIK if i % 2 else "#FFFFFF")
    ax.text(x + 0.14, KART_Y + 1.58, no, ha="left", va="center",
            fontsize=10.5, color=GRI, zorder=3)
    ax.text(x + KART_W / 2, KART_Y + 1.06, baslik, ha="center", va="center",
            fontsize=10.5, color=LAC, fontweight="bold", zorder=3)
    ax.text(x + KART_W / 2, KART_Y + 0.38, alt, ha="center", va="center",
            fontsize=9.5, color=GRI, zorder=3)
    if i < len(ADIMLAR) - 1:
        ax.text(x + KART_W + ARALIK / 2, KART_Y + KART_H / 2, "›",
                ha="center", va="center", fontsize=17, color=MAVI, zorder=3)

# geri dönüş: 4. adımın altından çıkıp 1. adımın altına girer (döngü)
x_sag = kart_x(len(ADIMLAR) - 1) + KART_W / 2
x_sol = kart_x(0) + KART_W / 2
geri = mpath.Path(
    [(x_sag, KART_Y), (x_sag, DÖNÜŞ_Y), (x_sol, DÖNÜŞ_Y), (x_sol, KART_Y)],
    [mpath.Path.MOVETO, mpath.Path.LINETO, mpath.Path.LINETO, mpath.Path.LINETO],
)
ax.add_patch(FancyArrowPatch(path=geri, arrowstyle="-|>", mutation_scale=13,
                             linewidth=1.8, color=MAVI, zorder=3))

fig.tight_layout(pad=0.35)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-arama.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
