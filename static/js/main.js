
// change the turkish formatting number string to float number
function changenumberformat(inputnumber){
	var output= inputnumber.replace(',','.');
	return parseFloat(output);
}