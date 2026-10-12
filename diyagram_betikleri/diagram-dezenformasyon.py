# 6. hafta: şüpheli içeriği kontrol — 1. haftanın beş sorusu.
# Kullanım: python3 diyagram_betikleri/diagram-dezenformasyon.py [--kontrol]
#           --kontrol : yazıların kutulara sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-06-internet-eposta-edevlet/gorseller/diagram-dezenformasyon.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8): başlık ders notunda şekil
# altyazısı, sunuda slayt başlığıdır.

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-06-internet-eposta-edevlet" / "gorseller"

LAC = "#1F3864"     # lacivert
ZEMIN = "#EDF2F9"   # zemin bandı
GRI = "#595959"     # alt yazı

plt.rcParams["font.family"] = "DejaVu Sans"

X0, ARALIK = 0.15, 0.20
KART_Y, KART_H = 0.95, 1.85
BASLIK_FS, ALT_FS = 10.5, 9.0
İÇ_PAY = 0.16        # kutu içinde iki yandan bırakılacak pay (eksen birimi)
DIŞ_PAY = 0.12       # şeridin sağ/sol kenarında kalan pay

# (başlık, alt satır, kart genişliği). Genişlikler --kontrol ile ölçüldü:
# başlığın en uzun satırı KART_W - İÇ_PAY değerini aşmamalı. Beşinci kart iki
# satıra bölündü: "Başka kaynak?" tek satırda kutuyu taşıyordu.
SORULAR = [
    ("Kaynak", "kim?", 1.92),
    ("Ne zaman?", "güncel mi?", 1.92),
    ("Kanıt", "var mı?", 1.92),
    ("Amaç", "ne?", 1.92),
    ("Başka\nkaynak?", "doğruluyor mu?", 1.92),
]

ALT = "Beş sorudan biri bile yanıtsızsa içeriği paylaşmayın."
ALT_FS_B = 10.0


def kart_x(i):
    return X0 + sum(w + ARALIK for _, _, w in SORULAR[:i])


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
    """yazılar kutuya ve satıra sığıyor mu; sığmıyorsa eksi değer yazılır."""
    sorun = 0
    for i, (soru, alt, gen_kart) in enumerate(SORULAR):
        for etiket, metin, fs, bold in [
            ("başlık", soru, BASLIK_FS, True),
            ("alt", alt, ALT_FS, False),
        ]:
            gen, _ = metin_olc(fig, ax, metin, fs, bold)
            # ortalanmış yazı: en uzun satır iki yandan payla sığmalı
            for sat in metin.split("\n"):
                g, _ = metin_olc(fig, ax, sat, fs, bold)
                if g > gen_kart - İÇ_PAY:
                    print(f"TAŞIYOR  kart {i + 1} {etiket}: {g:.3f} > "
                          f"{gen_kart - İÇ_PAY:.3f}  ({sat})")
                    sorun += 1
    gen, _ = metin_olc(fig, ax, ALT, ALT_FS_B, False)
    kullanilabilir = XMAX - 2 * (DIŞ_PAY + 0.10)
    if gen > kullanilabilir:
        print(f"TAŞIYOR  alt satır: {gen:.2f} > {kullanilabilir:.2f}")
        sorun += 1
    print(f"şema: son kart sağ kenarı {SAG:.2f}, eksen {XMAX:.2f} birim")
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


fig, ax = plt.subplots(figsize=(8.0, 2.5), dpi=200)
SAG = kart_x(len(SORULAR) - 1) + SORULAR[-1][2]     # son kartın sağ kenarı
XMAX = SAG + X0                                     # simetri: sağa da X0 kadar pay
ax.set_xlim(0, XMAX)
ax.set_ylim(0, 3.0)
ax.axis("off")

ax.add_patch(FancyBboxPatch((DIŞ_PAY, 0.12), XMAX - 2 * DIŞ_PAY, 2.76,
             boxstyle="round,pad=0.02,rounding_size=0.14",
             linewidth=0, facecolor=ZEMIN, zorder=0))

for i, (soru, alt, gen_kart) in enumerate(SORULAR):
    x = kart_x(i)
    ax.add_patch(FancyBboxPatch((x, KART_Y), gen_kart, KART_H,
                 boxstyle="round,pad=0.02,rounding_size=0.10",
                 linewidth=1.6, edgecolor=LAC, facecolor="#FFFFFF", zorder=2))
    ax.text(x + gen_kart / 2, KART_Y + 1.18, soru, ha="center", va="center",
            fontsize=BASLIK_FS, color=LAC, fontweight="bold", zorder=3)
    ax.text(x + gen_kart / 2, KART_Y + 0.44, alt, ha="center", va="center",
            fontsize=ALT_FS, color=GRI, zorder=3)

ax.text(XMAX / 2, 0.44, ALT, ha="center", va="center",
        fontsize=ALT_FS_B, color=GRI, style="italic", zorder=3)

fig.tight_layout(pad=0.35)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-dezenformasyon.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
