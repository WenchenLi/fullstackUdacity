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
  // var service;
  var markers = [];
  var currentAnimateMarker;
};

/**
* @description initial map with current user location, a search box in the map use to go to other place
*             TODO sometimes current location is off a lot refer to my udacity forum question
*             https://discussions.udacity.com/t/navigator-geolocation-get-wrong-current-location/175372/3
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
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);
  this.map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  this.map.addListener('bounds_changed', function() {
    searchBox.setBounds(self.map.getBounds());
    self.pos = {
      lat:self.map.getCenter().lat(),
      lng:self.map.getCenter().lng()
    };
    //change bounds init new search neighborhood with empty string
    vm.searchNeighborhood();
  });
  searchBox.addListener('places_changed', function() {

    var places = searchBox.getPlaces();
    if (places.length === 0) {
      return;
    }
    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(item) {
      var icon = {
        url: item.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      if (item.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(item.geometry.viewport);
      } else {
        bounds.extend(item.geometry.location);
      }
    });
    self.map.fitBounds(bounds);
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

      vm.searchNeighborhood();//search all nearby by using empty search text
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
*               TODO self.createMarker should be called from ViewModel not here remember MVVM
*               comments: since google map api binding is not required here, so directly createMarker within callback
* @param {string} searchtext: the searchtext from the search box
*/
MapView.prototype.searchMap = function(searchtext) {
  var self = this;
  console.log('MapView.prototype.searchMap with text: '+searchtext);
  console.log(self.pos);
  console.log(searchtext);
  var service = new google.maps.places.PlacesService(self.map);
  service.nearbySearch({
    location: { lat: self.pos.lat, lng: self.pos.lng},
    radius: 1000,//TODO add to ui
    type: [searchtext]
  }, function(results, status) {
    console.log('MapView.nearbySearchCallback');
    console.log(status);
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      if (vm.placeList.length===0){//clear all markers for new search results
        self.deleteMarkers();
      }
      results.forEach(function(place){
        self.createMarker(place);
        vm.placeList.push(place);
      });
    }else{
      console.log("google.maps.places.PlacesServiceStatus not ok");
    }
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
    // if (marker.getAnimation() !== null) {
    //   self.setMarkerAnimation(marker,false);
    // } else {
    //   self.setMarkerAnimation(marker,true);
    // }
  });
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
* @description animate place corresponding marker using LatLng search TODO use hashmap
* @param {[float,float]} LatLng:[lat,lng]
*/
MapView.prototype.animatePlaceWithLatLng = function(LatLng){
  var tempmapview = this;
  if (this.currentAnimateMarker){
    this.setMarkerAnimation(this.currentAnimateMarker,false);
  }

  this.markers.forEach(function(marker){
    if (marker.position.lat()==LatLng[0] && marker.position.lng()==LatLng[1]){
        tempmapview.setMarkerAnimation(marker,true);
    }
  });
  if (this.currentAnimateMarker===null){
    alert("sorry, this place is not marked on the map");
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
};


//VM  view model has been described as a state of the data in the model
/**
* @description ViewModel to bind html
* @constructor
*/
var ViewModel = function () {
    var self = this;

    this.searchtext = ko.observable("");

    this.placeList = ko.observableArray([]);

    initialPlaces.forEach(function(placeItem){
        self.placeList.push(new Place(placeItem));
    });

    this.currentPlace = self.placeList()[0];//ko.observable(self.placeList()[0]);

    this.changePlace = function(place){
      if (place ==self.currentPlace){
        alert("you just click the same place");
        return;
      }
      self.currentPlace = place;
      var curLatLng = [place.geometry.location.lat(),place.geometry.location.lng()];
      mapview.animatePlaceWithLatLng(curLatLng);
    };

};

/**
* @description bind for the search box, new search clears old markers in mapview and this.placeList
* @param {formElement} the html searchbox element
*/
ViewModel.prototype.searchNeighborhood = function (formElement) {
  var text = $(formElement).find( "input" ).val();
  this.placeList.removeAll();
  mapview.deleteMarkers();
  mapview.searchMap(text);
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

var initialPlaces = [];
var mapview = new MapView();
var vm = new ViewModel();
ko.applyBindings(vm);
