document.addEventListener("DOMContentLoaded", function () {
  console.log("=========== testing DOMContentLoaded =====");

  // Get the form elements
  const admissionNoField = document.querySelector('input[name="admission_no"]');
  const studentNameField = document.querySelector('input[name="student_name"]');
  const searchButton = document.querySelector('input[name="search_button"]');
  const classNoField = document.querySelector('select[name="class_no"]');
  const sectionField = document.querySelector('select[name="section"]');

  const feesForMonthsField = document.getElementById("id_fees_for_months");
  const feesPeriodMonthField = document.getElementById("id_fees_period_month");

  const studentDropdown = document.getElementById("student-dropdown");

  let month = "";
  let stuId = "";

  console.log("admissionNo", admissionNoField);
  console.log("studentName", studentNameField);
  console.log("classNo", classNoField);
  console.log("section", sectionField);

  // Function to load students based on the search criteria
  async function loadStudents() {
    const admissionNo = admissionNoField.value.trim();
    const studentName = studentNameField.value.trim();
    const classNo = classNoField.value.trim();
    const section = sectionField.value.trim();

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

      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();

        console.log("++++++ response +++++++", response);

        // Clear the dropdown
        studentDropdown.innerHTML =
          '<option value="">Select a Student</option>';

        const students = data.data.split(",");

        console.log("++++++ students +++++++", students);

        students.forEach((student) => {
          const [idName, classNo] = student.split(":");
          console.log("++++++ idName classNo +++++++", idName, classNo);
          const [id, sname] = idName.split("$");
          console.log("++++++ id +++++++", id);
          const option = document.createElement("option");
          option.value = id; // Use the student_id for the option value
          option.textContent = `${sname} (${classNo})`; // Display name and class number
          studentDropdown.appendChild(option);
        });
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    } else {
      console.warn(
        "Please enter either admission number or student name to search."
      );
    }
  }

  if (studentDropdown) {
    studentDropdown.addEventListener("change", async function () {
      const selectedId = this.value;
      if (selectedId) {
        await handleStudentId(selectedId);
      }
    });
  }

  // studentDropdown.addEventListener("change", async function () {
  //   const selectedId = this.value;
  //   if (selectedId) {
  //     await handleStudentId(selectedId);
  //   }
  // });

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
        document.querySelector('input[name="display_admission_no"]').value =
          details[5] || "";
        document.querySelector('input[name="display_student_name"]').value =
          details[2] || "";
        document.querySelector('input[name="display_father_name"]').value =
          details[4] || "";
        document.querySelector('input[name="display_student_class"]').value =
          details[1] || "";
        document.querySelector('input[name="display_student_section"]').value =
          details[3] || "";
        document.querySelector('input[name="student_id"]').value =
          details[0] || "";

        //console.log("details[0]==",Number(details[0]));

        // Extract the year part from the date (e.g., 2024-04-01 -> 2024)
        const selectedYear = details[6].split("-")[0];

        // Set the year field
        const yearField = document.querySelector('select[name="started_on"]');
        if (yearField) {
          yearField.value = selectedYear; // Pre-select the year
        }

        // Trigger the request to load previous fees
        await loadPreviousFees(studentId, false);

        // Trigger the request to calculate fees
        //await calculateFees(studentId, details[1], month, selectedYear);
        await feespay();

        // Trigger the request to pay fees (load action_payfees)
        //await loadPayFees(studentId, month);
      } else {
        console.warn("Unexpected data format:", data.data);
      }
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  }

  // Function to load previous fees
  // async function loadPreviousFees(studentId) {
  //   try {
  //     const response = await fetch(
  //       `/school-admin/app/student_fee/ajax/prev-fees/?student_id=${studentId}`
  //     );
  //     if (!response.ok) throw new Error("Network response was not ok");

  //     const data = await response.json();
  //     const fees = data.data.split("&");

  //     console.log("fees=============", fees);

  //     const feesElement = document.querySelector("#previous-fees-section");

  //     let feesSection = "";

  //     if (feesElement) {
  //       let tableHTML = `
  //       <table class="table">
  //         <thead>
  //           <tr>
  //             <th>Fees For Months</th>
  //             <th>Date Payment</th>
  //             <th>Amount Paid</th>
  //             <th>Fees Period Month</th>
  //             <th>Class</th>
  //           </tr>
  //         </thead>
  //         <tbody>
  //       `;

  //       if (fees && fees.length > 0) {
  //         fees.forEach((fee) => {
  //           const [
  //             feesForMonths,
  //             datePayment,
  //             amountPaid,
  //             feesPeriodMonth,
  //             studentClass,
  //           ] = fee.split("$");

  //           tableHTML += `
  //           <tr>
  //             <td>${feesForMonths}</td>
  //             <td>${datePayment}</td>
  //             <td>${amountPaid}</td>
  //             <td>${feesPeriodMonth}</td>
  //             <td>${studentClass}</td>
  //           </tr>
  //         `;
  //         });
  //       } else {
  //         tableHTML += `
  //         <tr>
  //           <td colspan="5" style="text-align: center;">No previous fees found for this student.</td>
  //         </tr>
  //         `;
  //       }

  //       tableHTML += `</tbody></table>`;
  //       feesElement.innerHTML = tableHTML;
  //     } else {
  //       console.error(
  //         "Error: Element #previous-fees-section not found in the DOM."
  //       );
  //     }
  //   } catch (error) {
  //     console.error("Error loading previous fees:", error);
  //   }
  // }

  // Function to load previous fees and populate either table or form
  async function loadPreviousFees(studentId, populateForm = false) {
    try {
      const response = await fetch(
        `/school-admin/app/student_fee/ajax/prev-fees/?student_id=${studentId}`
      );
      if (!response.ok) throw new Error("Network response was not ok");

      const data = await response.json();
      const fees = data.data.split("&");

      // if (populateForm) {
      //   // Populate form fields with the fetched data
      //   document.querySelector('input[name="tuition_fees_paid"]').value =
      //     data.tuition_fees_paid;
      //   document.querySelector('input[name="annual_fees_paid"]').value =
      //     data.annual_fees_paid;
      //   // Add other form fields accordingly
      // } else {
      // Populate the previous fees table
      const feesElement = document.querySelector("#previous-fees-section");
      let tableHTML = `
      <table class="table">
        <thead>
          <tr>
            <th>Fees For Months</th>
            <th>Date Payment</th>
            <th>Amount Paid</th>
            <th>Fees Period Month</th>
            <th>Class</th>
          </tr>
        </thead>
        <tbody>
      `;

      if (fees && fees.length > 0) {
        fees.forEach((fee) => {
          const [
            feesForMonths,
            datePayment,
            amountPaid,
            feesPeriodMonth,
            studentClass,
          ] = fee.split("$");

          tableHTML += `
          <tr>
            <td>${feesForMonths}</td>
            <td>${datePayment}</td>
            <td>${amountPaid}</td>
            <td>${feesPeriodMonth}</td>
            <td>${studentClass}</td>
          </tr>
        `;
        });
      } else {
        tableHTML += `
        <tr>
          <td colspan="5" style="text-align: center;">No previous fees found for this student.</td>
        </tr>
        `;
      }

      tableHTML += `</tbody></table>`;
      feesElement.innerHTML = tableHTML;
      // }
    } catch (error) {
      console.error("Error loading previous fees:", error);
    }
  }

  const button = document.getElementById("pre-button-id");
  button.addEventListener("click", function () {
    const studentId = document.getElementById("id_student_id").value;
    loadPreviousFees(studentId);
  });

  // const seButton = document.querySelector("#pre-button-id");
  // seButton.addEventListener("click", handleStudentSelection);

  // // Event listener for fetching previous fees and populating form or table
  // // Call this function when the student ID is selected
  // async function handleStudentSelection(event) {
  //   console.log("Full event object:", event);
  //   console.log("Event type:", event.type);
  //   console.log("Button clicked:", event.target);
  //   console.log("Selected Student ID:", studentId); // Check the student ID

  //   await loadPreviousFees(studentId);
  // }
  // document
  //   .getElementById("fetchPreviousFees")
  //   .addEventListener("click", async function () {
  //     console.log("/****  click  ****/");

  //     const studentId = document.querySelector(
  //       'input[name="student_id"]'
  //     ).value;

  //     console.log("/****  studentId  ****/", studentId);

  //     if (studentId) {
  //       // Call the function and pass `true` if you want to populate the form, `false` for the table
  //       await loadPreviousFees(studentId, true); // false means to load into table, true would populate the form
  //     } else {
  //       alert("Please select a student first.");
  //     }
  //   });

  // Attach event listener to search button
  if (searchButton) {
    searchButton.addEventListener("click", loadStudents);
  }

  // Set the current date into date_payment
  const datePaymentField = document.querySelector('input[name="date_payment"]');
  const today = new Date().toISOString().split("T")[0]; // Get the current date in YYYY-MM-DD format
  datePaymentField.value = today;

  // Get relevant fields for cheque
  const paymentModeField = document.querySelector(
    'select[name="payment_mode"]'
  );
  const chequeNoField = document.querySelector('input[name="cheque_no"]');
  const bankNameField = document.querySelector('select[name="bank_name"]');
  const branchNameField = document.querySelector('input[name="branch_name"]');
  const chequeStatusField = document.querySelector(
    'select[name="cheque_status"]'
  );

  // Function to toggle cheque-related fields based on payment mode
  function toggleChequeFields() {
    const paymentMode = paymentModeField.value;

    // Enable/Disable cheque fields based on the payment mode
    const isCheque = paymentMode === "Cheque";
    chequeNoField.disabled = !isCheque;
    bankNameField.disabled = !isCheque;
    branchNameField.disabled = !isCheque;
    chequeStatusField.disabled = !isCheque;

    if (!isCheque) {
      // Clear the values if payment mode is not Cheque
      chequeNoField.value = "";
      bankNameField.value = "";
      branchNameField.value = "";
      chequeStatusField.value = "";
    }
  }

  // Call the function initially in case the form has pre-selected values
  toggleChequeFields();

  // Add event listener to payment mode field to toggle cheque fields when it changes
  paymentModeField.addEventListener("change", toggleChequeFields);

  async function feespay() {
    var fm = document.getElementById("id_fees_for_months").value; // Updated field: fees_for_months
    //var sid = document.querySelector("student_id").value;

    if (fm == "") {
      function setValue(selector, value, defaultValue = "0") {
        console.log("value---", value);

        const element = document.querySelector(`input[name="${selector}"]`);

        if (element) {
          // Convert the value to a number
          let numValue = parseFloat(value);

          // If numValue is NaN or less than 0, use defaultValue
          if (isNaN(numValue) || numValue < 0) {
            numValue = parseFloat(defaultValue);
          }

          // Set the element's value as a string
          element.value = numValue.toString();
        }
      }

      // Clearing the previous fee inputs when no months are selected
      document.getElementById("id_fees_period_month").innerHTML = ""; // Updated: fees_period_month field

      setValue("annual_fees_paid", 0);
      setValue("tuition_fees_paid", 0);
      setValue("funds_fees_paid", 0);
      setValue("sports_fees_paid", 0);
      setValue("admission_fees_paid", 0);
      setValue("dayboarding_fees_paid", 0);
      setValue("miscellaneous_fees_paid", 0);
      setValue("bus_fees_paid", 0);
      setValue("late_fees_paid", 0);
      setValue("activity_fees", 0);
      setValue("concession_type_id", 0);
      setValue("concession_applied", 0);
      setValue("total_amount", 0);
      setValue("amount_paid", 0);
    } else {
      var x = document.getElementById("id_fees_for_months"); // Updated: fees_for_months
      document.getElementById("id_fees_period_month").innerHTML = ""; // Updated: fees_period_month field

      console.log("x------------", x);

      for (var i = 0; i < x.options.length; i++) {
        console.log("x.options[i].selected===", x.options[i].selected);

        if (x.options[i].selected == true) {
          console.log("x.options[i].value===", x.options[i].value);
          var tmpVar = x.options[i].value;

          await monthdata(tmpVar); // Fetch monthly data via AJAX
        }
      }

      var b = tmpVar;
      var feesmonth = tmpVar.split(",");
      var a = feesmonth.length;

      console.log("b------", b);
      console.log("a------", a);

      await feesformonths(a, b); // Process fee calculations
    }
  }

  async function monthdata(tmpVar) {
    try {
      const feesForMonths = tmpVar; // Use the selected month or passed tmpVar
      var studentId = stuId;

      console.log("feesForMonths---", feesForMonths);
      console.log("studentId----", studentId);

      const url = new URL(
        `/school-admin/app/student_fee/ajax/pay-fees/`,
        window.location.origin
      );
      url.searchParams.append("fm", feesForMonths); // Pass fees for months (fm)
      url.searchParams.append("sid", studentId); // Pass student ID (sid)

      console.log("url=======", url);

      const response = await fetch(url);

      console.log("response=====", response);

      if (!response.ok) throw new Error("Network response was not ok");
      const data = await response.json();

      if (data.success) {
        console.log("data----", data);
        console.log("data.data----", data.data);

        const b1 = data.data.split("&");
        const b = b1[0].split("$");
        const h = b[0].split(",");

        // Clear previous options
        const feesPeriodMonthField = document.getElementById(
          "id_fees_period_month"
        );
        feesPeriodMonthField.innerHTML = "";

        console.log("feesPeriodMonthField----", feesPeriodMonthField);

        for (let i = 0; i < h.length; i++) {
          // Append options dynamically to the fees_period_month select element
          const option = document.createElement("option");
          option.selected = true;
          option.id = h[i];
          option.textContent = h[i];
          feesPeriodMonthField.appendChild(option);
        }
      } else {
        console.error("Error loading fee periods:", data.error);
      }
    } catch (error) {
      console.error("There was a problem loading the fee periods:", error);
    }
  }

  async function feesformonths(a, b) {
    var count = a;
    var sessmon = b;

    var sid = document.getElementById("id_student_id").value; // Updated: student_id
    var mf = document.getElementById("id_fees_period_month").value;
    var cls = document.getElementById("id_display_student_class").value; // Updated: student_class
    var class_year = document.getElementById("id_started_on").value; // Updated: year

    console.log("sid-mf-cls-class_year", sid, mf, cls, class_year);

    if (mf != "") {
      var selectedMonthValues = document.querySelector(
        "#id_fees_period_month"
      ).value;
      if (!selectedMonthValues) {
        selectedMonthValues = mf;
      }

      try {
        // Get current value of fees_for_months field
        const selectedMonths = feesForMonthsField.value; // Get current value of fees_for_months
        const url = new URL(
          `/school-admin/app/student_fee/ajax/calculate-fees/`,
          window.location.origin
        );
        url.searchParams.append("sid", sid);
        url.searchParams.append("cls", cls);
        url.searchParams.append("mf", selectedMonths);
        url.searchParams.append("yr", class_year);

        // Fetch data
        const response = await fetch(url);
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();

        // Process the received data
        if (data !== "-----------") {
          console.log("Data received---", data.data);

          const d = data.data.split("|");

          console.log("d=========", d);

          function setValue(selector, value, defaultValue = "0") {
            console.log("value---", value);

            const element = document.querySelector(`input[name="${selector}"]`);

            if (element) {
              // Convert the value to a number
              let numValue = parseFloat(value);

              // If numValue is NaN or less than 0, use defaultValue
              if (isNaN(numValue) || numValue < 0) {
                numValue = parseFloat(defaultValue);
              }

              // Set the element's value as a string
              element.value = numValue.toString();
            }
          }

          // Populate fee fields or set default value
          setValue("annual_fees_paid", d[0]);
          setValue("tuition_fees_paid", d[1]);
          setValue("funds_fees_paid", d[2]);
          setValue("sports_fees_paid", d[3]);
          setValue("activity_fees", d[4]);
          setValue("admission_fees_paid", d[5]);
          setValue("security_fees", d[6]);
          setValue("dayboarding_fees_paid", d[7]);
          setValue("miscellaneous_fees_paid", d[8]);
          setValue("bus_fees_paid", d[9]);
          setValue("concession_applied", d[10]);
          setValue("late_fees_paid", d[11]);
          setValue("total_amount", d[12]);

          const concession = (document.querySelector(
            'input[name="concession_applied"]'
          ).value = d[13] || "");
          document.querySelector('input[name="concession_type"]').value =
            d[16] || "";

          // Calculate total amount
          const annualfees =
            parseInt(
              document.querySelector('input[name="annual_fees_paid"]').value
            ) || 0;
          console.log("annualfees", annualfees);
          const tutionfees =
            parseInt(
              document.querySelector('input[name="tuition_fees_paid"]').value
            ) || 0;
          console.log("tutionfees", tutionfees);
          const fundfees =
            parseInt(
              document.querySelector('input[name="funds_fees_paid"]').value
            ) || 0;
          console.log("fundfees", fundfees);
          const sportsfees =
            parseInt(
              document.querySelector('input[name="sports_fees_paid"]').value
            ) || 0;
          console.log("sportsfees", sportsfees);
          const admfees =
            parseInt(
              document.querySelector('input[name="admission_fees_paid"]').value
            ) || 0;
          console.log("admfees", admfees);
          const dayboardfees =
            parseInt(
              document.querySelector('input[name="dayboarding_fees_paid"]')
                .value
            ) || 0;
          console.log("dayboardfees", dayboardfees);
          const busfees =
            parseInt(
              document.querySelector('input[name="bus_fees_paid"]').value
            ) || 0;
          console.log("busfees", busfees);
          const activityfees =
            parseInt(
              document.querySelector('input[name="activity_fees"]').value
            ) || 0;
          console.log("activityfees", activityfees);
          //const concession = parseInt(document.querySelector("concession_applied").value) || 0;
          console.log("concession", concession);
          const miscfees =
            parseInt(
              document.querySelector('input[name="miscellaneous_fees_paid"]')
                .value
            ) || 0;
          console.log("miscfees", miscfees);
          const latefees =
            parseInt(
              document.querySelector('input[name="late_fees_paid"]').value
            ) || 0;
          console.log("latefees", latefees);

          // Calculate total based on data[16] or manually
          const total =
            d[12] ||
            annualfees +
              tutionfees +
              fundfees +
              sportsfees +
              activityfees +
              admfees +
              dayboardfees +
              busfees +
              latefees -
              concession;

          console.log("total=====", total);

          document.querySelector('input[name="total_amount"]').value = total;
          document.querySelector('input[name="amount_paid"]').value = total;
        } else {
          alert("Fees are not inserted for this class");
        }
      } catch (error) {
        console.error("There was a problem calculating fees:", error);
      }
    } else {
      alert("Please select fees for months first.");
    }
  }

  // Assuming these are your input elements
  const feesForMonths = document.getElementById("id_fees_for_months");

  const feesPeriodMonthElement = document.querySelector(
    'select[name="fees_period_month"]'
  ); // Select element for fees_period_month
  const feesForMonthsElement = document.querySelector(
    'select[name="fees_for_months"]'
  ); // Select element for fees_for_months

  // Event listener for fees_period_month
  if (feesPeriodMonthElement) {
    feesPeriodMonthElement.addEventListener("change", function () {
      // Capture the changed value of fees_period_month
      let periodValue = Array.from(this.selectedOptions)
        .map((option) => option.value)
        .join(",");

      console.log("periodValue (fees_period_month)--------", periodValue);

      // Update fees_for_months based on the periodValue
      updateFeesMonthsBasedOnPeriod(periodValue);
    });
  } else {
    console.error("fees_period_month element not found!");
  }

  // Event listener for fees_for_months
  if (feesForMonthsElement) {
    feesForMonthsElement.addEventListener("change", function () {
      let monthsValue = Array.from(this.selectedOptions)
        .map((option) => option.value)
        .join(",");

      console.log("monthsValue (fees_for_months)--------", monthsValue);

      // Update fees_period_month based on monthsValue
      updateFeesPeriodBasedOnMonths(monthsValue);
    });
  } else {
    console.error("fees_for_months element not found!");
  }

  // Update fees_for_months based on fees_period_month
  async function updateFeesMonthsBasedOnPeriod(periodValue) {
    const feesForMonthsElement = document.querySelector(
      'select[name="fees_for_months"]'
    ); // Select element for fees_for_months

    if (feesForMonthsElement) {
      // Split the periodValue (comma-separated) and select the corresponding options in the fees_for_months select element
      const monthsArray = periodValue.split(",");

      // Clear all previous selections
      for (let i = 0; i < feesForMonthsElement.options.length; i++) {
        feesForMonthsElement.options[i].selected = false;
      }

      // Select the matching options in the fees_for_months element
      monthsArray.forEach((month) => {
        let option = Array.from(feesForMonthsElement.options).find(
          (opt) => opt.value === month.trim()
        );
        if (option) {
          option.selected = true;
        }
      });

      await feesformonths();
    } else {
      console.error("fees_for_months element not found!");
    }
  }

  // Update fees_period_month based on fees_for_months
  async function updateFeesPeriodBasedOnMonths(monthsValue) {
    const feesPeriodMonthElement = document.querySelector(
      'select[name="fees_period_month"]'
    ); // Select element for fees_period_month

    if (feesPeriodMonthElement) {
      // Split the monthsValue (comma-separated) and select the corresponding options in the fees_period_month select element
      const monthsArray = monthsValue.split(",");

      // Clear all previous selections
      for (let i = 0; i < feesPeriodMonthElement.options.length; i++) {
        feesPeriodMonthElement.options[i].selected = false;
      }

      // Select the matching options in the fees_period_month element
      monthsArray.forEach((month) => {
        let option = Array.from(feesPeriodMonthElement.options).find(
          (opt) => opt.value === month.trim()
        );
        if (option) {
          option.selected = true;
        }
      });

      await feespay();
    } else {
      console.error("fees_period_month element not found!");
    }
  }

  // ============  show parent portal  ==================

  document
    .getElementById("show_parent_portal")
    .addEventListener("click", function () {
      var admissionNumber = document.getElementById(
        "id_display_admission_no"
      ).value;

      // Perform AJAX request to get OTP
      $.ajax({
        url: "/send-otp-verification/", // Django URL for sending OTP
        method: "GET",
        data: {
          admissionNumber: admissionNumber,
        },
        success: function (response) {
          if (response.success) {
            // OTP sent successfully
            var receivedOTP = response.otp;

            // Construct the URL with the received OTP
            var url =
              "https://shishuniketanmohali.org.in/pay-fees.php?admission_number=" +
              encodeURIComponent(admissionNumber) +
              "&otp=" +
              encodeURIComponent(receivedOTP);

            // Open the URL in a new tab
            window.open(url, "_blank");
          } else {
            alert(response.message);
          }
        },
        error: function () {
          alert("Error sending OTP request.");
        },
      });
    });

  // If it's an update case, prefill the admission number and enable the button
  function prefillAdmissionNumber(isUpdate, admissionNumber) {
    if (isUpdate) {
      document.getElementById("admission_number").value = admissionNumber;
      document.getElementById("show_parent_portal").disabled = false;
    }
  }
});
