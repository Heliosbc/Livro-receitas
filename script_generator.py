import os
import json
import re
from typing import List, Dict, Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


def generate_script(topic: str, niche: str, language: str = "pt", max_duration_sec: int = 45) -> List[Dict[str, Any]]:
    """
    Generates a video script divided into scenes. Each scene contains:
    - scene_id: int
    - text: str (narration text)
    - keyword: str (search query for background video)
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key and OpenAI is not None:
        try:
            client = OpenAI(api_key=api_key)
            prompt = f"""
Você é um especialista em criar roteiros virais para vídeos curtos (TikTok / YouTube Shorts / Reels).
Tema do vídeo: {topic}
Nicho: {niche}
Idioma: {language}
Duração total máxima: {max_duration_sec} segundos.

Crie um roteiro dinâmico e envolvente dividido em 3 a 5 cenas curtas.
A soma das frases de narração deve dar no máximo cerca de {max_duration_sec} segundos ao ser falada.
Cada cena deve conter:
1. "text": Texto exato falado pelo narrador (gancho forte na 1ª cena, conteúdo envolvente, chamada para ação na última).
2. "keyword": Palavra-chave simples em inglês para buscar um vídeo de fundo (B-roll) relevante na API de vídeos (ex: 'galaxy space', 'financial growth', 'fitness running').

Responda ESTRITAMENTE em formato JSON com uma lista de objetos:
[
  {{
    "scene_id": 1,
    "text": "...",
    "keyword": "..."
  }}
]
"""
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você gera roteiros em formato JSON válido sem formatação markdown adicional."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            content = response.choices[0].message.content.strip()
            # Clean markdown codeblocks if present
            content = re.sub(r"^```json\s*", "", content, flags=re.MULTILINE)
            content = re.sub(r"^```\s*", "", content, flags=re.MULTILINE)
            content = content.strip()

            scenes = json.loads(content)
            if isinstance(scenes, list) and len(scenes) > 0:
                return scenes
        except Exception as e:
            print(f"[Aviso] Falha ao usar OpenAI API ({e}). Usando gerador de roteiro padrão...")

    # Fallback default script generator if no OpenAI API key is present or on error
    print("[Info] Gerando roteiro estruturado automático...")
    fallback_scenes = [
        {
            "scene_id": 1,
            "text": f"Você sabia disto sobre {topic}? Preste muita atenção!",
            "keyword": f"{niche} technology" if niche else topic
        },
        {
            "scene_id": 2,
            "text": f"No universo de {niche}, {topic} é um dos assuntos mais impressionantes e cheios de curiosidades.",
            "keyword": topic
        },
        {
            "scene_id": 3,
            "text": "E o detalhe mais incrível é como isso impacta tudo ao nosso redor no dia a dia.",
            "keyword": "nature background"
        },
        {
            "scene_id": 4,
            "text": "Gostou dessa curiosidade? Curta o vídeo e siga o perfil para não perder nenhuma novidade!",
            "keyword": "subscribe follow"
        }
    ]
    return fallback_scenes


if __name__ == "__main__":
    test_script = generate_script("Buracos Negros", "Ciência")
    print("Roteiro Gerado:")
    print(json.dumps(test_script, indent=2, ensure_ascii=False))
