"""A bounded, rule-based recommendation agent with explicit verification."""
import logging
import math
from .recommender import recommend_songs

log = logging.getLogger(__name__)


def recommend(profile, songs, k=3, max_energy_gap=0.25):
    """Plan, retrieve, verify, and explain. Return only verified candidates.

    Energy is a hard constraint, rather than another weighted preference. The
    user can revise preferences when the catalog contains too few matches.
    """
    genre = str(profile.get('genre', '')).strip().lower()
    mood = str(profile.get('mood', '')).strip().lower()
    try:
        energy = float(profile['energy'])
    except (KeyError, TypeError, ValueError):
        raise ValueError('Energy must be a number from 0 to 1.') from None
    if not genre or not mood:
        raise ValueError('Genre and mood are required.')
    if not math.isfinite(energy) or not 0 <= energy <= 1:
        raise ValueError('Energy must be a number from 0 to 1.')
    if not isinstance(k, int) or isinstance(k, bool) or not 1 <= k <= 10:
        raise ValueError('Count must be an integer from 1 to 10.')
    if not math.isfinite(max_energy_gap) or not 0 <= max_energy_gap <= 1:
        raise ValueError('Energy gap must be from 0 to 1.')
    prefs = {'genre': genre, 'mood': mood, 'energy': energy}
    # Retrieve only relevant items; avoid presenting energy-only matches as
    # if they satisfied the listener's genre or mood.
    candidates = [s for s in songs if s['genre'].lower() == genre or s['mood'].lower() == mood]
    verified = [s for s in candidates if abs(s['energy'] - energy) <= max_energy_gap + 1e-12]
    rejected = len(candidates) - len(verified)
    results = recommend_songs(prefs, verified, k=k)
    log.info('candidates=%d rejected_energy=%d returned=%d', len(candidates), rejected, len(results))
    return {'candidates': len(candidates), 'rejected': rejected, 'results': results}
