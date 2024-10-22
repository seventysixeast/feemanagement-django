/* ========================================================================================== */

$(document).ready(function () {
  // console.log("=========== ssssssss testing DOMContentLoaded =====");

  // Get the form elements
  const $admissionNoField = $('input[name="admission_no"]');
  const $studentNameField = $('input[name="student_name"]');
  const $searchButton = $('input[name="search_button"]');
  const $classNoField = $('select[name="class_no"]');
  const $sectionField = $('select[name="section"]');

  const feesPeriodMonthElement = $('select[name="fees_period_month"]'); // Select element for fees_period_month
  const feesForMonthsElement = $('select[name="fees_for_months"]'); // Select element for fees_for_months

  const $studentDropdown = $("#student-dropdown");

  let month = "";
  let stuId = "";

  // console.log("admissionNo", $admissionNoField);
  // console.log("studentName", $studentNameField);
  // console.log("classNo", $classNoField);
  // console.log("section", $sectionField);

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
      const url = new URL(
        "/school-admin/app/student_fee/ajax/load-students/",
        window.location.origin
      );
      if (admissionNo) url.searchParams.append("admission_no", admissionNo);
      if (studentName) url.searchParams.append("student_name", studentName);
      if (classNo) url.searchParams.append("class_no", classNo);
      if (section) url.searchParams.append("section", section);

      $.ajax({
        url: url,
        method: "GET",
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
              $("<option>", {
                value: id, // Use the student_id for the option value
                text: `${sname} (${classNo})`, // Display name and class number
              })
            );
          });
        },
        error: function (error) {
          console.error("There was a problem with the fetch operation:", error);
        },
      });
    } else {
      console.warn(
        "Please enter either admission number or student name to search."
      );
    }
  }

  // Call loadStudents function when the search button is clicked
  $searchButton.on("click", loadStudents);

  if ($studentDropdown.length) {
    $studentDropdown.on("change", async function () {
      const selectedId = $(this).val();
      if (selectedId) {
        await handleStudentId(selectedId);
      }
    });
  }

  // get the specific student detail
  async function handleStudentId(studentId) {
    stuId = studentId;

    try {
      const response = await fetch(
        `/school-admin/app/student_fee/ajax/get-student/?student_id=${studentId}`
      );
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
        await loadPreviousFees(studentId, false);

        // Trigger the request to calculate fees
        // await calculateFees(studentId, details[1], month, selectedYear);
        await feespay();

        // Trigger the request to pay fees (load action_payfees)
        // await loadPayFees(studentId, month);
      } else {
        console.warn("Unexpected data format:", data.data);
      }
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  }

  // Function to load previous fees and populate either table or form
  async function loadPreviousFees(studentId) {
    try {
      const response = await fetch(
        `/school-admin/app/student_fee/ajax/prev-fees/?student_id=${studentId}`
      );
      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      const fees = data.data.split("&");

      const $feesElement = $("#previous-fees-section"); // jQuery to select the placeholder
      let tableHTML = `
      <table class="table table-striped" style="width: 100%; border-collapse: collapse;">
          <thead>
              <tr>
                <th>Class</th>
                <th>Fees for month</th>
                <th>Fees paid for month</th>
                <th>Payment Date</th>
                <th>Amount Paid</th>
                <th>Not Paid</th>
                <th>Remarks</th>
              </tr>
          </thead>
          <tbody>
      `;

      if (fees && fees.length > 0 && data.data != '') {
        fees.forEach((fee) => {


          console.log("previous fees data ===", fee);


          const [fees_for_months, date_payment, amount_paid, fees_period_month, student_class, remarks, cheque_status] =
            fee.split("$");

          tableHTML += `
              <tr>
                  <td>${student_class}</td>
                  <td>${fees_for_months}</td>
                  <td>${fees_period_month}</td>
                  <td>${date_payment}</td>
                  <td>${amount_paid}</td>
                  <td>${cheque_status}</td>
                  <td>${remarks}</td>
              </tr>`;
        });
      } else {
        tableHTML += `
          <tr>
              <td colspan="7" style="text-align: center;">No previous fees found for this student.</td>
          </tr>`;
      }

      tableHTML += `</tbody></table>`;
      $feesElement.html(tableHTML); // Use jQuery to insert the HTML content
    } catch (error) {
      console.error("Error loading previous fees:", error);
    }
  }

  $(document).ready(function () {
    $("#pre-button-id").on("click", function () {
      var studentId = $("#id_student_id").val();
      loadPreviousFees(studentId);
    });
  });

  // collapse pervious fees
  $("fieldset.collapse").each(function () {
    // Add toggle button to the fieldset
    $(this)
      .find("h2")
      .first()
      .append('<a class="collapse-toggle" href="#">(Show)</a>');

    // Check if the fieldset is collapsed by default
    if ($(this).hasClass("collapsed")) {
      $(this).find(".form-row").hide();
    }

    // Toggle the visibility when the toggle is clicked
    $(this)
      .find(".collapse-toggle")
      .on("click", function (e) {
        e.preventDefault();
        var $fieldset = $(this).closest("fieldset");
        if ($fieldset.hasClass("collapsed")) {
          $fieldset.removeClass("collapsed").find(".form-row").show();
          $(this).text("(Hide)");
        } else {
          $fieldset.addClass("collapsed").find(".form-row").hide();
          $(this).text("(Show)");
        }
      });
  });

  // Set the current date into date_payment
  const today = new Date().toISOString().split("T")[0]; // Get the current date in YYYY-MM-DD format
  $('input[name="date_payment"]').val(today);

  // Get relevant fields for cheque
  const paymentModeField = $('select[name="payment_mode"]');
  const chequeNoField = $('input[name="cheque_no"]');
  const bankNameField = $('select[name="bank_name"]');
  const branchNameField = $('input[name="branch_name"]');
  const chequeStatusField = $('select[name="cheque_status"]');

  // Function to toggle cheque-related fields based on payment mode
  function toggleChequeFields() {
    const paymentMode = paymentModeField.val();

    // Enable/Disable cheque fields based on the payment mode
    const isCheque = paymentMode === "Cheque";
    chequeNoField.prop("disabled", !isCheque);
    bankNameField.prop("disabled", !isCheque);
    branchNameField.prop("disabled", !isCheque);
    chequeStatusField.prop("disabled", !isCheque);

    if (!isCheque) {
      // Clear the values if payment mode is not Cheque
      chequeNoField.val("");
      bankNameField.val("");
      branchNameField.val("");
      chequeStatusField.val("");
    }
  }

  // Call the function initially in case the form has pre-selected values
  toggleChequeFields();

  // Add event listener to payment mode field to toggle cheque fields when it changes
  paymentModeField.on("change", toggleChequeFields);

  async function monthdata(tmpVar) {
    try {
      const studentId = stuId; // Assuming `stuId` is globally available

      //console.log("tmpVar------", tmpVar);


      const url = new URL(
        `/school-admin/app/student_fee/ajax/pay-fees/`,
        window.location.origin
      );
      url.searchParams.append("fm", tmpVar);
      url.searchParams.append("sid", studentId);

      //console.log("url----tmpVar------", url);


      const response = await fetch(url);
      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      if (data.success) {
        const feesPeriods = data.data.split("&")[0].split("$")[0].split(",");
        const feesPeriodMonthField = $("#id_fees_period_month");
        feesPeriodMonthField.empty();

        feesPeriods.forEach((period) => {
          feesPeriodMonthField.append(new Option(period, period, true, true));
        });
      } else {
        console.error("Error loading fee periods:", data.error);
      }
    } catch (error) {
      console.error("There was a problem loading the fee periods:", error);
    }
  }

  async function feesformonths(a, b) {
    var sid = $("#id_student_id").val(); // Get the student ID
    var mf = $("#id_fees_period_month").val(); // Get the selected fee periods
    var cls = $("#id_display_student_class").val(); // Get the class
    var class_year = $("#id_started_on").val(); // Get the class year

    if (mf) {

      // Get the current browser URL
      const currentBrowserUrl = window.location.href;

      // Define the pattern for the update URL in Django (e.g., "/change/" for updates)
      const updateUrlPattern = /\/change\/$/; // Ends with "/change/"

      if (!updateUrlPattern.test(currentBrowserUrl)) {
        //console.log("This is an update URL for Django and not an API URL.");

        // Call your logic for handling update URLs (e.g., skip API calls, load data, etc.)
        try {
          const url = new URL(
            `/school-admin/app/student_fee/ajax/calculate-fees/`,
            window.location.origin
          );
          url.searchParams.append("sid", sid);
          url.searchParams.append("cls", cls);
          url.searchParams.append("mf", mf); // Pass the selected months
          url.searchParams.append("yr", class_year);

          const response = await fetch(url);
          if (!response.ok) throw new Error("Network response was not ok");

          const data = await response.json();
          if (data !== "-----------") {
            const d = data.data.split("|");
            const fields = [
              "annual_fees_paid",
              "tuition_fees_paid",
              "funds_fees_paid",
              "sports_fees_paid",
              "activity_fees",
              "admission_fees_paid",
              "security_fees",
              "dayboarding_fees_paid",
              "miscellaneous_fees_paid",
              "bus_fees_paid",
              "concession_amount",
              "concession_applied",
              'concession_percent',
              'concession_id',
              'concession_type',
              "late_fees_paid",
              "total_amount",
            ];

            console.log("d--------",d);
            
            

            fields.forEach((field, index) => setValue(field, d[index] || 0));

            const concession = d[11] || "";
            $('input[name="concession_applied"]').val(concession);
            $('input[name="concession_type"]').val(d[14] || "");
            $('input[name="concession_type_id"]').val(d[13] || "");
            

            const total = d[16] || calculateTotal(d);
            $('input[name="total_amount"]').val(total);
            $('input[name="amount_paid"]').val(total);
          } else {
            alert("Fees are not inserted for this class");
          }
        } catch (error) {
          console.error("There was a problem calculating fees:", error);
        }
      }

    } else {
      alert("Please select fees for months first.");
    }
  }

  function calculateTotal(data) {
    return (
      ["0", "1", "2", "3", "4", "5", "7", "8", "9", "11"].reduce(
        (sum, index) => sum + (parseInt(data[index]) || 0),
        0
      ) - (parseInt(data[10]) || 0)
    );
  }

  function setValue(selector, value, defaultValue = "0") {

    console.log("selector--------",selector);
            console.log("value--------",value);

    let numValue = parseFloat(value);
    if (isNaN(numValue) || numValue < 0) numValue = parseFloat(defaultValue);
    $(`input[name="${selector}"]`).val(numValue.toString());
  }

  



  // Event listener for changes in fees_period_month
  feesPeriodMonthElement.on("change", async function () {
    const selectedFeesPeriodMonths = getSelectedValues("fees_period_month");

    console.log("Selected Fees Period Months: ", selectedFeesPeriodMonths);

    if (selectedFeesPeriodMonths.length === 0) {
      // If no months are selected in fees_period_month, do not clear fees_for_months
      //const selectedFeesForMonths = getSelectedValues("fees_for_months");
      //setFeesForMonths(selectedFeesForMonths);
      await feesformonths();  // Call feespay based on fees_for_months
    } else {
      // Only update fees_for_months if it's necessary
      //setFeesForMonths(selectedFeesPeriodMonths);
      await feesformonths();  // Call feespay based on fees_period_month
    }
  });

  // Change handler for fees_for_months to filter the options in fees_period_month
  feesForMonthsElement.on("change", async function () {
    const selectedFeesForMonths = getSelectedValues("fees_for_months");
    console.log("Selected Fees for Months:", selectedFeesForMonths);

    // Update the options shown in fees_period_month
    filterFeesPeriodMonths(selectedFeesForMonths);

    // Set fees_period_month based on the selected fees_for_months
    const allSelectedMonths = getAllSelectedMonths(selectedFeesForMonths);
    setFeesPeriodMonths(allSelectedMonths);

    // Fetch the latest fees when fees_for_months changes
    await feespay();
  });

  // Function to set fees_period_month based on selected fees_for_months
  function setFeesPeriodMonths(selectedMonths) {
    $("#id_fees_period_month option").each(function () {
      $(this).prop("selected", selectedMonths.includes($(this).val()));
    });
  }

  // Function to set fees_for_months based on selected fees_period_month
  function setFeesForMonths(selectedMonths) {
    $("#id_fees_for_months option").each(function () {
      const monthValue = $(this).val();
      if (selectedMonths.includes(monthValue)) {
        $(this).prop("selected", true);
      } else {
        $(this).prop("selected", false);
      }
    });
    $("#id_fees_for_months").trigger("change");
  }

  // Function to retrieve selected values as an array
  function getSelectedValues(fieldId) {
    return $(`#id_${fieldId}`).val() || [];
  }

  // Function to get all selected months based on selected fees_for_months
  function getAllSelectedMonths(selectedFeesForMonths) {
    let allMonths = new Set();
    selectedFeesForMonths.forEach(monthGroup => {
      monthGroup.split(",").forEach(month => {
        allMonths.add(month.trim());
      });
    });
    return Array.from(allMonths);
  }

  function filterFeesPeriodMonths(selectedMonths) {
    $("#id_fees_period_month").empty();  // Clear existing options

    // Flatten selectedMonths array to get individual months (e.g., ["1", "2", "3"])
    const individualMonths = selectedMonths.flatMap(monthGroup => monthGroup.split(','));

    // Remove duplicates and sort months numerically
    const uniqueMonths = [...new Set(individualMonths)].sort((a, b) => a - b);

    // Add unique months as options to fees_period_month with an id
    uniqueMonths.forEach(function (month) {
      // Create a unique id for each option using a prefix, like 'month_'
      const newOption = $("<option></option>")
        .val(month)
        .text(month)
        .attr("id", `month_${month}`);  // Assign an id like 'month_1', 'month_2', etc.

      $("#id_fees_period_month").append(newOption);  // Append the option to the select element
    });
  }

  // Existing feespay function updated to handle an array directly
  async function feespay() {
    var fm = $("#id_fees_for_months").val();

    if (!fm || fm.length === 0) {
      resetFeesFields();
    } else {
      var selectedMonths = getAllSelectedMonths(fm);
      await monthdata(selectedMonths);
      await feesformonths(selectedMonths.length, selectedMonths);
    }
  }

  // Function to reset fees fields
  function resetFeesFields() {
    function setValue(selector, value, defaultValue = "0") {
      let numValue = parseFloat(value);
      if (isNaN(numValue) || numValue < 0) numValue = parseFloat(defaultValue);
      $(`input[name="${selector}"]`).val(numValue.toString());
    }

    const feeFields = [
      "annual_fees_paid", "tuition_fees_paid", "funds_fees_paid",
      "sports_fees_paid", "admission_fees_paid", "dayboarding_fees_paid",
      "miscellaneous_fees_paid", "bus_fees_paid", "late_fees_paid",
      "activity_fees", "concession_type_id", "concession_applied",
      "total_amount", "amount_paid"
    ];

    feeFields.forEach(field => setValue(field, 0));
  }

  // ============  show parent portal  ==================
  $("#show-parent-portal").on("click", function () {
    //console.log("============  im clicked  ==================");

    // Get the admission number from the input field
    var admissionNo = $("#id_display_admission_no").val();
    //console.log("============  admissionNo  ==================", admissionNo);

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

  // Check if the student_id field has a value (i.e., editing mode)
  if ($('#id_student_id').val()) {
    // Hide the search section if student_id exists
    $('.search-student-section').hide();
  }

  $(".feeschange").change(function() {
    // Set the value of the 'isdefault' field to "false" when any fees field changes
    //document.getElementById('isdefault').value = "false";

    // Get the values of the fees fields, and use 0 as default if not filled
    let annualFeesPaid = parseInt($("#id_annual_fees_paid").val()) || 0;
    let tuitionFeesPaid = parseInt($("#id_tuition_fees_paid").val()) || 0;
    let fundsFeesPaid = parseInt($("#id_funds_fees_paid").val()) || 0;
    let sportsFeesPaid = parseInt($("#id_sports_fees_paid").val()) || 0;
    let activityFees = parseInt($("#id_activity_fees").val()) || 0;
    let admissionFeesPaid = parseInt($("#id_admission_fees_paid").val()) || 0;
    let dayboardingFeesPaid = parseInt($("#id_dayboarding_fees_paid").val()) || 0;
    let miscellaneousFeesPaid = parseInt($("#id_miscellaneous_fees_paid").val()) || 0;
    let busFeesPaid = parseInt($("#id_bus_fees_paid").val()) || 0;
    let concessionApplied = parseInt($("#id_concession_applied").val()) || 0;
    let lateFeesPaid = parseInt($("#id_late_fees_paid").val()) || 0;

    // Calculate the total amount
    let totalAmount = annualFeesPaid + tuitionFeesPaid + fundsFeesPaid + sportsFeesPaid +
                      activityFees + admissionFeesPaid + dayboardingFeesPaid + 
                      miscellaneousFeesPaid + busFeesPaid + lateFeesPaid - concessionApplied;

    // Update the total amount and amount paid fields
    $("#id_total_amount").val(totalAmount);
    $("#id_amount_paid").val(totalAmount);
});

});
