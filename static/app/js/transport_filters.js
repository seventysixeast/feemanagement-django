document.addEventListener('DOMContentLoaded', function() {
    const routeSelect = document.querySelector('#bus_route');
    const destinationSelect = document.querySelector('#destination');

    if (routeSelect && destinationSelect) {
        routeSelect.addEventListener('change', function() {
            const route = this.value;

            if (route) {
                fetch(`/admin/ajax/load-destinations/?route=${route}`)
                    .then(response => response.json())
                    .then(data => {
                        // Clear existing options
                        destinationSelect.innerHTML = '<option value="">All Destinations</option>';

                        // Populate new options
                        data.forEach(function(dest) {
                            const option = document.createElement('option');
                            option.value = dest.destination;
                            option.textContent = dest.destination;
                            destinationSelect.appendChild(option);
                        });
                    });
            } else {
                // Reset to all destinations when no route is selected
                destinationSelect.innerHTML = '<option value="">All Destinations</option>';
            }
        });
    }
});
