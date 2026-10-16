# 7. hafta: akademik dürüstlük — doğru ve yanlış, kaynak künyesi.
# Kullanım: python3 diyagram_betikleri/diagram-intihal.py [--kontrol]
#           --kontrol : yazıların kutulara sığıp sığmadığını ölçer, PNG üretmez
# Çıktı:    hafta-07-kelime-islemci/gorseller/diagram-intihal.png
#
# Şemanın içine başlık yazılmaz (AGENTS.md §8): başlık ders notunda şekil
# altyazısı, sunuda slayt başlığıdır. Eski PNG'de "AKADEMİK DÜRÜSTLÜK" başlığı
# gömülüydü ve kaynak betiği kayıptı; şema bu betikle başlıksız olarak yeniden
# çizildi (ölçüler eski PNG ile aynı tutuldu).

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

KOK = Path(__file__).resolve().parent.parent
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

LAC = "#1F3864"     # lacivert
MAVI = "#2E74B5"    # vurgu (doğru işareti)
ACIK = "#DCE7F5"    # açık mavi kutu
ZEMIN = "#EDF2F9"   # zemin bandı
GRI = "#595959"     # alt yazı
KIRMIZI = "#9E2B2B"     # yanlış işareti
ACIK_KIRMIZI = "#E3C9C9"  # yanlış sütunu zemini

plt.rcParams["font.family"] = "DejaVu Sans"

# veri birimi = cm; figür 17,4 × 6,96 cm (eski PNG 1373 × 548 px @200 dpi)
G, Y = 17.4, 6.96

SUTUN_H = 4.3                 # iki sütunun ortak yüksekliği
SUTUN_Y0 = 2.05
BASLIK_B = 0.8                # sütun başlık bandı
SOL_X, SAG_X, SUTUN_W = 0.6, 8.9, 7.9
SUT_PAY = 0.45                # sütun içi yatay pay
BASLIK_FS, MADDE_FS = 11, 9.5

DOGRU = ["✓ Alıntı yap ve kaynak göster",
         "✓ Kendi cümlelerinle anlat,\nyine kaynak göster"]
YANLIS = "✗ Kaynak göstermeden kullan"
ETIKET = "(İNTİHAL)"
ETIKET_W, ETIKET_H = 3.6, 0.9

ALT_X, ALT_W, ALT_Y, ALT_H = 0.6, 16.2, 0.5, 1.15
ALT_METIN = ("Kaynak gösterirken: yazar, eser adı, yayın yılı, sayfa "
             "— ve nereden erişildiği")
ALT_FS = 9.5


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
    sinir = SUTUN_W - 2 * SUT_PAY
    for m in DOGRU + [YANLIS]:
        g = en_uzun(m, MADDE_FS, False, fig, ax)
        if g > sinir:
            print(f"TAŞIYOR  sütun maddesi: {g:.2f} > {sinir:.2f}  ({m.splitlines()[0]})")
            sorun += 1
    for baslik, x in [("DOĞRU", SOL_X), ("YANLIŞ", SAG_X)]:
        g = en_uzun(baslik, BASLIK_FS, True, fig, ax)
        if g > SUTUN_W - 0.4:
            print(f"TAŞIYOR  {baslik} başlığı: {g:.2f} > {SUTUN_W - 0.4:.2f}")
            sorun += 1
    g = en_uzun(ETIKET, 10.5, True, fig, ax)
    if g > ETIKET_W - 0.3:
        print(f"TAŞIYOR  etiket: {g:.2f} > {ETIKET_W - 0.3:.2f}")
        sorun += 1
    g = en_uzun(ALT_METIN, ALT_FS, False, fig, ax)
    if g > ALT_W - 0.8:
        print(f"TAŞIYOR  alt satır: {g:.2f} > {ALT_W - 0.8:.2f}")
        sorun += 1
    print(f"şema: sütunlar x {SOL_X:.1f}–{SOL_X + SUTUN_W:.1f} ve "
          f"{SAG_X:.1f}–{SAG_X + SUTUN_W:.1f}, eksen {G} cm")
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

BASLIK_Y0 = SUTUN_Y0 + SUTUN_H - BASLIK_B

# sol sütun: doğrular
kutu(ax, SOL_X, SUTUN_Y0, SUTUN_W, SUTUN_H, "#FFFFFF")
kutu(ax, SOL_X, BASLIK_Y0, SUTUN_W, BASLIK_B, ACIK, yuvarlak=0.08)
ax.text(SOL_X + SUTUN_W / 2, BASLIK_Y0 + BASLIK_B / 2, "DOĞRU",
        ha="center", va="center", fontsize=BASLIK_FS, color=LAC,
        fontweight="bold", zorder=3)
for m, y in zip(DOGRU, [4.55, 3.55]):
    for j, satir in enumerate(m.split("\n")):
        ax.text(SOL_X + SUT_PAY, y - j * 0.45, satir, ha="left", va="center",
                fontsize=MADDE_FS, color=GRI, zorder=3)

# sağ sütun: yanlışlar
kutu(ax, SAG_X, SUTUN_Y0, SUTUN_W, SUTUN_H, "#FFFFFF")
kutu(ax, SAG_X, BASLIK_Y0, SUTUN_W, BASLIK_B, ACIK_KIRMIZI, yuvarlak=0.08)
ax.text(SAG_X + SUTUN_W / 2, BASLIK_Y0 + BASLIK_B / 2, "YANLIŞ",
        ha="center", va="center", fontsize=BASLIK_FS, color=KIRMIZI,
        fontweight="bold", zorder=3)
ax.text(SAG_X + SUT_PAY, 4.55, YANLIS, ha="left", va="center",
        fontsize=MADDE_FS, color=GRI, zorder=3)
kutu(ax, SAG_X + (SUTUN_W - ETIKET_W) / 2, 2.6, ETIKET_W, ETIKET_H,
     ACIK_KIRMIZI, renk=KIRMIZI, kalinlik=1.4, yuvarlak=0.45)
ax.text(SAG_X + SUTUN_W / 2, 2.6 + ETIKET_H / 2, ETIKET, ha="center",
        va="center", fontsize=10.5, color=KIRMIZI, fontweight="bold", zorder=3)

# alt künye satırı
kutu(ax, ALT_X, ALT_Y, ALT_W, ALT_H, ACIK, renk=ACIK, kalinlik=0, yuvarlak=0.12)
ax.text(ALT_X + ALT_W / 2, ALT_Y + ALT_H / 2, ALT_METIN, ha="center",
        va="center", fontsize=ALT_FS, color=LAC, zorder=3)

if "--kontrol" in sys.argv:
    raise SystemExit(1 if kontrol(fig, ax) else 0)

cikti = HEDEF / "diagram-intihal.png"
fig.savefig(cikti, dpi=200, facecolor="white")
plt.close(fig)
print(f"{cikti.relative_to(KOK)} üretildi")
