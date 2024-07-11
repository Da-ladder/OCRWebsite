// scripts.js

const cardWidth = 240; // Fixed card width
const cardHeight = 240; // Fixed card height
const cardMargin = 16; // Margin between cards
const cardWrappers = document.querySelectorAll('.card-wrapper');
const cardContain = document.querySelectorAll('.card-container');

function getCardsPerPage(containerWidth) {
    return Math.floor(containerWidth / (cardWidth + cardMargin));
}

function renderCards(wrapper, currentPage) {
    const cardContainer = wrapper.querySelector('.card-container');

    
    cardContainer.style.borderLeft = 65 + "px solid transparent";
    cardContainer.style.borderRight = 65 + "px solid transparent";
    const cards = Array.from(cardContainer.children);
    const containerWidth = cardContainer.clientWidth + 10; // Magic # does it look like I care? 4 hrs
    const cardsPerPage = getCardsPerPage(containerWidth);

    if (cardsPerPage >= cards.length) {
        // Hide all buttons it is able to accommodate it
        const showButton = document.getElementById('show' + cardContainer.id);
        const hideButton = document.getElementById('hide' + cardContainer.id);
        showButton.style.display = "none";
        hideButton.style.display = "none";
    } else {
        // Make hide button disapper when any navigation pages are clicked
        const showButton = document.getElementById('show' + cardContainer.id);
        const hideButton = document.getElementById('hide' + cardContainer.id);
        showButton.style.display = "inline";
        hideButton.style.display = "none";
    }

    const start = (currentPage - 1) * cardsPerPage;
    const end = Math.min(start + cardsPerPage, cards.length);
    const containerSize = (cardWidth + cardMargin) * cardsPerPage + cardMargin;
    const width = Math.max(65, (window.innerWidth - containerSize)/2);
    cardContainer.style.borderLeft = width+(cardMargin/2) + "px solid transparent";
    cardContainer.style.borderRight = width-(cardMargin/2) + "px solid transparent";
    

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

document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', () => {
        const url = card.getAttribute('data-url');
        if (url != "None") {
            window.location.href = url;
        } else {

            // only occurs when there is no webpage setup with the club. It is the default page that all clubs will start with
            // Additional information to send with the GET request
            const additionalInfo = {
                className: card.querySelector('.class-name').innerText,
            };

            // Construct query parameters
            const queryParams = new URLSearchParams(additionalInfo).toString();
            const url = 'default'
            const fullUrl = `${url}?${queryParams}`;
        
            window.location.href = fullUrl;
        }
    });
});

// TODO make hide button at the end of the club cards as well
function showAll(cat) {
    // Makes the card container able to be manipulated
    const contain = document.getElementById(cat);
    contain.style.whiteSpace = "wrap";
    contain.style.flexWrap = "wrap";

    const showButton = document.getElementById('show' + cat);
    const hideButton = document.getElementById('hide' + cat);
    showButton.style.display = "none";
    hideButton.style.display = "inline";

    for (var child of contain.children) {
        child.style.display = "inline-block";
    }

}

function hideExtra(cat) {
    // Makes the card container able to be manipulated
    const contain = document.getElementById(cat);
    contain.style.whiteSpace = "nowrap";
    contain.style.flexWrap = "nowrap";

    renderCards(contain.parentNode, 1);
}

// Search functions are below
function searchClubs() {
    resetQuery();
    var input = document.getElementById('searchInput').value.toLowerCase(); // Get input value and convert to lowercase
    var cards = document.querySelectorAll('.card'); // Select all club cards

    cards.forEach(card => {
        var name = card.querySelector('.card-text').innerText.toLowerCase(); // Get club name and convert to lowercase
        var discription = card.querySelector('.card-description').innerText.toLowerCase(); // Get club name and convert to lowercase

        // Check if input matches club name or descriptiona
        if (name.includes(input) || discription.includes(input)) {
            card.style.display = ""; // Show club card
        } else {
            card.style.display = "none"; // Hide club card
        }
    });

    var cats = document.querySelectorAll('.card-container');
    cats.forEach(cat => {
        var containsCard = false
            for (var child of cat.children) {
                if (child.style.display == "none") {

                } else {
                    containsCard = true
                    break;
                }
            }
        if (!containsCard) {
            cat.style.display = "none"
            cat.parentNode.style.display = "none"
        }
        
    });


    toggleCategories(true);
}

function clearSearch() {
    resetQuery();
    document.getElementById('searchInput').value = '';
}

function resetQuery(){
    var cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        card.style.display = ""; // Show all club cards
    });

    // Shows everything
    var cats = document.querySelectorAll('.card-container');
    cats.forEach(cat => {
        cat.style.display = ""
        cat.parentNode.style.display = ""
    });

    toggleCategories(false);
}

function toggleCategories(hidden) {
    var categoryNames = document.querySelectorAll('.category-name');

    categoryNames.forEach(name => {
        if (hidden) {
            name.classList.add('hidden'); // Add a class to hide the category name
        } else {
            name.classList.remove('hidden'); // Remove the class to show the category name
        }
    });
}

function initializePagination() {
    cardWrappers.forEach(wrapper => {
        let currentPage = 1;
        wrapper.dataset.currentPage = currentPage;

        renderCards(wrapper, currentPage);
    });

    // attaches event listener
    const inputElement = document.getElementById('searchInput');
    inputElement.addEventListener('input', searchClubs);

}

document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', () => {
        const url = card.getAttribute('data-url');
        if (url != "None") {
            window.location.href = url;
        } else {
            // only occurs when there is no webpage setup with the club. It is the default page that all clubs will start with
            // Additional information to send with the GET request
            const additionalInfo = {
                className: card.querySelector('.club-name').innerText,
            };

            // Construct query parameters
            const queryParams = new URLSearchParams(additionalInfo).toString();
            const url = 'default'
            const fullUrl = `${url}?${queryParams}`;
        
            window.location.href = fullUrl;
        }
    });
});

window.addEventListener('resize', initializePagination);
window.addEventListener('DOMContentLoaded', initializePagination);
