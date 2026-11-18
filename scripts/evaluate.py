"""Evaluate the complete recommendation workflow on fixed scenarios."""
from pathlib import Path
from src.agent import recommend
from src.recommender import load_songs


def main():
    songs = load_songs(str(Path(__file__).resolve().parents[1] / 'data' / 'songs.csv'))
    cases = [
        ('chill lofi', {'genre': 'lofi', 'mood': 'chill', 'energy': .4}, 'Midnight Coding', 0),
        ('happy pop', {'genre': 'pop', 'mood': 'happy', 'energy': .9}, 'Sunrise City', 0),
        ('intense rock', {'genre': 'rock', 'mood': 'intense', 'energy': .9}, 'Storm Runner', 0),
        ('high-energy lofi', {'genre': 'lofi', 'mood': 'chill', 'energy': .95}, None, 4),
        ('unknown labels', {'genre': 'unknown', 'mood': 'unknown', 'energy': .5}, None, 0),
    ]
    passed = 0
    for name, profile, expected, rejected in cases:
        result = recommend(profile, songs)
        actual = result['results'][0][0]['title'] if result['results'] else None
        ok = actual == expected and result['rejected'] == rejected
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} {name}: top={actual or 'none'}, rejected={result['rejected']}")
    print(f'Summary: {passed}/{len(cases)} passed')
    return 0 if passed == len(cases) else 1


if __name__ == '__main__':
    raise SystemExit(main())
