# React Component Tree #
This file shows how the react components relate to each other.

```
App.jsx
├── Map.jsx                  # the left side of the screen that displays openstreet map api
├──── CensusTiles.jsx        # the vector tiles that are displayed on the map
├──── LocationSearch.jsx     # the search bar at the top to search for finding locations
├──── Legend.jsx             # the legend that is displayed in the bottom right of the map
├── CensusForm.jsx           # the right side of the screen that handles the user input form
├──── YearGeoForm.jsx        # the options relating to the census year and geographic level
├──── ColourControl.jsx      # the options relating to the colours of the tiles on the map
├──── SearchBar.jsx          # the search bar just above the list of characteristics used to filter characteristics
├──── CharacteristicNode.jsx # the list of characteristics displayed in the bottom right
```