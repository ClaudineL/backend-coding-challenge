# About the API

This API queries a list of Canadian and American cities in order to return the most likely match to the given query. For greater accuracy, latitude and longitude can be provided but are not mandatory.


### Functionality

* **Endpoint**: `/api/suggestions`
* **Mandatory parameter:**
    * `q`: search term to match
* **Optional parameters**:
    * `latitude`: latitude of query location
    * `longitude`: longitude of query location
* **Response**:
    * `200 OK`
    * Format: JSON containing array of scored matches in order of descending score
    * Fields:
        * Name: uniquely identifying city name
        * Coordinates (latitude and longitude)
        * Population
        * Score: between 0 and 1 (inclusive) indicating likelihood, with 1 being the most likely match
    * If no matches, returns an empty list.

#### Graphical UI
A graphical version of the API's documentation is available at [/api/ui](/api/ui). An example query response and testing functionality can be accessed there.

#### Form version
A web form version is available at [/form](/form). The web form calls the same code as the `api/suggestions` endpoint but returns the results as a table for easier visualization.

### Scoring algorithm
* The following criteria are used to order the matches:
    * **Letter proportion**: Proportion of letters matched in name. For example, searching for 'london' will return a proportion of `1` for the city of London, Ontario, but `0.55` for the city of Londontowne, Maryland.
    * **Distance**: Increasing distance to the provided coordinates. If no coordinates are provided, distance is set to 0 for all matches.
    * **Population**: Ties are ordered by descending order of population.

