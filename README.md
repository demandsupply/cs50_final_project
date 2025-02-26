# MovieShowsDB
#### Video Demo:https://youtu.be/j-jA3RfNpRU
#### Description: a website which allows the user to compare different datas from movies/tv series using an Movie Database API.

FAQ
What will your software do?
	- extrapolate data from a movie/tv series the user input
	- shows the data in a table, allowing the user to sort it
	- allow the user to compare datas of different movies/tv shows
	- allow a registered user to create a favorite and watchlist lists for movies/shows

How will it be executed?
	- go to the project folder, then from the command-line type "Flask run"
	- additionally figure out how to upload the project on a server allowing the user to run it via url

What new skills will you need to acquire?
	- use of Ajax
	- eventually the use of APIs
	- improve sql skills
	- manage a medium-sized single person project

DETAILS
The website  mainly allows a user to search movies and shows and visit specified pages (using and API and the ID of the movie/show) where are shown all the important information about the movie/show, and then compare their ratings. The user can also register to the site and then login to unlock some new areas.

At the top of the main page there is a search bar which suggest matching titles of movies/shows as the user types in: this function was obtained using AJAX requests (similar to google search)
A normal user non signed in can:
- Visit the main page where he can:
	- use the search bar to look for movies and shows
	- scroll two carousels which display the most popular shows and movies of the moment (the two carousel have a width which will be related to the screen width - making them responsive and showing every time the right amount of items)
	- each time he visit the page a totally random movie and show are generated (every time the user visit the page a get request trigger a function whihc generates a random number which will be used as a random id to send to the api).
The main page (and other parts of the site) has many gentle css effects that respond to an user interaction (like mouse hovering), giving him instant feedback about its actions.

- Visit a specified compare movie page where he can compare up to ten movies. The rating of each movie will be displayed on a bar chart (obtained via ajax requests and displayed via Chart.js). Each time he hover a bar on the chart, on the bottom of the page will be displayed a box containing some info about the movie (title, year and plot). There is an analog compare shows page where the user can look for shows using the search bar and compare  the ratings of all the episodes of a show in a a scatter chart. The ratings of all episodes are obtained querying for each show more details to the API, and storing the rating in dicts and arrarys.
- Visit a page where are displayed the best 200 movies of all time

A registered user:
- have the possibility to save its favorite movies and shows in its "personal area"" page. From here he can have an overview of each “element” and he can decide to remove that element from the list.
- he also have access to a page where are displayed all databases data, and all stored elements into databases.

On App.py I've created many routes for the website, where usually every route has a GET and POST request. Some requests are used to fetch data from a free API (provided by THE MOVIE DB) which consist in movies and shows data; these data are used to answer specified queries from the user and, in some, cases, to store that data in a database. The database is locally created via SQLite and consist in different tables:
- a table to store all the registered accounts, their hashed passwords and id's
- more tables to store the favourite movies and tv shows of the users (and their watchlist). It is also possible for the user to remove the specified movie/show from the list clicking a button.


There is a layout html page used as a template for all the others html pages: using Jinja syntax, if the user is logged in the layout will be different than the layout of a user not logged in. Jinja syntax has also been used to display recurrent data (as for tables) dynamically on other pages.

For the styling no framework has been used, but all the aestetic of the site has been choosen and created from scratch (also the responsive part). The color palette is warm and elegant, meanwhile the font style is a standard and neutral one. The microinteraction effects are smooth and gentle, remembering the general site colors and style.
