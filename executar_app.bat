@echo off
echo ====================================================
echo   🚀 Iniciando Gerador de Vídeos Automáticos...
echo ====================================================

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nao foi encontrado no seu computador!
    echo Por favor, baixe e instale o Python em: https://www.python.org/
    pause
    exit /b
)

echo 📦 Verificando e instalando dependencias do projeto...
python -m pip install -r requirements.txt --quiet

echo.
echo 🌐 Abrindo o aplicativo no seu navegador...
python -m streamlit run app.py

pause
