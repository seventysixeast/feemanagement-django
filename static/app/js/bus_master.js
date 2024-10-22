document.addEventListener("DOMContentLoaded", function() {
    // Get all error and success messages
    const errorMessage = document.querySelector(".messagelist .error");
    const successMessages = document.querySelectorAll(".messagelist .success");

    // If there's an error message, hide all success messages
    if (errorMessage && successMessages.length > 0) {
        successMessages.forEach(function(successMessage) {
            successMessage.style.display = "none";
        });
    } else if (successMessages.length > 1) {
        // If multiple success messages, show only the first one and hide the rest
        successMessages.forEach(function(successMessage, index) {
            if (index !== 0) {
                successMessage.style.display = "none";
            }
        });
    }
});
