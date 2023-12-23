@echo off
call pip install --user pipenv && pipenv --python 3.11 && pipenv install -r ./requirements.txt
pause