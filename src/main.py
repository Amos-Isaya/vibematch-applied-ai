"""Run the VibeMatch recommendation agent from the command line."""
import argparse
import logging
from pathlib import Path
from .agent import recommend
from .recommender import load_songs


def main():
    parser = argparse.ArgumentParser(description='Find fictional songs matching your preferences.')
    parser.add_argument('--genre', required=True)
    parser.add_argument('--mood', required=True)
    parser.add_argument('--energy', required=True, type=float)
    parser.add_argument('--count', type=int, default=3)
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
    try:
        songs = load_songs(str(Path(__file__).resolve().parent.parent / 'data' / 'songs.csv'))
        output = recommend(vars(args), songs, args.count)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f'Error: {exc}\n')
    print(f"Retrieved: {output['candidates']} | Rejected by energy guardrail: {output['rejected']}")
    if not output['results']:
        print('No verified matches. Try changing genre, mood, or energy.')
    for i, (song, score, why) in enumerate(output['results'], 1):
        print(f"{i}. {song['title']} — {song['artist']} | score {score:.2f} | energy {song['energy']:.2f}")
        print(f'   {why}')
    print('Scores are rule-based fit, not probabilities. Review the suggestions yourself.')


if __name__ == '__main__':
    main()
