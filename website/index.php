<!DOCTYPE html>
<html>

<head>
	<title>
		Course search
	</title>

	<!-- linking the stylesheet(CSS) -->
	<link rel="stylesheet" type="text/css" href="./css/style.css">
	<script src="./js/script.js"></script>
	<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" />
	<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
</head>

<body>
<header>
  <!-- Navbar -->
  <nav class="navbar navbar-expand-lg navbar-light bg-white">
    <div class="container-fluid">
      <button
        class="navbar-toggler"
        type="button"
        data-mdb-toggle="collapse"
        data-mdb-target="#navbarExample01"
        aria-controls="navbarExample01"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
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
      </div>
    </div>
  </nav>
  <!-- Navbar -->

  <!-- Header image -->
  
  <!-- <div
    class="p-5 bg-image"
    style="
      background-image: url('../resources/header.png');
	  width: 80%;
    "> -->
    
  <!-- Header image -->
</header>
	<div class="container">
	<img src="../resources/header.png" alt="HeaderImage" class="center" style="width:100%;">
	</div>
	<hr>
	<div class="container">
		<!-- input tag -->



		<div class="row" id="search">
			<form id="search-form" action="" method="POST" enctype="multipart/form-data">
				<div class="form-group col-xs-9">
					<input id="searchbar" onkeyup="search_course()" class="form-control" type="text" name="search" placeholder="Search courses..">
				</div>
				<!-- <div class="form-group col-xs-3">
                <button type="submit" class="btn btn-block btn-primary">Search</button>
            </div> -->
			</form>
		</div>

		<!-- <div class="row" id="products">
			<div class="row" id="filter"> -->
				<form>
					<div class="form-group row">
						<div class="form-group col-md-3">
							<select data-filter="provider" class="filter-provider filter form-control">
								<option value="">Select Provider</option>
								<option value="">Show All</option>
							</select>
						</div>
						<div class="form-group col-md-2">
							<select data-filter="price" class="filter-price filter form-control">
								<option value="">Select Price Range</option>
								<option value="">Show All</option>
							</select>
						</div>
						<div class="form-group col-md-3">
							<select data-filter="location" class="filter-location filter form-control">
								<option value="">Select Location</option>
								<option value="">Show All</option>
							</select>
						</div>
						<div class="form-group col-md-2">
							<select data-filter="start-date" class="filter-start-date filter form-control">
								<option value="">Select Start Date</option>
								<option value="">Show All</option>
							</select>
						</div>
						<div class="form-group col-md-2">
							<select data-filter="duration" class="filter-duration filter form-control">
								<option value="">Select Duration</option>
								<option value="">Show All</option>
							</select>
						</div>
						
					</div>
				</form>
			<!-- </div>
		</div> -->
		<!-- ordered list -->
		<ol id='list'>
			<?php
			$json = file_get_contents('http://course-api-service/');
			$obj = json_decode($json);
			$courses = $obj->Courses;
			foreach ($courses as $course) {
				echo "<li class='course'>$course</li>";
			}
			?>
			<!-- <li class="courses">Cat</li>
		<li class="courses">Dog</li>
		<li class="courses">Elephant</li>
		<li class="courses">Fish</li>
		<li class="courses">Gorilla</li>
		<li class="courses">Monkey</li>
		<li class="courses">Turtle</li>
		<li class="courses">Whale</li>
		<li class="courses">Aligator</li>
		<li class="courses">Donkey</li>
		<li class="courses">Horse</li> -->
		</ol>


</body>

</html>