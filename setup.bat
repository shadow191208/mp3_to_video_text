@echo off
echo ========================================
echo TAO MOI TRUONG AO VA CAI DAT THU VIEN
echo ========================================
echo.

echo 1. Tao thu muc venv...
python -m venv venv
if errorlevel 1 (
    echo Loi: Khong the tao venv. Vui long cai dat Python!
    pause
    exit /b
)

echo 2. Kich hoat moi truong ao...
call venv\Scripts\activate.bat

echo 3. Nang cap pip...
python -m pip install --upgrade pip

echo 4. Cai dat moviepy...
pip install moviepy==1.0.3

echo 5. Cai dat speechrecognition...
pip install speechrecognition

echo 6. Cai dat pydub...
pip install pydub

echo 7. Cai dat numpy...
pip install numpy

echo 8. Cai dat librosa...
pip install librosa

echo.
echo ========================================
echo CAI DAT HOAN TAT!
echo ========================================
echo.
echo De chay chuong trinh:
echo 1. Mo Command Prompt moi
echo 2. cd vao thu muc nay
echo 3. Chay: venv\Scripts\activate
echo 4. Chay: python Main.py
echo.
pause