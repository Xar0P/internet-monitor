@echo off

cd ..

mkdir reports
call env/Scripts/activate.bat
python main.py
PAUSE