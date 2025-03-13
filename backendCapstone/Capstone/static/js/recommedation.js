let selectedCourse = "";

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

        function addlist() {
            document.getElementById('addToListForm').style.display = 'block';
        }

        function closeAddListForm() {
            document.getElementById('addToListForm').style.display = 'none';
            clearForm();
        }

        function submitAddToList() {
            const form = document.getElementById('addListForm');
            const formData = new FormData(form);
            formData.append('course', selectedCourse);

            fetch('{% url "add_to_list" %}', { 
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                alert(data.message); 
                closeCourseInfo(); 
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error with the submission.');
            });
        }

        function closeCourseInfo() {
            document.getElementById('courseInfoModal').style.display = 'none';
            document.getElementById('addToListForm').style.display = 'none';
            clearForm();
        }

        function clearForm() {
            const form = document.getElementById('addListForm');
            form.reset(); 
            document.getElementById('courseInput').value = selectedCourse; 
        }