document.addEventListener('DOMContentLoaded', function() {
    const class_no = document.getElementById('id_class_no');
    const student_name = document.getElementById('id_student_name');

    if (class_no) {
        class_no.addEventListener('change', function () {
            const selectedClass = this.value;
            if (selectedClass) {
                fetch(`/school-admin/app/specialfee_master/ajax/get-students/?class_no=${selectedClass}`)
                .then(response => response.json())
                .then(data => {

                    var studentNames = document.getElementById("id_student_name");
                    studentNames.innerHTML = "";  // Clear previous results

                    var option = document.createElement("option");
                    option.value = "";
                    option.textContent = "Select student";
                    studentNames.appendChild(option);

                    data.forEach(function(student) {
                        var option = document.createElement("option");
                        option.value = student.student_id + '-' + student.class_id;  // Use the student_id and student_class_id for the option value
                        option.textContent = `${student.class_no} ${student.section} ${student.student_name}`;  // Display name and admission number
                        studentNames.appendChild(option);
                    });
                })
                .catch(error => console.error('Error fetching student data:', error));
            } else {
                // Clear student_name dropdown if no class_no is selected
                studentNames.innerHTML = "";
                var option = document.createElement("option");
                option.value = "";
                option.textContent = "Select student";
                studentNames.appendChild(option);
            }
        });
    }

    if (student_name) {
        student_name.addEventListener('change', function () {
            const selectedValue = this.value;
    
            if (selectedValue) {
                const [student_id, student_class_id] = selectedValue.split('-');
                // Assign the values to the hidden input fields
                document.getElementById('id_student_id').value = student_id;
                document.getElementById('id_student_class_id').value = student_class_id;
            }
        });
    }
    

    const feeTypeField = document.getElementById('id_fee_type');
    const monthsApplicableForField = document.getElementById('id_months_applicable_for');

    const MONTHS = [
        ['', 'Please Select Month'],
        ['1', 'January'],
        ['2', 'February'],
        ['3', 'March'],
        ['4', 'April'],
        ['5', 'May'],
        ['6', 'June'],
        ['7', 'July'],
        ['8', 'August'],
        ['9', 'September'],
        ['10', 'October'],
        ['11', 'November'],
        ['12', 'December']
    ];

    // Function to populate months_applicable_for based on data from the server
    function populateMonthsDropdown() {
        const feeType = feeTypeField.value;
        console.log('+++++++ feeType 123 ++++++++', feeType);

        fetch(`/school-admin/app/specialfee_master/ajax/get-payment-schedules/?feeType=${feeType}`)
        .then(response => response.json())
        .then(data => {
            console.log('+++++++ data ++++++++', data);

            // Clear the current options
            monthsApplicableForField.innerHTML = '';

            // Add a placeholder option
            const placeholder = document.createElement('option');
            placeholder.value = "";
            placeholder.textContent = "Please Select";
            monthsApplicableForField.appendChild(placeholder);

            // Populate dropdown with the payment schedule data
            data.forEach(schedule => {
                const option = document.createElement('option');
                option.value = schedule.fees_for_months;
                option.textContent = `${schedule.fees_for_months}`;  // Customize based on your model fields
                monthsApplicableForField.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching payment schedules:', error));
    }

    // Function to update the dropdown choices based on the selected fee type
    function updateMonthsApplicableChoices() {
        const feeType = feeTypeField.value;
        console.log("++++++ feeType ++++++++++", feeType);

        if (feeType === 'bus_fees') {
            monthsApplicableForField.innerHTML = '';
            // Fetch the payment schedule data only for bus_fees
            // populateMonthsDropdown();
            MONTHS.forEach(choice => {
                const option = new Option(choice[1], choice[0]);
                monthsApplicableForField.add(option);
            });
            monthsApplicableForField.removeAttribute('disabled');
        } else if (feeType === 'ignore_prev_outstanding_fees') {
            // Disable the field for ignore_prev_outstanding_fees
            monthsApplicableForField.setAttribute('disabled', 'disabled');
            monthsApplicableForField.value = null;
        } else {
            // Fetch the payment schedule data for other fee types
            populateMonthsDropdown(feeType);
            monthsApplicableForField.removeAttribute('disabled');
        }
    }



    // // Function to update the choices based on the selected fee type
    // function updateMonthsApplicableChoices() {
    //     const feeType = feeTypeField.value;

    //     // Clear the current options
    //     monthsApplicableForField.innerHTML = '';

    //     if (feeType === 'bus_fees') {
    //         // Use MONTHS choices
    //         console.log('+++++ BUS FEES +++++++');
    //         MONTHS.forEach(choice => {
    //             const option = new Option(choice[1], choice[0]);
    //             monthsApplicableForField.add(option);
    //         });
    //         monthsApplicableForField.removeAttribute('disabled');
    //         // monthsApplicableForField.setAttribute('required', 'required');
    //     } else if (feeType === 'ignore_prev_outstanding_fees') {
    //         console.log('+++++ ignore_prev_outstanding_fees +++++++');
    //         // Disable the field and set its value to null
    //         monthsApplicableForField.setAttribute('disabled', 'disabled');
    //         monthsApplicableForField.value = null;
    //         // monthsApplicableForField.removeAttribute('required');
    //     } else {
    //         // Use MONTHS_APPL_CHOICES choices
    //         console.log('+++++ Except BUS FEES +++++++');
    //         MONTHS_APPL_CHOICES.forEach(choice => {
    //             const option = new Option(choice[1], choice[0]);
    //             monthsApplicableForField.add(option);
    //         });
    //         monthsApplicableForField.removeAttribute('disabled');
    //         // monthsApplicableForField.setAttribute('required', 'required');
    //     }
    // }

    // Initialize the choices on page load
    updateMonthsApplicableChoices();

    // Update the choices when the fee type changes
    feeTypeField.addEventListener('change', updateMonthsApplicableChoices);
});
