import os
import json
import re
import random
from typing import Dict, Any, List

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

SUPPORTED_GAME_TYPES = [
    "tug_of_war",   # Cabo de Guerra (Time A vs Time B)
    "race",         # Corrida (Carrinhos, Animais, Personagens)
    "boss_battle",  # Batalha de Chefão (Chat vs Monstro/Boss)
    "castle_defense", # Defesa de Castelo / Torre
    "drop_balls"    # Queda de Bolas nas Caixas de Pontos
]


def create_fallback_game_config(prompt: str) -> Dict[str, Any]:
    """
    Generates a rich, structured TikTok Live game configuration based on prompt heuristics
    when OpenAI is not configured or unavailable.
    """
    prompt_lower = prompt.lower()

    # Determine game type from prompt keywords
    if any(k in prompt_lower for k in ["boss", "monstro", "dragão", "chefe", "batalha", "atacar", "demonio", "gigante"]):
        game_type = "boss_battle"
    elif any(k in prompt_lower for k in ["corrida", "carro", "sapo", "tartaruga", "cavalo", "pista", "run", "speed"]):
        game_type = "race"
    elif any(k in prompt_lower for k in ["castelo", "torre", "defesa", "muralha", "destruir"]):
        game_type = "castle_defense"
    elif any(k in prompt_lower for k in ["bola", "bolinha", "drop", "caixa", "moeda", "plinko"]):
        game_type = "drop_balls"
    else:
        game_type = "tug_of_war"

    # Extract or infer team names / characters
    if "vs" in prompt_lower or "x" in prompt_lower or "contra" in prompt_lower:
        parts = re.split(r'\bvs\b|\bx\b|\bcontra\b', prompt, flags=re.IGNORECASE)
        name_a = parts[0].strip()[:20] if len(parts) > 0 and parts[0].strip() else "Time Vermelho"
        name_b = parts[1].strip()[:20] if len(parts) > 1 and parts[1].strip() else "Time Azul"
    else:
        name_a = "Time Vermelho 🔴"
        name_b = "Time Azul 🔵"

    if game_type == "tug_of_war":
        return {
            "game_id": f"game_{random.randint(1000, 9999)}",
            "title": f"Cabo de Guerra: {name_a} vs {name_b}",
            "game_type": "tug_of_war",
            "description": f"Comente '1' para puxar para {name_a} ou '2' para {name_b}! Curtidas dão força e presentes dão super puxões!",
            "theme": {
                "background_color": "#121829",
                "primary_color": "#ff4757",
                "secondary_color": "#1e90ff",
                "accent_color": "#ffa502"
            },
            "entities": {
                "team_a": {
                  "name": f"{name_a}",
                  "keyword": "1",
                  "avatar": "🔴",
                  "color": "#ff4757",
                  "score": 50,
                  "max_score": 100
                },
                "team_b": {
                  "name": f"{name_b}",
                  "keyword": "2",
                  "avatar": "🔵",
                  "color": "#1e90ff",
                  "score": 50,
                  "max_score": 100
                }
            },
            "triggers": {
                "comments": [
                    {"keyword": "1", "action": "score_team_a", "value": 2, "description": f"Comentar '1' fortalece {name_a}"},
                    {"keyword": "2", "action": "score_team_b", "value": 2, "description": f"Comentar '2' fortalece {name_b}"}
                ],
                "likes": {
                    "multiplier": 1,
                    "threshold": 20,
                    "action": "boost_leading_team",
                    "description": "A cada 20 curtidas, a equipe ativa recebe impulso de +1"
                },
                "gifts": [
                    {"gift_name": "Rosa", "gift_icon": "🌹", "action": "score_team_a", "value": 15, "description": f"Rosa (+15 para {name_a})"},
                    {"gift_name": "TikTok", "gift_icon": "🎵", "action": "score_team_b", "value": 15, "description": f"TikTok (+15 para {name_b})"},
                    {"gift_name": "Donut", "gift_icon": "🍩", "action": "score_team_a", "value": 40, "description": f"Donut (+40 para {name_a})"},
                    {"gift_name": "Universo", "gift_icon": "🌌", "action": "super_pull_team_b", "value": 80, "description": f"Universo (Super Puxão +80 para {name_b})"}
                ]
            },
            "win_condition": {
                "target_score": 100,
                "win_message": "🎉 VITÓRIA IMPRESSIONANTE NA LIVE!"
            }
        }

    elif game_type == "race":
        return {
            "game_id": f"game_{random.randint(1000, 9999)}",
            "title": f"Grand Prix TikTok: {name_a} vs {name_b}",
            "game_type": "race",
            "description": "Comente o número do seu piloto ('1' ou '2') para acelerar! Curtidas ativam Nitro e Presentes soltam Bônus Veloz!",
            "theme": {
                "background_color": "#0d1117",
                "primary_color": "#ff6b6b",
                "secondary_color": "#4ecdc4",
                "accent_color": "#feca57"
            },
            "entities": {
                "team_a": {
                  "name": f"Piloto {name_a}",
                  "keyword": "1",
                  "avatar": "🏎️",
                  "color": "#ff6b6b",
                  "score": 0,
                  "max_score": 500
                },
                "team_b": {
                  "name": f"Piloto {name_b}",
                  "keyword": "2",
                  "avatar": "🚗",
                  "color": "#4ecdc4",
                  "score": 0,
                  "max_score": 500
                }
            },
            "triggers": {
                "comments": [
                    {"keyword": "1", "action": "score_team_a", "value": 5, "description": "Comentar '1' avança Piloto 1"},
                    {"keyword": "2", "action": "score_team_b", "value": 5, "description": "Comentar '2' avança Piloto 2"}
                ],
                "likes": {
                    "multiplier": 2,
                    "threshold": 10,
                    "action": "nitro_boost",
                    "description": "Curtidas ativam Nitro para o carro mais votado"
                },
                "gifts": [
                    {"gift_name": "Rosa", "gift_icon": "🌹", "action": "score_team_a", "value": 30, "description": "Rosa (+30m de Pista para Piloto 1)"},
                    {"gift_name": "TikTok", "gift_icon": "🎵", "action": "score_team_b", "value": 30, "description": "TikTok (+30m de Pista para Piloto 2)"},
                    {"gift_name": "Capetinha", "gift_icon": "🚀", "action": "turbo_both", "value": 75, "description": "Super Foguete (+75m Turbo)"}
                ]
            },
            "win_condition": {
                "target_score": 500,
                "win_message": "🏁 CHEGOU EM PRIMEIRÍSSIMO LUGAR NA LINHA DE CHEGADA!"
            }
        }

    elif game_type == "boss_battle":
        return {
            "game_id": f"game_{random.randint(1000, 9999)}",
            "title": "Batalha Épica contra o Chefão Dragão 🐲",
            "game_type": "boss_battle",
            "description": "O chat vs o Chefão! Comente 'atacar' ou '1' para atacar. Curtidas carregam o Super Golfe e Presentes lançam Magias Lendárias!",
            "theme": {
                "background_color": "#1b0000",
                "primary_color": "#ff3838",
                "secondary_color": "#ff9f1a",
                "accent_color": "#fff200"
            },
            "entities": {
                "boss": {
                    "name": "Dragão do Caos 🐲",
                    "avatar": "🐲",
                    "hp": 2000,
                    "max_hp": 2000,
                    "color": "#ff3838"
                },
                "chat_hero": {
                    "name": "Heróis do Chat ⚔️",
                    "color": "#ff9f1a",
                    "score": 0
                }
            },
            "triggers": {
                "comments": [
                    {"keyword": "atacar", "action": "damage_boss", "value": 15, "description": "Comentar 'atacar' causa 15 de Dano ao Chefão"},
                    {"keyword": "1", "action": "damage_boss", "value": 10, "description": "Comentar '1' dispara flecha de 10 de Dano"},
                    {"keyword": "curar", "action": "heal_chat", "value": 20, "description": "Comentar 'curar' fortalece a defesa"}
                ],
                "likes": {
                    "multiplier": 1,
                    "threshold": 30,
                    "action": "damage_boss",
                    "description": "Cada 30 curtidas do chat causam 50 de Dano Coletivo"
                },
                "gifts": [
                    {"gift_name": "Rosa", "gift_icon": "🌹", "action": "damage_boss", "value": 100, "description": "Rosa (Lança Espada de Fogo: -100 HP)"},
                    {"gift_name": "TikTok", "gift_icon": "🎵", "action": "damage_boss", "value": 250, "description": "TikTok (Lança Raio Elétrico: -250 HP)"},
                    {"gift_name": "Universo", "gift_icon": "🌌", "action": "damage_boss", "value": 1000, "description": "Universo (Meteoro Lendário: -1000 HP!)"}
                ]
            },
            "win_condition": {
                "target_score": 0, # Boss reach 0 HP
                "win_message": "⚔️ O CHAT DERROTOU O CHEFÃO! VITÓRIA LENDÁRIA!"
            }
        }

    elif game_type == "castle_defense":
        return {
            "game_id": f"game_{random.randint(1000, 9999)}",
            "title": f"Defesa do Castelo: {name_a} vs {name_b}",
            "game_type": "castle_defense",
            "description": "Comente '1' para atacar o Castelo A ou '2' para o Castelo B! Presentes soltam Bombas de Canhão!",
            "theme": {
                "background_color": "#17202a",
                "primary_color": "#e74c3c",
                "secondary_color": "#3498db",
                "accent_color": "#f1c40f"
            },
            "entities": {
                "castle_a": {
                    "name": f"Castelo {name_a}",
                    "avatar": "🏰",
                    "hp": 500,
                    "max_hp": 500,
                    "color": "#e74c3c"
                },
                "castle_b": {
                    "name": f"Castelo {name_b}",
                    "avatar": "🏰",
                    "hp": 500,
                    "max_hp": 500,
                    "color": "#3498db"
                }
            },
            "triggers": {
                "comments": [
                    {"keyword": "1", "action": "damage_castle_b", "value": 5, "description": "Comentar '1' ataca o Castelo B"},
                    {"keyword": "2", "action": "damage_castle_a", "value": 5, "description": "Comentar '2' ataca o Castelo A"}
                ],
                "likes": {
                    "multiplier": 1,
                    "threshold": 25,
                    "action": "repair_castles",
                    "description": "Curtidas reparam a defesa dos castelos"
                },
                "gifts": [
                    {"gift_name": "Rosa", "gift_icon": "🌹", "action": "damage_castle_b", "value": 40, "description": "Rosa (Bomba de Canhão no Castelo B)"},
                    {"gift_name": "TikTok", "gift_icon": "🎵", "action": "damage_castle_a", "value": 40, "description": "TikTok (Bomba de Canhão no Castelo A)"},
                    {"gift_name": "Super Gift", "gift_icon": "💥", "action": "nuke_random", "value": 150, "description": "Super Presente (Meteoro de Destruição)"}
                ]
            },
            "win_condition": {
                "target_score": 0,
                "win_message": "🏰 O CASTELO INIMIGO FOI DESTRUÍDO!"
            }
        }

    else:  # drop_balls
        return {
            "game_id": f"game_{random.randint(1000, 9999)}",
            "title": "Chuva de Esferas da Sorte TikTok",
            "game_type": "drop_balls",
            "description": "Comente 'soltar' ou '1'/'2' para soltar esferas nas caixas multiplicadoras! Presentes soltam Chuva de Bolas Raras!",
            "theme": {
                "background_color": "#0f172a",
                "primary_color": "#38bdf8",
                "secondary_color": "#a855f7",
                "accent_color": "#f59e0b"
            },
            "entities": {
                "team_a": {
                    "name": f"{name_a}",
                    "keyword": "1",
                    "avatar": "🔮",
                    "color": "#38bdf8",
                    "score": 0,
                    "max_score": 1000
                },
                "team_b": {
                    "name": f"{name_b}",
                    "keyword": "2",
                    "avatar": "💎",
                    "color": "#a855f7",
                    "score": 0,
                    "max_score": 1000
                }
            },
            "triggers": {
                "comments": [
                    {"keyword": "1", "action": "drop_ball_a", "value": 10, "description": "Comentar '1' solta esfera para Time 1"},
                    {"keyword": "2", "action": "drop_ball_b", "value": 10, "description": "Comentar '2' solta esfera para Time 2"}
                ],
                "likes": {
                    "multiplier": 1,
                    "threshold": 15,
                    "action": "drop_random_ball",
                    "description": "Curtidas soltam esferas douradas bônus"
                },
                "gifts": [
                    {"gift_name": "Rosa", "gift_icon": "🌹", "action": "drop_multi_a", "value": 50, "description": "Rosa (Chuva de 5 Esferas para Time 1)"},
                    {"gift_name": "TikTok", "gift_icon": "🎵", "action": "drop_multi_b", "value": 50, "description": "TikTok (Chuva de 5 Esferas para Time 2)"},
                    {"gift_name": "Festa", "gift_icon": "🎉", "action": "mega_ball_drop", "value": 250, "description": "Festa (Super Mega Esfera Dourada!)"}
                ]
            },
            "win_condition": {
                "target_score": 1000,
                "win_message": "💎 RECORD DE PONTUAÇÃO ALCANÇADO NA CHUVA DE ESFERAS!"
            }
        }


def generate_game_config(prompt: str) -> Dict[str, Any]:
    """
    Main entrypoint to build a TikTok Live game JSON config using OpenAI GPT or intelligent fallback generator.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key and OpenAI is not None:
        try:
            client = OpenAI(api_key=api_key)
            system_prompt = """
Você é um desenvolvedor especialista em jogos interativos e virais para TikTok Live (Interactive Live Stream Games).
Sua tarefa é ler a descrição do usuário e gerar uma estrutura JSON completa do jogo.

O jogo deve integrar perfeitamente:
1. Comentários da Live (ex: palavras-chave como '1', '2', 'atacar', nomes de times) -> Ações do jogo (pontuação, movimento, ataques, curas).
2. Curtidas (Likes) -> Acelerador, boosts, multiplicadores.
3. Envio de Presentes (Gifts do TikTok como 'Rosa', 'TikTok', 'Donut', 'Dragão', 'Universo') -> Ações especiais épicas (super ataques, chuvas de itens, avanços gigantescos).

Tipos de Jogos Suportados (escolha o mais adequado):
- "tug_of_war": Cabo de guerra entre duas equipes.
- "race": Corrida de veículos/personagens até a linha de chegada.
- "boss_battle": Chat unido contra um Monstro/Chefão.
- "castle_defense": Batalha entre castelos/torres.
- "drop_balls": Queda de bolas em caixas multiplicadoras.

Responda ESTRITAMENTE em formato JSON válido, sem markdown ou textos explicativos adicionais.
Formato exato exigido:
{
  "game_id": "game_123",
  "title": "Título do Jogo",
  "game_type": "tug_of_war",
  "description": "Instruções claras de como o chat joga na Live",
  "theme": {
    "background_color": "#121829",
    "primary_color": "#ff4757",
    "secondary_color": "#1e90ff",
    "accent_color": "#ffa502"
  },
  "entities": {
    "team_a": {"name": "Time A", "keyword": "1", "avatar": "🔴", "color": "#ff4757", "score": 50, "max_score": 100},
    "team_b": {"name": "Time B", "keyword": "2", "avatar": "🔵", "color": "#1e90ff", "score": 50, "max_score": 100}
  },
  "triggers": {
    "comments": [
      {"keyword": "1", "action": "score_team_a", "value": 2, "description": "Descrição"},
      {"keyword": "2", "action": "score_team_b", "value": 2, "description": "Descrição"}
    ],
    "likes": {
      "multiplier": 1,
      "threshold": 20,
      "action": "boost_leading_team",
      "description": "Descrição"
    },
    "gifts": [
      {"gift_name": "Rosa", "gift_icon": "🌹", "action": "score_team_a", "value": 15, "description": "Descrição"},
      {"gift_name": "TikTok", "gift_icon": "🎵", "action": "score_team_b", "value": 15, "description": "Descrição"},
      {"gift_name": "Universo", "gift_icon": "🌌", "action": "ultimate_attack", "value": 100, "description": "Descrição"}
    ]
  },
  "win_condition": {
    "target_score": 100,
    "win_message": "Mensagem de Vitória!"
  }
}
"""
            user_msg = f"Descrição do Jogo Solicitado: {prompt}"

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.7
            )

            raw_content = response.choices[0].message.content.strip()
            # Clean possible markdown block formatting
            raw_content = re.sub(r"^```json\s*", "", raw_content, flags=re.MULTILINE)
            raw_content = re.sub(r"^```\s*", "", raw_content, flags=re.MULTILINE)
            raw_content = raw_content.strip()

            parsed_json = json.loads(raw_content)
            if isinstance(parsed_json, dict) and "game_type" in parsed_json:
                print(f"[GameGenerator] Jogo gerado via OpenAI com sucesso: {parsed_json.get('title')}")
                return parsed_json
        except Exception as e:
            print(f"[Aviso] Falha ao gerar jogo com OpenAI ({e}). Utilizando gerador heurístico...")

    return create_fallback_game_config(prompt)


if __name__ == "__main__":
    test_prompt = "Uma corrida maluca entre sapo e tartaruga onde mandar presente solta bombas"
    game_cfg = generate_game_config(test_prompt)
    print(json.dumps(game_cfg, indent=2, ensure_ascii=False))
