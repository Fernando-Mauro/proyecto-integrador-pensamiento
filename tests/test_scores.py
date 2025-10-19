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
        self.assertEqual(data.get("Alice"), 150)

    def test_sorted_desc(self):
        scores.write_score("Bob", 120, path=self.tmp)
        scores.write_score("Charlie", 200, path=self.tmp)
        scores.write_score("Ana", 50, path=self.tmp)
        ordered = list(scores.read_scores(path=self.tmp).items())
        self.assertEqual(ordered[0][0], "Charlie")
        self.assertEqual(ordered[0][1], 200)
        self.assertEqual(ordered[-1][0], "Ana")


if __name__ == '__main__':
    unittest.main()
