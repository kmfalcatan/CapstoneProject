function login(){
    const loginButton = document.querySelector(' .loginFormContainer');

    if(loginButton.style.display === 'none'){
        loginButton.style.display = 'block';
    } else{
        loginButton .style.display = 'none'
    }
}

function login1(){
    const loginButton = document.querySelector(' .errorContainer');

    if(loginButton.style.display === 'none'){
        loginButton.style.display = 'block';
    } else{
        loginButton .style.display = 'none'
    }
}

function error(){
    const errorButton = document.querySelector(' .errorContainer');

    if(errorButton.style.display === 'none'){
        errorButton.style.display = 'block';
    } else{
        errorButton .style.display = 'none'
    }
}

function forgot() {
    const forgotContainer = document.querySelector('.loginFormContainer.forgot');
    
    if (forgotContainer.style.display === 'none' || forgotContainer.style.display === '') {
        forgotContainer.style.display = 'block';
    } else {
        forgotContainer.style.display = 'none';
    }
    
    if (forgotContainer.style.display === 'block') {
        document.getElementById("newPassword").value = "";
        document.getElementById("confirmPassword").value = "";
        document.getElementById("otpEmail").value = "";
    }
}


function otp() {
    const otpContainer = document.querySelector('.loginFormContainer.OtpContainer');
    
    if (otpContainer.style.display === 'none' || otpContainer.style.display === '') {
        otpContainer.style.display = 'block';
    } else {
        otpContainer.style.display = 'none';
    }
    
    if (otpContainer.style.display === 'block') {
        document.getElementById("otpCode").value = "";
    }
}
