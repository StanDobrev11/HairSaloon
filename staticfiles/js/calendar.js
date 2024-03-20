document.addEventListener('DOMContentLoaded', function () {
    var calendarEl = document.getElementById('calendar');

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

        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },


        events: function (fetchInfo, successCallback, failureCallback) {
            fetch('/api/get-all-bookings/')
                .then(function (response) {
                    return response.json(); // This already converts the JSON string to a JavaScript object/array
                })
                .then(function (bookings) {
                    successCallback(bookings); // Directly use the bookings data, no need for JSON.parse
                })
                .catch(function (error) {
                    console.error("Error fetching bookings:", error);
                    failureCallback(error);
                });
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
});