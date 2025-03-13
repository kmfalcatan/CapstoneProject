var previousSelectedElement = null;
        var currentStudentId = null;

        function showStudent(id, name, email, avgGrade, avgCet, number, ApplicationNo, address, course, element) {
            if (previousSelectedElement) {
                previousSelectedElement.classList.remove('selected');
            }

            element.classList.add('selected');
            previousSelectedElement = element;

            document.getElementById('studentName').innerText = name;
            document.getElementById('studentEmail').innerText = email;
            document.getElementById('studentAvgGrade').innerText = 'Grade avg: ' + avgGrade;
            document.getElementById('studentAvgCet').innerText = 'CET avg: ' + avgCet;
            document.getElementById('studentNumber').innerText = number;
            document.getElementById('ApplicationNo').innerText = ApplicationNo;
            document.getElementById('studentAddress').innerText = address;
            document.getElementById('studentCourse').innerText = course;
            document.getElementById('studentDetail').style.display = 'block';

            currentStudentId = id;
        }

        function closeStudent() {
            document.getElementById('studentDetail').style.display = 'none';
        }

        function filterByCourse() {
            document.getElementById('filterForm').submit();
        }

        function updateStatus(status) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', `{% url 'update_student_status' %}`, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');

            xhr.onload = function() {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    alert(response.message);
                    if (response.message === 'Status updated successfully!') {
                        closeStudent();
                    }
                } else {
                    alert('Failed to update status.');
                }
            };

            xhr.onerror = function() {
                alert('Request failed.');
            };

            xhr.send(JSON.stringify({
                id: currentStudentId,
                status: status
            }));
        }

        function fetchStudents(query, course) {
            const xhr = new XMLHttpRequest();
            const url = `{% url 'teacherPanel' %}?search=${query}&course=${course}`;
            
            xhr.open('GET', url, true);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.onload = function () {
                if (this.status >= 200 && this.status < 400) {
                    const response = JSON.parse(this.responseText);
                    const listContainer = document.querySelector('.listContainer');
                    listContainer.innerHTML = '';

                    response.students.forEach(student => {
                        const studentDiv = document.createElement('div');
                        studentDiv.className = 'subListContainer';

                        const nameContainer = document.createElement('div');
                        nameContainer.className = 'nameContainer';
                        
                        const subNameContainer = document.createElement('div');
                        subNameContainer.className = 'subNameContainer';
                        subNameContainer.innerHTML = `<p>${student.Name}</p>`;
                        
                        const averageContainer = document.createElement('div');
                        averageContainer.className = 'averageContainer';
                        averageContainer.innerHTML = `
                            <div class="grades">
                                <p>Grade avg: ${student.AvgGrade}</p>
                            </div>
                            <div class="grades">
                                <p>CET avg: ${student.AvgCet}</p>
                            </div>
                        `;

                        nameContainer.appendChild(subNameContainer);
                        nameContainer.appendChild(averageContainer);
                        
                        const viewButtonContainer = document.createElement('div');
                        viewButtonContainer.className = 'viewButtonContainer';
                        viewButtonContainer.innerHTML = `<button class="viewButton" id="student-${student.id}" onclick="showStudent('${student.id}', '${student.Name}', '${student.Email}', '${student.AvgGrade}', '${student.AvgCet}', '${student.Number}', '${student.ApplicationNo}', '${student.Address}', '${student.Course}', this)">View</button>`;

                        studentDiv.appendChild(nameContainer);
                        studentDiv.appendChild(viewButtonContainer);
                        
                        listContainer.appendChild(studentDiv);
                    });
                }
            };
            xhr.send();
        }


        document.getElementById('searchBar').addEventListener('input', function () {
            const query = this.value;
            const course = document.getElementById('courseFilter').value;
            fetchStudents(query, course);
        });

        document.getElementById('courseFilter').addEventListener('change', function () {
            const query = document.getElementById('searchBar').value;
            const course = this.value;
            fetchStudents(query, course);
        });

        function toggleMenu(element) {
            element.classList.toggle('active');
        }