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

