//ChatGPT carries lo
document.querySelectorAll('.class-card').forEach(card => {
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
            const url = 'clubs/default'
            const fullUrl = `${url}?${queryParams}`;
        
            window.location.href = fullUrl;
        }
    });
});

// static/classCards.js

document.querySelectorAll('.navigation').forEach(nav => {
    const row = nav.previousElementSibling.querySelector('.clubs-row');
    const scrollStep = row.clientWidth; // Adjust this as needed based on your design

    let scrollPosition = 0;

    nav.querySelector('.button-left').addEventListener('click', () => {
        scrollPosition -= scrollStep;
        if (scrollPosition < 0) {
            scrollPosition = 0;
        }
        row.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
    });

    nav.querySelector('.button-right').addEventListener('click', () => {
        scrollPosition += scrollStep;
        if (scrollPosition > row.scrollWidth - row.clientWidth) {
            scrollPosition = row.scrollWidth - row.clientWidth;
        }
        row.scrollTo({
            left: scrollPosition,
            behavior: 'smooth'
        });
    });
});
// search.js

function searchClubs() {
    var input = document.getElementById('searchInput').value.toLowerCase(); // Get input value and convert to lowercase
    var cards = document.querySelectorAll('.class-card'); // Select all club cards
    cards.forEach(card => {
        var name = card.querySelector('.class-name').innerText.toLowerCase(); // Get club name and convert to lowercase

        // Check if input matches club name or descriptiona
        if (name.includes(input)) {
            card.style.display = ""; // Show club card
        } else {
            card.style.display = "none"; // Hide club card
        }
    });
    toggleCategories(true);
}

function resetQuery(){
    document.getElementById('searchInput').value = '';
    var cards = document.querySelectorAll('.class-card');

    cards.forEach(card => {
        card.style.display = ""; // Show all club cards
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



