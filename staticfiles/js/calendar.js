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

let selectedHairdresserId = null; // Global variable to store the selected hairdresser ID

document.addEventListener('DOMContentLoaded', function () {
    const hairdresserSelect = document.getElementById('id_hairdresser'); // The select element for hairdressers
    const calendarEl = document.getElementById('calendar');
    const userRoleElement = document.getElementById('user-role');
    const userRole = userRoleElement.getAttribute('data-role');

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
                        // Filter and process bookings based on user role
                        const events = bookings.reduce((acc, booking) => {
                            // Logic for superuser: Include all except cancelled bookings
                            if (userRole === 'superuser' && !booking.isCancelled) {
                                acc.push({
                                    title: booking.title,
                                    start: booking.start,
                                    end: booking.end,
                                    backgroundColor: 'blue',
                                    textColor: 'black',
                                });
                            }

                            // Logic for staff: Include all own bookings, including cancelled
                            if (userRole === 'staff' && booking.isHairDresser) {
                                let backgroundColor = 'green';
                                let textColor = 'white';
                                if (booking.isCancelled) {
                                    backgroundColor = 'orange';
                                    textColor = 'black';
                                }
                                acc.push({
                                    title: booking.title,
                                    start: booking.start,
                                    end: booking.end,
                                    backgroundColor: backgroundColor,
                                    textColor: textColor,
                                });
                            }

                            // Logic for clients: Display own booking regardless of the hairdresser and
                            // selected hairdresser's bookings if selected for a new booking
                            if (userRole === 'client') {
                                if (booking.isOwner) {
                                    acc.push({
                                        title: booking.title,
                                        start: booking.start,
                                        end: booking.end,
                                        backgroundColor: 'green',
                                        textColor: 'white',
                                    });
                                }

                                else if (hairdresserSelect.value === booking.hairdresserId) {
                                    acc.push({
                                        title: booking.title,
                                        start: booking.start,
                                        end: booking.end,
                                        backgroundColor: 'yellow',
                                        textColor: 'black',
                                    });
                                }
                            }

                            return acc;
                        }, []);

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

   if (hairdresserSelect) {
        hairdresserSelect.addEventListener('change', function () {
            selectedHairdresserId = this.value; // Update the global variable
            calendar.refetchEvents(); // Refetch the calendar events
        });
    }
})
;

