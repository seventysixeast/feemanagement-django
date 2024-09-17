document.addEventListener('DOMContentLoaded', function() {
    const search_results = document.getElementById('id_search_results');
    const searchButton = document.getElementById('search-button');
    const studentIdField = document.getElementById('id_student_id');
    const display_admission_no = document.getElementById('id_display_admission_no');
    const display_student_name = document.getElementById('id_display_student_name');
    var form = document.getElementById('student-class-form');

    // Check if a CSRF token is already present, if not create it
    if (!document.querySelector('[name=csrfmiddlewaretoken]')) {
        var csrfToken = document.createElement('input');
        csrfToken.setAttribute('type', 'hidden');
        csrfToken.setAttribute('name', 'csrfmiddlewaretoken');
        csrfToken.setAttribute('value', getCSRFToken());  // Function to get CSRF token
        
        form.appendChild(csrfToken);
    }

    function getCSRFToken() {
        let name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    searchButton.addEventListener('click',async function() {
        const studentName = document.getElementById('id_student_name').value;
        const admissionNo = document.getElementById('id_admission_no').value;

        if (studentName || admissionNo) {
            try{
                const url = '/school-admin/app/student_class/ajax/load-students/?student_name=' + studentName +'&admission_no='+ admissionNo;
                const response = await fetch(url)
    
                const data = await response.json();  // Parse JSON from the response
                // console.log(data);  // This should log the array of student objects
    
                var searchResults = document.getElementById("id_search_results");
                searchResults.innerHTML = "";  // Clear previous results

                var option = document.createElement("option");
                option.value = "";
                option.textContent = "Select student";
                searchResults.appendChild(option);
    
                data.forEach(function(student) {
                    var option = document.createElement("option");
                    option.value = student.student_id;  // Use the student_id for the option value
                    option.textContent = `${student.student_name} (${student.addmission_no})`;  // Display name and admission number
                    searchResults.appendChild(option);
                });
            } catch (error) {
                console.error('Error:', error);  // Handle errors
            }
        } else {
            alert('Please enter a student name or admission number to search.');
        }
    });

    if (search_results) {
        search_results.addEventListener('change', function () {
            const selectedStudentId = this.value;
            
            if (selectedStudentId) {
                fetch(`/school-admin/app/student_class/ajax/get-student/?student_id=${selectedStudentId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (data.student_id) {
                            console.log('++++++ data ++++++++', data);
                            studentIdField.value = data.student_id;
                            display_student_name.value = data.student_name;
                            display_admission_no.value = data.admission_no;
                            // studentIdField.disabled = false; // Re-enable the field to allow submission
                        }
                    })
                    .catch(error => console.error('Error fetching student data:', error));
            } else {
                studentIdField.value = '';
                display_student_name.value = '';
                display_admission_no.value = '';
            }
        });
    }

});