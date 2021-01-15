import { DateTime } from 'luxon';

window.Datetime = DateTime;

const TIME_FORMAT = { hour: '2-digit', minute: '2-digit', hour12: true };

const DATETIME_FORMAT = { ...DateTime.DATETIME_SHORT, ...TIME_FORMAT };

const DATE_READABLE_FORMAT = { ...DateTime.DATE_MED };

const formatISODate = (date, format, locale = 'es') => (
    date
        ? DateTime.fromISO(date)
            .setLocale(locale)
            .toLocaleString(format)
        : date
);

const formatJSDate = (date, format) => (
    date
        ? DateTime.fromJSDate(date)
            .setLocale('es')
            .toLocaleString(format)
        : date
);

const jsDateToISO = date => (
    date
        ? DateTime.fromJSDate(date)
            .toISODate()
        : date
);

const formatDateToISO = date => jsDateToISO(date);

const ISODateToJSDate = date => (
    date
        ? DateTime.fromISO(date).toJSDate()
        : date
);

const jsDateToUnixTimeStamp = date => (
    date
        ? DateTime.fromJSDate(date).toSeconds()
        : date
);

const unixTimeStampToJsDate = date => (
    date
        ? DateTime.fromSeconds(date).toJSDate()
        : date
);

export {
    TIME_FORMAT,
    DATETIME_FORMAT,
    DATE_READABLE_FORMAT,
    jsDateToISO,
    formatJSDate,
    formatISODate,
    formatDateToISO,
    ISODateToJSDate,
    jsDateToUnixTimeStamp,
    unixTimeStampToJsDate,
};