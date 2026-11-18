"""Run the VibeMatch recommendation agent from the command line."""
import argparse
import logging
from pathlib import Path
from .agent import recommend
from .recommender import load_songs
from .context import format_explanation


def main():
    parser = argparse.ArgumentParser(description='Find fictional songs matching your preferences.')
    parser.add_argument('--genre', required=True)
    parser.add_argument('--mood', required=True)
    parser.add_argument('--energy', required=True, type=float)
    parser.add_argument('--count', type=int, default=3)
    parser.add_argument('--style', choices=('standard', 'brief'), default='standard')
    parser.add_argument('--trace', metavar='FILE', help='Save workflow decisions to a text file')
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
        print('   ' + format_explanation(song, why, args.style).replace('\n', '\n   '))
    print('Scores are rule-based fit, not probabilities. Review the suggestions yourself.')
    if args.trace:
        lines = [f'Input: genre={args.genre}, mood={args.mood}, energy={args.energy}',
                 'Plan: validate input -> retrieve relevant songs -> verify energy -> rank -> return',
                 f"Retrieve: {output['candidates']} candidates matched genre or mood",
                 f"Verify: rejected {output['rejected']} candidates with energy gap above 0.25",
                 'Rank: original genre, mood, and energy scoring',
                 'Return: ' + (', '.join(song['title'] for song, _, _ in output['results']) or 'no verified matches')]
        try:
            Path(args.trace).write_text('\n'.join(lines) + '\n', encoding='utf-8')
        except OSError as exc:
            parser.exit(2, f'Error saving trace: {exc}\n')


if __name__ == '__main__':
    main()
