@echo off
REM ============================================
REM Setup ambiente virtuale Python per il progetto
REM ============================================

REM --- Crea ambiente virtuale solo se non esiste ---
if not exist "venv" (
    echo Creazione ambiente virtuale...
    python -m venv venv
) else (
    echo Ambiente virtuale già presente.
)

REM --- Attiva ambiente virtuale ---
call venv\Scripts\activate.bat

REM --- Aggiorna pip ---
python -m pip install --upgrade pip

REM --- Installa tutte le dipendenze dal requirements.txt ---
if exist requirements.txt (
    echo Installazione dipendenze da requirements.txt...
    pip install -r requirements.txt
) else (
    echo ATTENZIONE: file requirements.txt non trovato!
)

REM --- Scarica modello SpaCy italiano ---
python -m spacy download it_core_news_sm

echo.
echo ============================================
echo Ambiente pronto! Il venv è attivo.
echo Puoi ora eseguire i tuoi script Python:
echo python "Popolamento da ARCO.py"
echo.
echo Per uscire dal venv: deactivate
echo ============================================
cmd /k
