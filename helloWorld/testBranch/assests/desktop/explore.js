// New things

document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', () => {
        const url = card.getAttribute('data-url');
        if (url != "None") {
            window.location.replace(location.host + url);
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

    document.querySelectorAll('.catButton').forEach(button => {
        button.style.color = ""
    });

    var button = document.getElementById("All");
    button.style.color = "yellow"
}

function initializePagination() {
    // Sees if buttons are required
    catButtoninit();

    // attaches event listener
    const inputElement = document.getElementById('searchInput');
    inputElement.addEventListener('input', searchClubs);

    // Sets all button to be yellow
    var button = document.getElementById("All");
    button.style.color = "yellow"
}

function catButtoninit() {
    var catNav = document.getElementById("categoryNav");
    var maxWidth = catNav.getBoundingClientRect().width;
    var bottomNav = document.getElementById("botNav");

    // Sees how much width all catButtons(TM) will take up
    var totalWidth = 0;
    document.querySelectorAll('.catButton').forEach(button => {
        totalWidth += button.getBoundingClientRect().width;
    });

    const prevBtn = document.querySelector('.prev-btn');
    const nextBtn = document.querySelector('.next-btn');

    if (totalWidth > maxWidth) {
        // make em buttons appear
        prevBtn.classList.remove('disabled');
        nextBtn.classList.remove('disabled');
        bottomNav.style.scrollMarginRight = "20px"

    } else {
        prevBtn.classList.add('disabled');
        nextBtn.classList.add('disabled');
    }

}

function filterClubs(catName) {
    // Sets all buttons to white
    document.querySelectorAll('.catButton').forEach(button => {
        button.style.color = ""
    });

    // Sets category button to yellow
    var button = document.getElementById(catName);
    button.style.color = "yellow"

    // Makes all clubs in that category show up
    document.querySelectorAll('.card').forEach(card => {
        var categories = Array.from(card.getAttribute("data-tags").split(",  "))
        for (var i = 0; i < categories.length; i++) {
            // could be optimized as it is changing the diplay every tag it runs but eh
            if (categories[i] == catName || catName == "All") {
                card.style.display = "";
                break;
            } else {
                card.style.display = "none";
            }
        }
    });
}

function moveLeft(){
    var element = document.getElementById("categoryNav");
    element.scrollLeft = element.scrollLeft - 500;
}

function moveRight(){
    var element = document.getElementById("categoryNav");
    element.scrollLeft = element.scrollLeft + 500;

}

document.querySelectorAll('.card').forEach(card => {
    card.addEventListener('click', () => {
        const url = card.getAttribute('data-url');
        if (1 == 2) { //url != "None" FIX THIS LATER
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

window.addEventListener('DOMContentLoaded', initializePagination);
