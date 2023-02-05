<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>AWT - SMART Learning</title>
    <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Lato:300,400,700&amp;display=swap">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.12.0/css/all.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="assets/fonts/fontawesome5-overrides.min.css">
    <link rel="stylesheet" href="assets/css/Footer-Multi-Column-icons.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/css/select2.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tom-select@2.0.1/dist/css/tom-select.css">
    <link rel="stylesheet" href="assets/css/Ludens---TomSelect-Form.css">
    <link rel="stylesheet" href="assets/css/pikaday.min.css">
    <link rel="stylesheet" href="assets/css/style.css">
</head>

<body>
    <nav class="navbar navbar-dark navbar-expand-lg bg-white portfolio-navbar gradient">
        <div class="container"><a class="navbar-brand logo" href="#">AWT 22/23</a><button data-bs-toggle="collapse" class="navbar-toggler" data-bs-target="#navbarNav"><span class="visually-hidden">Toggle navigation</span><span class="navbar-toggler-icon"></span></button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item"><a class="nav-link active" href="projects-no-images.html">Smart Learning</a></li>
                </ul>
            </div>
        </div>
    </nav>
    <main class="page projets-page">
        <section class="portfolio-block project-no-images">
            <div class="container">
                <h2 class="text-center" style="margin-top: -90px;">SMART Learning Platform</h2>
            </div>
            <form style="max-width: 10000px;padding-top: 20px;border-top-style: none;padding-bottom: 1px;" role="form" action="indexTeachers.html" method="post" enctype="multipart/form-data">
                <div class="container" style="margin-bottom: 20px;border-style: none;border-top-style: none;border-right-style: none;">
                    <div class="row">
                        <div class="user col" style="border-top-style: none;">
                            <p id="userText">Your UserID is:</p>
                        </div>
                        <div class="col" style="border-top-style: none;"><button class="btn btn-primary" type="button" onclick=copyUserID();>Copy</button></div>
                    </div>
                    <div class="row">
                        <div class="col" style="border-top-style: none;">
                            <div class="input-group mb-3" style="margin-top: 10px;">
                                <div class="input-group-prepend"><span class="input-group-text"><i class="fa fa-user" style="font-size: 24px;"></i></span></div><input id="userID" name="restoreEuropassText" class="form-control" type="text" placeholder="User ID"><button id="restoreEuropassBtn" class="btn btn-primary" type="button" onclick=restoreUser()>Restore user</button>
                            </div>
                        </div>
                        <div class="col" style="border-top-style: none;">
                            <div class="input-group mb-3" style="margin-top: 10px;">
                                <div class="input-group-prepend"><span class="input-group-text"><i class="fa fa-user" style="font-size: 24px;"></i></span></div><input id="europassURL" name="europassURL" class="form-control" type="text" placeholder="Europass URL"><button id="europassbtn" class="btn btn-primary" type="button" onclick=storeEuropassSkills()>Import Europass</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div id="user">
                    <div class="form-group mb-3"><label for="occupation-select" class="form-label">Planned Occupation</label><select class="form-select" id="occupation-select" onchange="getOccupation(); updateExistingCompetencies(); getUnobtainableSkills();" required="" name="caat">
                            <option class='occupation' value="none">none</option>
                            <?php
                            $json = file_get_contents('http://course-api-service/occupations');
                            $obj = json_decode($json);
                            $occupations = $obj;
                            foreach ($occupations as $occupation) {
                                echo "<option class='occupation' value='$occupation->OccupationUri'>$occupation->preferred_label</option>";
                            }
                            ?>
                        </select>

                        <div class="row" id="existing-competencies">
                            <label for="existing-competencies-select">Existing Competencies</label>

                            <div id="exist" class="scrollable">
                                <div id="existing-comp"> </div>
                            </div>

                        </div>
                    </div>

                    <hr style="margin-top: 30px;margin-bottom: 10px;">

                    <select id="searchbar" class="searchbar" name="states[]" multiple="multiple">

                    </select>
                    <div class="row">
                        <div class="col">
                            <div class="row" id="recommendations">
                                <label for="recommendation-items">Recommendations</label><br>
                                <select multiple id="recommendation-items" onchange='SelectRecommendation();'>

                                </select>
                            </div>
                        </div>
                        <div class="col">
                            <p>Skills not covered by any courses</p>
                            <select multiple id="unobtainable-items">

                            </select>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col">
                            <p>Filter Date</p><input class="form-control" type="date" id="date-select" name="date">
                        </div>
                        <div class="col">
                            <div id="location">
                                <label for="location-select">Location</label><br>
                                <select id="location-select" class="form-select">
                                    <option value="none">No Preference</option>
                                    <?php
                                    $json = file_get_contents('http://course-api-service/locations');
                                    $obj = json_decode($json);
                                    $locations = $obj;
                                    foreach ($locations as $location) {
                                        echo "<option value='$location'>$location</option>";
                                    }
                                    ?>
                                </select>
                            </div>

                        </div>
                    </div>
                    <hr style="margin-top: 30px;margin-bottom: 10px;">
                    <div class="row">
                        <div class="col" style="margin-bottom: 10px;"><button onclick="filterCourses();" class="btn btn-secondary d-block w-100" id="submitButton-1" type="button"><i class="fas fa-brain"></i>&nbsp;Recommend</button></div>
                        <div class="col"><button onclick="getRelatedSkills();" class="btn btn-secondary d-block w-100" id="submitButton-3" type="button"><i class="fas fa-share-alt-square"></i>&nbsp;Related skills (occupation)</button></div>
                        <div class="col"><button onclick="getRelatedSkillsUser();" class="btn btn-secondary d-block w-100" id="submitButton-4" type="button"><i class="fas fa-share-alt-square"></i>&nbsp;Related skills (user skillset)</button></div>
                    </div>
                    <div class="form-group mb-3"><button onclick="filterCourses();" class="btn btn-primary d-block w-100" id="submitButton-2" type="button" style="margin-bottom: 0px;"><i class="fas fa-filter"></i>&nbsp;Filter</button></div>
            </form>
            <p class="fs-1 text-center" style="margin-top: 10px;margin-bottom: 0px;">Course list</p>
            <div class="container">
                <div class="heading"></div>
                <header></header>

                <!-- <div id="courseList" class="list-group courseList">
			        <?php
                    $json = file_get_contents('http://course-api-service/');
                    $obj = json_decode($json);
                    $courses = $obj;
                    foreach ($courses as $course) {
                        // echo "<li class='course' data-UUID='$course->course_id'>$course->course_name</li>";
                        echo '<a href="#" data-UUID=' . $course->course_id . ' class="course list-group-item list-group-item-action flex-column align-items-start">
			        				<div class="d-flex w-100 justify-content-between">
			        				  <h5 class="mb-1">' . $course->course_name . '
			        				  </h5>
      		        				  <small>' . $course->course_datetime . '</small>
			        					</div>
			        					<small>' . $course->course_location . '</small>
			        					</a>';
                    }
                    ?>
		        </div> -->

                <div id="courseList" class="row courseList" style="margin-top: -70px;">
                    <?php
                    $json = file_get_contents('http://course-api-service/');
                    $obj = json_decode($json);
                    $courses = $obj;
                    foreach ($courses as $course) {
                        // echo "<li class='course' data-UUID='$course->course_id'>$course->course_name</li>";
                        // echo '<a href="#" data-UUID=' . $course->course_id . ' class="course list-group-item list-group-item-action flex-column align-items-start">
                        // 			<div class="d-flex w-100 justify-content-between">
                        // 			  <h5 class="mb-1">' . $course->course_name . '
                        // 			  </h5>
                        // 			  <small>' . $course->course_datetime . '</small>
                        // 				</div>
                        // 				<small>' . $course->course_location . '</small>
                        // 				</a>';

                        echo '<div data-UUID=' . $course->course_id . ' class="course col-md-6 col-lg-4">
                            <div class="project-card-no-image">
                                <h3>' . $course->course_name . '</h3>
                                <h4>Short description</h4>
                                <small>Date: ' . $course->course_datetime . '</small>
                                <small>Location: ' . $course->course_location . '</small>
                                <div class="tags"><a href="#">#</a></div>
                            </div>
                        </div>';
                    }
                    ?>
                </div>



                <!-- <div class="row" style="margin-top: -70px;">
                    <div class="col-md-6 col-lg-4">
                        <div class="project-card-no-image">
                            <h3>Lorem Ipsum</h3>
                            <h4>Lorem ipsum dolor sit amet</h4><a class="btn btn-outline-primary btn-sm" role="button" href="#">See More</a>
                            <div class="tags"><a href="#">JavaScript</a></div>
                        </div>
                    </div>
                </div> -->


            </div>
        </section>
        <footer>
            <div class="container py-4 py-lg-5">
                <div class="row justify-content-center">
                    <div class="col-sm-4 col-md-3 text-center text-lg-start d-flex flex-column">
                        <ul class="list-unstyled"></ul>
                        <p>Yang, Kora S, Heimbrecht, Ronellfitsch, Souissi</p>
                    </div>
                    <div class="col-sm-4 col-md-3 text-center text-lg-start d-flex flex-column">
                        <ul class="list-unstyled"></ul><img src="assets/img/14_fokus_rgb.png">
                    </div>
                    <div class="col-sm-4 col-md-3 text-center text-lg-start d-flex flex-column">
                        <ul class="list-unstyled">
                            <li></li>
                        </ul>
                    </div>
                    <div class="col-lg-3 text-center text-lg-start d-flex flex-column align-items-center order-first align-items-lg-start order-lg-last">
                        <div class="fw-bold d-flex align-items-center mb-2"></div><img src="assets/img/Logo_der_Technischen_Universität_Berlin.svg" width="177" height="90">
                    </div>
                </div>
            </div>
        </footer>
    </main>
    <script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/tom-select@2.0.1/dist/js/tom-select.complete.min.js"></script>
    <script src="assets/js/Ludens---TomSelect-Form-main.js"></script>
    <script src="assets/js/pikaday.min.js"></script>
    <script src="assets/js/script.js"></script>
    <script src="assets/js/theme.js"></script>
</body>

</html>