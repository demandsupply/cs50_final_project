var currentResults = [];  // Store all search results
var displayedResults = 20;  // Number of results to display initially


function performMovieSearch() {
    var query = document.getElementById('searchMovieInput').value;

    $.ajax({
        type: 'POST',
        url: '/ajax',
        data: { q: query },
        success: function(data) {
            currentResults = data.results;  // Assuming your API response has a 'results' property

            // Display the first 'displayedResults' results
            displayMovieResults(currentResults.slice(0, displayedResults));
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function displayMovieResults(results) {
    var resultsContainer = document.getElementById('searchMovieResults');
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
        var date = result.release_date;
        year = date.split('-')[0]
        link.textContent = result.title + " (" + year + ")";  // Shows the movie title and its year
        ul.appendChild(li);
        li.appendChild(link);
    });

    resultsContainer.appendChild(ul);
}


function performShowSearch() {
    var query = document.getElementById('searchShowInput').value;

    $.ajax({
        type: 'POST',
        url: '/comparetvshow',
        data: { q: query },
        success: function(data) {
            currentResults = data.results;  // Assuming your API response has a 'results' property

            // Display the first 'displayedResults' results
            displayShowResults(currentResults.slice(0, displayedResults));
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function displayShowResults(results) {
    var resultsContainer = document.getElementById('searchShowResults');
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = 'No results found.';
        return;
    }

    var ul = document.createElement('ul');
    results.forEach(function(result) {
        var li = document.createElement('li');
        var link = document.createElement('a');
        link.setAttribute('href', 'tvshow/'+ result.id);
        link.textContent = result.name;  // Shows the tv show title and its year
        ul.appendChild(li);
        li.appendChild(link);
    });

    resultsContainer.appendChild(ul);
}


document.addEventListener('keyup', function(event) {
    if(event.target.id === 'searchMovieInput') {
        performMovieSearch();
    } else if(event.target.id === 'searchShowInput') {
        performShowSearch();
    }
});



function showBox() {
    var toggle = document.getElementById('loginChild');
    if (toggle.style.display === 'block') {
        toggle.style.display = 'none';
    } else {
        toggle.style.display = 'block';
    }
}

function seasonToggle(season) {
    // alert("button pressed " + season)
    button_show = document.getElementById("button-" + season);
    table = document.getElementById("table-" + season);
    if (table.style.display === 'block') {
        table.style.display = 'none';
    } else {
        table.style.display = 'block';
        }
}

// function addOrRemove() {
//     var adremove = document.getElementById('adremove');
//     if (adremove.value =='add') {
//         adremove.value = 'aaaa';
//     } else {
//         adremove.value ='bbbbb';
//     }
// }
