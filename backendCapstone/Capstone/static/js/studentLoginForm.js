function sendOtp() {
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const email = document.getElementById("otpEmail").value;

    if (!newPassword || !confirmPassword || !email) {
        alert("Please fill in all fields.");
        return;
    }

    if (newPassword !== confirmPassword) {
        alert("Passwords do not match.");
        return;
    }

    fetch("{% url 'send_otp' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}', 
        },
        body: JSON.stringify({ email: email, password: newPassword }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}

function verifyOtp() {
    const otpCode = document.getElementById("otpCode").value;
    const email = document.getElementById("otpEmail").value; 
    const newPassword = document.getElementById("newPassword").value; 

    if (!otpCode || !email || !newPassword) {
        alert("Please fill in all fields.");
        return;
    }

    fetch("{% url 'reset_password' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}', 
        },
        body: JSON.stringify({ email: email, otp: otpCode, new_password: newPassword }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.success) {
            window.location.href = "{% url 'loginForm' %}"; 
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}

function generateStudentID() {
    fetch("{% url 'generate_student_id' %}", {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        window.location.href = "{% url 'dashboard' %}";
    })
    .catch(error => {
        console.error('Error:', error);
    });
}