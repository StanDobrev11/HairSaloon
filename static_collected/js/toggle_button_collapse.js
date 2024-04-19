document.addEventListener('DOMContentLoaded', function () {
    // Select all toggle buttons
    const toggleButtons = document.querySelectorAll('.toggle-button');

    // Function to toggle display of corresponding div
    function toggleDisplay(event) {
        // The next sibling of the button which is the div that should be shown/hidden
        const contentDiv = event.target.nextElementSibling;
        const isDisplayed = contentDiv.style.display === 'block';
        contentDiv.style.display = isDisplayed ? 'none' : 'block';
    }

    // Attach click event listener to each toggle button
    toggleButtons.forEach(button => {
        button.addEventListener('click', toggleDisplay);
    });
});
