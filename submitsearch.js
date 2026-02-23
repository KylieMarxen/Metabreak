// js/submit.search.js
document.addEventListener('DOMContentLoaded', () => {
  MB.seedGamesIfNeeded();

  const $q = document.getElementById('gameSearch');
  const $results = document.getElementById('results');
  const $chosen = document.getElementById('chosen');
  const $form = document.getElementById('form');
  const $gameId = document.getElementById('gameId');

  const $chosenTitle = document.getElementById('chosenTitle');
  const $chosenStudio = document.getElementById('chosenStudio');
  const $chosenRelease = document.getElementById('chosenRelease');
  const $chosenCover  = document.getElementById('chosenCover');
  const $change = document.getElementById('change');

  function resetChoice() {
    $chosen.classList.add('hidden');
    $form.classList.add('hidden');
    $results.innerHTML = '';
    $gameId.value = '';
    $q.value = '';
    $q.focus();
  }

  function choose(game) {
    $gameId.value = game.id;
    $chosenTitle.textContent = game.title;
    $chosenStudio.textContent = game.studio;
    $chosenRelease.textContent = game.releaseYear || '';
    $chosenCover.src = game.cover || 'assets/placeholder.png';
    $chosenCover.alt = `${game.title} cover`;
    $chosen.classList.remove('hidden');
    $form.classList.remove('hidden');
    $results.innerHTML = '';
  }

  $change.addEventListener('click', resetChoice);

  let last = '';
  $q.addEventListener('input', () => {
    const q = $q.value.trim();
    if (q.length < 2) { $results.innerHTML = ''; last = q; return; }
    if (q === last) return;
    last = q;

    const matches = MB.findGamesByTitle(q).slice(0, 12);
    if (!matches.length) { $results.innerHTML = `<div class="muted">No matches.</div>`; return; }

    $results.innerHTML = matches.map(g => `
      <div class="item" data-id="${g.id}">
        <img class="thumb" src="${g.cover || 'assets/placeholder.png'}" alt="">
        <div>
          <div style="font-weight:600">${g.title}</div>
          <div class="muted">${g.studio} • ${g.releaseYear || ''}</div>
        </div>
      </div>
    `).join('');

    [...$results.querySelectorAll('.item')].forEach(el => {
      el.addEventListener('click', () => {
        const id = el.getAttribute('data-id');
        const game = MB.getAllGames().find(x => x.id === id);
        if (game) choose(game);
      });
    });
  });
});
