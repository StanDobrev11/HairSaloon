document.addEventListener('DOMContentLoaded', function () {
    const serviceSelect = document.getElementById('id_service'); // Adjust the ID as necessary
    const startTimeInput = document.getElementById('id_start'); // Adjust the ID as necessary
    const endTimeDisplay = document.getElementById('end_time_display'); // You need to add this element in HTML

    const updateEndTime = () => {
        const serviceId = serviceSelect.value;
        const startTime = startTimeInput.value;

        if (serviceId && startTime) {
            fetch(`/api/get-service-duration/${serviceId}/`)
                .then(response => response.json())
                .then(data => {
                    const duration = data.duration; // Assuming duration is in minutes

                    if (startTime) {
                        // Assumes startTime is in 'HH:mm' format
                        const [hours, minutes] = startTime.split(':').map(Number);
                        const startTimeDate = new Date();
                        startTimeDate.setHours(hours, minutes, 0, 0); // Set hours and minutes without altering the date

                        const endTime = new Date(startTimeDate.getTime() + duration * 60000);
                        // Format end time to display it in HH:mm format
                        const formattedEndTime = endTime.getHours().toString().padStart(2, '0') + ':' + endTime.getMinutes().toString().padStart(2, '0');
                        endTimeDisplay.textContent = formattedEndTime;
                    }
                })
                .catch(error => console.error('Error fetching service duration:', error));
        }
    };

    // Listen for changes on both the service select and start time input
    serviceSelect.addEventListener('change', updateEndTime);
    startTimeInput.addEventListener('change', updateEndTime);
});
