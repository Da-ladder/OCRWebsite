// scripts.js

const cardWidth = 200; // Fixed card width
const cardHeight = 300; // Fixed card height
const cardMargin = 16; // Margin between cards
const cardWrappers = document.querySelectorAll('.card-wrapper');

function getCardsPerPage(containerWidth) {
    return Math.floor(containerWidth / (cardWidth + cardMargin));
}

function renderCards(wrapper, currentPage) {
    const cardContainer = wrapper.querySelector('.card-container');
    const cards = Array.from(cardContainer.children);
    const containerWidth = cardContainer.clientWidth;
    const cardsPerPage = getCardsPerPage(containerWidth);
    const start = (currentPage - 1) * cardsPerPage;
    const end = Math.min(start + cardsPerPage, cards.length);

    cards.forEach((card, index) => {
        if (index >= start && index < end) {
            card.style.display = 'inline-block';
        } else {
            card.style.display = 'none';
        }
    });

    renderPaginationControls(wrapper, currentPage, cardsPerPage, cards.length);
}

function renderPaginationControls(wrapper, currentPage, cardsPerPage, totalCards) {
    const totalPages = Math.ceil(totalCards / cardsPerPage);

    const prevBtn = wrapper.querySelector('.prev-btn');
    const nextBtn = wrapper.querySelector('.next-btn');

    if (currentPage === 1) {
        prevBtn.classList.add('disabled');
    } else {
        prevBtn.classList.remove('disabled');
    }

    if (currentPage === totalPages) {
        nextBtn.classList.add('disabled');
    } else {
        nextBtn.classList.remove('disabled');
    }

    prevBtn.onclick = () => {
        if (currentPage > 1) {
            currentPage--;
            renderCards(wrapper, currentPage);
        }
    };

    nextBtn.onclick = () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderCards(wrapper, currentPage);
        }
    };
}

function initializePagination() {
    cardWrappers.forEach(wrapper => {
        let currentPage = 1;
        wrapper.dataset.currentPage = currentPage;
        renderCards(wrapper, currentPage);
    });
}

window.addEventListener('resize', initializePagination);
window.addEventListener('DOMContentLoaded', initializePagination);
