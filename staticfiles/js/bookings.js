document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

    // Initialize the calendar
    var calendar = new FullCalendar.Calendar(calendarEl, {
        plugins: ['dayGrid', 'timeGrid', 'interaction'],
        defaultView: 'dayGrid',
        firstDay: 1,
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        businessHours: {
            daysOfWeek: [1, 2, 3, 4, 5], // Monday - Friday
            startTime: '10:00',
            endTime: '18:00',
        },
        dateClick: function (info) {
            calendar.changeView('timeGridWeek', info.dateStr);
        },
        // hourClick: function (info) {
        //     calendar.changeView('hour')
        // },
        slotDuration: '00:30:00',
        slotLabelInterval: '00:30:00',
        slotLabelFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },
        scrollTime: '10:00:00',
        minTime: '10:00:00',
        maxTime: '18:00:00',
        selectable: true,
        events: function (fetchInfo, successCallback, failureCallback) {
            if (1 === 1) {
                fetch('/dashboard/api/bookings/')
                    .then(response => response.json())
                    .then(data => {
                        const events = data.map(booking => {
                            return {
                                title: booking.fields.service, // Adjust according to your data structure
                                start: booking.fields.date + 'T' + booking.fields.time,
                            };
                        });
                        successCallback(events);
                    })
                    .catch(error => failureCallback(error));
            } else {
                successCallback([]); // No events for other views
            }
        }
    });
    calendar.render();
});