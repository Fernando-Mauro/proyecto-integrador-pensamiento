import os
import tempfile
import unittest

import scores


class TestScores(unittest.TestCase):
    def setUp(self):
        fd, self.tmp = tempfile.mkstemp(prefix="scores_", suffix=".json")
        os.close(fd)
        # ensure empty
        with open(self.tmp, "w", encoding="utf-8") as f:
            f.write("{}")

    def tearDown(self):
        try:
            os.remove(self.tmp)
        except FileNotFoundError:
            pass

    def test_write_and_keep_highest(self):
        scores.write_score("Alice", 100, path=self.tmp)
        scores.write_score("Alice", 90, path=self.tmp)  # lower, should keep 100
        scores.write_score("Alice", 150, path=self.tmp)  # higher, should update
        data = scores.read_scores(path=self.tmp)
        # find Alice at default difficulty 'dificil'
        alice = next((e for e in data if e["name"] == "Alice" and e["difficulty"] == "dificil"), None)
        self.assertIsNotNone(alice)
        self.assertEqual(alice["score"], 150)

    def test_sorted_desc(self):
        scores.write_score("Bob", 120, path=self.tmp)
        scores.write_score("Charlie", 200, path=self.tmp)
        scores.write_score("Ana", 50, path=self.tmp)
        ordered = scores.read_scores(path=self.tmp)
        # Ensure sorted by score desc
        self.assertEqual(ordered[0]["name"], "Charlie")
        self.assertEqual(ordered[0]["score"], 200)
        self.assertEqual(ordered[-1]["name"], "Ana")

    def test_difficulty_independent_highest(self):
        # Same player different difficulties keep independent highs
        scores.write_score("Dana", 100, difficulty="facil", path=self.tmp)
        scores.write_score("Dana", 90, difficulty="facil", path=self.tmp)
        scores.write_score("Dana", 80, difficulty="dificil", path=self.tmp)
        scores.write_score("Dana", 150, difficulty="dificil", path=self.tmp)
        data = scores.read_scores(path=self.tmp)
        easy = next((e for e in data if e["name"] == "Dana" and e["difficulty"] == "facil"), None)
        hard = next((e for e in data if e["name"] == "Dana" and e["difficulty"] == "dificil"), None)
        self.assertEqual(easy["score"], 100)
        self.assertEqual(hard["score"], 150)


if __name__ == '__main__':
    unittest.main()
