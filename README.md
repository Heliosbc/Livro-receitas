# Automação de Vídeos Verticais (YouTube Shorts / TikTok / Reels)

Este projeto é um script em Python completo para automatizar a criação de vídeos verticais (formato 9:16) a partir de uma simples descrição de texto ou tema.

---

## 🛠️ Como Funciona o Fluxo

1. **Entrada**: Forneça o tema/descrição e o nicho do vídeo no terminal.
2. **Roteiro Dinâmico**: Usa a API da OpenAI (ou um gerador estruturado automático de fallback) para criar um roteiro curto dividido em cenas.
3. **Áudio / Narração Realista**: Converte o texto em voz usando `edge-tts` (vozes neurais hiper-realistas) ou `gTTS`.
4. **B-roll Visuais**: Baixa vídeos de fundo em formato vertical (9:16) da API do Pexels baseando-se nas palavras-chave do roteiro (ou gera telas de fundo estilizadas caso não haja chave de API).
5. **Edição e Legendas Automáticas**: Utiliza a biblioteca `MoviePy` e `Pillow` para recortar/formatar vídeos em 1080x1920, sincronizar o áudio da narração e aplicar legendas estilizadas centralizadas na tela.
6. **Saída**: Salva o arquivo final `.mp4` na pasta de saída (padrão: `output/short_video.mp4`).

---

## 📋 Requisitos Pré-requisitos do Sistema

Certifique-se de ter instalado no seu sistema operacional:
- **Python 3.10+**
- **FFmpeg** e **ImageMagick**

### Instalando dependências do sistema:

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install -y ffmpeg imagemagick
```

#### macOS (Homebrew):
```bash
brew install ffmpeg imagemagick
```

---

## 📦 Instalação das Bibliotecas Python

No seu terminal, clone o repositório ou navegue até a pasta do projeto e instale as dependências executando:

```bash
pip install -r requirements.txt
```

As bibliotecas instaladas incluem:
- `moviepy` (edição e composição de vídeo)
- `edge-tts` / `gTTS` (conversão de texto para voz)
- `requests` (download de vídeos B-roll)
- `pillow` (renderização e estilo das legendas)
- `openai` (geração de roteiro com IA)

---

## 🔑 Configuração de Chaves de API (Opcional)

O script funciona **100% de forma autônoma mesmo sem chaves de API**, utilizando geradores e backgrounds de fallback. Para potencializar a geração automática com inteligência artificial e vídeos de acervo reais:

Configure as seguintes variáveis de ambiente no seu terminal:

```bash
# Para gerar roteiros via ChatGPT/OpenAI:
export OPENAI_API_KEY="sua_chave_openai_aqui"

# Para baixar vídeos HD B-roll do Pexels:
export PEXELS_API_KEY="sua_chave_pexels_aqui"
```

---

## 🚀 Como Executar no Terminal

Para gerar um vídeo, basta executar o script `generate_short.py` passando o tema e o nicho do vídeo.

### Exemplo Simples:
```bash
python3 generate_short.py --topic "Curiosidades sobre o Espaço" --niche "Ciência"
```

### Exemplo Completo com Caminho de Saída e Voz Personalizada:
```bash
python3 generate_short.py \
  --topic "Como economizar dinheiro investindo" \
  --niche "Finanças" \
  --output "output/financas_investimento.mp4" \
  --voice "pt-BR-AntonioNeural" \
  --lang "pt"
```

### Parâmetros Disponíveis:
- `--topic` / `-t`: (Obrigatório) O tema ou descrição do vídeo.
- `--niche` / `-n`: O nicho do conteúdo (ex: `Ciência`, `Finanças`, `Tecnologia`, `Fitness`).
- `--output` / `-o`: Onde salvar o arquivo final `.mp4` (padrão: `output/short_video.mp4`).
- `--voice` / `-v`: A voz neural para narração (ex: `pt-BR-AntonioNeural`, `pt-BR-FranciscaNeural`).
- `--lang` / `-l`: Idioma do roteiro e narração (`pt` para português, `en` para inglês).

---

## 📁 Estrutura do Projeto

```
.
├── generate_short.py   # CLI e fluxo principal de automação
├── script_generator.py # Módulo de geração de roteiro (OpenAI / Fallback)
├── tts_generator.py    # Módulo de conversão de texto para voz (Edge-TTS / gTTS)
├── video_fetcher.py    # Módulo de busca e download de B-roll (Pexels / Canvas)
├── video_editor.py     # Módulo de edição, enquadramento 9:16 e legendas (MoviePy)
├── requirements.txt    # Lista de bibliotecas necessárias
└── README.md           # Guia de uso e documentação em português
```
