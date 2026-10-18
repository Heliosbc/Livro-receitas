#!/usr/bin/env python3
"""
Shorts / TikTok Video Automation Generator
Flow: Description/Topic -> Script Generation -> TTS Narration -> B-roll Download -> MoviePy Video Assembly & Subtitles -> Output MP4
"""

import os
import argparse
import sys
import shutil
import tempfile
from script_generator import generate_script
from tts_generator import generate_audio
from video_fetcher import fetch_background_video
from video_editor import create_scene_clip, assemble_final_video


def build_short_video(topic: str, niche: str, output_path: str, voice: str = "pt-BR-AntonioNeural", language: str = "pt"):
    print("=" * 60)
    print(f"🎬 Iniciando a geração do vídeo curto...")
    print(f"📌 Tema: {topic}")
    print(f"📌 Nicho: {niche}")
    print(f"📌 Idioma: {language}")
    print(f"📌 Saída: {output_path}")
    print("=" * 60)

    # Step 1: Script Generation
    print("\n[Passo 1/5] Gerando Roteiro...")
    scenes = generate_script(topic=topic, niche=niche, language=language)
    print(f"✅ Roteiro gerado com {len(scenes)} cenas:")
    for scene in scenes:
        print(f"  - Cena {scene.get('scene_id')}: \"{scene.get('text')}\" [Busca: {scene.get('keyword')}]")

    temp_dir = tempfile.mkdtemp(prefix="short_gen_")
    scene_clips = []

    try:
        for idx, scene in enumerate(scenes, start=1):
            text = scene.get("text", "")
            keyword = scene.get("keyword", topic)

            print(f"\n[Passo 2 e 3/5] Processando Cena {idx}/{len(scenes)}...")

            # Step 2: TTS Audio Generation
            audio_path = os.path.join(temp_dir, f"scene_{idx}.mp3")
            generate_audio(text=text, output_path=audio_path, voice=voice, lang=language)

            # Step 3: Background Video Fetching
            bg_video_path = os.path.join(temp_dir, f"bg_{idx}.mp4")
            fetch_background_video(keyword=keyword, output_path=bg_video_path, target_duration=5.0)

            # Step 4: Scene Clip Assembly & Subtitle Overlay
            print(f"[Passo 4/5] Renderizando composição da cena {idx} com legendas...")
            clip = create_scene_clip(
                video_path=bg_video_path,
                audio_path=audio_path,
                narration_text=text
            )
            scene_clips.append(clip)

        # Step 5: Final Video Export
        print(f"\n[Passo 5/5] Renderizando vídeo final de todas as cenas unidas...")
        final_path = assemble_final_video(scene_clips, output_path)
        print("\n" + "=" * 60)
        print(f"🎉 VÍDEO GERADO COM SUCESSO! 🎉")
        print(f"📍 Salvo em: {os.path.abspath(final_path)}")
        print("=" * 60)

    finally:
        # Cleanup temporary files
        print("[Limpeza] Removendo arquivos temporários...")
        for c in scene_clips:
            try:
                c.close()
            except Exception:
                pass
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Automação de criação de vídeos verticais (Shorts/TikTok) por descrição de texto.")
    parser.add_argument("--topic", "-t", type=str, required=True, help="Tema ou assunto do vídeo (ex: 'Curiosidades sobre o Espaço')")
    parser.add_argument("--niche", "-n", type=str, default="Geral", help="Nicho do vídeo (ex: 'Ciência', 'Finanças', 'Fitness')")
    parser.add_argument("--output", "-o", type=str, default="output/short_video.mp4", help="Caminho do arquivo final (.mp4)")
    parser.add_argument("--voice", "-v", type=str, default="pt-BR-AntonioNeural", help="Voz TTS (padrão: pt-BR-AntonioNeural)")
    parser.add_argument("--lang", "-l", type=str, default="pt", help="Idioma do roteiro e narração (ex: 'pt', 'en')")

    args = parser.parse_args()
    build_short_video(
        topic=args.topic,
        niche=args.niche,
        output_path=args.output,
        voice=args.voice,
        language=args.lang
    )


if __name__ == "__main__":
    main()
