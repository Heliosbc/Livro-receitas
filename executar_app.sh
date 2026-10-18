#!/usr/bin/env bash
echo "===================================================="
echo "  🚀 Iniciando Gerador de Vídeos Automáticos..."
echo "===================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 não foi encontrado no seu computador."
    echo "Por favor, baixe e instale o Python em: https://www.python.org/"
    exit 1
fi

echo "📦 Verificando e instalando dependências necessárias..."
python3 -m pip install -r requirements.txt --quiet

echo ""
echo "🌐 Abrindo o aplicativo no seu navegador..."
python3 -m streamlit run app.py
