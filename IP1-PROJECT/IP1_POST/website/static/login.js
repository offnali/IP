document.addEventListener('DOMContentLoaded', function () {
    let eyeicon = document.getElementById("eyeicon");
    let passwordInput = document.getElementById("password");

    eyeicon.addEventListener('click', function () {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            eyeicon.src = "static/images/eye-open.png";
        } else {
            passwordInput.type = "password";
            eyeicon.src = "static/images/eye-close.png";
        }
    });
});
