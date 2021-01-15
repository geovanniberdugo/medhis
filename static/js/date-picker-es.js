function setDatePickerLocale(container) {
    const datePickerEsLocale = {
        // An array with the full names of months starting
        // with January.
        monthNames: [
            'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo',
            'Junio', 'Julio', 'Agosto', 'Septiembre',
            'Octubre', 'Noviembre', 'Diciembre'
        ],

        // An array of weekday names starting with Sunday. Used
        // in screen reader announcements.
        weekdays: [
            'Domingo', 'Lunes', 'Martes', 'Miercoles',
            'Jueves', 'Viernes', 'Sabado'
        ],

        // An array of short weekday names starting with Sunday.
        // Displayed in the calendar.
        weekdaysShort: [
            'Dom', 'Lun', 'Mar', 'Mie', 'Jue', 'Vie', 'Sab'
        ],

        // An integer indicating the first day of the week
        // (0 = Sunday, 1 = Monday, etc.).
        firstDayOfWeek: 1,

        // Used in screen reader announcements along with week
        // numbers, if they are displayed.
        week: 'Semana',

        // Translation of the Calendar icon button title.
        calendar: 'Calendario',

        // Translation of the Clear icon button title.
        clear: 'Limpiar',

        // Translation of the Today shortcut button text.
        today: 'Hoy',

        // Translation of the Cancel button text.
        cancel: 'Cancelar',

        // A function to format given `Object` as
        // date string. Object is in the format `{ day: ..., month: ..., year: ... }`
        formatDate: d => {
            // returns a string representation of the given
            // object in 'DD/MM/YYYY' -format
            const yearStr = String(d.year).replace(/\d+/, y => '0000'.substr(y.length) + y);
            return [d.day, d.month + 1, yearStr].join('/');
        },

        // A function to parse the given text to an `Object` in the format `{ day: ..., month: ..., year: ... }`.
        // Must properly parse (at least) text
        // formatted by `formatDate`.
        // Setting the property to null will disable
        // keyboard input feature.
        parseDate: text => {
            // Parses a string in 'DD/MM/YYYY', 'DD/MM' or 'DD' -format to
            // an `Object` in the format `{ day: ..., month: ..., year: ... }`.
            const parts = text.split('/');
            const today = new Date();
            let date, month = today.getMonth(), year = today.getFullYear();

            if (parts.length === 3) {
                year = parseInt(parts[2]);
                if (parts[2].length < 3 && year >= 0) {
                    year += year < 50 ? 2000 : 1900;
                }
                month = parseInt(parts[1]) - 1;
                date = parseInt(parts[0]);
            } else if (parts.length === 2) {
                month = parseInt(parts[1]) - 1;
                date = parseInt(parts[0]);
            } else if (parts.length === 1) {
                date = parseInt(parts[0]);
            }

            if (date !== undefined) {
                return { day: date, month, year };
            }
        },

        // A function to format given `monthName` and
        // `fullYear` integer as calendar title string.
        formatTitle: (monthName, fullYear) => {
            return monthName + ' ' + fullYear;
        }
    };

    [...container.querySelectorAll('vaadin-date-picker')].map((e) => {
        e.i18n = datePickerEsLocale;
        e.placeholder = 'DD/MM/YYYY';
    });
}