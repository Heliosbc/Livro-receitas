# 🎬 Studio AI: Gerador de Vídeos Automáticos & Criador de Jogos TikTok Live

Este aplicativo completo permite:
1. **Gerar Vídeos Automáticos** (**TikTok/Shorts 9:16**, **YouTube 16:9** e **Instagram 1:1**) com inteligência artificial, voz realista e legendas.
2. **Criar Jogos Interativos para TikTok Live** apenas digitando uma descrição, conectando **comentários**, **curtidas** e **envio de presentes** com ações em tempo real dentro do jogo!

---

## 🖱️ Como Abrir o Aplicativo com 1 Clique

### 🪟 No Windows:
1. Dê **dois cliques** no arquivo **`executar_app.bat`**.
2. O aplicativo vai instalar as dependências e abrir a interface no navegador!

### 🍎 No Mac ou 🐧 Linux:
1. Execute no terminal:
   ```bash
   ./executar_app.sh
   ```
2. O navegador abrirá automaticamente com o aplicativo pronto para uso!

---

## 🎮 Criador de Jogos Interativos para TikTok Live

A aba **"Criador de Jogos TikTok Live"** transforma qualquer ideia digitada em um jogo interativo completo de alta taxa de quadros (60 FPS) pronto para transmissão ao vivo!

### 🕹️ Como Funciona a Interação na Live:
- 💬 **Comentários do Chat:** O público comenta palavras-chave (ex: `1`, `2`, `atacar`, `Flamengo`) para mover personagens, defender castelos, pontuar ou atacar o Chefão.
- ❤️ **Curtidas (Likes):** As curtidas acumuladas acionam impulso de velocidade (Nitro Boost), recarregam magias e aumentam multiplicadores.
- 🎁 **Envio de Presentes:** Enviar presentes (Rosa 🌹, TikTok 🎵, Donut 🍩, Universo 🌌) lança super habilidades, ataca castelos inimigos ou causa meteoros devastadores!

### 🎲 Tipos de Jogos Suportados:
- **🪢 Cabo de Guerra (Tug of War):** Batalhas entre duas equipes (ex: Flamengo vs Palmeiras, Cães vs Gatos).
- **🏎️ Corrida (Grand Prix):** Pistas com veículos ou animais avançando com os votos e nitro da Live.
- **🐲 Batalha de Chefão (Boss Battle):** Todo o chat unido contra um Monstro/Dragão com barra de vida e magias.
- **🏰 Defesa de Castelo (Castle Defense):** Guerra entre castelos destruídos por bombas de presentes.
- **🔮 Chuva de Esferas (Drop Balls):** Esferas físicas caindo em caixas multiplicadoras.

### 🎥 Como Transmitir no OBS Studio ou TikTok Live Studio:
1. No aplicativo, crie o jogo desejado.
2. Ative a opção **"Modo Transmissão OBS Clean"** para remover botões de teste se desejar a tela limpa.
3. No **OBS Studio** ou **TikTok Live Studio**, adicione uma fonte de **Captura de Janela (Window Capture)** ou **Navegador (Browser)** apontando para a tela do jogo.
4. Prontinho! Seu público poderá jogar ao vivo interativamente!

---

## 📱 Gerador de Vídeos Automáticos

1. **Descrição**: Digite o tema (ex: *"Curiosidades sobre Buracos Negros"*).
2. **Formato**: Escolha 9:16 (Vertical), 16:9 (YouTube) ou 1:1 (Instagram).
3. **Voz**: Escolha narração em Português ou Inglês.
4. **Clique em "Gerar Vídeo Agora"**: Assista e baixe o arquivo `.mp4` pronto.

---

## 📋 Pré-requisitos (FFmpeg)

O utilitário gratuito **FFmpeg** é necessário para a geração dos arquivos de vídeo `.mp4`.

- **Linux**: `sudo apt install -y ffmpeg`
- **Mac**: `brew install ffmpeg`
- **Windows**: Baixar no site oficial do FFmpeg.
