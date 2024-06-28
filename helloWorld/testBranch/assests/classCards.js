//ChatGPT carries lol
document.querySelectorAll('.class-card').forEach(card => {
    card.addEventListener('click', () => {
        const url = card.getAttribute('data-url');
        if (url) {
            window.location.href = url;
        } else {
            alert('URL not set for this class.');
        }
    });
});