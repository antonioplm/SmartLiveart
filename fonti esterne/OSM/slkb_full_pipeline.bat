@echo off
setlocal enabledelayedexpansion

REM ==========================================================
REM  SLKB - Pipeline completa: OSM → Quartieri → Indirizzi → Nome POI
REM ==========================================================

REM === PARAMETRO CITTA' ===
if "%~1"=="" (
    echo ERRORE: devi specificare la citta', es.:
    echo     slkb_full_pipeline.bat "Napoli"
    pause
    exit /b
)

set CITY=%~1
set CITY_SLUG=%CITY%
set CITY_SLUG=%CITY_SLUG: =_%

REM === OPZIONALI: MAX_POI e FILTER_ONLY_WITH_LINKS ===
REM default se non passati: MAX_POI=0 (nessun limite), FILTER_ONLY_WITH_LINKS=0 (False)
set MAX_POI=0
set FILTER_ONLY_WITH_LINKS=0
if NOT "%~2"=="" set MAX_POI=%~2
if NOT "%~3"=="" set FILTER_ONLY_WITH_LINKS=%~3

REM === FILE DI OUTPUT ===
set FILE_OSM_POI=%CITY_SLUG%_osm_poi.json
set FILE_NEIGHBORHOOD=%CITY_SLUG%_neighborhood.json
set FILE_OSM_ADDRESS=%CITY_SLUG%_osm_address.json
set FILE_OSM_POI_NAME=%CITY_SLUG%_osm_poi_name.json

REM === STEP 1: POI ===
echo ==========================================
echo     SLKB - Generazione POI da OSM (%CITY%)...
echo ==========================================
python osm_poi.py "%CITY%" %MAX_POI% %FILTER_ONLY_WITH_LINKS%
if %errorlevel% neq 0 (
    echo ERRORE durante osm_to_slkb.py
    pause
    exit /b
)
if not exist "%FILE_OSM_POI%" (
    echo ATTENZIONE: File di output mancante: %FILE_OSM_POI%
    pause
    exit /b
)
echo OK: POI generati correttamente.
echo.

REM === STEP 2: Quartieri ===
echo ==========================================
echo     SLKB - Generazione Quartieri da OSM (%CITY%)...
echo ==========================================
python osm_neighborhood.py "%CITY%"
if %errorlevel% neq 0 (
    echo ERRORE durante generate_quartieri.py
    pause
    exit /b
)
if not exist "%FILE_NEIGHBORHOOD%" (
    echo ATTENZIONE: File di output mancante: %FILE_NEIGHBORHOOD%
    pause
    exit /b
)
echo OK: Quartieri generati.
echo.

REM === STEP 3: Indirizzi ===
echo ======================================================
echo     SLKB - Arricchimento con indirizzi e quartieri (%CITY%)...
echo ======================================================
python osm_poi_address.py "%CITY%" --no-cache
if %errorlevel% neq 0 (
   echo ERRORE durante enrich_osm_poi.py
   pause
   exit /b
)
if not exist "%FILE_OSM_ADDRESS%" (
    echo ATTENZIONE: File di output mancante: %FILE_OSM_ADDRESS%
    pause
    exit /b
)
echo OK: Arricchimento indirizzi completato.
echo.

REM === STEP 4: Specifica nomi ===
echo ==========================================
echo     SLKB - Specifica dei nomi POI (%CITY%)...
echo ==========================================
python osm_names.py "%CITY%"
if %errorlevel% neq 0 (
    echo ERRORE durante clean_osm_names.py
    pause
    exit /b
)
if not exist "%FILE_OSM_POI_NAME%" (
    echo ATTENZIONE: File di output mancante: %FILE_OSM_POI_NAME%
    pause
    exit /b
)
echo OK: Specifica nomi completata.
echo.

echo ==========================================
echo  OK: Pipeline completata con successo per %CITY%
echo ==========================================
pause
exit /b
