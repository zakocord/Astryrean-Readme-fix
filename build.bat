@echo off

pip uninstall -r interact.txt
pip install -r requirements.txt
py build/build.py
