document.addEventListener("DOMContentLoaded", function () {
    // Get the form elements
    const admissionNoField = document.querySelector('input[name="admission_no"]');
    const studentNameField = document.querySelector('input[name="student_name"]');
    const searchButton = document.querySelector('input[name="search_button"]');
    const feesForMonthsField = document.querySelector('select[name="fees_for_months"]');
    //const feesForMonthsField = document.getElementById('id_fees_for_months');
    const feesPeriodMonthField = document.getElementById('id_fees_period_month');
  
    let month = '';
  
    // Function to create the table structure
    /* function createTable() {
      const container = document.querySelector("#previous-fees-record");
      if (!container) {
        console.error("Container for table not found");
        return;
      }
  
      // Create table
      const table = document.createElement("table");
      table.id = "feesTable";
      table.className = "table table-striped";
  
      // Create table header
      const thead = document.createElement("thead");
      const headerRow = document.createElement("tr");
      const headers = ["Fees For Months", "Date Payment", "Amount Paid", "Fees Period Month", "Student Class"];
      headers.forEach(headerText => {
        const th = document.createElement("th");
        th.textContent = headerText;
        headerRow.appendChild(th);
      });
      thead.appendChild(headerRow);
      table.appendChild(thead);
  
      // Create table body
      const tbody = document.createElement("tbody");
      table.appendChild(tbody);
  
      // Append the table to the container
      container.innerHTML = "";  // Clear any existing content
      container.appendChild(table);
    }
   */
    // Function to load students based on the search criteria
    async function loadStudents() {
      const admissionNo = admissionNoField.value.trim();
      const studentName = studentNameField.value.trim();
  
      if (admissionNo || studentName) {
        const url = new URL(
          "/admin/app/student_fee/ajax/load-students/",
          window.location.origin
        );
        if (admissionNo) url.searchParams.append("admission_no", admissionNo);
        if (studentName) url.searchParams.append("student_name", studentName);
  
        try {
          const response = await fetch(url);
          if (!response.ok) throw new Error("Network response was not ok");
          const data = await response.json();
          const students = data.data.split(",");
          students.forEach(async (student) => {
            const [idName, classNo] = student.split(":");
            const [id] = idName.split("$");
            await handleStudentId(id);
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
  
    async function handleStudentId(studentId) {
      try {
        const response = await fetch(
          `/admin/app/student_fee/ajax/get-student/?student_id=${studentId}`
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
          document.querySelector('input[name="student_id"]').value = details[0] || "";
  
          //console.log("details[0]==",Number(details[0]));
          
  
          // Extract the year part from the date (e.g., 2024-04-01 -> 2024)
          const selectedYear = details[6].split("-")[0];
  
          // Set the year field
          const yearField = document.querySelector('select[name="display_year"]');
          if (yearField) {
            yearField.value = selectedYear; // Pre-select the year
          }
  
          // Trigger the request to load previous fees
          await loadPreviousFees(studentId);
  
          // Trigger the request to calculate fees
          await calculateFees(studentId, details[1], month, selectedYear);
  
          // Trigger the request to pay fees (load action_payfees)
          await loadPayFees(studentId, month);
  
        } else {
          console.warn("Unexpected data format:", data.data);
        }
      } catch (error) {
        console.error("There was a problem with the fetch operation:", error);
      }
    }
  
    async function calculateFees(studentId, studentClass, month, year) {
      try {
        // Get current value of fees_for_months field
        const selectedMonths = feesForMonthsField.value; // Get current value of fees_for_months
        const url = new URL(`/admin/app/student_fee/ajax/calculate-fees/`, window.location.origin);
        url.searchParams.append("sid", studentId);
        url.searchParams.append("cls", studentClass);
        url.searchParams.append("mf", selectedMonths);
        url.searchParams.append("yr", year);
  
        // Fetch data
        const response = await fetch(url);
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
  
        // Process the received data
        if (data !== '-----------') {
  
          console.log("Data received---", data.data);
  
          const d = data.data.split('|');
  
          console.log("d=========", d);
  
          // Helper function to set input value
          /* function setValue(selector, value, defaultValue = '0') {
            console.log("value---",value);
            
            const element = document.querySelector(`input[name="${selector}"]`);
            if (element && element.value != 'undefined') {
              element.value = parseInt(value) > 0 ? parseInt(value) : defaultValue;
            }
          }
          */
  
          function setValue(selector, value, defaultValue = '0') {
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
  
          const concession = document.querySelector('input[name="concession_applied"]').value = d[13] || "";
          document.querySelector('input[name="concession_type"]').value = d[16] || "";
  
          /* 
          Updated annual_fees: 0
          Updated tuition_fees: 9465.0
          Updated funds_fees: 0.0
          Updated sports_fees: 0
          Updated activity_fees: 0
          Updated admission_fees: 0
          Updated security_fees: 0
          Updated dayboarding_fees: 0.0
          Updated miscellaneous_fees: 0
          Updated bus_fees: 0
          Updated concession_applied: 0
          Updated late_fee: 420.0
          Updated total_fee: 9885.0
          Set concession_amount: None
          Set concession_percent: None
          Set concession_id: None
          Set concession_type: None */
  
  
          // Calculate total amount
          const annualfees = parseInt(document.querySelector('input[name="annual_fees_paid"]').value) || 0;
          console.log("annualfees", annualfees);
          const tutionfees = parseInt(document.querySelector('input[name="tuition_fees_paid"]').value) || 0;
          console.log("tutionfees", tutionfees);
          const fundfees = parseInt(document.querySelector('input[name="funds_fees_paid"]').value) || 0;
          console.log("fundfees", fundfees);
          const sportsfees = parseInt(document.querySelector('input[name="sports_fees_paid"]').value) || 0;
          console.log("sportsfees", sportsfees);
          const admfees = parseInt(document.querySelector('input[name="admission_fees_paid"]').value) || 0;
          console.log("admfees", admfees);
          const dayboardfees = parseInt(document.querySelector('input[name="dayboarding_fees_paid"]').value) || 0;
          console.log("dayboardfees", dayboardfees);
          const busfees = parseInt(document.querySelector('input[name="bus_fees_paid"]').value) || 0;
          console.log("busfees", busfees);
          const activityfees = parseInt(document.querySelector('input[name="activity_fees"]').value) || 0;
          console.log("activityfees", activityfees);
          //const concession = parseInt(document.querySelector("concession_applied").value) || 0;
          console.log("concession", concession);
          const miscfees = parseInt(document.querySelector('input[name="miscellaneous_fees_paid"]').value) || 0;
          console.log("miscfees", miscfees);
          const latefees = parseInt(document.querySelector('input[name="late_fees_paid"]').value) || 0;
          console.log("latefees", latefees);
  
          // Calculate total based on data[16] or manually
          const total = d[12] || (
            annualfees + tutionfees + fundfees + sportsfees +
            activityfees + admfees + dayboardfees +
            busfees + latefees - concession
          );
  
          console.log("total=====", total);
  
  
          document.querySelector('input[name="total_amount"]').value = total;
          document.querySelector('input[name="amount_paid"]').value = total;
  
        } else {
          alert("Fees are not inserted for this class");
        }
      } catch (error) {
        console.error("There was a problem calculating fees:", error);
      }
    }
  
  
    /* async function calculateFees(studentId, studentClass, month, year) {
      try {
        const selectedMonths = feesForMonthsField.value; // Get current value of fees_for_months
        const url = new URL(`/admin/app/student_fee/ajax/calculate-fees/`, window.location.origin);
        url.searchParams.append("sid", studentId);
        url.searchParams.append("cls", studentClass);
        url.searchParams.append("mf", selectedMonths);
        url.searchParams.append("yr", year);
  
        const response = await fetch(url);
    
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.text();
    
        // Process the received data
        if (data !== '-----------') {
          const d = data.split('|');
    
          if (d[1] === "") {
            alert("Fees is not inserted");
          }
    
          // Populate fee fields with values or set default to '0'
          $("#annualfees").val(d[0] || '0');
          $("#tutionfees").val(d[1] > 0 ? d[1] : '0');
          $("#fundfees").val(d[2] > 0 ? d[2] : '0');
          $("#sportsfees").val(d[3] > 0 ? d[3] : '0');
          $("#admfees").val(d[4] || '0');
          $("#dayboardfees").val(d[6] > 0 ? parseInt(d[6]) : '0');
          $("#busfees").val(d[7] > 0 ? parseInt(d[7]) : '0');
          $("#activityfees").val(parseInt(d[10]) || '0');
          $("#concession").val(d[13] || '0');
          $("#miscfees").val(d[14] || '0');
          $("#latefees").val(d[15] || '0');
    
          // Calculate total amount
          const annualfees = parseInt($("#annualfees").val()) || 0;
          const tutionfees = parseInt($("#tutionfees").val()) || 0;
          const fundfees = parseInt($("#fundfees").val()) || 0;
          const sportsfees = parseInt($("#sportsfees").val()) || 0;
          const admfees = parseInt($("#admfees").val()) || 0;
          const dayboardfees = parseInt($("#dayboardfees").val()) || 0;
          const busfees = parseInt($("#busfees").val()) || 0;
          const activityfees = parseInt($("#activityfees").val()) || 0;
          const concession = parseInt($("#concession").val()) || 0;
          const miscfees = parseInt($("#miscfees").val()) || 0;
          const latefees = parseInt($("#latefees").val()) || 0;
    
          // Using the total from data, if available, otherwise calculate manually
          const total = d[16] || (
            annualfees + tutionfees + fundfees + sportsfees +
            activityfees + admfees + dayboardfees +
            busfees + latefees - concession
          );
    
          $("#totamt").val(total);
          $("#amtpaid").val(total);
          
        } else {
          alert("Fees is not inserted for this class");
        }
      } catch (error) {
        console.error("There was a problem calculating fees:", error);
      }
    } */
  
  
    /* async function calculateFees(studentId, studentClass, month, year) {
      try {
        const selectedMonths = feesForMonthsField.value; // Get current value of fees_for_months
        const url = new URL(`/admin/app/student_fee/ajax/calculate-fees/`, window.location.origin);
        url.searchParams.append("sid", studentId);
        url.searchParams.append("cls", studentClass);
        url.searchParams.append("mf", selectedMonths);
        url.searchParams.append("yr", year);
  
        const response = await fetch(url);
  
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
  
        if (data.success) {
          console.log("Total Fees:", data.total_fees);
          // Update the UI with the total fees if needed
          // document.querySelector('#totalFees').textContent = `Total Fees: ${data.total_fees}`;
        } else {
          console.error("Error calculating fees:", data.error);
        }
      } catch (error) {
        console.error("There was a problem calculating fees:", error);
      }
    } */
  
    // Function to load the action_payfees
    async function loadPayFees(studentId, month) {
      try {
        const feesForMonths = feesForMonthsField.value || month; // Use the selected month
        const url = new URL(
          `/admin/app/student_fee/ajax/pay-fees/`,
          window.location.origin
        );
        url.searchParams.append("fm", feesForMonths); // Pass fees for months (fm)
        url.searchParams.append("sid", studentId); // Pass student ID (sid)
  
        const response = await fetch(url);
  
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
  
        if (data.success) {
          //console.log("Pay fees result:", data.detail);
          // You can update the UI with the data returned from action_payfees if needed
          // document.querySelector('#feesResult').textContent = `Fees Detail: ${data.detail}`;
        } else {
          console.error("Error paying fees:", data.error);
        }
      } catch (error) {
        console.error("There was a problem loading pay fees:", error);
      }
    }
  
    // Function to load previous fees
    async function loadPreviousFees(studentId) {
      /*  createTable(); */ // Create the table structure
  
      try {
        const response = await fetch(`/admin/app/student_fee/ajax/prev-fees/?student_id=${studentId}`);
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();
        const fees = data.data.split("&");
  
        console.log("fees======", fees);
  
        // Populate the table
        const feesTable = document.querySelector("#feesTable tbody");
        if (!feesTable) {
          console.error("Table body not found");
          return;
        }
  
        feesTable.innerHTML = ""; // Clear existing rows
  
        fees.forEach((fee) => {
          const [feesForMonths, datePayment, amountPaid, feesPeriodMonth, studentClass] = fee.split("$");
  
          // Create a new row
          const row = feesTable.insertRow();
  
          // Insert cells into the row
          row.insertCell(0).textContent = feesForMonths;
          row.insertCell(1).textContent = datePayment;
          row.insertCell(2).textContent = amountPaid;
          row.insertCell(3).textContent = feesPeriodMonth;
          row.insertCell(4).textContent = studentClass;
  
          console.log("row==", row);
        });
      } catch (error) {
        console.error("There was a problem loading previous fees:", error);
      }
    }
  
    // Attach event listener to search button
    if (searchButton) {
      searchButton.addEventListener("click", loadStudents);
    }
  
    // Define the mapping for the period months based on the selected group of months
    const monthsMapping = {
      '4,5,6': ['4', '5', '6'],
      '7,8,9': ['7', '8', '9'],
      '10,11,12': ['10', '11', '12'],
      '1,2,3': ['1', '2', '3']
    };
  
    // Handle change event on fees_for_months
    feesForMonthsField.addEventListener('change', function () {
      // Get all selected options as an array
      const selectedValues = Array.from(feesForMonthsField.selectedOptions).map(option => option.value);
  
      // Clear current options in fees_period_month
      feesPeriodMonthField.innerHTML = '';
  
      // Collect months from the selected groups
      let monthsList = [];
      selectedValues.forEach(function (selectedRange) {
        if (selectedRange in monthsMapping) {
          monthsList = monthsList.concat(monthsMapping[selectedRange]);
        }
      });
  
      // Remove duplicates and sort the monthsList
      monthsList = [...new Set(monthsList)].sort((a, b) => a - b);
  
      // Add each month as an option in feesPeriodMonthField
      monthsList.forEach(function (month) {
        const option = document.createElement('option');
        option.value = month;
        option.text = month;
        feesPeriodMonthField.appendChild(option);
      });
    });
  
    
     // Set the current date into date_payment
      const datePaymentField = document.querySelector('input[name="date_payment"]');
      const today = new Date().toISOString().split('T')[0];  // Get the current date in YYYY-MM-DD format
      datePaymentField.value = today;
  
      // Get relevant fields for cheque
      const paymentModeField = document.querySelector('select[name="payment_mode"]');
      const chequeNoField = document.querySelector('input[name="cheque_no"]');
      const bankNameField = document.querySelector('select[name="bank_name"]');
      const branchNameField = document.querySelector('input[name="branch_name"]');
      const chequeStatusField = document.querySelector('select[name="cheque_status"]');
  
      // Function to toggle cheque-related fields based on payment mode
      function toggleChequeFields() {
          const paymentMode = paymentModeField.value;
          
          // Enable/Disable cheque fields based on the payment mode
          const isCheque = paymentMode === 'Cheque';
          chequeNoField.disabled = !isCheque;
          bankNameField.disabled = !isCheque;
          branchNameField.disabled = !isCheque;
          chequeStatusField.disabled = !isCheque;
  
          if (!isCheque) {
              // Clear the values if payment mode is not Cheque
              chequeNoField.value = '';
              bankNameField.value = '';
              branchNameField.value = '';
              chequeStatusField.value = '';
          }
      }
  
      // Call the function initially in case the form has pre-selected values
      toggleChequeFields();
  
      // Add event listener to payment mode field to toggle cheque fields when it changes
      paymentModeField.addEventListener('change', toggleChequeFields);
  
  });
  
  