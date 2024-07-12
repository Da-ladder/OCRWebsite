// MOBILE SITE USE ONLY

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

// Search functions are below
function searchClubs() {
    resetQuery();
    toggleAll(false);
    var input = document.getElementById('searchInput').value.toLowerCase(); // Get input value and convert to lowercase

    var cards = document.querySelectorAll('.card'); // Select all club cards

    cards.forEach(card => {
        var name = card.querySelector('.class-name').innerText.toLowerCase(); // Get club name and convert to lowercase

        // Check if input matches club name or descriptiona
        if (name.includes(input)) {
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

    var drops = document.querySelectorAll('.dropdown-content')
    toggleAll(true);

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

function toggleAll(onOff) {
    // false or off is down
    var drops = document.querySelectorAll('.dropdown-content');
    var arrows = document.querySelectorAll('.arrow');

    drops.forEach(dropdown => {
        if (onOff){
            dropdown.style.display = 'none';
        } else {
            dropdown.style.display = 'flex';
        }
    })

    arrows.forEach(arrow => {
        if (onOff){
            arrow.innerHTML = "&#9656;"; // Arrow pointing to the right
        } else {
            arrow.innerHTML = "&#9662;"; // Arrow pointing down
        }
    })
}

function toggleDropdown(dropID, arrID) {
    var content = document.getElementById(dropID);
    var arrow = document.getElementById(arrID);
    if (content.style.display === "flex") {
        content.style.display = "none";
        arrow.innerHTML = "&#9656;"; // Arrow pointing to the right
    } else {
        content.style.display = "flex";
        arrow.innerHTML = "&#9662;"; // Arrow pointing down
    }
}

function initializePage() {
    // attaches event listener
    const inputElement = document.getElementById('searchInput');
    inputElement.addEventListener('input', searchClubs);
}

window.addEventListener('DOMContentLoaded', initializePage);


