
# Neighborhood-map
A neighborhood map using Model View ViewModel architecture based on knockout.js.
Supported features are growing!

## Dependcies
* [knockout.js](http://knockoutjs.com/)
* [levenshtein.js](https://github.com/hiddentao/fast-levenshtein) (used to get edit distance between place names)

## Features includes:

* seperate model, view using controller/ViewModel, knockout.js helps with updating view once observable data changed defined in the controller/ViewModel.
* use google map api to locate the neighborhood area
* use knockout.js to keep track of the filter and update the view in map
* foursquare api tell the current number of people check-in onclick the name of the place in the listView.
* A filter based on the types of the place.
## Quick Run
To test the implementation please navigate the root folder of the project
and to setup the localhost use:

```python -m SimpleHTTPServer 8000```

then open your webbrowser type ```127.0.0.1:8000```

please change to other port if 8000 if taken.
