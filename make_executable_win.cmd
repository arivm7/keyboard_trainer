#
# CP: windows-1251
# EOL: CRLF
#

cd _tmp

pyinstaller -F --clean --name kb_training_smile ../main.py

echo "Копирую ../conf.json"
copy ..\conf.json dist\conf.json

echo "Копирую ../img"
xcopy /E ..\img dist\img\

echo "Копирую ../books"
xcopy /E ..\books dist\books\

echo "Копирую ../saves"
xcopy /E ..\saves dist\saves\

echo "Удаляем не понятное и лишнее..."
del kb_training_smile.spec
del /Q /S build
rmdir /S /Q build
ren dist kb_training_smile_win

echo "Ок"

cd ..


