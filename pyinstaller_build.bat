cls
del /F /Q ".\dist"
pyinstaller ^
  --clean ^
  --noconfirm ^
  --name "GuitarTabs2Notes" ^
  --add-data ".\data\config.yaml;.\data" ^
  --add-data ".\data\img\treble_clef.svg;.\data\img" ^
  --add-data ".\data\img\bass_clef.svg;.\data\img" ^
  --add-binary ".\data\font\BeautifulPeople.ttf;.\data\font" ^
  --add-binary ".\data\font\Countryside.ttf;.\data\font" ^
  --add-data ".\README.MD;." ^
  ".\main.py"
del /F /Q ".\GuitarTabs2Notes.spec"
del /F /Q ".\build"

:: .\dist\GuitarTabs2Notes\GuitarTabs2Notes.exe
