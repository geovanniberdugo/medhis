import { DateTime } from 'luxon';
import { 
    ISODateToJSDate,
    formatDateToISO,
    unixTimeStampToJsDate,
    jsDateToUnixTimeStamp,
    formatISODate,
    formatJSDate as formatJSDATE,
    TIME_FORMAT,
    DATETIME_FORMAT,
    DATE_READABLE_FORMAT,
} from './date';

const NON_FIELD_ERROR = 'non_field_errors';

const ESTADOS = {
    NC: { label: 'No confirmada', color: 'red' },
    CO: { label: 'Confirmada', color: 'yellow' },
    CU: { label: 'Cumplida', color: 'green' },
    TE: { label: 'Atendida', color: 'lightgreen' },
    NT: { label: 'No atendida', color: 'pink' },
    CA: { label: 'Cancelada', color: 'blue' },
    EX: { label: 'Excusada', color: 'gray' },
    NA: { label: 'No asistio', color: 'purple' },
};

const ESTADOS_ARRAY = Object.entries(ESTADOS).map(estado => ({ value: estado[0], ...estado[1] }));

/**
 * Formatea COP 10,000.00
 * @param {String|Number} value Valor a formatear.
 */
const formatMoney = value => (
    value
        ? Number(value).toLocaleString('es', { style: 'currency', currency: 'COP' })
        : value
);

const dateToUnixTimeStamp = date => jsDateToUnixTimeStamp(date);

/**
 * Formatea date as time. HH:MM AM/PM
 * @param {string} date JS date to format.
 */
const formatISOTime = date => formatISODate(date, TIME_FORMAT, 'en');

/**
 * Formatea la fecha. Default: DD/MM/YYYY.
 * @param {string} date JS date to format.
 * @param {object} format
 */
const formatJSDate = (date, format = DATE_READABLE_FORMAT) => formatJSDATE(date, format);

/**
 * Formatea la fecha y hora YYYY-MM-DD.
 * @param {Object} date JS format date.
 */
const formatDateTimeToISO = date => (
    date
        ? DateTime.fromJSDate(date)
            .toISO()
        : date
);

/**
 * Notifica toast para mostrar un success.
 * @param {Object} elem Elemento que envia la notificación.
 * @param {sting} msg Mensaje de exito.
 * @event 'notify-toast-success'
 */
const notifySuccessMessage = (elem, msg) => {
    elem.dispatchEvent(new CustomEvent('notify-toast-success', {
        bubbles: true,
        composed: true,
        detail: { text: msg },
    }));
};

/**
 * Notifica toast para mostrar un error.
 * @param {Object} elem Elemento que envia la notificación.
 * @param {sting} msg Mensaje de error.
 * @event 'notify-toast-error'
 */
const notifyErrorMessage = (elem, msg) => {
    elem.dispatchEvent(new CustomEvent('notify-toast-error', {
        bubbles: true,
        composed: true,
        detail: { text: msg },
    }));
};

/**
 * Convierte URL query en un dict. si hay un valor repetido en el query se guarda separado por comas.
 * @param {string} query query string (Por defecto se usa location.search).
 */
const urlQueryToDict = (query) => {
    const params = new URLSearchParams(query || window.location.search);
    return [...params.entries()].reduce((obj, param) => {
        const [key, value] = param;
        if (!obj[key]) {
            // eslint-disable-next-line no-param-reassign
            obj[key] = value;
        } else {
            // eslint-disable-next-line no-param-reassign
            obj[key] = `obj[key],${value}`;
        }

        return obj;
    }, {});
};

const createUrlQueryStringFromObject = (obj) => {
    const params = new URLSearchParams();

    // eslint-disable-next-line no-restricted-syntax
    for (const [key, value] of Object.entries(obj)) {
        if (Array.isArray(value)) {
            value.forEach(val => params.append(key, val));
        } else {
            params.append(key, value);
        }
    }

    return params.toString();
}

/**
 * Actualiza la URL con query params con los filtros ingresados.
 * @param {object} filtros Filtros.
 * @param {boolean} replace si true reemplaza la historia.
 */
const updateFiltersOnUrl = (filtros, replace = false) => {
    const queryString = createUrlQueryStringFromObject(filtros);
    if (replace) {
        window.history.replaceState({}, '', `?${queryString}`);
    } else {
        window.history.pushState({}, '', `?${queryString}`);
    }
};

/**
 * Convierte una cadena de snake_case a camelCase.
 * @param {String} str cadena a convertir.
 */
const toCamel = str => (
    str.replace(/([-_][a-z])/ig, $1 => $1.toUpperCase().replace('-', '').replace('_', ''))
);

/**
 * Sets los errores en el formulario.
 * @param {HTMLELement} form Formulario.
 * @param {Array} errors Errores del formulario.
 */
const setErrorsOnForm = (form, errors) => {
    errors.forEach((error) => {
        const { field, messages } = error;
        const errorMessage = messages.join('.');
        if (field !== NON_FIELD_ERROR) {
            const key = toCamel(field);
            const input = form.querySelector(`*[name="${key}"]`);
            if (input) {
                input.errorMessage = errorMessage;
                input.invalid = true;
            }
        } else {
            notifyErrorMessage(form, errorMessage);
        }
    });
};

/**
 * Groups a list of items by function.
 * @param {Array} items List of items.
 * @param {Func} groupFunc Function to group by the items.
 */
const groupBy = (items, groupFunc) => {
    return items.reduce((obj, item) => {
        const key = groupFunc(item);

        if (!obj[key]) {
            obj[key] = [item];
        } else {
            obj[key].push(item);
        }

        return obj;
    }, {});
};

/**
 * Maps over an object to apply a function to each key.
 * @param {Object} obj Object to map.
 * @param {Function} func Function to apply to value of the object.
 */
const mapObject = (obj, func) => {
    let result = {};
    Object.entries(obj).forEach(([key, value]) => {
        result[key] = func(key, value);
    });

    return result;
};

/**
 * Totalize values from array of items.
 * @param {Array} items
 * @param {Function} func Function to get the value to totalize
 */
const totalizeBy = (items, func) => items.reduce((total, item) => total + func(item), 0);

/** */
const getAge = (fechaNacimiento) => {
    if (!fechaNacimiento) return '';

    const today = DateTime.local();
    const birthDate = DateTime.fromISO(fechaNacimiento);

    let age = today.year - birthDate.year;
    console.log(age);
    const dMonth = today.month - birthDate.month;

    if (age === 0 && dMonth === 0) {
        return `${today.day - birthDate.day} Dias`;
    }

    if (age === 0) {
        return `${dMonth} Meses`;
    }

    if (dMonth < 0 || (dMonth === 0 && today.day < birthDate.day)) {
        age--;
    }

    return `${age} Años`;
};

export {
    ESTADOS,
    TIME_FORMAT,
    ESTADOS_ARRAY,
    NON_FIELD_ERROR,
    DATETIME_FORMAT,
    DATE_READABLE_FORMAT,
    getAge,
    groupBy,
    mapObject,
    totalizeBy,
    formatMoney,
    formatJSDate,
    formatISOTime,
    formatISODate,
    urlQueryToDict,
    ISODateToJSDate,
    formatDateToISO,
    setErrorsOnForm,
    updateFiltersOnUrl,
    notifyErrorMessage,
    dateToUnixTimeStamp,
    formatDateTimeToISO,
    notifySuccessMessage,
    unixTimeStampToJsDate,
    createUrlQueryStringFromObject,
};
