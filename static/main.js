var currentResults = [];  // Store all search results
var displayedResults = 10;  // Number of results to display initially



function performSearch() {
    var query = document.getElementById('searchInput').value;

    $.ajax({
        type: 'POST',
        url: '/comparetvshows',
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
        if (result.name) {
            var dateStr = result.first_air_date;
            var dateArray = dateStr.split('-');
            link.textContent = "Tv: " + result.name + " (" + dateArray[0] + ")";  // Shows the tv show title and its year
            link.setAttribute('href', 'tvshow/'+ result.id);
    } else {
            var date2Str = result.release_date;
            var date2Array = date2Str.split('-');
            link.textContent = "Movie: " + result.title + " (" + date2Array[0] + ")";  // Shows the tv show title and its year
            link.setAttribute('href', 'movie/'+ result.id);
    }
        
        ul.appendChild(li);
        li.appendChild(link);
    });

    resultsContainer.appendChild(ul);
}


document.addEventListener('keyup', function(event) {
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
