// JavaScript code

var curr_occupancy = ""
var saved_competencies = []




function search_course() {
	let input = document.getElementById('searchbar').value
	input = input.toLowerCase();
	let x = document.getElementsByClassName('course');

	for (i = 0; i < x.length; i++) {
		if (!x[i].innerHTML.toLowerCase().includes(input)) {
			x[i].style.display = "none";
		} else {
			x[i].style.display = "list-item";
		}
	}
}

function filterCourses() {
	const selected = document.querySelectorAll('#competency-select option:checked');
	const values = Array.from(selected).map(el => el.value);

	var params = "?";
	for (const value of values) {
		params = params + "skill=" + encodeURIComponent(value) + "&"
	}
	params = params.substring(0, params.length - 1)
	// All the elements of the array the array 
	// is being printed.
	var xhttp = new XMLHttpRequest();
	var data;
	xhttp.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			data = this.responseText;
			console.log(data);
			var coursesResponse = JSON.parse(data);
			let x = document.getElementsByClassName('course');
			for (i = 0; i < x.length; i++) {
				x[i].style.display = "none";
			}
			for (var j = 0; j < coursesResponse.length; j++) {
				var course = coursesResponse[j];
				// console.log(course.course_name);
				for (i = 0; i < x.length; i++) {
					if (x[i].innerHTML.includes(course.course_name)) {
						x[i].style.display = "list-item";
					}
				}
			}
		}
	};
	xhttp.open("GET", "http://localhost:5001/courses" + params, true);
	xhttp.setRequestHeader("Content-type", "application/json");
	xhttp.send(null);



}


function clearFilter() {
	let x = document.getElementsByClassName('course');
	for (i = 0; i < x.length; i++) {
		x[i].style.display = "list-item";
	}
	var elementsCompetencies = document.getElementById("competency-select").options;
	for (var i = 0; i < elementsCompetencies.length; i++) {
		elementsCompetencies[i].selected = false;
	}
}


function saveCompetenices() {
	var items = document.getElementsByName("skill");
	var selectedItems = [];
	for (var i = 0; i < items.length; i++) {
		if (items[i].type == "checkbox" && items[i].checked == true) selectedItems.push(items[i].value);
	}
	console.log(selectedItems);
	setSavedCompetencies(selectedItems)
	
}

function setSavedCompetencies(s) {
	saved_competencies = s
}

function getOccupancy() {
	var sel = document.getElementById("occupency-select")
	var occupancy = sel.options[sel.selectedIndex].text
	console.log(sel.options[sel.selectedIndex].text)


	let xhr = new XMLHttpRequest();
	xhr.open('get', 'http://localhost:5001/occupationsuri?occupation=' + encodeURIComponent(occupancy), true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.send();

	xhr.onload = function() {
	    curr_occupancy = JSON.parse(xhr.response)[0][0]
	}
	
}

function postOccupancy(){
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "http://localhost:5001/users");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");

	xhr.onreadystatechange = function () {
	  if (xhr.readyState === 4) {
	    console.log(xhr.status);
	    console.log(xhr.responseText);
	  }};
	console.log(JSON.stringify({
		"OccupationUri": curr_occupancy,
		"Competencies": saved_competencies}));
	xhr.send(JSON.stringify({
		"OccupationUri": curr_occupancy,
		"Competencies": saved_competencies}));
}

function recommendCourses() {
	const selectedOccupation = document.getElementById("occupency-select").value;
	console.log(encodeURIComponent(selectedOccupation))
	var param = selectedOccupation;

	var xhr = new XMLHttpRequest();
	var data;

	xhr.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			data = this.responseText;
			console.log(data);
			var recommenderResponse = JSON.parse(data);
			console.log(recommenderResponse)
		}
	};

	xhr.open("GET", "http://localhost:5001/occupationessential?occupationUri=" + encodeURIComponent(param), true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.send(null);
}