async function loadArticles() {
  try {
    const res = await fetch('public/articles.json');
    const data = await res.json();
    const container = document.getElementById('articles');
    container.innerHTML = '';
    data.articles.forEach(a => {
      const div = document.createElement('div');
      div.className = 'article';
      div.innerHTML = `
        <img src="${a.image}" alt="${a.title}">
        <h2><a href="${a.link}" target="_blank">${a.title}</a></h2>
        <p>${a.description}</p>`;
      container.appendChild(div);
    });
  } catch (err) {
    console.error('Error loading articles:', err);
  }
}
loadArticles();
