document.addEventListener('DOMContentLoaded', function () {
    let eyeIcon = document.getElementById("eyeicon");
    let passwordInput = document.getElementById("password");
    const requirementList = document.querySelectorAll(".requirement-list li");

    const requirements = [
        { regex: /.{8,}/, index: 0 }, 
        { regex: /[a-z]/, index: 1 },
        { regex: /[A-Z]/, index: 2 },
        { regex: /[0-9]/, index: 3 }, 
        { regex: /[^A-Za-z0-9]/, index: 4 }, 
    ];

    eyeIcon.addEventListener('click', function () {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            eyeIcon.src = "static/images/eye-open.png";
        } else {
            passwordInput.type = "password";
            eyeIcon.src = "static/images/eye-close.png";
        }
    });

    passwordInput.addEventListener("keyup", (e) => {
        requirements.forEach(item => {
            const isValid = item.regex.test(e.target.value);
            const requirementItem = requirementList[item.index];

            if (isValid) {
                requirementItem.classList.add("valid");
                requirementItem.firstElementChild.className = "fa-solid fa-check";
            } else {
                requirementItem.classList.remove("valid");
                requirementItem.firstElementChild.className = "fa-solid fa-circle";
            }
        });
    });
});
