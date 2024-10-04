
/* ========================================================================================== */

$(document).ready(function () {

  console.log("=========== ssssssss testing DOMContentLoaded =====");

  // Get the form elements
  const $admissionNoField = $('input[name="admission_no"]');
  const $studentNameField = $('input[name="student_name"]');
  const $searchButton = $('input[name="search_button"]');
  const $classNoField = $('select[name="class_no"]');
  const $sectionField = $('select[name="section"]');

  const $feesForMonthsField = $('#id_fees_for_months');
  const $feesPeriodMonthField = $('#id_fees_period_month');

  const $studentDropdown = $('#student-dropdown');

  let month = "";
  let stuId = "";

  console.log("admissionNo", $admissionNoField);
  console.log("studentName", $studentNameField);
  console.log("classNo", $classNoField);
  console.log("section", $sectionField);

  // Function to load students based on the search criteria
  function loadStudents() {
    const admissionNo = $admissionNoField.val().trim();
    const studentName = $studentNameField.val().trim();
    const classNo = $classNoField.val().trim();
    const section = $sectionField.val().trim();

    console.log("admissionNo", admissionNo);
    console.log("studentName", studentName);
    console.log("classNo", classNo);
    console.log("section", section);

    if (admissionNo || studentName || section || classNo) {
      const url = new URL("/school-admin/app/student_fee/ajax/load-students/", window.location.origin);
      if (admissionNo) url.searchParams.append("admission_no", admissionNo);
      if (studentName) url.searchParams.append("student_name", studentName);
      if (classNo) url.searchParams.append("class_no", classNo);
      if (section) url.searchParams.append("section", section);

      $.ajax({
        url: url,
        method: 'GET',
        success: function (data) {
          console.log("++++++ response +++++++", data);

          // Clear the dropdown
          $studentDropdown.html('<option value="">Select a Student</option>');

          const students = data.data.split(",");

          console.log("++++++ students +++++++", students);

          students.forEach(function (student) {
            const [idName, classNo] = student.split(":");
            console.log("++++++ idName classNo +++++++", idName, classNo);
            const [id, sname] = idName.split("$");
            console.log("++++++ id +++++++", id);
            $studentDropdown.append(
              $('<option>', {
                value: id, // Use the student_id for the option value
                text: `${sname} (${classNo})` // Display name and class number
              })
            );
          });
        },
        error: function (error) {
          console.error("There was a problem with the fetch operation:", error);
        }
      });
    } else {
      console.warn("Please enter either admission number or student name to search.");
    }
  }

  // Call loadStudents function when the search button is clicked
  $searchButton.on('click', loadStudents);

  if ($studentDropdown.length) {
    $studentDropdown.on('change', async function () {
      const selectedId = $(this).val();
      if (selectedId) {
        await handleStudentId(selectedId);
      }
    });
  }

  async function handleStudentId(studentId) {
    stuId = studentId;

    try {
      const response = await fetch(`/school-admin/app/student_fee/ajax/get-student/?student_id=${studentId}`);
      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();
      const details = data.data.split("$");
      if (details.length >= 7) {
        $('input[name="display_admission_no"]').val(details[5] || "");
        $('input[name="display_student_name"]').val(details[2] || "");
        $('input[name="display_father_name"]').val(details[4] || "");
        $('input[name="display_student_class"]').val(details[1] || "");
        $('input[name="display_student_section"]').val(details[3] || "");
        $('input[name="student_id"]').val(details[0] || "");

        // Extract the year part from the date (e.g., 2024-04-01 -> 2024)
        const selectedYear = details[6].split("-")[0];

        // Set the year field
        const $yearField = $('select[name="started_on"]');
        if ($yearField.length) {
          $yearField.val(selectedYear); // Pre-select the year
        }

        // Trigger the request to load previous fees
        //await loadPreviousFees(studentId, false);

        // Trigger the request to calculate fees
        // await calculateFees(studentId, details[1], month, selectedYear);
        //await feespay();

        // Trigger the request to pay fees (load action_payfees)
        // await loadPayFees(studentId, month);
      } else {
        console.warn("Unexpected data format:", data.data);
      }
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  }





  // ============  show parent portal  ==================

  $("#show-parent-portal").on("click", function () {
    console.log("============  im clicked  ==================");

    // Get the admission number from the input field
    var admissionNo = $("#id_display_admission_no").val();
    console.log("============  admissionNo  ==================", admissionNo);

    if (admissionNo) {
      // Make the AJAX request to send OTP
      $.ajax({
        url: `/send-otp-verification-from-admin/`, // Ensure this URL matches your Django URL routing
        method: "GET",
        data: {
          admissionNumber: admissionNo,
        },
        success: function (response) {
          if (response.success) {
            alert(`OTP sent successfully: ${response.data.otp}`);
            // You can handle further actions like opening a new window here
            // Redirect to the OTP verification page with admission number and OTP in query params
            var url = `/send-otp/?admissionNumber=${admissionNo}&otp=${response.data.otp}`;
            window.open(url, "_blank"); // Open in a new window
            //window.location.href = url;  // Redirect to the OTP verification page
          } else {
            alert(response.message);
          }
        },
        error: function (xhr, status, error) {
          console.error("Error:", error);
          alert("An error occurred while sending the OTP.");
        },
      });
    } else {
      alert("Admission number is required.");
    }
  });
});
