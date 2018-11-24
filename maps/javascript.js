// Initialize and add the map
var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
var labelIndex = 0;
var icons = ['http://maps.google.com/mapfiles/ms/icons/green-dot.png', 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png','http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'];
var iconIndex=0;

//Map initialization
var lausanne = {lat:46.537504, lng: 6.613019}

//Origin destinations
var city_A = {lat: 48.866, lng: 2.333}; //Paris
var city_B = {lat: 40.416775, lng: -3.70379}; //Madrid
var city_C = {lat: 50.85034, lng: 4.35171}; //Brussels

// Variable "calculation" set to 0 before the routing algorithm runs
// Variable set to 1 if algortihm has run
var calculation = 1;

var dest_A = {lat: 41.9027835, lng: 12.4963655}; //Rome
var dest_B = {lat: 55.676097, lng: 12.568337}; //Copenhagen
  
var origin_cities = [city_A, city_B, city_C];
var destination_cities = [dest_A, dest_B];

function initMap(calculation) {
	// The map, centered at lausanne
	var map = new google.maps.Map(
      document.getElementById('map'), {zoom: 4, center: lausanne});
	  
	// Markers positioned at the different origin cities
	//var count = origin_cities.length;
	for (var i = 0; i<origin_cities.length; i++) {
		var city = origin_cities[i];
		var marker = new google.maps.Marker({position: city, label: labels[labelIndex++ % labels.length], map: map}); 
	};
	if (calculation != 0) {
		for (var i = 0; i<destination_cities.length; i++) {
			var city = destination_cities[i];
			var marker = new google.maps.Marker({
				position: city,
				icon: icons[iconIndex++ % icons.length],
				map: map,
				title : 'Test' });
		}
	}
}
