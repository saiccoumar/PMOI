@echo off
echo Welcome to PMOI, Putta Mask On It

@REM Get PIP and install
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

@REM Run PIP
python get-pip.py

@REM Install PIP requirements
pip install -r requirements.txt

@REM Run PMOI!
@REM If "imutils" or similar module is not found, you may have multiple installations of Python. Change python to python3
python app.py

@pause