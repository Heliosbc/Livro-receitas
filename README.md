# 🎬 Gerador de Vídeos Automáticos com IA

Este aplicativo permite criar vídeos completos (**TikTok/Shorts 9:16**, **YouTube 16:9** e **Instagram 1:1**) apenas digitando uma descrição ou tema do conteúdo!

---

## 🖱️ Como Abrir o Aplicativo com 1 Clique (Sem Precisar Saber Programar!)

Para facilitar o seu uso, foram criados executadores automáticos:

### 🪟 No Windows:
1. Abra a pasta do projeto.
2. Dê **dois cliques** no arquivo **`executar_app.bat`**.
3. O aplicativo vai instalar tudo sozinho e abrir a tela do aplicativo diretamente no seu navegador de internet!

### 🍎 No Mac ou 🐧 Linux:
1. Dê **dois cliques** ou execute no terminal o arquivo **`executar_app.sh`**:
   ```bash
   ./executar_app.sh
   ```
2. O navegador abrirá automaticamente com o aplicativo pronto para uso!

---

## 📱 Como Usar a Interface do Aplicativo

Quando o aplicativo abrir no seu navegador:

1. **Campo de Texto**: Digite sobre o que você quer que o vídeo seja (ex: *"Curiosidades sobre o universo e buracos negros"*).
2. **Formato**: Escolha se deseja um vídeo **Vertical (TikTok/Shorts/Reels)**, **Horizontal (YouTube)** ou **Quadrado**.
3. **Voz do Narrador**: Escolha a voz masculina ou feminina em Português.
4. **Clique em "Gerar Vídeo Agora"**:
   - O aplicativo vai escrever o roteiro, gravar a narração, escolher os vídeos de fundo e colocar legendas bonitas na tela.
   - Quando terminar, você pode **assistir ao vídeo na própria tela** e clicar no botão **"Baixar Arquivo MP4"** para salvar no seu computador!

---

## 📋 Pré-requisito Único (FFmpeg)

Para que o computador consiga unir o som e a imagem no arquivo final `.mp4`, o programa precisa do utilitário gratuito **FFmpeg** instalado no seu computador.

- **Linux**: `sudo apt install -y ffmpeg`
- **Mac**: `brew install ffmpeg`
- **Windows**: Baixar o FFmpeg pelo site oficial ou instalador rápido.
