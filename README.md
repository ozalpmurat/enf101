# ENF101 — Temel Bilgi Teknolojileri Ders Materyali

Bilecik Şeyh Edebali Üniversitesi'nde tüm fakültelerin 1. sınıf öğrencilerine verilen
**ENF101 Temel Bilgi Teknolojileri** dersi için hazırlanmış, 14 haftalık ders materyali.
İçerik Türkçedir.

Materyal [Quarto](https://quarto.org) ile üretilir. Depoda hem kaynak (`.qmd`, `.tex`) hem de
üretilmiş **PDF** çıktıları birlikte tutulur.

## PDF'leri indirme (git gerekmez)

Bütün PDF'ler tek bir ZIP dosyasında toplanır. ZIP **elle çıkarılan sürümlerle** yenilenir; aşağıdaki bağlantı her zaman en son çıkarılan sürümü gösterir:

**[enf101-pdf.zip](https://github.com/ozalpmurat/enf101/releases/download/pdf/enf101-pdf.zip)**

İçinde 14 haftanın ders notu, sunum ve alıştırma PDF'leri; ayrıca izlence, başlık listesi ve ders
kılavuzu. (`ornekler/` klasöründeki Quarto başvuru belgeleri ders içeriği sayılmadığı için ZIP'e alınmaz.)
Dosyalar hafta klasörlerine göre düzenlenmiştir, yani ZIP'i açtığınızda `hafta-01/ders-notu.pdf` gibi bir
yapı görürsünüz. Git, terminal veya hesap gerekmez.

Yalnızca PDF'leri git ile indirmek isterseniz (klasör yapısı korunur):

```bash
git clone --filter=blob:none --sparse https://github.com/ozalpmurat/enf101.git
cd enf101
git sparse-checkout set --no-cone '*.pdf'
```

## İçerik

- **`izlence.qmd` / `izlence.pdf`** — ders izlencesi.
- **`BASLIKLAR.qmd` / `BASLIKLAR.pdf`** — 14 haftanın **ders notu** başlıklarının bir arada görünümü (içerik haritası). Elle düzenlenmez; `araclar/basliklari-uret.py` betiğiyle üretilir.
- **`hafta-NN/`** — her haftanın paketi: `ders-notu.qmd`+`.pdf`, `sunum.qmd`+`.pdf`,
  `alistirma.qmd`+`.pdf` ve `gorseller/` klasörü (NN = 01 … 14).
- **`tema/notlar.tex` ve `tema/sunum.tex`** — ders notu ve sunumun ortak görünüm dosyaları.
- **`ornekler/`** — Quarto özelliklerine ilişkin başvuru belgeleri (ders içeriği değildir).
- **`KILAVUZ_Quarto_Kurulum_ve_Kullanim.qmd` / `.pdf`** — Quarto kurulum ve kullanım kılavuzu.
- **`AGENTS.md`** — proje kuralları, üretim talimatları ve geçmiş hatalardan çıkarılan uyarılar.

**Katkı yapmadan veya üretim komutunu çalıştırmadan önce `AGENTS.md` okunmalıdır.** Klasörün nasıl
derlendiği, hangi dosyalara dokunulmaması gerektiği ve hangi tuzaklara düşülmemesi gerektiği orada yazılıdır.

## Gereksinimler

- **Quarto** — güncel sürüm ([quarto.org/docs/download](https://quarto.org/docs/download))
- **XeLaTeX / TeX Live** — güncel sürüm (`quarto install tinytex`)
- Mermaid veya Graphviz şemaları PDF'e gömülecekse **Chrome Headless**
  (`quarto install chrome-headless-shell`)

**Sürüm sabitlenmez.** Güncel Quarto ve TeX kullanılır; hangi sürüm kuruluysa onun ürettiği çıktı
esas alınır. PDF çıktısı sürüme göre ufak görsel farklar gösterebilir (örneğin madde imi glifleri);
bu kadarı sorun sayılmaz.

**Esas olan kaynaktır:** ölçüt, `.qmd` dosyalarının düzgün derlenmesidir. PDF'ler onlardan üretilen
çıktılardır ve gerektiğinde yeniden üretilir; sürüm yükseltmesinde hepsini birden yenilemek gerekmez.

## Derleme

Proje kökünde:

```bash
quarto render hafta-03        # bir haftanın üç belgesini üretir
quarto render izlence.qmd     # tek dosya
```

`quarto render` yalnızca **tek yol** alır; `quarto render hafta-01 hafta-03` çalışmaz. Tüm projeyi
tek komutta derlemek uzun sürdüğü için hafta hafta derlemek gerekir. Ayrıntı: `AGENTS.md`.

## PDF'ler hakkında

PDF'ler aslında birer derleme çıktısıdır, ama bu depoda bilinçli olarak takip edilir: böylece
Quarto/TeX kurulu olmayan hocalar depoyu indirip PDF'leri doğrudan kullanabilir. Bir kaynağı
düzenlediğinizde, yeniden ürettiğiniz PDF'i de aynı commit'te göndermeniz iyi olur — ama bu bir
zorunluluk değil; kaynak her zaman esas alınır.
`.gitattributes` PDF'leri ikili dosya olarak işaretler; Git bunlar üzerinde satır satır fark almaya çalışmaz.

## Katkı

1. Depoyu forklayın ya da bir dal (branch) açın.
2. Hafta bazında çalışın; bir haftayı düzenlerken diğer haftaları etkilemeyin.
3. Düzenlediğiniz `.qmd` dosyasını ve yeniden ürettiğiniz ilgili PDF'i birlikte commit'leyin.
4. `tema/` altındaki dosyalar kritiktir; silmeyin, taşımayın, adını değiştirmeyin (AGENTS.md §4).
5. Göndermeden önce `AGENTS.md`'nin sonundaki teslim öncesi doğrulama listesini çalıştırın.

## GitHub'a yükleme

```bash
git init -b main
git add -A
git commit -m "İlk sürüm: ENF101 ders materyali"
git remote add origin <depo-adresi>
git push -u origin main
```

## Lisans

Depoda henüz bir lisans dosyası yoktur. Materyalin başka kurum ve hocalarca kullanılıp
düzenlenebilmesi amaçlandığından, uygun bir lisans (örneğin eğitim içerikleri için **CC BY-SA**)
seçilip `LICENSE` dosyası eklenmesi önerilir. Bu, yeniden kullanım koşullarını netleştirir.
