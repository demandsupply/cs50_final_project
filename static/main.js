
function performShowSearch() {
    var query = document.getElementById('searchShowInput').value;

    $.ajax({
        type: 'POST',
        url: '/comparetvshows',
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
    var resultsContainer = document.getElementById('searchResults');
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = 'No results found.';
        return;
    }

    var ul = document.createElement('ul');
    ul.classList.add("results");
    results.forEach(function(result) {
        var li = document.createElement('li');
        var link = document.createElement('a');
        var dateStr = result.first_air_date || '';
        var year = dateStr.split('-', 1)[0];
        link.textContent = result.name + " (" + year + ")";  // Shows the tv show title and its year
        link.setAttribute('href', 'tvshow/'+ result.id);

        
        ul.appendChild(li);
        li.appendChild(link);
    });

    resultsContainer.appendChild(ul);

    // close results div if the user clicks outside the div
    window.addEventListener("click", function(e) {
        if (e.target != document.querySelector(".results")) {
            ul.remove();
        }
    });
}

function performSearch() {
    var query = document.getElementById('searchInput').value;

    $.ajax({
        type: 'POST',
        url: '/',
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
    ul.classList.add("results");
    results.forEach(function(result) {
        var li = document.createElement('li');
        var link = document.createElement('a');
        if ((result.name)) {
            var dateStr = result.first_air_date || '';
            var year = dateStr.split('-', 1)[0];
            link.textContent = "Tv: " + result.name + " (" + year + ")";  // Shows the tv show title and its year
            link.setAttribute('href', 'tvshow/'+ result.id);
        } else {
                var date2Str = result.release_date || '';
                var year2 = date2Str.split('-', 1)[0];
                link.textContent = "Movie: " + result.title + " (" + year2 + ")";  // Shows the tv show title and its year
                link.setAttribute('href', 'movie/'+ result.id);
        }
        
        ul.appendChild(li);
        li.appendChild(link);
    });

    resultsContainer.appendChild(ul);

    // close results div if the user clicks outside the div
    window.addEventListener("click", function(e) {
        if (e.target != document.querySelector(".results")) {
            ul.remove();
        }
    });
}

// if (document.getElementById("searchMovieInput")) {
//     document.addEventListener('keyup', function(event) {
//         performMovieSearch(); 
//     });
// } else if (document.getElementById("searchShowInput")) {
//     document.addEventListener('keyup', function(event) {
//         performShowSearch(); 
//     });
// } else {
//     document.addEventListener('keyup', function(event) {
//         performSearch();
//     });
// }

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

// show/hide navbar menu onclick 
function navToggle() {
    var responsiveNav = document.getElementById("myResponsiveNav");
    if (responsiveNav.classList.contains ("responsive")) {
        responsiveNav.classList.remove("responsive");
    } else {
        responsiveNav.classList.add("responsive");
    }
}

// Carousel functions
if (document.getElementById("movieCarouselList")) {
    const prevbtn = document.getElementById('movieBtnPrev');
    const nextbtn = document.getElementById("movieBtnNext");
    const list = document.getElementById("movieCarouselList");
    const listElements = document.getElementById("movieCarouselList").children;

    // Obtain the with of the carousel item
    const firstItemStyle = window.getComputedStyle(listElements[0]);
    const itemWidthStr = firstItemStyle.getPropertyValue("width");
    const itemWidth = Number(itemWidthStr.substring(0, itemWidthStr.length-2))
    let listWidth = list.offsetWidth;

    // On smaller screens the buttons will scroll less
    if (window.innerWidth < 641) {
        listWidth = itemWidth * 2;
    }

    // Clicknig on buttons will scroll the carousel
    prevbtn.addEventListener("click", ()=> {
        list.scrollLeft -= (listWidth - itemWidth);
    })
    nextbtn.addEventListener("click", ()=> {
        list.scrollLeft += (listWidth - itemWidth);
    })
}

if (document.getElementById("showCarouselList")) {
    const prevbtn = document.getElementById('showBtnPrev');
    const nextbtn = document.getElementById("showBtnNext");
    const list = document.getElementById("showCarouselList");
    const listElements = document.getElementById("showCarouselList").children;

    // Obtain the with of the carousel item
    const firstItemStyle = window.getComputedStyle(listElements[0]);
    const itemWidthStr = firstItemStyle.getPropertyValue("width");
    const itemWidth = Number(itemWidthStr.substring(0, itemWidthStr.length-2))
    let listWidth = list.offsetWidth;

    // On smaller screens the buttons will scroll less
    if (window.innerWidth < 641) {
        listWidth = itemWidth * 2;
    }

    // Clicknig on buttons will scroll the carousel
    prevbtn.addEventListener("click", ()=> {
        list.scrollLeft -= (listWidth - itemWidth);
    })
    nextbtn.addEventListener("click", ()=> {
        list.scrollLeft += (listWidth - itemWidth);
    })
}


// Refreshing the page reset the carousel index
window.onload = function() {
    const movieList = document.getElementById("movieCarouselList");
    const showList = document.getElementById("showCarouselList");

    movieList.scrollLeft = 0;
    showList.scrollLeft = 0;
}


// function addOrRemove() {
//     var adremove = document.getElementById('adremove');
//     if (adremove.value =='add') {
//         adremove.value = 'aaaa';
//     } else {
//         adremove.value ='bbbbb';
//     }
// }
