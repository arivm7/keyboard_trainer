#
# CP: windows-IBM866
# EOL: CRLF
#

cd output

pyinstaller -F --clean --name kb_trainer_smile ../main.py

echo "������� ../conf.json"
copy ..\conf.json dist\conf.json

echo "������� ../img"
xcopy /E ..\img dist\img\

echo "������� ../books"
xcopy /E ..\books dist\books\

echo "������� ../saves"
xcopy /E ..\saves dist\saves\

echo "����塞 �� ����⭮� � ��譥�..."
del kb_trainer_smile.spec
del /Q /S build
rmdir /S /Q build
ren dist kb_trainer_smile_win

echo "��"

cd ..


