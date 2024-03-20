document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');
    var userElement = document.getElementById('user-role')
    var userRole = userElement.getAttribute('data-role');
    console.log(userRole);

    var calendar = new FullCalendar.Calendar(calendarEl, {
        selectable: true,
        initialView: 'timeGridWeek',
        firstDay: 1,
        hiddenDays: [1,],

        slotLabelInterval: '00:30',
        slotDuration: '00:30',
        slotMinTime: '10:00',
        slotMaxTime: '18:00',

        slotLabelFormat:
            {
                hour: 'numeric',
                minute: '2-digit',
                omitZeroMinute: false,
                meridiem: 'short',
                hour12: false,
            },

        eventTimeFormat: {
            hour: '2-digit',
            minute: '2-digit',
            hour12: false
        },

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },


        events: function (fetchInfo, successCallback, failureCallback) {
            fetch('/api/get-all-bookings')
                .then(function (response) {
                    return response.json();
                })
                .then(function (bookings) {
                    const events = bookings.map(booking => {
                        let event = {
                            start: booking.start,
                            end: booking.end,
                            title: 'test',
                        };

                        if (userRole === 'admin') {
                            event.title = booking.title; // Adjust according to your actual data structure
                            event.backgroundColor = 'green'; // Example color for admin's or specific user's own booking
                        } else if (userRole === 'staff') {
                            // Limited detail for staff
                            event.title = 'Occupied';
                            event.backgroundColor = 'red'; // Example color for occupied times
                        } else if (userRole === 'client') {
                            // Assuming a 'client' role wants to see limited details
                            event.title = 'Booking';
                            // event.backgroundColor = 'black'; // Example color for available times
                        }
                        return event;
                    });

                    successCallback(events);
                })
                .catch(function (error) {
                    console.error("Error fetching bookings:", error);
                    failureCallback(error);
                });
        },

        eventContent: function (arg) {
            // Define variables outside of the if/else scope
            var startTime = FullCalendar.formatDate(arg.event.start, {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false // Or true based on your preference
            });

            var endTime = FullCalendar.formatDate(arg.event.end, {
                hour: '2-digit',
                minute: '2-digit',
                hour12: false // Or true based on your preference
            });

            // Create a div to display the time
            var eventTimeDisplay = document.createElement('div');

            // Check the current view of the calendar to customize the display
            if (calendar.view.type === 'dayGridMonth') {
                eventTimeDisplay.innerText = `${arg.event.title}`;
            } else if (calendar.view.type === 'timeGridWeek') {
                eventTimeDisplay.innerText = `${startTime} - ${endTime} ${arg.event.title}`;
            }

            return {domNodes: [eventTimeDisplay]};
        },

        // functions
        // dateClick: function (info) {
        //     alert('clicked ' + info.dateStr);
        // },
        // select: function (info) {
        //     alert('selected ' + info.startStr + ' to ' + info.endStr);
        // }
    });


    calendar.render();
})
;