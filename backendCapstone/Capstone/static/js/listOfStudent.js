document.getElementById('searchBar').addEventListener('input', filterStatus);

    function filterStatus() {
    var select = document.getElementById('statusFilter');
    var status = select.options[select.selectedIndex].value;
    var search = document.getElementById('searchBar').value;

    $.ajax({
        url: '{% url "fetch_students" %}', 
        data: { 
            'status': status,
            'search': search  
        },
        success: function(response) {
            updateStudentList(response.students);
            updateTitle(status);
        }
    });
}

function updateStudentList(students) {
    var container = document.getElementById('studentListContainer');
    container.innerHTML = '';

    if (students.length > 0) {
        students.forEach(function(student, index) {
            var div = document.createElement('div');
            div.className = 'subListContainer';
            div.innerHTML = `
                <div class="nameContainer">
                    <div class="subNameContainer">
                        <p>${student.Name}</p>
                    </div>
                    <div class="averageContainer">
                        <div class="grades">
                            <p>Grade avg: ${student.AvgGrade}</p>
                        </div>
                        <div class="grades">
                            <p>CET avg: ${student.AvgCet}</p>
                        </div>
                    </div>
                </div>
                <div class="viewButtonContainer">
                    <button onclick="showStudentDetails(${index})" class="viewButton">View</button>
                </div>
            `;
            container.appendChild(div);

            div.dataset.studentInfo = JSON.stringify(student);
        });
    } else {
        container.innerHTML = '<p>No students found.</p>';
    }
}

function showStudentDetails(index) {
    var studentDiv = document.getElementsByClassName('subListContainer')[index];
    var student = JSON.parse(studentDiv.dataset.studentInfo);

    document.querySelector('.addListContainer .infoContainer').innerHTML = `
            <div class="subInfoContainer" style="flex-direction: column;">
                <p style="width: 100%; justify-content: left; padding-left: 2rem;">Name:</p>
                <div class="info" style="min-height: 3rem;">
                <p>${student.Name}</p>
            </div>
        </div>
            <div class="subInfoContainer" style="flex-direction: column; margin-top: 1rem;">
                <p style="width: 100%; justify-content: left; padding-left: 2rem;">Name:</p>
                <div class="info" style="min-height: 3rem;">
                <p>${student.Email}</p>
            </div>
        </div>

        <div class="subInfoContainer" style="gap: 1rem;">
            <div style="flex-direction: column; margin-top: 2rem;">
                <p style="width: 100%; justify-content: left;">Grade average:</p>
                <div class="info" style="width: 10rem; min-height: 3rem;">
                    <p>Grade avg: ${student.AvgGrade}</p>
                </div>
            </div>
            
            <div style="flex-direction: column; margin-top: 2rem;">
                <p style="width: 100%; justify-content: left;">CET average:</p>
                <div class="info" style="width: 10rem; min-height: 3rem;">
                    <p>CET avg: ${student.AvgCet}</p>
                </div>
            </div>
        </div>

        <div class="subInfoContainer" style="flex-direction: column; margin-top: 2rem;">
            <p style="width: 100%; justify-content: left; padding-left: 2rem;">Contact No.:</p>
            <div class="info" style="min-height: 3rem;">
                <p>${student.Number}</p>
            </div>
        </div>

        <div class="subInfoContainer" style="flex-direction: column; margin-top: 1rem;">
            <p style="width: 100%; justify-content: left; padding-left: 2rem;">Application No.:</p>
            <div class="info" style="min-height: 3rem;">
                <p>${student.ApplicationNo}</p>
            </div>
        </div>

        <div class="subInfoContainer" style="flex-direction: column; margin-top: 1rem;">
            <p style="width: 100%; justify-content: left; padding-left: 2rem;">Address:</p>
            <div class="info" style="min-height: 3rem;">
                <p>${student.Address}</p>
            </div>
        </div>

        <div class="subInfoContainer1" style="flex-direction: column;">
            <p style="width: 100%; justify-content: left; padding-left: 2rem;">Course:</p>
            <div class="info1" style="min-height: 3rem;">
                <p>${student.Course}</p>
            </div>
        </div>
    `;

    document.querySelector('.addListContainer').style.display = 'block';
}

function updateTitle(status) {
    document.getElementById('pageTitle').innerText = 'List of Students - ' + status;
}

function printStudentList() {
    
    window.print();
}

document.addEventListener('DOMContentLoaded', function() {
    var select = document.getElementById('statusFilter');
    select.addEventListener('change', filterStatus);

    filterStatus();
});
