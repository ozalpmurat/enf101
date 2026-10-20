# 7. hafta: ders notunun üst ve alt bilgisini gösteren ÖRNEK görsel.
# Görsel, 07-ders-notu.pdf'in ikinci sayfasından bir kez kırpılmıştır; canlı bir
# kopya değildir. Sayfa numarası gibi değerlerin güncel kalması beklenmez.
# Yalnızca notun tasarımı belirgin biçimde değişirse yeniden üretilir.
# Kullanım: python3 diyagram_betikleri/ekran-ders-notu-bilgi.py
# Çıktı:    hafta-07-kelime-islemci/gorseller/ekran-ders-notu-bilgi.png

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

KOK = Path(__file__).resolve().parent.parent
PDF = KOK / "hafta-07-kelime-islemci" / "07-ders-notu.pdf"
HEDEF = KOK / "hafta-07-kelime-islemci" / "gorseller"

DPI = 200
MM = DPI / 25.4          # 1 mm = 7,87 px
SAYFA = 2
UST_MM = 26              # üst şerit yüksekliği
ALT_MM = 20              # alt şerit yüksekliği
ARA_MM = 3               # iki şerit arasındaki boşluk


def main():
    if not PDF.exists():
        raise SystemExit(f"PDF bulunamadı: {PDF}")

    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            ["pdftoppm", "-r", str(DPI), "-f", str(SAYFA), "-l", str(SAYFA), "-png",
             str(PDF), str(Path(td) / "sayfa")],
            check=True,
        )
        dosyalar = sorted(Path(td).glob("sayfa*.png"))
        if not dosyalar:
            raise SystemExit("sayfa görüntüsü üretilemedi")
        tam = Image.open(dosyalar[0]).convert("RGB")

    W, H = tam.size
    ust = tam.crop((0, 0, W, int(UST_MM * MM)))
    alt = tam.crop((0, H - int(ALT_MM * MM), W, H))

    ara = int(ARA_MM * MM)
    yeni = Image.new("RGB", (W, ust.size[1] + ara + alt.size[1]), "white")
    yeni.paste(ust, (0, 0))
    yeni.paste(alt, (0, ust.size[1] + ara))

    cikti = HEDEF / "ekran-ders-notu-bilgi.png"
    yeni.save(cikti, dpi=(DPI, DPI))
    print(f"{cikti.relative_to(KOK)} üretildi ({yeni.size[0]}×{yeni.size[1]} px)")


if __name__ == "__main__":
    main()
