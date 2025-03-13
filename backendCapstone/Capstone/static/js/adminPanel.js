function showTeacherDetails(button) {
    const name = button.getAttribute('data-name');
    const email = button.getAttribute('data-email');
    const rank = button.getAttribute('data-rank');
    const designation = button.getAttribute('data-designation');
    const course = button.getAttribute('data-course');
    const contactNo = button.getAttribute('data-contactNo');
    const address = button.getAttribute('data-address');
    const college = button.getAttribute('data-college');

    document.getElementById('teacherName').innerText = name || 'N/A';
    document.getElementById('teacherEmail').innerText = email || 'N/A';
    document.getElementById('teacherRank').innerText = rank || 'N/A';
    document.getElementById('teacherDesignation').innerText = designation || 'N/A';
    document.getElementById('teacherCourse').innerText = course || 'N/A';
    document.getElementById('teacherContactNo').innerText = contactNo || 'N/A';
    document.getElementById('teacherAddress').innerText = address || 'N/A';
    document.getElementById('teacherCollege').innerText = college || 'N/A';

    document.getElementById('teacherDetailsContainer').style.display = 'block';
}

function addlist() {
    const container = document.getElementById('teacherDetailsContainer');
    container.style.display = container.style.display === 'none' ? 'block' : 'none';
}

function deleteTeacher(button) {
const teacherId = button.getAttribute('data-id');

if (confirm("Are you sure you want to delete this teacher?")) {
    fetch("{% url 'delete_teacher' %}", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ 'id': teacherId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Teacher deleted successfully.");
            location.reload();
        } else {
            alert("Error: Unable to delete the teacher.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
}

function filterTeachers() {
const searchInput = document.getElementById('searchBar').value.toLowerCase();
const teachers = document.querySelectorAll('.subListContainer');

teachers.forEach(teacher => {
    const teacherName = teacher.querySelector('.subNameContainer p').innerText.toLowerCase();
    if (teacherName.includes(searchInput)) {
        teacher.style.display = 'block';
        teacher.style = 'display: flex; flex-direction: row;'
    } else {
        teacher.style.display = 'none';
    }
});
}
