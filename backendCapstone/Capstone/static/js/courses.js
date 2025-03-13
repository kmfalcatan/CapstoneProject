document.getElementById('collegeSelect').addEventListener('change', function() {
    const selectedCollege = this.value;
    window.location.href = `?college=${selectedCollege}`;
});

function viewCourse(courseId) {
    window.location.href = `?view=${courseId}`;
}

function editCourse(courseId) {
    window.location.href = `?edit=${courseId}`;
}