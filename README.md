# Automação de Gerador de Vídeos com Interface Web & CLI

Este projeto é uma aplicação completa em Python para automatizar a criação de vídeos em múltiplos formatos (**Vertical 9:16**, **Horizontal 16:9** e **Quadrado 1:1**) a partir de uma simples descrição de texto ou tema.

---

## 💻 Interface Web Interativa (Streamlit) e Terminal (CLI)

O projeto conta com **duas formas de uso**:
1. **Interface Web (Navegador/App)**: Painel interativo para preencher o tema, escolher o formato e baixar o arquivo final `.mp4`.
2. **Terminal (Linha de Comando)**: Execução direta por parâmetros de terminal.

---

## 🛠️ Como Funciona o Fluxo

1. **Entrada**: Você fornece o tema/detalhes do conteúdo e escolhe o formato (`9:16`, `16:9` ou `1:1`).
2. **Roteiro Dinâmico**: Gera um roteiro em formato de cenas curtas usando ChatGPT/OpenAI (com gerador inteligente de fallback caso não haja chave de API).
3. **Áudio e Narração**: Gera narração em voz neural hiper-realista com `edge-tts` (ou `gTTS`).
4. **Acervo de Vídeo B-roll**: Baixa vídeos de fundo em HD correspondentes a cada cena usando a API do Pexels (ou gera fundos de alta qualidade estilizados).
5. **Edição e Legendas**: Enquadra o vídeo no formato selecionado, alinha o áudio e aplica legendas dinâmicas em destaque.
6. **Saída**: Disponibiliza o arquivo `.mp4` para download na web ou grava na pasta local `output/`.

---

## 📋 Requisitos do Sistema (FFmpeg)

O sistema exige o **FFmpeg** instalado na máquina:

### Linux (Ubuntu/Debian):
```bash
sudo apt update && sudo apt install -y ffmpeg
```

### macOS (Homebrew):
```bash
brew install ffmpeg
```

---

## 📦 Instalação das Dependências

Instale todas as bibliotecas necessárias executando:

```bash
pip install -r requirements.txt
```

---

## 🌐 Executando a Interface Web (App no Navegador)

Para abrir a interface web no seu navegador:

```bash
streamlit run app.py
```

O aplicativo abrirá no seu navegador (geralmente em `http://localhost:8501`), permitindo:
- Digitar o tema/descrição do vídeo num campo de texto.
- Selecionar o nicho e formato (`9:16 TikTok/Shorts/Reels`, `16:9 YouTube`, `1:1 Instagram`).
- Escolher a voz do narrador.
- Inserir chaves de API opcionalmente.
- Assistir ao vídeo direto no navegador e fazer o download do `.mp4`.

---

## 🚀 Executando via Terminal (Linha de Comando)

Também é possível gerar vídeos via CLI:

```bash
# Vídeo Vertical (Shorts/TikTok - 9:16)
python3 generate_short.py --topic "Curiosidades do Espaço" --niche "Ciência" --format 9:16

# Vídeo Horizontal (YouTube - 16:9)
python3 generate_short.py --topic "Dicas de Finanças Pessoais" --niche "Finanças" --format 16:9 --output output/financas_yt.mp4
```

### Parâmetros do CLI:
- `--topic` / `-t`: Tema do vídeo.
- `--niche` / `-n`: Categoria ou nicho do conteúdo.
- `--format` / `-f`: Formato (`9:16`, `16:9`, `1:1`).
- `--output` / `-o`: Caminho do arquivo de saída `.mp4`.
- `--voice` / `-v`: Voz do narrador (ex: `pt-BR-AntonioNeural`, `pt-BR-FranciscaNeural`).
- `--lang` / `-l`: Idioma do roteiro e narração (`pt` ou `en`).
