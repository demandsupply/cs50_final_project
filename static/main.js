var currentResults = [];  // Store all search results
var displayedResults = 20;  

function performSearch() {
    var query = document.getElementById('searchInput').value;

    $.ajax({
        type: 'POST',
        url: '/ajax',
        data: { q: query },
        success: function(data) {
            currentResults = data.results;  

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
        li.textContent = result.title;  
        ul.appendChild(li);
    });

    resultsContainer.appendChild(ul);
}

document.getElementById('searchInput').addEventListener('keyup', function() {
    performSearch();
});