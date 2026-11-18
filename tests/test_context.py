import unittest
from src.context import retrieve_notes, format_explanation


class ContextTests(unittest.TestCase):
    def test_retrieves_two_attributed_sources(self):
        song = {'genre': 'lofi', 'mood': 'chill'}
        notes = retrieve_notes(song)
        self.assertEqual([source for source, _ in notes], ['genres.json#lofi', 'moods.json#chill'])
        self.assertIn(notes[0][1], format_explanation(song, 'Genre match'))

    def test_unknown_labels_do_not_invent_context(self):
        self.assertEqual(retrieve_notes({'genre': 'missing', 'mood': 'missing'}), [])

    def test_brief_style_retains_scoring_reasons(self):
        song = {'genre': 'lofi', 'mood': 'chill'}
        brief = format_explanation(song, 'Genre match (+3.0)', 'brief')
        self.assertIn('Genre match (+3.0)', brief)
        self.assertNotIn('Context', brief)


if __name__ == '__main__':
    unittest.main()
