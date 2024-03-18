$(document).ready(function () {
    $('#bookingDate').change(function () {
        const selectedDate = $(this).val();
        if (selectedDate) {
            generateTimeSlots();
        } else {
            $('#timeSlotsContainer').empty();
        }
    });

    function generateTimeSlots() {
        const container = $('#timeSlotsContainer');
        container.empty();
        const startTime = 10; // Start at 10:00
        const endTime = 18; // End at 18:00
        for (let hour = startTime; hour < endTime; hour++) {
            for (let minute = 0; minute < 60; minute += 30) {
                const timeString = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
                container.append(`<label><input type="radio" name="time" value="${timeString}"> ${timeString}</label><br>`);
            }
        }
    }
});