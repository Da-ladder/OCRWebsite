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

// TODO: get new posts when they appear from the server
function openDropdown(postID) {
    document.getElementById(postID).style.display = "flex";
}

function closeDropdown(postID) {
    document.getElementById(postID).style.display = "none";
}

// Function to auto expand textarea
function autoExpand(field) {
    // Reset the height of the field to auto to calculate the new scroll height
    field.style.height = 'auto';
    // Set the height of the field to the scroll height
    field.style.height = field.scrollHeight + 'px';
}

// Add input event listener to all textareas
document.addEventListener('input', function (event) {
    if (event.target.tagName.toLowerCase() === 'textarea') {
        autoExpand(event.target);
    }
});

function openPostCreator() {
    const postMakerOpener = document.getElementById("post-button");
    const postMaker = document.getElementById("post-creator");

    postMakerOpener.style.display = "none";
    postMaker.style.display = "";
}

function closePostCreator() {
    const postMakerOpener = document.getElementById("post-button");
    const postMaker = document.getElementById("post-creator");

    postMakerOpener.style.display = "";
    postMaker.style.display = "none";
}

function deletePost(postID) {
    document.getElementById("postKey").value = postID;
    document.getElementById("deletePost").submit();
}

function submitForm() {
    // Verify that there is something in the title and body before submission
    const title = document.getElementById("newPostTitleInput");
    const body = document.getElementById("newPostbodyInput");

    console.log(title.value)
    console.log(body.value)

    if (title.value == "" || body.value == "") {
        document.getElementById("userErrorMessage").style.display = "";
    } else {
        // submit the form with the information provided
        document.getElementById('newPostTitle').value = title.value;
        document.getElementById('newPostBody').value = body.value;
        // Submit the form
        document.getElementById('postCreateForm').submit();
    }
}

function initializePage() {
    // attaches event listener
    const inputElement = document.getElementById('show');
    inputElement.addEventListener('click', toggleDropdown);
}

window.addEventListener('DOMContentLoaded', initializePage);