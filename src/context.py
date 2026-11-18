"""Retrieve labeled catalog notes from two local, editable sources."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'knowledge'


def retrieve_notes(song):
    """Return exact-match evidence with a source label, never invented notes."""
    notes = []
    for field, filename in [('genre', 'genres.json'), ('mood', 'moods.json')]:
        with (ROOT / filename).open(encoding='utf-8') as stream:
            index = json.load(stream)
        key = song[field].strip().lower()
        if key in index:
            notes.append((f'{filename}#{key}', index[key]))
    return notes


def format_explanation(song, reasons, style='standard'):
    """Produce an extractive explanation from ranking reasons and local notes."""
    notes = retrieve_notes(song)
    if style == 'brief':
        return f"Match: {reasons}."  # deterministic specialized output
    lines = [f'Because: {reasons}']
    lines.extend(f'Context [{source}]: {note}' for source, note in notes)
    return '\n'.join(lines)
