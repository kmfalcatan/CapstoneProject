document.getElementById('gradesForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    var form = this;

    fetch(form.action, {
        method: form.method,
        body: new FormData(form),
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        }
    }).then(response => {
        if (response.ok) {
            alert('Please note that the information you provide will be shared with your teacher to help guide your progress and ensure you receive the best possible support. Your responses will remain confidential and will only be used for educational purposes..');
            window.location.href = "{% url 'result' %}";
        } else {
            alert('Failed to submit the form. Please try again.');
        }
    }).catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
});

function submitFeedback() {
    var name = document.getElementById('feedbackName').value;
    var feedback = document.getElementById('feedbackText').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '{% url "dashboard" %}', true);
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            alert('Feedback submitted successfully!');
            document.getElementById('feedbackName').value = '';
            document.getElementById('feedbackText').value = '';
            document.querySelector('.courseInfoContainer').style.display = 'none';
        }
    };

    xhr.send('name=' + encodeURIComponent(name) + '&feedback=' + encodeURIComponent(feedback));
}

function feedback() {
    var feedbackContainer = document.querySelector('.courseInfoContainer');
    feedbackContainer.style.display = feedbackContainer.style.display === 'none' ? 'block' : 'none';
}

function course1(){
    const courseButton = document.querySelector('.courseContainer');

    if(courseButton.style.display === 'none' || courseButton.style.display === ''){
        courseButton.style.display = 'block';
    } else{
        courseButton.style.display = 'none'
    }
}