// JavaScript function to dynamically add new tag input fields
    function addNewTagField() {
        const container = document.getElementById("new-tags-container");
        const input = document.createElement("input");
        input.type = "text";
        input.name = "new_tags[]";
        input.placeholder = "New tag (optional)";
        input.maxLength = 64;
        container.appendChild(input);
    }