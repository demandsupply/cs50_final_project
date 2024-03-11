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
        var link = document.createElement('a');
        link.setAttribute('href', 'movie/'+ result.id);
        link.textContent = result.title;  // Adjust based on your API response structure
        ul.appendChild(li);
        li.appendChild(link);
    });

    resultsContainer.appendChild(ul);
}

document.getElementById('searchInput').addEventListener('keyup', function() {
    performSearch();
});




function showBox() {
    var toggle = document.getElementById('loginChild');
    if (toggle.style.display === 'block') {
        toggle.style.display = 'none';
    } else {
        toggle.style.display = 'block';
    }
}
