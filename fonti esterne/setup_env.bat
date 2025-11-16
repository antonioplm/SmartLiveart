@echo off
REM === Crea ambiente virtuale ===
python -m venv venv

REM === Attiva ambiente virtuale ===
call venv\Scripts\activate.bat

REM === Aggiorna pip ===
python -m pip install --upgrade pip

REM === Installa dipendenze ===
pip install -r requirements.txt

REM === Scarica modello SpaCy italiano ===
python -m spacy download it_core_news_sm

echo.
echo Ambiente pronto! Per attivare l'ambiente in futuro:
echo call venv\Scripts\activate.bat
pause
