document.addEventListener('DOMContentLoaded', function () {
    const routeField = document.getElementById('id_route');
    const destinationField = document.getElementById('id_destination');
    print("+++++++++++++++++++++++++++++++++++++++++++++++ ");

    routeField.addEventListener('change', function () {
        const route = this.value;
        const url = '/admin/app/student_master/ajax/load-destinations/?route=' + route;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                destinationField.innerHTML = '<option value="">Select Destination</option>';
                data.forEach(destination => {
                    const option = document.createElement('option');
                    option.value = destination['destination'];
                    option.textContent = destination['destination'];
                    destinationField.appendChild(option);
                });
            });
    });
});
