import unittest
from pathlib import Path
from src.agent import recommend
from src.recommender import load_songs


class AgentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.songs = load_songs(str(Path(__file__).resolve().parents[1] / 'data/songs.csv'))

    def test_chill_lofi(self):
        result = recommend({'genre': 'lofi', 'mood': 'chill', 'energy': .4}, self.songs)
        self.assertEqual(result['results'][0][0]['title'], 'Midnight Coding')

    def test_energy_guardrail(self):
        result = recommend({'genre': 'lofi', 'mood': 'chill', 'energy': .95}, self.songs)
        self.assertGreater(result['rejected'], 0)
        self.assertTrue(all(abs(song['energy'] - .95) <= .25 for song, _, _ in result['results']))
        self.assertEqual(result['results'], [])

    def test_no_relevant_candidates(self):
        result = recommend({'genre': 'unknown', 'mood': 'unknown', 'energy': .5}, self.songs)
        self.assertEqual(result['results'], [])

    def test_invalid_energy(self):
        for value in [-1, 2, float('nan'), 'no']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                recommend({'genre': 'pop', 'mood': 'happy', 'energy': value}, self.songs)

    def test_invalid_count(self):
        with self.assertRaises(ValueError):
            recommend({'genre': 'pop', 'mood': 'happy', 'energy': .8}, self.songs, 0)

    def test_case_and_explanation(self):
        result = recommend({'genre': ' POP ', 'mood': 'HAPPY', 'energy': .9}, self.songs)
        self.assertEqual(result['results'][0][0]['title'], 'Sunrise City')
        self.assertIn('Genre match', result['results'][0][2])


if __name__ == '__main__':
    unittest.main()
