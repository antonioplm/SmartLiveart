@echo off
echo ==========================================
echo  SLKB - Aggiunge informazioni da Wikipedia e Wikidata
echo ==========================================

python wiki_poi.py "cosenza"
if %errorlevel% neq 0 (
    echo ❌ Errore durante wiki_poi.py
    pause
    exit /b
)
echo Informazioni da Wikipedia e Wikidata completata.
echo.

pause
