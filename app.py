import os
import json
import streamlit as st
import streamlit.components.v1 as components
from generate_short import build_short_video
from game_generator import generate_game_config, SUPPORTED_GAME_TYPES
from tiktok_game_engine import render_tiktok_game_html

st.set_page_config(
    page_title="Studio TikTok AI - Vídeos & Jogos Interativos",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Studio de Criação para TikTok & Redes Sociais")
st.markdown("Crie **vídeos automáticos** e **jogos interativos em tempo real para TikTok Live** usando Inteligência Artificial!")

st.sidebar.header("🔑 Configurações de API (Opcional)")
openai_key_input = st.sidebar.text_input("OpenAI API Key (Roteiros & Jogos IA)", type="password", value=os.getenv("OPENAI_API_KEY", ""))
pexels_key_input = st.sidebar.text_input("Pexels API Key (Vídeos B-roll)", type="password", value=os.getenv("PEXELS_API_KEY", ""))

if openai_key_input:
    os.environ["OPENAI_API_KEY"] = openai_key_input
if pexels_key_input:
    os.environ["PEXELS_API_KEY"] = pexels_key_input

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica:** O sistema possui geradores heurísticos e funciona perfeitamente mesmo sem chaves de API!")

# Create Main Navigation Tabs
tab_videos, tab_games = st.tabs(["🎬 Gerador de Vídeos Automáticos", "🎮 Criador de Jogos TikTok Live"])

# ==============================================================================
# TAB 1: GERADOR DE VÍDEOS AUTOMÁTICOS
# ==============================================================================
with tab_videos:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📌 Detalhes do Vídeo")
        topic = st.text_area(
            "Tema / Descrição Curta do Vídeo:",
            placeholder="Ex: Curiosidades impressionantes sobre Buracos Negros no universo",
            height=100
        )

        niche = st.text_input("Nicho / Categoria:", value="Ciência e Tecnologia")

        format_choice = st.selectbox(
            "Formato do Vídeo:",
            options=["9:16", "16:9", "1:1"],
            format_func=lambda x: {
                "9:16": "📱 Vertical 9:16 (TikTok / Shorts / Reels)",
                "16:9": "🖥️ Horizontal 16:9 (YouTube Padrão)",
                "1:1": "🔲 Quadrado 1:1 (Instagram Feed / Posts)"
            }[x]
        )

        voice_choice = st.selectbox(
            "Voz do Narrador (TTS):",
            options=[
                "pt-BR-AntonioNeural",
                "pt-BR-FranciscaNeural",
                "pt-BR-ThalitaNeural",
                "pt-BR-ManuelaNeural",
                "en-US-GuyNeural",
                "en-US-JennyNeural"
            ],
            format_func=lambda x: {
                "pt-BR-AntonioNeural": "🇧🇷 Antônio (Masculina - PT-BR)",
                "pt-BR-FranciscaNeural": "🇧🇷 Francisca (Feminina - PT-BR)",
                "pt-BR-ThalitaNeural": "🇧🇷 Thalita (Feminina - PT-BR)",
                "pt-BR-ManuelaNeural": "🇧🇷 Manuela (Feminina - PT-BR)",
                "en-US-GuyNeural": "🇺🇸 Guy (Masculina - EN-US)",
                "en-US-JennyNeural": "🇺🇸 Jenny (Feminina - EN-US)"
            }.get(x, x)
        )

        lang_choice = "pt" if "pt-BR" in voice_choice else "en"

        generate_btn = st.button("🚀 Gerar Vídeo Agora", type="primary", use_container_width=True)

    with col2:
        st.subheader("📺 Pré-visualização & Resultado")

        if generate_btn:
            if not topic.strip():
                st.error("Por favor, digite um tema ou descrição para o vídeo!")
            else:
                with st.spinner("🎬 Gerando roteiro, áudio, vídeos de fundo e montando o vídeo... Por favor aguarde..."):
                    output_dir = "output"
                    os.makedirs(output_dir, exist_ok=True)
                    output_filepath = os.path.join(output_dir, "web_generated_video.mp4")

                    try:
                        build_short_video(
                            topic=topic,
                            niche=niche,
                            output_path=output_filepath,
                            format_ratio=format_choice,
                            voice=voice_choice,
                            language=lang_choice
                        )

                        st.success("🎉 Vídeo gerado com sucesso!")

                        if os.path.exists(output_filepath):
                            with open(output_filepath, "rb") as file:
                                video_bytes = file.read()
                                st.video(video_bytes)

                                st.download_button(
                                    label="⬇️ Baixar Arquivo MP4",
                                    data=video_bytes,
                                    file_name="meu_video_gerado.mp4",
                                    mime="video/mp4",
                                    use_container_width=True
                                )
                    except Exception as e:
                        st.error(f"Ocorreu um erro durante a geração do vídeo: {e}")
        else:
            st.info("Preencha as informações ao lado e clique em **Gerar Vídeo Agora** para visualizar o resultado aqui.")


# ==============================================================================
# TAB 2: CRIADOR DE JOGOS INTERATIVOS TIKTOK LIVE
# ==============================================================================
with tab_games:
    st.subheader("🎮 Criador de Jogos Interativos para TikTok Live")
    st.markdown("""
    Crie jogos completos interativos para suas Lives no TikTok apenas descrevendo a sua ideia!

    ✨ **Ações Interativas Integradas:**
    - 💬 **Comentários do Chat:** Palavras ou números acionam movimentos, ataques e pontos para as equipes.
    - ❤️ **Curtidas (Likes):** Tapping de curtidas gera aceleração, nitro boost e recarga de energia.
    - 🎁 **Envio de Presentes:** Presentes (Rosa, TikTok, Donut, Universo) ativam super habilidades, tempestades de ataques e reviravoltas no jogo!
    """)

    col_g1, col_g2 = st.columns([1, 1.2])

    with col_g1:
        st.markdown("### 📝 Configurar Novo Jogo")
        game_prompt = st.text_area(
            "Descreva como deseja o seu jogo:",
            value="Uma batalha de Cabo de Guerra de Flamengo vs Palmeiras onde o presente de Rosa dá super puxão e curtidas dão turbo!",
            placeholder="Ex: Corrida de carros onde comente 1 para vermelho e 2 para azul. Presentes soltam bombas na pista...",
            height=120
        )

        with st.expander("⚙️ Opções Avançadas & Estilo do Jogo", expanded=False):
            game_type_override = st.selectbox(
                "Mecânica Principal:",
                options=["Automático (IA)", "tug_of_war", "race", "boss_battle", "castle_defense", "drop_balls"],
                format_func=lambda x: {
                    "Automático (IA)": "🤖 Automático (Identificar pela descrição)",
                    "tug_of_war": "🪢 Cabo de Guerra (Time A vs Time B)",
                    "race": "🏎️ Corrida de Pilotos / Pista",
                    "boss_battle": "🐲 Batalha de Chefão (Chat vs Monstro)",
                    "castle_defense": "🏰 Defesa de Castelo / Torres",
                    "drop_balls": "🔮 Chuva de Esferas Multiplicadoras"
                }.get(x, x)
            )

            obs_mode = st.checkbox("🎥 Modo Transmissão OBS Clean (Ocultar painel de simulação)", value=False)

        create_game_btn = st.button("🚀 Criar Jogo com IA Agora", type="primary", use_container_width=True)

        st.markdown("---")
        st.markdown("### 📂 Importar / Exportar Configuração")
        uploaded_json = st.file_uploader("Carregar arquivo .json de jogo salvo:", type=["json"])
        if uploaded_json is not None:
            try:
                loaded_cfg = json.load(uploaded_json)
                st.session_state["active_game_config"] = loaded_cfg
                st.success("✅ Jogo carregado do arquivo JSON!")
            except Exception as ex:
                st.error(f"Erro ao ler arquivo JSON: {ex}")

    with col_g2:
        st.markdown("### 📺 Tela do Jogo Live (OBS / TikTok Live Studio Ready)")

        # Handle Game Generation Logic
        if create_game_btn:
            if not game_prompt.strip():
                st.error("Por favor, digite uma descrição para criar o jogo!")
            else:
                with st.spinner("🎮 Gerando regras, entidades, gráficos e conexões de eventos do TikTok Live..."):
                    try:
                        game_cfg = generate_game_config(game_prompt)
                        if game_type_override != "Automático (IA)":
                            game_cfg["game_type"] = game_type_override

                        st.session_state["active_game_config"] = game_cfg
                        st.success(f"🎉 Jogo '{game_cfg.get('title')}' criado com sucesso!")
                    except Exception as err:
                        st.error(f"Erro ao criar jogo: {err}")

        # Render Active Game Canvas
        if "active_game_config" in st.session_state and st.session_state["active_game_config"]:
            active_cfg = st.session_state["active_game_config"]

            # Display Game Details Expander
            with st.expander("🔍 Mapeamento de Eventos (Comentários, Curtidas, Presentes)", expanded=False):
                st.json(active_cfg)

            # Render HTML Canvas Game
            game_html = render_tiktok_game_html(active_cfg, show_controls=not obs_mode)
            components.html(game_html, height=800, scrolling=True)

            # Download JSON button
            st.download_button(
                label="💾 Baixar Arquivo JSON do Jogo",
                data=json.dumps(active_cfg, indent=2, ensure_ascii=False),
                file_name=f"{active_cfg.get('game_id', 'game')}_config.json",
                mime="application/json",
                use_container_width=True
            )
        else:
            st.info("💡 Digite a descrição do jogo ao lado e clique em **Criar Jogo com IA Agora** para iniciar!")
