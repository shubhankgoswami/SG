document.addEventListener('DOMContentLoaded', () => {
    const app = document.getElementById('app');
    const loading = document.getElementById('loading');

    // Sample data in case the file isn't generated yet or for initial demo
    const fallbackData = [
        {
            category: "AI BREAKTHROUGH",
            title: "Gemini 1.5 Flash Sets New Speed Records",
            summary: "• Unprecedented performance in real-time tasks.\n• Optimized for low-latency visual applications.",
            link: "https://blog.google/technology/ai/google-gemini-next-generation-model-flash-1-5/"
        },
        {
            category: "BIG TECH",
            title: "Apple Vision Pro 2 Rumors Intensify",
            summary: "• Supply chain reports suggest lighter design.\n• Potential release window late 2025.",
            link: "https://www.theverge.com/apple"
        }
    ];

    function loadNews() {
        if (window.NEWS_DATA && Array.isArray(window.NEWS_DATA)) {
            renderCards(window.NEWS_DATA);
        } else {
            console.warn('NEWS_DATA not found, using fallback demo data.');
            renderCards(fallbackData);
        }
    }

    function renderCards(newsItems) {
        loading.style.display = 'none';
        app.innerHTML = ''; // Clear loading state

        newsItems.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = 'card';
            card.style.animationDelay = `${index * 0.1}s`;

            // Prepare summary text
            let summaryText = '';
            if (Array.isArray(item.summary)) {
                summaryText = item.summary.join(' ');
            } else {
                summaryText = item.summary;
            }

            card.innerHTML = `
                <span class="category">${item.category}</span>
                <h2 class="title">${item.title}</h2>
                <div class="summary-container">
                    <div class="summary">
                        ${summaryText}
                    </div>
                    <a href="${item.link}" target="_blank" class="cta-button">Read Full Story</a>
                </div>
            `;

            card.addEventListener('click', (e) => {
                // If clicking the link, don't toggle
                if (e.target.classList.contains('cta-button')) return;

                const isExpanded = card.classList.contains('expanded');

                // Collapse all other cards
                document.querySelectorAll('.card.expanded').forEach(otherCard => {
                    if (otherCard !== card) {
                        otherCard.classList.remove('expanded');
                    }
                });

                // Toggle current card
                card.classList.toggle('expanded');
            });

            app.appendChild(card);
        });
    }

    loadNews();
});
