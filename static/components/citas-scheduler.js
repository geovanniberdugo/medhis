import resourceTimeGridPlugin from '@fullcalendar/resource-timegrid';
import { Debouncer } from '@polymer/polymer/lib/utils/debounce';
import { timeOut } from '@polymer/polymer/lib/utils/async';
import { Calendar } from '@fullcalendar/core';
import { DateTime } from 'luxon';
import gql from 'graphql-tag';
import { ESTADOS_ARRAY, formatISODate, formatDateTimeToISO } from '../utils';

import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker-light';
import { ApolloQuery } from '@apollo-elements/lit-apollo';
import '@polymer/paper-icon-button/paper-icon-button';
import DetalleCita from '../components/detalle-cita';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-toast/paper-toast';
import { html, css } from 'lit-element';
import '../components/nueva-cita-form';
import './es-date-picker';

const MOVER_CITA_MUTATION = gql`
    mutation MoverCita($cita: CitaUpdateGenericType!) {
        moverCita(input: $cita) {
            ok
            errors { field, messages }
        }
    }
`;

/** Transform el intervalo a un duracion. */
const getDuration = (interval) => {
    const duration = {};
    const [hour, minute, second] = interval.split(':');

    if (parseInt(hour, 10) > 0) duration.hours = parseInt(hour, 10);
    if (parseInt(minute, 10) > 0) duration.minutes = parseInt(minute, 10);
    if (parseInt(second, 10) > 0) duration.seconds = parseInt(second, 10);

    return duration;
};

const availableSlots = (fecha, horas, medico, duracion) => {
    const _duracion = getDuration(duracion);
    return horas.map(hora => {
        const inicio = DateTime.fromFormat(`${fecha} ${hora}`, 'yyyy-LL-dd HH:mm:ss')
        const fin = inicio.plus(_duracion);
        return {
            disponible: true,
            end: fin.toISO(),
            color: '#6CA5C1',
            textColor: 'black',
            resourceId: medico,
            start: inicio.toISO(),
        }
    });
}

// Templates
const estadoItem = estado => html`<li><div style="background-color: ${estado.color};"></div> ${estado.label}</li>`;

/**
 * `citas-scheduler` Calendario de citas.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class CitasScheduler extends ApolloQuery {
    static get properties() {
        return {
            /** Fecha del calendario. */
            _fecha: { type: String },

            /** Tipo de agenda. */
            agenda: { type: String },

            /** Id de la sucursal. */
            sucursal: { type: String },

            /** Id del medico. */
            medico: { type: String },

            /** Cita a mover */
            citaMover: { type: String },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            ul {
                padding-left: 0;
            }

            li {
                list-style: none;
                margin-right: 10px;
                display: inline-block;
            }

            li div {
                width: 15px;
                height: 15px;
                border-radius: 50%;
                display: inline-block;
            }

            section {
                font-size: 20px;
                text-align: center;
            }

            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--app-primary-color);
            }

            paper-toast paper-button {
                color: red;
            }

            .fc-scroller {
                height: auto !important;
                overflow-y: hidden !important;
            }
        `;
    }

    render() {
        const { _fecha, loading, citaMover } = this;
        return html`
            <link rel="stylesheet" href="/static/node_modules/@fullcalendar/core/main.css">
            <link rel="stylesheet" href="/static/node_modules/@fullcalendar/timegrid/main.css">
            
            <section>
                <div>
                <paper-icon-button icon="my-icons:navigate-before" @click="${this._beforeDate}"></paper-icon-button>
                <es-date-picker>
                    <vaadin-date-picker-light value="${_fecha}" @change="${e => this.fecha = e.target.value}">
                        <paper-icon-button icon="my-icons:event"></paper-icon-button>
                        <iron-input><input type="hidden"></iron-input>
                    </vaadin-date-picker-light>
                </es-date-picker>
                <paper-icon-button icon="my-icons:navigate-next" @click="${this._nextDate}"></paper-icon-button>
                </div>
                <div>${formatISODate(_fecha, DateTime.DATE_HUGE)}</div>
            </section>
            <ul>${ESTADOS_ARRAY.map(estado => estadoItem(estado))}</ul>
            <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
            <div id="calendar"></div>
            <paper-toast text="Escoge el nuevo horario donde deseas mover la cita." duration="0" ?opened="${citaMover}">
                <paper-button @click="${this._cancelarMover}">cancelar</paper-button>
            </paper-toast>
        `;
    }

    constructor() {
        super();
        this.events = [];
        this.medicos = [];
        this.fecha = DateTime.local().toISODate();
        this.query = gql`
            query AgendaCitas($sucursal: ID!, $fecha: Date!, $agenda: ID, $medico: ID) {
                medicos: empleados(medicos: true, activo: true, sucursal: $sucursal, agenda: $agenda, id: $medico) {
                    results {
                        id
                        duracion
                        nombreCompleto @title_case
                        horasAtencion(sucursal: $sucursal, fecha: $fecha)
                    }
                }
                citas(sucursal: $sucursal, medico: $medico, agenda: $agenda, start: $fecha) {
                    results {
                        id
                        color
                        end: fin
                        resourceId
                        start: inicio
                        title @title_case
                    }
                }
            }
        `;

        this._boundMoverCitaListener = this._moverCita.bind(this);
    }

    get fecha() {
        return this._fecha;
    }

    set fecha(value) {
        this._fecha = value;
        if (this._calendar && value) {
            this._calendar.gotoDate(DateTime.fromISO(value).toJSDate());
        }
    }

    get data() {
        return this._data;
    }

    set data(value) {
        this._data = value;
        this._setCalendarData(value);
    }

    set slotDuration(value) {
        if (this._calendar && value) {
            this._calendar.setOption('slotDuration', value);
        }
    }

    // Lifecycles

    firstUpdated() {
        this._initializeCalendar();
    }

    connectedCallback() {
        super.connectedCallback();
        DetalleCita.instance.addEventListener('mover-cita', this._boundMoverCitaListener);
    }

    disconnectedCallback() {
        DetalleCita.instance.removeEventListener('mover-cita', this._boundMoverCitaListener);
        super.disconnectedCallback();    
    }

    shouldUpdate(changedProperties) {
        return super.shouldUpdate() || changedProperties.has('_fecha') || changedProperties.has('citaMover') || changedProperties.has('medico');
    }

    updated(changedProperties) {
        if (changedProperties.has('medico') || changedProperties.has('agenda') || changedProperties.has('sucursal') || changedProperties.has('_fecha')) this._debounceFetch();
    }

    /** Inicializa fullcalendar. */
    _initializeCalendar() {
        const calendarEl = this.shadowRoot.getElementById('calendar');
        this._calendar = new Calendar(calendarEl, {
            schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
            plugins: [resourceTimeGridPlugin],
            defaultView: 'resourceTimeGridDay',
            slotDuration: '00:10:00',
            slotEventOverlap: false,
            eventTextColor: 'black',
            minTime: '06:00:00',
            maxTime: '20:00:00',
            nowIndicator: true,
            allDaySlot: false,
            hiddenDays: [0],
            header: false,
            resourceText: resource => resource.extendedProps.nombreCompleto,
            resources: (fetchInfo, successCallback, failureCallback) => {
                successCallback(this.medicos);
            },
            events: (fetchInfo, successCallback, failureCallback) => {
                successCallback(this.events);
            },
            eventClick: ({event, el, jsEvent, view} = {}) => {
                const medico = event.getResources()[0];
                if(this.citaMover) {
                    if (event.extendedProps.disponible) this.mover(event.start, medico.id);
                    return;
                }

                if (event.extendedProps.disponible) {
                    this._showNuevaCitaForm(event.start, medico.id);
                } else {
                    this._showDetalleCita(event.id);
                }
            },
        });
        this._calendar.render();
    }

    /**
     * Muestra el formulario para agendar nueva cita.
     * @param {Date} date Fecha en la cual se va a crear la cita.
     * @param {String} medico Medico al cual se va a crear la cita.
     */
    _showNuevaCitaForm(date, medico) {
        this.dispatchEvent(new CustomEvent('show-nueva-cita-form', {
            bubbles: true,
            composed: true,
            detail: {
                medico,
                horario: date,
                sucursal: this.sucursal,
            }
        }));
    }

    /** Muestra el detalle de una cita */
    _showDetalleCita(id) {
        DetalleCita.instance.id = id;
        if (DetalleCita.instance.estadoForm) DetalleCita.instance.estadoForm.reset();
        DetalleCita.instance.opened = true;
    }

    /** Fecha siguiente. */
    _nextDate() {
        this.fecha = DateTime.fromISO(this.fecha).plus({ days: 1 }).toISODate();
    }

    /** Fecha anterior. */
    _beforeDate() {
        this.fecha = DateTime.fromISO(this.fecha).minus({ days: 1 }).toISODate();
    }

    /** Debounce fetch */
    _debounceFetch() {
        this._debouncer = Debouncer.debounce(
            this._debouncer,
            timeOut.after(500),
            () => this._fetchData(),
        );
    }

    /** Fetch los datos para el calendario */
    _fetchData() {
        const { medico, sucursal, agenda, fecha } = this;
        if (!sucursal || !fecha || !agenda || (agenda === 'm' && !medico)) return;

        const vars = agenda === 'm' ? { medico, agenda: null } : { agenda, medico: null };
        this.variables = { ...vars, sucursal, fecha };
        this.subscribe();
    }

    /** Sets data en calendario */
    _setCalendarData(data) {
        const { medicos: { results: medicos }, citas: { results: citas } } = data;
        this.medicos = [...medicos];
        this._calendar.refetchResources();

        const events = [];
        medicos.forEach(medico => {
            const { horasAtencion, duracion, id } = medico;
            if (horasAtencion.length > 0) events.push(...availableSlots(this.fecha, horasAtencion, id, duracion));
        });
        const _hadEvents = this.events.length === 0; 
        this.events = [...events, ...citas];

        if(!_hadEvents) {
            this._calendar.refetchEvents();
        } else {
            this._calendar.refetchEvents();
            this._calendar.render();
            this._calendar.refetchEvents();
        }
    }

    /** Permite mover la cita a otro horario. */
    _moverCita(e) {
        this.citaMover = e.detail.cita;
    }

    /** Cancela la opcion de mover la cita. */
    _cancelarMover() {
        this.citaMover = '';
    }

    /**
     * Mueve la cita.
     * @param {Date} date Fecha a la que se mueve la cita.
     * @param {String} medico Id del medico.
     */
    mover(date, medico) {
        const cita = {
            medico,
            id: this.citaMover,
            sucursal: this.sucursal,
            inicio: formatDateTimeToISO(date),
        };
        window.__APOLLO_CLIENT__.mutate({
            variables: { cita },
            mutation: MOVER_CITA_MUTATION,
            refetchQueries: ['AgendaCitas'],
        })
            .then((result) => {
                const data = result.data.moverCita;
                if (data.ok) {
                    this.citaMover = '';
                }
            })
            .catch(error => console.error(error));
    }
}

customElements.define('citas-scheduler', CitasScheduler);
