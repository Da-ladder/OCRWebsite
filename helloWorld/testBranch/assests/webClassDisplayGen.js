// scripts.js

const cardWidth = 200; // Fixed card width
const cardHeight = 300; // Fixed card height
const cardMargin = 16; // Margin between cards
const totalCards = 50; // Adjust based on actual number of cards
const cardWrappers = document.querySelectorAll('.card-wrapper');

function getCardsPerPage(containerWidth) {
    return Math.floor(containerWidth / (cardWidth + cardMargin));
}

function createCard(index) {
    const card = document.createElement('div');
    card.classList.add('card');
    card.textContent = `Card ${index + 1}`;
    return card;
}

function renderCards(wrapper, currentPage) {
    const cardContainer = wrapper.querySelector('.card-container');
    const paginationContainer = wrapper.querySelector('.pagination-container');
    cardContainer.innerHTML = '';
    const containerWidth = cardContainer.clientWidth;
    const cardsPerPage = getCardsPerPage(containerWidth);
    const start = (currentPage - 1) * cardsPerPage;
    const end = Math.min(start + cardsPerPage, totalCards);
    for (let i = start; i < end; i++) {
        cardContainer.appendChild(createCard(i));
    }
    renderPaginationControls(wrapper, currentPage, cardsPerPage);
}

function renderPaginationControls(wrapper, currentPage, cardsPerPage) {
    const paginationContainer = wrapper.querySelector('.pagination-container');
    paginationContainer.innerHTML = '';
    const totalPages = Math.ceil(totalCards / cardsPerPage);

    const prevBtn = wrapper.querySelector('.prev-btn');
    const nextBtn = wrapper.querySelector('.next-btn');

    prevBtn.onclick = () => {
        if (currentPage > 1) {
            renderCards(wrapper, currentPage - 1);
        }
    };

    nextBtn.onclick = () => {
        if (currentPage < totalPages) {
            renderCards(wrapper, currentPage + 1);
        }
    };

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('a');
        btn.classList.add('pagination-btn');
        if (i === currentPage) {
            btn.classList.add('disabled');
        }
        btn.textContent = i;
        btn.addEventListener('click', () => {
            if (i !== currentPage) {
                renderCards(wrapper, i);
            }
        });
        paginationContainer.appendChild(btn);
    }
}

function initializePagination() {
    cardWrappers.forEach(wrapper => {
        let currentPage = 1;
        renderCards(wrapper, currentPage);
    });
}

window.addEventListener('resize', initializePagination);
window.addEventListener('DOMContentLoaded', initializePagination);
