# 7. hafta: başlık stilleri ve otomatik içindekiler.
# Kullanım: python3 diyagram_betikleri/diagram-baslik.py [--kontrol]
#           --kontrol : yazıların kutulara sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-07-kelime-islemci/gorseller/diagram-baslik.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8): başlık ders notunda şekil
# altyazısı, sunuda slayt başlığıdır. Eski PNG'de "BAŞLIK HİYERARŞİSİ ve
# İÇİNDEKİLER" başlığı gömülüydü ve kaynak betiği kayıptı; şema bu betikle
# başlıksız olarak yeniden çizildi (ölçüler eski PNG ile aynı tutuldu).

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

LAC = "#1F3864"     # lacivert
MAVI = "#2E74B5"    # vurgu (oklar)
ACIK = "#DCE7F5"    # açık mavi kutu
ZEMIN = "#EDF2F9"   # zemin bandı
GRI = "#595959"     # alt yazı

plt.rcParams["font.family"] = "DejaVu Sans"

# veri birimi = cm; figür 17,4 × 7,6 cm (eski PNG 1373 × 597 px @200 dpi)
G, Y = 18.6, 8.4

KUTU_W, KUTU_H = 6.8, 1.5
SEVIYE_X = [0.7, 1.4, 2.1]        # her seviye biraz içeriden başlar
KUTU_Y = [5.0, 2.95, 0.9]         # 1. seviye üstte: 1,5 yükseklik + 0,55 boşluk
SOL_BASLIK = "ANAHATLAR (BAŞLIKLAR)"
SOL_BASLIK_Y0, SOL_BASLIK_H = 6.6, 1.2
SEVIYE = [
    "Başlık 1 — BÖLÜM",
    "Başlık 2 — alt bölüm",
    "Başlık 3 — alt başlık",
]
KUTU_FS, KUTU_PAY = 10.5, 0.30

PAN_X, PAN_W = 11.0, 6.7          # içindekiler paneli
PAN_Y0, PAN_Y1 = 0.9, 7.8
BASLIK_H = 1.2                    # panel başlık bandı
PAN_FS, PAN_PAY = 9.5, 0.35

MADDELER = [
    "• Başlıklardan otomatik oluşur",
    "• Sayfa numaraları kendiliğinden\ngüncellenir",
    "• İstenen seviyeye kadar\nbaşlıklar dahil edilebilir",
]


def metin_olc(fig, ax, metin, fs, bold):
    """metnin eksen birimindeki (cm) genişliği."""
    t = ax.text(0, 0, metin, fontsize=fs, fontweight="bold" if bold else "normal")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    inv = ax.transData.inverted()
    (x1, _), (x2, _) = inv.transform([(bb.x0, bb.y0), (bb.x1, bb.y1)])
    t.remove()
    return x2 - x1


def en_uzun(metin, fs, bold, fig, ax):
    return max(metin_olc(fig, ax, s, fs, bold) for s in metin.split("\n"))


def kontrol(fig, ax):
    """yazılar kutuya sığıyor mu; sığmıyorsa ölçü yazılır."""
    sorun = 0
    sinir = KUTU_W - 2 * KUTU_PAY
    for i, seviye in enumerate(SEVIYE):
        g = en_uzun(seviye, KUTU_FS, True, fig, ax)
        if g > sinir:
            print(f"TAŞIYOR  seviye {i + 1}: {g:.2f} > {sinir:.2f}  ({seviye})")
            sorun += 1
    sinir = PAN_W - 2 * PAN_PAY
    for m in MADDELER:
        g = en_uzun(m, PAN_FS, False, fig, ax)
        if g > sinir:
            print(f"TAŞIYOR  panel maddesi: {g:.2f} > {sinir:.2f}  ({m.splitlines()[0]})")
            sorun += 1
    g = en_uzun(SOL_BASLIK, 10.5, True, fig, ax)
    if g > KUTU_W - 0.4:
        print(f"TAŞIYOR  sol başlık: {g:.2f} > {KUTU_W - 0.4:.2f}")
        sorun += 1
    g = en_uzun("İÇİNDEKİLER TABLOSU", 11, True, fig, ax)
    if g > PAN_W - 0.4:
        print(f"TAŞIYOR  panel başlığı: {g:.2f} > {PAN_W - 0.4:.2f}")
        sorun += 1
    print(f"şema: seviye kutuları x {SEVIYE_X[0]:.1f}–{SEVIYE_X[-1] + KUTU_W:.1f}, "
          f"panel x {PAN_X:.1f}–{PAN_X + PAN_W:.1f}, eksen {G} cm")
    print("kontrol: " + ("TAŞMA VAR" if sorun else "temiz"))
    return sorun


def kutu(ax, x, y, w, h, fc, renk=LAC, kalinlik=1.6, yuvarlak=0.10):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0.02,rounding_size={yuvarlak}",
                 linewidth=kalinlik, edgecolor=renk, facecolor=fc, zorder=2))


fig = plt.figure(figsize=(G / 2.54, Y / 2.54), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, G)
ax.set_ylim(0, Y)
ax.axis("off")

# zemin bandı
ax.add_patch(FancyBboxPatch((0.15, 0.15), G - 0.3, Y - 0.3,
             boxstyle="round,pad=0.02,rounding_size=0.14",
             linewidth=0, facecolor=ZEMIN, zorder=0))

# solda: seviye başlığı (bantsız, yalnızca metin)
ax.text(SEVIYE_X[0] + KUTU_W / 2, SOL_BASLIK_Y0 + SOL_BASLIK_H / 2, SOL_BASLIK,
        ha="center", va="center", fontsize=10.5, color=LAC, fontweight="bold", zorder=3)

# solda: seviyeler (içe giren kutular)
for i, (x, y, metin) in enumerate(zip(SEVIYE_X, KUTU_Y, SEVIYE)):
    kutu(ax, x, y, KUTU_W, KUTU_H, "#FFFFFF")
    ax.text(x + KUTU_W / 2, y + KUTU_H / 2, metin, ha="center", va="center",
            fontsize=KUTU_FS, color=LAC, fontweight="bold", zorder=3)
    if i < len(SEVIYE) - 1:
        ax.text(x + KUTU_W / 2, y - 0.28, "↓", ha="center", va="center",
                fontsize=13, color=MAVI, zorder=3)

# soldan sağa ok
ax.text((SEVIYE_X[-1] + KUTU_W + PAN_X) / 2, 3.7, "→", ha="center", va="center",
        fontsize=15, color=MAVI, zorder=3)

# sağda: içindekiler paneli
kutu(ax, PAN_X, PAN_Y0, PAN_W, PAN_Y1 - PAN_Y0, "#FFFFFF")
ax.text(PAN_X + PAN_W / 2, PAN_Y1 - BASLIK_H / 2, "İÇİNDEKİLER TABLOSU",
        ha="center", va="center", fontsize=11, color=LAC, fontweight="bold", zorder=3)
for metin, y in zip(MADDELER, [6.3, 5.3, 4.2]):
    for j, satir in enumerate(metin.split("\n")):
        ax.text(PAN_X + PAN_PAY, y - j * 0.4, satir, ha="left", va="center",
                fontsize=PAN_FS, color=GRI, zorder=3)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-baslik.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
