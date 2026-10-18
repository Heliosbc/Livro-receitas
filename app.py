import os
import streamlit as st
import tempfile
from generate_short import build_short_video

st.set_page_config(
    page_title="Gerador de Vídeos Automáticos",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Gerador de Vídeos Automáticos com IA")
st.markdown("Crie vídeos completos (Shorts, Reels, TikTok ou YouTube) a partir de uma simples descrição de texto!")

st.sidebar.header("🔑 Configurações de API (Opcional)")
openai_key_input = st.sidebar.text_input("OpenAI API Key (Roteiros IA)", type="password", value=os.getenv("OPENAI_API_KEY", ""))
pexels_key_input = st.sidebar.text_input("Pexels API Key (Vídeos B-roll)", type="password", value=os.getenv("PEXELS_API_KEY", ""))

if openai_key_input:
    os.environ["OPENAI_API_KEY"] = openai_key_input
if pexels_key_input:
    os.environ["PEXELS_API_KEY"] = pexels_key_input

st.sidebar.markdown("---")
st.sidebar.info("💡 **Dica:** O sistema funciona perfeitamente com roteiros estruturados e fundos visuais mesmo sem chaves de API!")

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
