document.addEventListener('click', function (e) {
  const btn = e.target.closest('.read-more');
  if (!btn) return;
  const targetId = btn.getAttribute('data-target');
  const snippet = document.getElementById(targetId);
  if (!snippet) return;

  const expanded = btn.getAttribute('aria-expanded') === 'true';

  if (!expanded) {
    // Expand
    snippet.style.display = 'block';
    // remove line-clamp styles
    snippet.style.webkitLineClamp = 'unset';
    snippet.style.overflow = 'visible';
    snippet.style.maxHeight = 'none';
    btn.textContent = 'Show less';
    btn.setAttribute('aria-expanded', 'true');
  } else {
    // Collapse back to 3-line clamp
    snippet.style.display = '-webkit-box';
    snippet.style.webkitBoxOrient = 'vertical';
    snippet.style.webkitLineClamp = '3';
    snippet.style.maxHeight = '';
    snippet.style.overflow = 'hidden';
    btn.textContent = 'Read more';
    btn.setAttribute('aria-expanded', 'false');
  }
});