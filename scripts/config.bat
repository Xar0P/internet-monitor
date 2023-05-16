@echo off

cd ..
del .env
cls

echo Digite a velocidade minima de download aceitavel
@set /p MIN_DOWNLOAD=
echo MIN_DOWNLOAD=%MIN_DOWNLOAD% >> .env

echo Digite a velocidade minima de upload aceitavel
@set /p MIN_UPLOAD=
echo MIN_UPLOAD=%MIN_UPLOAD% >> .env