//NOW just assigning MVC to different function pieces

//MapView
var MapView = {
   initMap : function(){
      map = new google.maps.Map(document.getElementById('map-container'), {
        center: {lat: -34.397, lng: 150.644},
        scrollwheel: false,
        zoom: 8
      });
      var infoWindow = new google.maps.InfoWindow({map: map});

      // Try HTML5 geolocation.
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
          var pos = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };

          infoWindow.setPosition(pos);
          infoWindow.setContent('Location found.');
          map.setCenter(pos);
        }, function() {
          handleLocationError(true, infoWindow, map.getCenter());
        });
      } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
      }
    },

   handleLocationError: function(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
  }
};

//Init/test data
var initialPlaces = [{
    name: "Little Manuels",
    lon: 38.00684,
    lat: -121.805525,
    content: "<div class='info'>Little Manuels</div>"
}, {
    name: "Hazels Drive-in",
    lon: 38.0127268,
    lat: -121.83241,
    content: "<div class='info'>Hazels Drive-in</div>"
}, {
    name: "Tao San Jin",
    lon: 37.9628493,
    lat: -121.7366144,
    content: "<div class='info'>Tao San Jin</div>"
}, {
    name: "Johnny Garlics",
    lon: 37.94536,
    lat: -121.742153,
    content: "<div class='info'>Johnny Garlics</div>"
}, {
    name: "In-N-Out Burger",
    lon: 37.955532,
    lat: -121.6194595,
    content: "<div class='info'>In-N-Out Burger</div>"
}, {
    name: "Bluefin Sushi",
    lon: 37.6058122,
    lat: -122.1113959,
    content: "<div class='info'>Bluefin Sushi</div>"
}, {
    name: "E.J.Phair",
    lon: 38.0330084,
    lat: -121.8846951,
    content: "<div class='info'>E.J.Phair</div>"
}];

//M
var Place = function (data) {
    this.name = ko.observable(data.name);
    this.imgSrc = ko.observable(data.imgSrc);
};

//VM
var ViewModel = function () {
    var map ;
    var infoWindow ;
    var self = this;

    this.placeList = ko.observableArray([]);
    initialPlaces.forEach(function(placeItem){
        self.placeList.push(new Place(placeItem));
    });

    this.currentPlace = ko.observable(self.placeList()[0]);

    this.changePlace = function(place){
      self.currentPlace(place);
    };

    function loadGoogleMaps(){
      var googleMaps = document.createElement("script");
      googleMaps.type = "text/javascript";
      googleMaps.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyCMcRmHm0M2Z_WoNneWdwUrawwZqJAvb4Q&libraries=places&callback=initMap";
      // googleMaps.setAttritube
      document.body.appendChild(googleMaps);
    }

    function initMap (){
        map = new google.maps.Map(document.getElementById('map-container'), {
          center: {lat: -34.397, lng: 150.644},
          scrollwheel: false,
          zoom: 8
        });
        var infoWindow = new google.maps.InfoWindow({map: map});

        // Try HTML5 geolocation.
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            map.setCenter(pos);
          }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }

    function handleLocationError(browserHasGeolocation, infoWindow, pos) {
      infoWindow.setPosition(pos);
      infoWindow.setContent(browserHasGeolocation ?
                            'Error: The Geolocation service failed.' :
                            'Error: Your browser doesn\'t support geolocation.');
    }

    this.searchNeighborhood = function (formElement) {
      var text = $(formElement).find( "input" ).val();
      console.log(text);
    };

    function submitText () {

    }

    function initMapWithSearch(){
      var pyrmont = {lat: -33.867, lng: 151.195};

      map = new google.maps.Map(document.getElementById('map-container'), {
        center: pyrmont,
        zoom: 15
      });

      infoWindow = new google.maps.infoWindow();
      var service = new google.maps.places.PlacesService(map);
      service.nearbySearch({
        location: pyrmont,
        radius: 500,
        type: ['store']
      }, nearbySearchCallback);
    }

    function nearbySearchCallback(results, status) {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
          createMarker(results[i]);
        }
      }
    }

    //create marker on the map for given place ,V
    function createMarker(place) {
      var placeLoc = place.geometry.location;
      var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
      });

      google.maps.event.addListener(marker, 'click', function() {
        infoWindow.setContent(place.name);
        infoWindow.open(map, this);
      });
    }

};

vm = new ViewModel();
ko.applyBindings(vm);
