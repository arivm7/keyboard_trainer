#
# CP: windows-IBM866
# EOL: CRLF
#

cd output

pyinstaller -F --clean --name kb_trainer_smile ../main.py

echo "Копирую ../conf.json"
copy ..\conf.json dist\conf.json

echo "Копирую ../img"
xcopy /E ..\img dist\img\

echo "Копирую ../books"
xcopy /E ..\books dist\books\

echo "Копирую ../saves"
xcopy /E ..\saves dist\saves\

echo "Удаляем не понятное и лишнее..."
del kb_trainer_smile.spec
del /Q /S build
rmdir /S /Q build
ren dist kb_trainer_smile_win

echo "Ок"

cd ..


