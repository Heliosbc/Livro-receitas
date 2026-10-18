import unittest
import json
from game_generator import generate_game_config, create_fallback_game_config
from tiktok_game_engine import render_tiktok_game_html
from script_generator import generate_script


class TestTikTokGameCreator(unittest.TestCase):

    def test_fallback_game_generation_tug_of_war(self):
        prompt = "Cabo de Guerra entre Cães e Gatos"
        cfg = create_fallback_game_config(prompt)
        self.assertIn("game_id", cfg)
        self.assertIn("title", cfg)
        self.assertEqual(cfg["game_type"], "tug_of_war")
        self.assertIn("team_a", cfg["entities"])
        self.assertIn("team_b", cfg["entities"])
        self.assertIn("comments", cfg["triggers"])
        self.assertIn("likes", cfg["triggers"])
        self.assertIn("gifts", cfg["triggers"])

    def test_fallback_game_generation_race(self):
        prompt = "Corrida de Sapo e Tartaruga"
        cfg = create_fallback_game_config(prompt)
        self.assertEqual(cfg["game_type"], "race")
        self.assertIn("target_score", cfg["win_condition"])

    def test_fallback_game_generation_boss_battle(self):
        prompt = "Batalha contra o Dragão Monstro Chefão"
        cfg = create_fallback_game_config(prompt)
        self.assertEqual(cfg["game_type"], "boss_battle")
        self.assertIn("boss", cfg["entities"])
        self.assertIn("hp", cfg["entities"]["boss"])

    def test_fallback_game_generation_castle_defense(self):
        prompt = "Defesa do Castelo Vermelho contra Azul"
        cfg = create_fallback_game_config(prompt)
        self.assertEqual(cfg["game_type"], "castle_defense")
        self.assertIn("castle_a", cfg["entities"])

    def test_fallback_game_generation_drop_balls(self):
        prompt = "Chuva de bolas nas caixas"
        cfg = create_fallback_game_config(prompt)
        self.assertEqual(cfg["game_type"], "drop_balls")

    def test_main_game_generator_wrapper(self):
        cfg = generate_game_config("Cabo de Guerra Piratas vs Ninjas")
        self.assertIsInstance(cfg, dict)
        self.assertIn("game_type", cfg)

    def test_render_tiktok_game_html(self):
        cfg = generate_game_config("Corrida de Carros")
        html_code = render_tiktok_game_html(cfg, show_controls=True)
        self.assertIsInstance(html_code, str)
        self.assertIn("<canvas id=\"gameCanvas\"", html_code)
        self.assertIn("window.triggerGameAction", html_code)
        self.assertIn(cfg["title"], html_code)

    def test_existing_video_script_generator(self):
        scenes = generate_script("Buracos Negros", "Ciência")
        self.assertIsInstance(scenes, list)
        self.assertGreater(len(scenes), 0)


if __name__ == "__main__":
    unittest.main()
