document.getElementById("edit-post-btn").addEventListener("click", function () {
        // Get the form container
        const formContainer = document.getElementById("update-post-form");

        // Toggle visibility of the form
        if (formContainer.style.display === "none") {
            formContainer.style.display = "block";
        } else {
            formContainer.style.display = "none";
        }
    });

document.getElementById("cancel-edit-btn").addEventListener("click", function ()
 {
        // Get the form container
        const formContainer = document.getElementById("update-post-form");

        // Toggle visibility of the form
        if (formContainer.style.display === "block") {
            formContainer.style.display = "none";
        } else {
            formContainer.style.display = "none";
        }
    });