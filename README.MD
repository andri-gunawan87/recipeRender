# RECIPE

This Project is about Food Recipe. We can view, Search, Like, Comment and Share your own Recipe. Half of this web using Indonesian language, because all recipe are made from Indonesian food and im intend to target Indonesian people as user.

### Distinctiveness
This Project using most of the features from all previous project. The different from other project are my base data populated from external api. Im not import all the data. I only take enough objects to test all my site function. Im using data from https://github.com/tomorisakura/unofficial-masakapahariini-api as a seed in my database. So i can populate my database and test all my function without manually input data first.

I take 10 page from that site and, request.get parsing in json and input it into each field in my models. Each page contain 10 objects so my database had 100 recipes total plus with some recipes that I enter for testing purpose. My first plan is only make a web based only database from external database. But i think thats not enough. So i make a database based an external database, add "like counts" and "comments" feature on top of it. So my web can grow based user input and not depend on external database. Of course i give credit to all site which data im used

## Complexity
### Login/Register
My Project using same function from previous project, which using custom user models.
### New Recipe
Im using similiar function im using at e-commerce project. Include like, favorite, comments models. Because base database populated using api from external site, im not using field image to store recipe image, but using URLField. Im planning pushing this to free hosting site like heroku. Because space limitations in free hosting, im decided not to store image but url instead. In my plan, i will push another projects so storage space is important.

### Pagination
This feature introduced at mail projects. Im using same technique im using at previous database. Using it on profile and all recipe page and limited it to 8 objects so it can fit on web layout.

### Favorite
This is same feature with e-commerce project. You can add or remove recipe as favorite. You can see all favorite recipes on user profile page. You need login to using this feature.

### Like/Dislike
Because base data from external api didnt include like/dislike feature, im assign a random number (0, 100) for each recipe. You can only like or dislike once. After that button will disable and opposite button will enable after reload. For the first time both button will enable.

### Comments
Index page display three comments order by date regardless user. In profile page display all comments by user. In detail page display all comments for that recipe. You can add comments in each recipe and need login to use this feature.

### Search
Search feature is simple, using icontain commands and filter the database based the keyword. Im using pagination on search page and limit it by 5 because my database had 100+ objects and icontain commands can broaden search result

### Javascript
This web using some simple javascript code. Which is:

##### Slide
This code responsible for image slide in index page. Highlight in index page are defined by filter objects with highest like counts, limit it to three and display that objects image in index page.

##### toggleEllipsis
The description on detail page it long. At first, desc field in my models only take charfield with limit 200 char. But after i inspect, most of the recipe have more than 500 char. So i alter the field and changed it to textfield. As expected description on detail page take lots coloumn. So im using Ellipsis function to limit description to 4 coloumn and expand/toggle it when description text clicked.

##### Like/Dislike Counter
This is bit tricky. For counter value im not taking a value from template and directly add or subtract it, but fetch it from database using url + id and add/subtraction bassed button clicked. For this function only, i serialize recipe models so javascript can fetch it as json code. With this javascript function even there is a connection problem, the like value is still consisten and sync with value from database.

##### Add input form
Ingredient and step for making a dish is varied each recipe. So i cant make certain input for ingredients and cooks step. For this problem i make javascipt function button to make add input field for both ingredient and steps. Each field get collected by getlist commands and put it in my database in jsonfield. With jsonfield i can iterate it easily in my web.
### Front End
My web template mainly using Grid System Bootstrap. So i can plan layout better and meet the requirements for "mobile responsive". For mobile responsive, im using Firefox developer tool Responsive Design Mode to test it with different resolution. Im using side Navigation with custom Niconne Font from google because look fancy. The top navbar from previous projects looks common and lifeless. The default image for profile im using svg image from vecteezy.com. Because it has picture with different color im using viewbox to focus on particular picture. Like and Dislike icon are icon i get from Fontello.