document.addEventListener('DOMContentLoaded', function () {
    const hairdresserSelect = document.querySelector('#id_hairdresser');
    const serviceSelect = document.querySelector('#id_service');

    // Function to update services based on selected hairdresser
    const updateServices = (hairdresserId) => {

        const url = `/api/load-services/?hairdresser_id=${hairdresserId}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Clear existing options in the service dropdown
                serviceSelect.innerHTML = '';

                // Create a default "Please select" option
                const defaultOption = new Option("Please select a service", "");
                serviceSelect.add(defaultOption);

                // Populate dropdown with services returned by the API
                data.forEach(service => {
                    const option = new Option(service.name, service.id);
                    serviceSelect.add(option);
                });
            })
            .catch(error => console.error('Error loading services:', error));
    };

    // Add event listener for when the hairdresser selection changes
    hairdresserSelect.addEventListener('change', function () {
        updateServices(this.value);
    });
})
;

