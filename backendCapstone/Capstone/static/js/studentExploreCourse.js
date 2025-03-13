function filterCourses() {
    const selectedCollege = document.getElementById('collegeSelect').value;
    const courses = document.querySelectorAll('.subCourse');

    courses.forEach(course => {
        if (selectedCollege === 'all' || course.getAttribute('data-college') === selectedCollege) {
            course.style.display = 'block';
        } else {
            course.style.display = 'none';
        }
    });
}

function showAllCourses() {
    const courses = document.querySelectorAll('.subCourse');
    courses.forEach(course => course.style.display = 'block');
    document.getElementById('collegeSelect').value = 'all';
}

function showCourseInfo(courseName, courseDescription, college, avgGrade, avgCet, logoSrc) {
    selectedCourse = courseName; 
    document.getElementById('courseName').innerText = courseName;
    document.getElementById('courseDescription').innerText = courseDescription;
    document.getElementById('college').innerText = college;
    document.getElementById('avgGrade').innerText = avgGrade;
    document.getElementById('avgCet').innerText = avgCet;

    document.getElementById('courseLogo').src = logoSrc;

    document.getElementById('courseInfoModal').style.display = 'block';
    document.getElementById('courseInput').value = courseName; 
}

function closeCourseInfo() {
    document.getElementById('courseInfoModal').style.display = 'none';
}

function closeAddListForm() {
    document.getElementById('addToListForm').style.display = 'none';
    clearForm();
}

function clearForm() {
    const form = document.getElementById('addListForm');
    form.reset(); 
    document.getElementById('courseInput').value = selectedCourse; 
}

function viewCourse(courseName) {
    document.getElementById('courseInput').value = courseName;
}

function submitAddToList() {
    const form = document.getElementById('addListForm');
    const formData = new FormData(form);

    const selectedCourse = document.getElementById('courseInput').value;
    formData.append('course', selectedCourse); 

    fetch('{% url "exploreCourses" %}', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': formData.get('csrfmiddlewaretoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);  
            closeAddListForm(); 
        } else {
            alert('An error occurred: ' + data.message);  
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.'); 
    });
}