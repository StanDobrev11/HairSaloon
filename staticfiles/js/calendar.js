function changeDateFormat(date) {
    // Split the date string into month, day, and year
    var dateParts = date.split('/');
    var month = dateParts[0];
    var day = dateParts[1];
    var year = dateParts[2];
    // Forming a new date string in 'YYYY-MM-DD' format
    var newDate = `${year}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;
    return newDate;
}

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
                hour: 'numeric',
                minute: '2-digit',
                hour12: false
            },

            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'timeGridWeek,timeGridDay'
            },


            events: function (fetchInfo, successCallback, failureCallback) {
                fetch('/api/get-all-bookings')
                    .then(function (response) {
                        return response.json();
                    })
                    .then(function (bookings) {
                        const events = bookings.map(booking => {

                            let backgroundColor = 'red'; // Default color
                            let textColor = 'white';
                            let bookingTitle = booking.title;


                            if (userRole === 'superuser') {
                                backgroundColor = 'blue';
                            } else if (userRole === 'client' && booking.isOwner) {
                                backgroundColor = 'green';
                            } else if (userRole === 'staff' && booking.isHairDresser) {
                                backgroundColor = 'green';
                                if (booking.isCancelled) {
                                    bookingTitle = 'Cancelled'
                                    backgroundColor = 'yellow'
                                    textColor = 'black'
                                }
                            }
                            return {
                                title: bookingTitle,
                                start: booking.start,
                                end: booking.end,
                                backgroundColor: backgroundColor,
                                textColor: textColor,
                                // Add other event properties as needed
                            };
                        });

                        successCallback(events);
                    })
                    .catch(function (error) {
                        console.error("Error fetching bookings:", error);
                        failureCallback(error);
                    });
            },

            // this function regulates the size of the booking square
            eventDidMount: function (info) {
                // Calculate duration in minutes
                var duration = (info.event.end - info.event.start) / (1000 * 60);
                var height;

                if (duration <= 30) {
                    height = '30px'; // Example height, adjust as needed
                } else if (duration > 30 && duration <= 60) {
                    height = '60px'; // Example height for 30-60 min
                } else if (duration > 60 && duration <= 90) {
                    height = '90px'; // Example height for 60-90 min
                } else {
                    // Continue with your logic for other durations
                }

                // Adjust the height of the event element
                info.el.style.height = height;
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

            // the click should return date and time on the form

            dateClick: function (info) {
                // Format the clicked date/time as needed. Example: '2024-03-20T14:30:00'


                var clickedTime = FullCalendar.formatDate(info.date, {
                    hour: '2-digit',
                    minute: '2-digit',
                    hour12: false
                });
                var clickedDate = FullCalendar.formatDate(info.date, {
                    year: 'numeric',
                    month: '2-digit',
                    day: '2-digit',
                    hour12: false // Ensuring 24-hour format
                });
                var formattedClickedDate = changeDateFormat(clickedDate);
                console.log(formattedClickedDate)
                console.log(clickedTime)
                // Update the start time input field with the selected date/time
                document.getElementById('id_start').value = clickedTime;
                document.getElementById('id_date').value = formattedClickedDate;

                // Optionally, switch the view to a more detailed view, such as timeGridDay
                // calendar.changeView('timeGridDay', info.dateStr);
            }
            ,
            // select: function (info) {
            //     alert('selected ' + info.startStr + ' to ' + info.endStr);
            // }
        })
    ;


    calendar.render();
})
;