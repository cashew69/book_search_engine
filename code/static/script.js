const searchInput = document.getElementById('search-input');
const suggestionsContainer = document.getElementById('suggestions-container');

const searchButton = document.getElementById('search-button'); // Get the search button




var content = '';
var selected = [];
// Event listener for input changes
searchInput.addEventListener('input', () => {
    const searchTerm = searchInput.value.toLowerCase();
    
    // Clear previous suggestions
    suggestionsContainer.innerHTML = '';
    // Send a POST request to the backend with the search term
    fetch('/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ searchTerm }),})
        .then((res) => res.json())
        .then(data => {
        // Display autocomplete suggestions from the server
        data.forEach(suggestion => {
            const suggestionElement = document.createElement('div');
            suggestionElement.classList.add('suggestion');
            suggestionElement.textContent = suggestion;
            suggestionElement.addEventListener('click', () => {
                searchInput.value = suggestion;
                selected = suggestion[0];
                suggestionsContainer.style.display = 'none';
            });
            suggestionsContainer.appendChild(suggestionElement);
        });

        // Show/hide suggestions container
        if (data.length > 0) {
            suggestionsContainer.style.display = 'block';
        } else {
            suggestionsContainer.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
    
});
searchButton.addEventListener('click', () => { // Add event listener to the search button
    const bookId = selected;
    
    // Send a GET request to the backend with the book_id in the URL
    fetch(`/book_id=${bookId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response)
    .then(data => {
        // Handle the response data as needed
        window.location.href = data.url
    })
    .catch(error => {
        console.error('Error:', error);
    });
    });    
