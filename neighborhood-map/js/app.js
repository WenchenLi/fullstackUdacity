//NOW just assigning MVC to different function pieces

//MapView

/**
* @description Represents a mapview
* @constructor
*/
var MapView = function ()  {
  var pos;
  var map;
  var infowindow;
  var markers;
  var typeMarkersHashMap;
  var currentAnimateMarker;
};

/**
* @description initial map with current user location, a search box in the map use to go to other place
*/
MapView.prototype.initMapWithCurrentLocation  =  function(){
  var self = this;

  this.map = new google.maps.Map(document.getElementById('map-container'), {
    center: {lat: -33.867, lng: 151.195},
    scrollwheel: true,
    zoom:  15
  });
  this.infoWindow = new google.maps.InfoWindow({map: this.map});

  // add search area
  var input = document.getElementById('pac-input-neighborhood');
  var searchBox = new google.maps.places.SearchBox(input);
  // this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);//when want a compact view in the map
  this.map.addListener('center_changed', function() {
    console.log("center changed");
    // vm.initNewPlacesOnMap();
  });
  this.map.addListener('zoom_changed', function() {
    console.log("zoom changed");
    // vm.initNewPlacesOnMap();
  });
  // Bias the SearchBox results towards current map's viewport.
  this.map.addListener('bounds_changed', function() {
    console.log("bounds changed");
    searchBox.setBounds(self.map.getBounds());
    self.pos = {
      lat:self.map.getCenter().lat(),
      lng:self.map.getCenter().lng()
    };
    vm.initNewPlacesOnMap();
  });

  this.map.addListener('tilesloaded', function() {
    console.log("tiles loaded");
    vm.initNewPlacesOnMap();
  });
  searchBox.addListener('places_changed', function() {
    console.log("places_changed");
    var places = searchBox.getPlaces();
    if (places.length === 0) {
      return;
    }
    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(item) {
      var icon = {
        url: item.icon,
        size: new google.maps.Size(30, 30),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(10, 10),
        scaledSize: new google.maps.Size(10, 10)
      };

      if (item.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(item.geometry.viewport);
      } else {
        bounds.extend(item.geometry.location);
      }
    });
    self.map.fitBounds(bounds);
    self.map.setCenter(self.map.getCenter());
  });

  if (navigator.geolocation) {
    // in global scope again. so self
    navigator.geolocation.getCurrentPosition(function(position) {
      self.pos = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
      };
      self.infoWindow.setPosition(self.pos);
      self.infoWindow.setContent('Location found.');
      self.map.setCenter(self.pos);
    }, function() {
      handleLocationError(true, self.infoWindow, self.map.getCenter());
    });
  } else {
    // Browser doesn't support Geolocation
    handleLocationError(false, self.infoWindow, self.map.getCenter());
  }
};

/**
* @description Search nearby with current user location using google.maps.places.PlacesService
*               and place markers on the map with callback results and update ViewModel placeList
* @param {string} searchtext: the searchtext from the search box
*/
MapView.prototype.getAllPlacesOnMap = function() {
  // vm.availableTypes.removeAll();//this change got dilivered to the system, so init as below
  // vm.availableTypes.push("No Filter");
  vm.availableTypes(["No Filter"]);
  var self = this;
  console.log('MapView.prototype.getAllPlacesOnMap');
  var service = new google.maps.places.PlacesService(self.map);
  var currentTypes = types_all;
  self.typeMarkersHashMap = {};
  currentTypes.forEach(function(type){
    self.typeMarkersHashMap[type] =[];
  });
  currentTypes.forEach(function(type){
    service.nearbySearch({
      location: { lat: self.pos.lat, lng: self.pos.lng},
      radius: 1000, //TODO add to ui
      type: [type]
    },function(results, status) {
        console.log('MapView.nearbySearchCallback');
        if (status === google.maps.places.PlacesServiceStatus.OK) {
          vm.availableTypes.push(type);
          results.forEach(function(place){
            var marker = self.createMarker(place);
            self.typeMarkersHashMap[type].push(marker);
            vm.placeList.push(place);
          });
        }else{//hancle type not on the current map view
          console.log("No " + type + " is available at here.");
        }
      });
    });
};
/**
* @description create marker given place data and push marker to mapview.markers
* @param {Place} data - place:one of the callback results from nearbySearchCallback
*/
MapView.prototype.createMarker = function(place) {
  var self = this;
  console.log("MapView.createMarker");
  var marker = new google.maps.Marker({
    map: self.map,
    position: place.geometry.location,
    animation: google.maps.Animation.DROP
  });
  self.markers.push(marker);
  google.maps.event.addListener(marker, 'click', function() {
    self.infoWindow.setContent(place.name);
    self.infoWindow.open(self.map, this);
    vm.changePlace(place);
  });
  return marker;
};

/**
* @description // Sets the map on all markers in the array.
*/
MapView.prototype.setMapOnAll = function (map) {
  if (this.markers===undefined){
    this.marker = [];
  }else{
    this.markers.forEach(function(marker){
      marker.setMap(map);
      }
    );
  }
};

/**
* @description Removes the markers from the map, but keeps them in the array.
*/
MapView.prototype.clearMarkers = function() {
  this.setMapOnAll(null);
};

/**
* @description Shows any markers currently in the array.
*/
MapView.prototype.showMarkers = function() {
  this.setMapOnAll(this.map);
};

/**
* @description Deletes all markers in the array by removing references to them.
*/
MapView.prototype.deleteMarkers = function() {
  this.clearMarkers();
  this.markers = [];
};

/**
* @description Deletes all typeMarkersHashMap.
*/
MapView.prototype.deletetypeMarkers = function() {
  this.typeMarkersHashMap ={};
};
/**
* @description animate place corresponding marker using LatLng search TODO use hashmap
* @param {[float,float]} LatLng:[lat,lng]
*/
MapView.prototype.initNewPlacesOnMap = function(place){
  var tempmapview = this;
  var LatLng = [place.geometry.location.lat(),place.geometry.location.lng()];
  if (this.currentAnimateMarker){
    this.setMarkerAnimation(this.currentAnimateMarker,false);
  }

  this.markers.forEach(function(marker){
    if (marker.position.lat()==LatLng[0] && marker.position.lng()==LatLng[1]){
        tempmapview.setMarkerAnimation(marker,true);
    }
  });
  if (this.currentAnimateMarker===null){
    alert("sorry," + place.name + " is not marked on the map");
  }else{
    console.log("place found");
  }
};

/**
* @description toggle marker
* @param {marker} marker
* @param {boolean} state
*/
MapView.prototype.setMarkerAnimation = function(marker,state){
  if (state === true){
    marker.setAnimation(google.maps.Animation.BOUNCE);
    this.currentAnimateMarker = marker;
    var self = this;
    setTimeout(function(){
        marker.setAnimation(null);
    }, 1500);
  }else{
    marker.setAnimation(null);
    this.currentAnimateMarker = null;
  }
};

//M
/**
* @description Place data model
* @constructor
* @param {Place} data - place:one of the callback results from nearbySearchCallback
*/
var Place = function (data) {
    this.name = ko.observable(data.name);
    this.location = ko.observable(data.geometry.location);
    this.types = data.types;
};


//VM  view model has been described as a state of the data in the model
/**
* @description ViewModel to bind html
* @constructor
*/
var ViewModel = function () {
    var self = this;

    // this.searchtext = ko.observable("");

    this.hereNow = ko.observable("");

    self.filterText = ko.observable("");

    this.alert = ko.observable("");

    this.availableTypes = ko.observableArray(["No Filter"]);

    this.selectedType = ko.observable(this.availableTypes[0]);

    // this apply filter as dropdown
    this.applyFilter = function(){
      // console.log(self.selectedType());
      if (this.selectedType()==="No Filter"){
        mapview.setMapOnAll(mapview.map);
      }else{
        mapview.clearMarkers();
        mapview.typeMarkersHashMap[this.selectedType()].forEach(function(marker){
            marker.setMap(mapview.map);
        });
      }
    };

    this.placeList = ko.observableArray([]);

    initialPlaces.forEach(function(placeItem){
        self.placeList.push(new Place(placeItem));
    });

    this.currentPlace = self.placeList()[0];//ko.observable(self.placeList()[0]);

    this.changePlace = function(place){
      if (place ==self.currentPlace){//such way avoid unnecessary recompuation
        alert("Aren't you just asked for the same place?");
        return;
      }
    self.currentPlace = place;
    self.showInfo(place);
    };

    self.filteredList = ko.computed(function(){
        var filterText = self.filterText().toLowerCase();
        if (filterText===""){
          mapview.setMapOnAll(mapview.map);
        }else{
          mapview.clearMarkers();
          if (filterText in mapview.typeMarkersHashMap && mapview.typeMarkersHashMap[filterText].length>0){
            mapview.typeMarkersHashMap[filterText].forEach(function(marker){
                marker.setMap(mapview.map);
            });
          }
        }
        var targetList = [];
        if (self.placeList()){
          self.placeList().forEach(function(place){
            if (place.types.includes(filterText))targetList.push(place);
          });
        }
        if(targetList.length===0)self.alert("Sorry, this filter does not apply");
        else self.alert("");


        if (targetList.length!==0){
          mapview.clearMarkers();
          targetList.forEach(function(place){
          mapview.createMarker(place);
          });
        }
        return targetList;
    }, this);

    // self.alertWithTimeOut = ko.computed(function(text){
    //     console.log(self);
    //     self.alert(text);
    //     setTimeout(function(){
    //         self.alert("");
    //     }, 1000);
    // }, this);
};


/**
* @description bind for the search box, new search clears old markers in mapview and this.placeList
* @param {formElement} the html searchbox element
*/
ViewModel.prototype.initNewPlacesOnMap = function () {
  var self = this;
  this.placeList.removeAll();
  mapview.deleteMarkers();
  mapview.deletetypeMarkers();
  mapview.getAllPlacesOnMap();
};

/**
* @description get Foursquare data via ajax call, callback return count of people given the clicked place
* @param {place} current clicked place in the listView
*/
ViewModel.prototype.ajaxFourSquare = function (place) {
  var self = this;
  /* get Foursquare data via ajax call */
  $.ajax({
    type: 'GET',
    dataType: 'json',
    url: 'https://api.foursquare.com/v2/venues/search',
    data: 'client_id=' + client_id + '&client_secret=' + client_secret + '&v=20150815&ll=' + place.geometry.location.lat()+',' +place.geometry.location.lng()+'&limit=5',
    async: true,
    success: function(data) {
      var nameDistances = [];
      data.response.venues.forEach(function(item){
        var dist = Levenshtein.get(place.name,item.name);
        nameDistances.push(dist);
      });
      var index = indexOfMinValue(nameDistances);
      var minDist = nameDistances[index];
      if (minDist>3){
        alert("Sorry " + place.name + " is not registered at Foursquare.");
      }else{
        console.log(data.response.venues[index].name);
        self.hereNow("There are "+data.response.venues[index].hereNow.count + " people at " + data.response.venues[index].name);}
      },
    error: function(error) {
      alert('Foursquare data is not available');
    }
  });
};

/**
* @description show how many people are there (via AJAX request), bounce the marker once
* @param {placeItem} abstract level of play that can be put at listView and on the map
*/
ViewModel.prototype.showInfo = function (placeItem) {
    this.ajaxFourSquare(placeItem);
    mapview.initNewPlacesOnMap(placeItem);
};
/**
* @description handler for location error when location current user position
* @param {boolean} browserHasGeolocation
* @param {infoWindow} infoWindow
* @param {position} pos
*/
var handleLocationError = function(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
};

/**
* @description error handler for google map api
*/
var googleError = function() {
  alert("Sorry google map api is not working, try refresh please.");
};

/**
* @description find index of min element in array
* @param {array} array
* @return {int} index,
*/
var indexOfMinValue = function(array){
  var index = 0;
  var value = array[0];
  for (var i = 1; i < array.length; i++) {
    if (array[i] < value) {
      value = array[i];
      index = i;
    }
  }
  return index;
};
var initialPlaces = [
  {
    name:"Schuetzen Park",
    geometry:{location:{lat: 40.77641839999999, lng: -74.03310199999999}},
    types:["restaurant"]
  },
  {
    name:"The Skyline Hotel",
    geometry:{location:{lat: 40.7643802, lng: -73.9924603}},
    types:["hotel"]
  },
  {
    name:"Mandarin Oriental, New York",
    geometry:{location:{lat: 40.7690089, lng: -73.98301099999998}},
    types:["restaurant"]
  },
  {
    name:"The Empire Hotel",
    geometry:{location:{lat: 40.7714959, lng: -73.9826673}},
    types:["hotel"]
  },
  {
    name:"Trump International Hotel & Tower New York",
    geometry:{location:{lat: 40.7690287, lng: -73.98160899999999}},
    types:["hotel","point_of_interest"]
  }
];
var mapview = new MapView();
var vm = new ViewModel();
ko.applyBindings(vm);
