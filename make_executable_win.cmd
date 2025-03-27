#
# CP: windows-1251
# EOL: CRLF
#

cd _tmp

pyinstaller -F --clean --name kb_training_smile ../main.py

echo "������� ../conf.json"
copy ..\conf.json dist\conf.json

echo "������� ../img"
xcopy /E ..\img dist\img\

echo "������� ../books"
xcopy /E ..\books dist\books\

echo "������� ../saves"
xcopy /E ..\saves dist\saves\

echo "������� �� �������� � ������..."
del kb_training_smile.spec
del /Q /S build
rmdir /S /Q build
ren dist kb_training_smile_win

echo "��"

cd ..


