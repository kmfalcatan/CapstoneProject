const answers = document.querySelectorAll('.answer');

        answers.forEach(answer => {
            answer.addEventListener('click', () => {
                answers.forEach(a => a.classList.remove('clicked'));
                answer.classList.add('clicked');
            });
        });

function course(){
    const courseButton = document.querySelector('.courseContainer');

    if(courseButton.style.display === 'none'){
        courseButton.style.display = 'block';
    } else{
        courseButton .style.display = 'none'
    }
}

function submitFeedback() {
    var name = document.getElementById('feedbackName').value;
    var feedback = document.getElementById('feedbackText').value;

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '{% url 'dashboard' %}', true);
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

