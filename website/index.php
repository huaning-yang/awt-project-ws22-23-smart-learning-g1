<!DOCTYPE html>
<html>

<head>
	<title>
		Course search
	</title>

	<!-- linking the stylesheet(CSS) -->
	<link rel="stylesheet" type="text/css" href="./css/style.css">
	<script src="./js/script.js"></script>
	<!-- <script src="./js/multiselect-dropdown.js" ></script> -->
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" />
	<!-- <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-multiselect/0.9.15/css/bootstrap-multiselect.css" /> -->
	<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.js"></script>
	<!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-multiselect/0.9.15/js/bootstrap-multiselect.min.js"></script> -->
</head>

<body>
	<header>
		<!-- Navbar -->
		<nav class="navbar navbar-expand-lg navbar-light bg-white">
			<div class="container-fluid">
				<button class="navbar-toggler" type="button" data-mdb-toggle="collapse" data-mdb-target="#navbarExample01" aria-controls="navbarExample01" aria-expanded="false" aria-label="Toggle navigation">
					<i class="fas fa-bars"></i>
				</button>
				<div class="collapse navbar-collapse" id="navbarExample01">
					<ul class="navbar-nav me-auto mb-2 mb-lg-0">
						<li class="nav-item active">
							<a class="nav-link" aria-current="page" href="#">Home/Search</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#">Users</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#">Courses</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#">Competencies</a>
						</li>
					</ul>
					<ul class="navbar-nav ms-auto">
						<li class="nav-item">
							<a class="nav-link" href="">User ABC</a>
						</li>
					</ul>
				</div>
			</div>
		</nav>
		<!-- Navbar -->
	</header>
	<div class="container">
		<img src="../resources/header.png" alt="HeaderImage" class="center" style="width:100%;">
	</div>
	<hr>
	<div class="container">

		<div class="row" id="user">
			<label for="occupency-select">Current occupency</label><br>
			<select id="occupency-select">
				<option class='occupation' value="none">none</option>
				<?php
				$json = file_get_contents('http://course-api-service/occupations');
				$obj = json_decode($json);
				$occupations = $obj;
				foreach ($occupations as $occupation) {
					echo "<option class='occupation' value='$occupation->OccupationUri'>$occupation->OccupationUri</option>";
				}
				?>
			</select>
			<div class="row" id="existing-competencies">
				<label for="existing-competencies-select">Existing Competencies</label><br>
				<select multiple id="existing-competencies-select">
					<?php
					$json = file_get_contents('http://course-api-service/skills');
					$obj = json_decode($json);
					$skills = $obj;
					foreach ($skills as $skill) {
						echo "<option class='existing-skill' value='$skill->preferred_label'>$skill->preferred_label</option>";
					}
					?>
				<input id="europassURL" class="form-control" type="text" name="europassURL" placeholder="Europass URL">
				<button type="button">Import europass</button>
			</div>


			<div class="row" id="search">
				<form id="search-form" action="" method="POST" enctype="multipart/form-data">
					<div class="form-group col-xs-9">
						<input id="searchbar" onkeyup="search_course()" class="form-control" type="text" name="search" placeholder="Search courses..">
					</div>
					</for </div>

					<div class="row" id="competencies">
						<label for="competency-select">Filter Competencies</label><br>
						<select multiple id="competency-select">
							<?php
							$json = file_get_contents('http://course-api-service/skills');
							$obj = json_decode($json);
							$skills = $obj;
							foreach ($skills as $skill) {
								echo "<option class='skill' value='$skill->preferred_label'>$skill->preferred_label</option>";
							}
							?>
						</select>
					</div>
					<div class="row" id="filter">
						<button type="submit" class="btn btn-block btn-primary" onclick="filterCourses();">Filter</button>
						<button type="submit" class="btn btn-block btn-danger" onclick="clearFilter();">Reset</button>
					</div>

					<ol id='list'>

						<?php
						$json = file_get_contents('http://course-api-service/');
						$obj = json_decode($json);
						$courses = $obj;
						foreach ($courses as $course) {
							echo "<li class='course'>$course->course_name</li>";
						}
						?>
						<!--\"neo4j+s://b367eb11. databases.neo4j.io\"In",
user = \"neo4i\"n"
password = \"2WPduo4-J4EK5ZEOuW5cm3hE3ZI85IgaXSOEFTDXHYE\"\n", -->
					</ol>

</body>

</html>