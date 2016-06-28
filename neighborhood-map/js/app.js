//NOW just assigning MVC to different function pieces

//MapView
var MapView = function ()  {
  var pos;
  var map;
  var infowindow;
  var service;
};

MapView.prototype.initMapWithCurrentLocation  =  function(){
  var self = this;
  this.map = new google.maps.Map(document.getElementById('map-container'), {
    center: {lat: -33.867, lng: 151.195},
    scrollwheel: true,
    zoom:  15
  });
  this.infoWindow = new google.maps.InfoWindow({map: this.map});

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

MapView.prototype.searchMap = function(searchtext) {
  var self = this;
  var geocoder =new google.maps.Geocoder();
  console.log('MapView.prototype.searchMap');
  self.service = new google.maps.places.PlacesService(self.map);
  console.log('new map service with text: '+searchtext);
  self.service.nearbySearch({
    location: { lat: self.pos.lat, lng: self.pos.lng},
    radius: 1000,//TODO add to ui
    type: [searchtext]
  }, function(results, status) {
    console.log('MapView.nearbySearchCallback');
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      results.forEach(function(place){
        self.createMarker(place);
      });
    }else{
      console.log("google.maps.places.PlacesServiceStatus not ok");
    }
  });
};

MapView.prototype.createMarker = function(place) {
  var self = this;
  console.log("MapView.createMarker");
  var marker = new google.maps.Marker({
    map: self.map,
    position: place.geometry.location,
    animation: google.maps.Animation.DROP
  });
  google.maps.event.addListener(marker, 'click', function() {
    self.infoWindow.setContent(place.name);
    self.infoWindow.open(self.map, this);
    if (marker.getAnimation() !== null) {
      marker.setAnimation(null);
    } else {
      marker.setAnimation(google.maps.Animation.BOUNCE);
    }
  });
};

//M
var Place = function (data) {
    this.name = ko.observable(data.name);
    this.location = ko.observable(data.geometry.location);
    // this.imgSrc = ko.observable(data.imgSrc);
};

//VM
var ViewModel = function () {
    var self = this;

    this.searchtext = ko.observable("store");

    this.placeList = ko.observableArray([]);

    initialPlaces.forEach(function(placeItem){
        self.placeList.push(new Place(placeItem));
    });

    this.currentPlace = ko.observable(self.placeList()[0]);

    this.changePlace = function(place){
      self.currentPlace(place);
    };
};

ViewModel.prototype.searchNeighborhood = function (formElement) {
  var text = $(formElement).find( "input" ).val();
  mapview.searchMap(text);//TODO what if to be more general i want to refer to a instance of MapView
};

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
