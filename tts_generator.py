import os
import asyncio
from gtts import gTTS

try:
    import edge_tts
except ImportError:
    edge_tts = None


async def _generate_edge_tts(text: str, output_path: str, voice: str = "pt-BR-AntonioNeural"):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)


def generate_audio(text: str, output_path: str, voice: str = "pt-BR-AntonioNeural", lang: str = "pt") -> str:
    """
    Generates an audio file from text using Edge-TTS (high quality neural voice) or gTTS (fallback).
    Returns path to created audio file.
    """
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

    if edge_tts is not None:
        try:
            asyncio.run(_generate_edge_tts(text, output_path, voice=voice))
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"[Audio] Áudio (edge-tts) gerado com sucesso: {output_path}")
                return output_path
        except Exception as e:
            print(f"[Aviso] Falha ao gerar áudio com edge-tts ({e}). Tentando gTTS...")

    # Fallback with gTTS
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(output_path)
        print(f"[Audio] Áudio (gTTS) gerado com sucesso: {output_path}")
        return output_path
    except Exception as e:
        raise RuntimeError(f"Erro ao gerar áudio TTS: {e}")


if __name__ == "__main__":
    test_file = "test_audio.mp3"
    generate_audio("Olá! Este é um teste da narração de voz realista para vídeos curtos.", test_file)
    if os.path.exists(test_file):
        print(f"Teste OK! Arquivo criado com tamanho {os.path.getsize(test_file)} bytes.")
        os.remove(test_file)
