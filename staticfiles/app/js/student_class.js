document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.getElementById('search-button');

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
    
    searchButton.addEventListener('click', function() {
        const studentName = document.getElementById('id_student_name').value;
        const admissionNo = document.getElementById('id_admission_no').value;
        console.log("+++++++++++++++++++++++++",studentName, "++++", admissionNo);

        if (studentName || admissionNo) {
            // fetch(
            //     '/admin/app/student_class/search/', 
            //     {
            //         method: 'POST',
            //         headers: {
            //             'Content-Type': 'application/json',
            //             'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            //         },
            //         body: JSON.stringify({
            //             student_name: studentName,
            //             admission_no: admissionNo
            //         })
            //     }
            // )
            const url = '/admin/app/student_class/ajax/load-students/?student_name=' + student_name +'&admission_no='+ admissionNo;
            fetch(url)
            .then(response => {
                console.log('++++++++++++++ response +++++', response.json());
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json()
            })
            .then(data => {
                console.log('++++++ data ++++++', data);
                const searchResults = document.getElementById('id_search_results');
                searchResults.innerHTML = ''; // Clear previous results

                if (data.length > 0) {
                    data.forEach(student => {
                        const option = document.createElement('option');
                        option.value = student.pk;
                        option.textContent = `${student.student_name}, Class: ${student.class_no}, Section: ${student.section}`;
                        searchResults.appendChild(option);
                    });
                } else {
                    alert('No students found.');
                }
            });
        } else {
            alert('Please enter a student name or admission number to search.');
        }
    });
});