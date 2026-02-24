
// js/app.js
window.MB = (() => {
  const KEYS = { GAMES: 'mb_games', GAMES_SEEDED: 'mb_games_seeded' };

  const load  = (k) => JSON.parse(localStorage.getItem(k) || '[]');
  const save  = (k, v) => localStorage.setItem(k, JSON.stringify(v));

  function seedGamesIfNeeded() {
    if (localStorage.getItem(KEYS.GAMES_SEEDED)) return;
    if (Array.isArray(window.MB_GAMES_SEED)) {
      save(KEYS.GAMES, window.MB_GAMES_SEED);
      localStorage.setItem(KEYS.GAMES_SEEDED, '1');
      console.log('Seeded games:', window.MB_GAMES_SEED.length);
    } else {
      console.warn('No MB_GAMES_SEED found — check js/gamedata.js');
    }
  }

  function getAllGames() { return load(KEYS.GAMES); }

  function findGamesByTitle(q) {
    const txt = (q || '').toLowerCase().trim();
    if (!txt) return [];
    return getAllGames().filter(g => g.title.toLowerCase().includes(txt));
  }

  return { seedGamesIfNeeded, getAllGames, findGamesByTitle };
})();
