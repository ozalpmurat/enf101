# Windows'ta ENF101 deposu — kurulum komutları

PowerShell'de çalıştırın. Yönetici yetkisi gerekmez.

## 1. Git ve Quarto

```powershell
winget install --id Git.Git -e
winget install --id Posit.Quarto -e
```

Kurduktan sonra terminali kapatıp yeniden açın (PATH güncellenir).
`winget` yoksa Quarto'yu <https://quarto.org/docs/download/> adresinden
`quarto-...-win.msi` indirip çift tıklayarak kurun.

## 2. Depoyu alın

OneDrive'ın eşitlediği bir klasöre **açmayın** (derleme sırasında dosyalar kilitlenebilir).

```powershell
cd $HOME\Documents
git clone https://github.com/ozalpmurat/enf101.git
cd enf101
```

## 3. PDF motoru (bir kez, ~400-500 MB)

```powershell
quarto install tinytex
```

## 4. Şemalar için Chrome (isteğe bağlı)

Yalnızca `ornekler/` klasöründeki Mermaid/Graphviz belgeleri için gerekir.

```powershell
quarto install chrome-headless-shell
```

## 5. Doğrulama

```powershell
quarto --version
git --version
```

## 6. Derleme

```powershell
quarto render hafta-01-giris-temel-kavramlar
```

Altbilgi düzeltmesini de yapan sarmalayıcı (Git Bash gerekir):

```bash
bash araclar/derle.sh hafta-01-giris-temel-kavramlar
```

Git Bash'i açıp depo klasörüne girmek için:

```bash
cd /c/Users/<kullanıcı>/Documents/enf101
```

## Notlar

- Tam TeX Live (TinyTeX değil) kullanacaksanız `fontawesome5` paketi de kurulu olmalı; TinyTeX ile birlikte
  gelir. Paket yoksa belgeler derlenmez (`File 'fontawesome5.sty' not found`) ve `araclar/derle.sh`
  altbilgiyi düzeltemez. Kurmak için:

  ```powershell
  tlmgr install fontawesome5
  ```

  Debian/Ubuntu'daki TeX Live karşılığı: `sudo apt install texlive-fonts-extra`.
- Dosya/klasör adlarında Türkçe karakter kullanmayın (depodaki adlar zaten uygundur).
