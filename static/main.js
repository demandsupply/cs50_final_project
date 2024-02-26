var currentResults = [];  // Store all search results
var displayedResults = 20;  // Number of results to display initially

function performSearch() {
    var query = document.getElementById('searchInput').value;

    $.ajax({
        type: 'POST',
        url: '/ajax',
        data: { q: query },
        success: function(data) {
            currentResults = data.results;  // Assuming your API response has a 'results' property

            // Display the first 'displayedResults' results
            displayResults(currentResults.slice(0, displayedResults));
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function displayResults(results) {
    var resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = 'No results found.';
        return;
    }

    var ul = document.createElement('ul');
    results.forEach(function(result) {
        var li = document.createElement('li');
        li.textContent = result.title;  // Adjust based on your API response structure
        ul.appendChild(li);
    });

    resultsContainer.appendChild(ul);
}

document.getElementById('searchInput').addEventListener('keyup', function() {
    performSearch();
});