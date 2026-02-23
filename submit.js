// js/submit.js
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('form');
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const gameId = document.getElementById('gameId').value;
    if (!gameId) return alert('Choose a game first.');

    const game = MB.getAllGames().find(g => g.id === gameId);
    if (!game) return alert('Selected game not found.');

    const data = {
      id: Date.now(),
      type: 'review',
      title: document.getElementById('title').value.trim(),
      game: game.title,
      platform: document.getElementById('platform').value,
      difficulty: Number(document.getElementById('difficulty').value),
      score: Number(document.getElementById('score').value),
      review: document.getElementById('review').value.trim(),
      author: (document.getElementById('author').value || 'Anonymous').trim(),
      createdAt: new Date().toISOString()
    };

    if (!data.title || !data.review) return alert('Please fill all required fields.');
    if (data.difficulty < 1 || data.difficulty > 5) return alert('Difficulty must be 1–5.');
    if (data.score < 0 || data.score > 100) return alert('Score must be 0–100.');

    // store under 'mb_reviews'
    const key = 'mb_reviews';
    const list = JSON.parse(localStorage.getItem(key) || '[]');
    list.push(data);
    localStorage.setItem(key, JSON.stringify(list));

    alert('Your Review has been submitted!.');
    window.location.href = 'index.html';
  });
});
