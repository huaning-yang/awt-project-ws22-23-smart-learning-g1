// JavaScript code
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

	xhr.open("GET", "http://localhost:5001/essentials?occupationUri=" + encodeURIComponent(param), true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.send(null);
}