function showFormAndSetCourse(course) {
    document.getElementById('courseInput').value = course;
    document.querySelector('.addListContainer').style.display = 'block';
    clearForm(); 
    document.getElementById('courseDisplay').value = course;
}

function hideAddListContainer() {
    document.querySelector('.addListContainer').style.display = 'none';
}

function handleFormSubmission() {
    var form = document.getElementById('addListForm');
    var formData = new FormData(form);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/add_to_list/', true);
    xhr.setRequestHeader('X-CSRFToken', formData.get('csrfmiddlewaretoken'));

    xhr.onload = function() {
        if (xhr.status === 200) {
            alert('Successfully added to the list!');
            hideAddListContainer();
            clearForm(); 
        } else {
            alert('Failed to add to the list.');
            clearForm(); 
        }
    };

    xhr.send(formData);
}

function clearForm() {
var form = document.getElementById('addListForm');
form.reset();
}

function course() {
    getRecommendations();
}

function getRecommendations() {
    var studentId = '{{ request.session.student_id }}';
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `/recommend_courses/${studentId}/`, true);
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var recommendContainer = document.getElementById('recommendContainer');
            recommendContainer.innerHTML = '';

            if (response.message) {
                recommendContainer.innerHTML = `
                    <div class="noRecommendations">
                        <p>${response.message}</p>
                    </div>
                `;
            } else {
                var recommendations = response.recommendations;
                
                recommendations.forEach(function(rec) {
                    var recommendationHTML = `
                        <div class="subRecommendContainer" style="min-height: 3rem;">
                            <div class="recommend">
                                <p>${rec.course}</p>
                            </div>
                            <div class="addButton">
                                <button onclick="showFormAndSetCourse('${rec.course}')" class="addtolist">Add to list</button>
                            </div>
                        </div>
                    `;
                    recommendContainer.innerHTML += recommendationHTML;
                });
            }

            document.getElementById('courseContainer').style.display = 'block';
        } else if (xhr.readyState === 4) {
            console.error("Failed to fetch recommendations: " + xhr.status);
        }
    };

    xhr.send();
}