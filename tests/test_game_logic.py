import os
import tempfile
import unittest
from unittest import mock

from tkinter import Tk
from PIL import Image

from ventana import GameWindow


def _make_temp_images(dir_path: str, count: int = 9):
    # create simple colored PNGs
    for i in range(count):
        img = Image.new("RGB", (64, 64), (i * 20 % 255, i * 40 % 255, i * 60 % 255))
        img.save(os.path.join(dir_path, f"{i+1}.png"))


class TestGameWindow(unittest.TestCase):
    def setUp(self):
        # temp directory for images
        self.tmpdir = tempfile.mkdtemp(prefix="memorama_imgs_")
        _make_temp_images(self.tmpdir, count=10)

        # Tk root
        self.root = Tk()
        self.root.withdraw()

    def tearDown(self):
        try:
            # Close root safely
            self.root.destroy()
        except Exception:
            pass
        # Cleanup images
        for f in os.listdir(self.tmpdir):
            try:
                os.remove(os.path.join(self.tmpdir, f))
            except Exception:
                pass
        try:
            os.rmdir(self.tmpdir)
        except Exception:
            pass

    def test_setup_board(self):
        # patch name prompt and disable music init
        with mock.patch.object(GameWindow, "_prompt_name", return_value="Tester"), \
             mock.patch.object(GameWindow, "_init_music", return_value=None):
            gw = GameWindow(self.root, grid_size=4, theme_dir=self.tmpdir, player_name="Tester")
            self.assertEqual(len(gw.buttons), 16)
            self.assertEqual(len(gw.card_values), 16)
            # pairs should be exactly double the unique faces used
            self.assertEqual(sorted(gw.card_values).count(0), 2)
            gw.destroy()

    def test_scoring_logic(self):
        with mock.patch.object(GameWindow, "_prompt_name", return_value="Tester"), \
             mock.patch.object(GameWindow, "_init_music", return_value=None):
            gw = GameWindow(self.root, grid_size=4, theme_dir=self.tmpdir, player_name="Tester")
            # No attempts initially => best score
            self.assertGreaterEqual(gw._score(), 0)
            # Simulate attempts beyond optimal
            total_pairs = len(gw.card_values) // 2
            gw.attempts = total_pairs + 3
            s2 = gw._score()
            self.assertLess(s2, 1000)
            gw.destroy()

    def test_click_match_flow(self):
        with mock.patch.object(GameWindow, "_prompt_name", return_value="Tester"), \
             mock.patch.object(GameWindow, "_init_music", return_value=None):
            gw = GameWindow(self.root, grid_size=4, theme_dir=self.tmpdir, player_name="Tester")
            # Find a pair indices
            value_to_indices = {}
            for idx, val in enumerate(gw.card_values):
                value_to_indices.setdefault(val, []).append(idx)
            pair = next((idxs for idxs in value_to_indices.values() if len(idxs) >= 2), None)
            self.assertIsNotNone(pair)
            i, j = pair[0], pair[1]

            gw.on_card_click(i)
            gw.on_card_click(j)
            # After a match, both indices must be in revealed_indices
            self.assertIn(i, gw.revealed_indices)
            self.assertIn(j, gw.revealed_indices)
            gw.destroy()


if __name__ == '__main__':
    unittest.main()
