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


        events:
            [
                {
                    title: 'Meeting',
                    start: '2024-03-20T14:30:00',
                    extendedProps: {
                        status: 'done'
                    }
                },
                {
                    title: 'Birthday Party',
                    start: '2024-03-21T07:00:00',
                    backgroundColor: 'green',
                    borderColor: 'green'
                }
            ],

        // functions
        dateClick: function (info) {
            alert('clicked ' + info.dateStr);
        },
        select: function (info) {
            alert('selected ' + info.startStr + ' to ' + info.endStr);
        }
    });


    calendar.render();
});