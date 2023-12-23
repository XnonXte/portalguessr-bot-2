@echo off
call pip install --user pipenv && pipenv install -r ./requirements.txt
pause