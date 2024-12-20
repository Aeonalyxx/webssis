//===================================================================
// Search Student Functionality
//===================================================================
document.getElementById('searchButton').addEventListener('click', function() {
    const filterBy = document.getElementById('filterSelect').value;
    const searchQuery = document.getElementById('studentSearch').value;

    if (filterBy && searchQuery) {
        window.location.href = `/students?filter_by=${filterBy}&search_query=${encodeURIComponent(searchQuery)}`;
    }
});

//===================================================================
// Reset Add Student Modal on Open
//===================================================================
$('#addStudentModal').on('show.bs.modal', function () {
    $(this).find('input, select, textarea').val(''); // Clear inputs
});

//===================================================================
// Add Student Form Validation
//===================================================================
$('form').on('submit', function(event) {
    var studentId = $('#student_id').val();
    var studentIdPattern = /^\d{4}-\d{4}$/;

    if ($('#addStudentModal').is(':visible')) {
        if (!studentIdPattern.test(studentId)) {
            alert("Student ID must be in YYYY-NNNN format");
            event.preventDefault();
        }
    }
});

//===================================================================
// Populate Edit Student Modal
//===================================================================
$('#editStudentModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 
    var studentId = button.data('student-id');
    var firstName = button.data('first-name');
    var lastName = button.data('last-name');
    var gender = button.data('gender');
    var courseCode = button.data('course-code');
    var year = button.data('year'); 

    var modal = $(this);
    modal.find('form').attr('action', '/students/edit_student/' + studentId);

    modal.find('#edit_student_id').val(studentId);
    modal.find('#edit_first_name').val(firstName);
    modal.find('#edit_last_name').val(lastName);
    modal.find('#edit_gender').val(gender);
    modal.find('#edit_course_code').val(courseCode);
    modal.find('#edit_year').val(year);
});

//===================================================================
// Delete Student Modal
//===================================================================
$('#deleteStudentModal').on('show.bs.modal', function(event) {
    var button = $(event.relatedTarget);
    var studentId = button.data('id');
    var modal = $(this);
    modal.find('#delete_student_id').val(studentId);
});

//===================================================================
// Confirm Delete Student
//===================================================================
$('#confirmDeleteStudent').on('click', function() {
    $('#deleteStudentForm').submit();
});


//===========================================================================SAED COURSE===============================++======================
document.getElementById('searchButton').addEventListener('click', function() {
    const filterBy = document.getElementById('filterSelect').value;
    const searchQuery = document.getElementById('courseSearch').value;

    if (filterBy && searchQuery) {
        window.location.href = `/courses?filter_by=${filterBy}&search_query=${encodeURIComponent(searchQuery)}`;
    }
});


$('#addCourseModal').on('show.bs.modal', function () {
    $(this).find('input, select, textarea').val(''); 
});

$('#editCourseModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 
    var courseCode = button.data('course-code');
    var courseName = button.data('course-name');
    var colCode = button.data('col-code'); 

    var modal = $(this);
    modal.find('form').attr('action', '/courses/edit_course/' + courseCode);

    modal.find('#edit_course_code').val(courseCode);
    modal.find('#edit_course_name').val(courseName);
    modal.find('#edit_col_code').val(colCode);  // Set the selected college code
});



$('#deleteCourseModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var courseCode = button.data('code');
    var modal = $(this);
    modal.find('#delete_course_code').val(courseCode);
});

$('#confirmDeleteCourse').on('click', function () {
    $('#deleteCourseForm').submit(); 
});



//===========================================================================SAED COLLEGE===============================++======================
document.getElementById('searchButton').addEventListener('click', function() {
    const filterBy = document.getElementById('filterSelect').value;
    const searchQuery = document.getElementById('collegeSearch').value;

    if (filterBy && searchQuery) {
        window.location.href = `/colleges?filter_by=${filterBy}&search_query=${encodeURIComponent(searchQuery)}`;
    }
});


$('#addCollegeModal').on('show.bs.modal', function () {
    $(this).find('input, select, textarea').val(''); 
});

$('#editCollegeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 
    var colCode = button.data('col-code'); 
    var colName = button.data('col-name');
    
    var modal = $(this);
    modal.find('form').attr('action', '/colleges/edit_college/' + colCode);
    
    modal.find('#edit_col_code').val(colCode);
    modal.find('#edit_college_name').val(colName);
    modal.find('#old_col_code').val(colCode);
});


$('#deleteCollegeModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget); 
    var colCode = button.data('col-code'); 
    var modal = $(this);
    modal.find('#delete_col_code').val(colCode); 
});

$('#confirmDeleteCollege').on('click', function () {
    $('#deleteCollegeForm').submit(); 
});
