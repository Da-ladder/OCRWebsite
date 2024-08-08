function toggleDropdown() {
    var contents = document.querySelectorAll('.sidebar-section');
    var arrow = document.getElementById('arr');
    if (contents[0].style.display != "block") {
        contents.forEach(content => {
            content.style.display = "block"
        })
        arrow.innerHTML = "&#9662;"; // Arrow pointing down
    } else {    
        contents.forEach(content => {
            content.style.display = "none"
        })
        arrow.innerHTML = "&#9656;"; // Arrow pointing to the right
    }
}

function initializePage() {
    // attaches event listener
    const inputElement = document.getElementById('show');
    inputElement.addEventListener('click', toggleDropdown);
}

window.addEventListener('DOMContentLoaded', initializePage);