// JavaScript code

var curr_occupation = ""
var existing_occupations = []
var saved_competencies = []
var required_skills = []
var userID = -1


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
	const selected = document.querySelectorAll('#recommendation-items option:checked');
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
			// console.log(data);
			var coursesResponse = JSON.parse(data);
			let x = document.getElementsByClassName('course');
			for (i = 0; i < x.length; i++) {
				x[i].style.display = "none";
			}
			for (var j = 0; j < coursesResponse.length; j++) {
				var course = coursesResponse[j];
				// console.log(course.course_name);
				for (i = 0; i < x.length; i++) {
					if (x[i].dataset['uuid'].includes(course.course_id)) {
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
	saved_competencies = saved_competencies.concat(selectedItems)
	console.log(saved_competencies);

}

function setSavedCompetencies(s) {
	saved_competencies = s
}

function getOccupation() {
	var sel = document.getElementById("occupation-select")
	var occupation = sel.options[sel.selectedIndex].text
	console.log(sel.options[sel.selectedIndex].text)


	let xhr = new XMLHttpRequest();
	xhr.open('get', 'http://localhost:5001/occupationsuri?occupation=' + encodeURIComponent(occupation), true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.send();

	xhr.onload = function () {
		curr_occupation = JSON.parse(xhr.response)[0][0]
	}

}

function postOccupation() {
	let xhr = new XMLHttpRequest();
	xhr.open("POST", "http://localhost:5001/users");
	xhr.setRequestHeader("Accept", "application/json");
	xhr.setRequestHeader("Content-Type", "application/json");

	console.log(JSON.stringify({
		"OccupationUri": curr_occupation,
		"Competencies": saved_competencies
	}));
	xhr.send(JSON.stringify({
		"OccupationUri": curr_occupation,
		"Competencies": saved_competencies,
		"ExistingOccupations": existing_occupations
	}));
	xhr.onreadystatechange = function () {
		if (this.readyState === 4 && this.status == 200) {
			console.log(JSON.parse(this.responseText));

		}
	};
}

function updateExistingCompetencies() {
	const selectedOccupation = document.getElementById("occupation-select").value;
	console.log(selectedOccupation)
	const exisitingCompetencies = document.getElementById("existing-comp");
	var box = document.getElementById("exist")
	var param = selectedOccupation;
	var xhr = new XMLHttpRequest();
	var data;

	xhr.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			data = this.responseText;
			console.log(data);
			var recommenderResponse = JSON.parse(data);
			exisitingCompetencies.remove();
			var form = document.createElement("form");
			form.id = "existing-comp"
			box.appendChild(form);
			for (const sk of recommenderResponse) {
				var checkbox = document.createElement("input")
				var linebreak = document.createElement("br")
				checkbox.type = "checkbox";
				checkbox.value = sk['preferred_label'];
				checkbox.name = "skill";
				form.appendChild(checkbox);
				form.append(sk['preferred_label'])
				form.appendChild(linebreak)
			}

		}
	};

	xhr.open("GET", "http://localhost:5001/occupationessential?occupationUri=" + encodeURIComponent(param), true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.send();
}

function getRelatedSkills() {
	const selectedOccupation = document.getElementById("occupation-select").value;
	const recommenderBox = document.getElementById("recommendation-items")
	var param = selectedOccupation;
	var xhr = new XMLHttpRequest();
	var data;
	xhr.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			data = this.responseText;
			var response = JSON.parse(data);
			var i, L = recommenderBox.options.length - 1;
			for (i = L; i >= 0; i--) {
				recommenderBox.remove(i)
			}
			for (var sk of response) {
				recommenderBox.options[recommenderBox.options.length] = new Option(sk)
			}
		}
	}
	xhr.open("GET", "http://localhost:5001/occupationrelated?occupationUri=" + encodeURIComponent(param), true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.send();
}

function recommendCourses() {
	const selectedOccupation = document.getElementById("occupation-select").value;
	const recommenderBox = document.getElementById("recommendation-items")
	var param = selectedOccupation;

	var xhr = new XMLHttpRequest();
	var data;

	xhr.onreadystatechange = function () {
		if (this.readyState == 4 && this.status == 200) {
			data = this.responseText;
			var recommenderResponse = JSON.parse(data);
			var i, L = recommenderBox.options.length - 1;
			for (i = L; i >= 0; i--) {
				recommenderBox.remove(i)
			}
			for (const sk of recommenderResponse) {
				recommenderBox.options[recommenderBox.options.length] = new Option(sk['preferred_label'], sk['concept_uri'])
			}
		}
	};

	xhr.open("GET", "http://localhost:5001/essentials?occupationUri=" + encodeURIComponent(param) + "&personID=" + userID, true);
	xhr.setRequestHeader("Content-type", "application/json");
	xhr.send();
}

function storeEuropassSkills() {
	const europass_url = document.getElementById('europassURL').value;
	const out1 = document.getElementById('output1');

	let xhr = new XMLHttpRequest();
	xhr.open("GET", "http://localhost:5001/europass?europassURL=" + europass_url, true);
	xhr.setRequestHeader("Accept", "application/json");
	xhr.send();

	xhr.onreadystatechange = function () {
		if (xhr.readyState === XMLHttpRequest.DONE) {
			console.log(xhr.status);
			existing_occupations = existing_occupations.concat(JSON.parse(xhr.responseText)["occupations"]);
			saved_competencies = saved_competencies.concat(JSON.parse(xhr.responseText)["preferred_labels"]);
			checkCheckboxes();
		}
	};
	out1.innerHTML = "Europass imported";


}

function checkCheckboxes() {
	const checkboxes = document.getElementsByName("skill")

	for (const cb of checkboxes) {
		if (saved_competencies.includes(cb.value)) {
			cb.checked = true;
		}
	}

}