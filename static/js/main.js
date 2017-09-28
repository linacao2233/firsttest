
// change the turkish formatting number string to float number
function changenumberformat(inputnumber){
	var output= inputnumber.replace(',','.');
	return parseFloat(output);
}

// google map related functions

function setMapOnAll(markers, map) {
	for (var i=0; i< markers.length; i++) {
		markers[i].setMap(map);
	}
}

function clearMarkers(markers) {
	setMapOnAll(markers, null);
}

