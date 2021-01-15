function setFormErrors(form, errors) {
    for (let key in errors) {
        let input = form.querySelector('*[name=' + key + ']');
        input.errorMessage = errors[key];
        input.invalid = true;
    }
}

// Original JavaScript code by Chirp Internet: www.chirp.com.au
// Please acknowledge use of this code by including this header.

function getCookie(name)
{
    let re = new RegExp(name + "=([^;]+)");
    let value = re.exec(document.cookie);
    return (value != null) ? unescape(value[1]) : null;
}

function getCsrfToken() {
    return getCookie('csrftoken');
}

/**
 * Dispara un evento para mostrar una notificación satisfactoria.
 */
function notifySuccessMessage(element, msg) {
    element.dispatchEvent(new CustomEvent('notify-toast-success', {
        bubbles: true,
        composed: true,
        detail: { text: msg },
    }));
}

/**
 * Dispara un evento para mostrar una notificación de error.
 */
function notifyErrorMessage(element, msg) {
    element.dispatchEvent(new CustomEvent('notify-toast-error', {
        bubbles: true,
        composed: true,
        detail: { text: msg },
    }));
}

/** Formato a valores de dinero */
function formatCurrency(value) {
    return value !== undefined ? Number(value).toLocaleString('es', { style: 'currency', currency: 'COP' }) : value;
}