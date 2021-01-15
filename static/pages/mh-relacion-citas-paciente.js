import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import { DateTime } from 'luxon';
import gql from 'graphql-tag';
// eslint-disable-next-line object-curly-newline
import { formatDateToISO, formatISODate, dateToUnixTimeStamp, unixTimeStampToJsDate, formatMoney, updateFiltersOnUrl, urlQueryToDict, ISODateToJSDate } from '../utils';

import '@doubletrade/lit-datepicker/lit-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '../components/pacientes-combo';
import '../elements';

const groupCitaByDate = (obj, cita) => {
    const { inicio: fecha, estadoDisplay: estado, autorizacion, medico: { nombreCompleto } } = cita;
    const key = DateTime.fromISO(fecha).toISODate();
    // eslint-disable-next-line object-curly-newline
    const newCita = { fecha, estado, autorizacion, pago: 0, medico: nombreCompleto };
    if (!obj[key]) {
        // eslint-disable-next-line no-param-reassign
        obj[key] = [newCita];
    } else {
        // eslint-disable-next-line no-param-reassign
        obj[key] = [...obj[key], newCita];
    }
    return obj;
};

const fillPagoEnCitas = (obj, recibo) => {
    const { valor: pago, fecha } = recibo;
    const key = DateTime.fromISO(fecha).toISODate();
    if (!obj[key]) {
        // eslint-disable-next-line object-curly-newline
        obj[key] = [{ fecha, pago, estado: 'PAGO', autorizacion: '', medico: '' }];
    } else {
        const index = obj[key].findIndex(cita => !cita.pago);
        const citaIndex = index === -1 ? 0 : index;
        // eslint-disable-next-line no-param-reassign
        obj[key][citaIndex].pago = (obj[key][citaIndex].pago || 0) + pago;
    }

    return obj;
};

const buildDetalle = (citas = [], recibos = []) => {
    const citasGrouppedByDate = citas.reduce(groupCitaByDate, {});
    const citasConPagos = recibos.filter(recibo => !recibo.anuladoPor).reduce(fillPagoEnCitas, citasGrouppedByDate);
    return Object.values(citasConPagos).flat();
};

const formatReportData = (tratamiento) => {
    const { citas, recibos, ...data } = tratamiento;
    return { ...data, detalles: buildDetalle(citas, recibos) };
}

/**
 * `mh-relacion-citas-paciente` Reporte de citas por paciente en un rango de fechas.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisRelacionCitasPaciente extends ApolloQuery {
    static get properties() {
        return {
            desde: { type: String },
            hasta: { type: String },
            paciente: { type: Object },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            ul {
                padding: 0;
            }

            li {
                padding: 16px;
                list-style: none;
                margin-bottom: 10px;
                border-radius: 2px;
                background-color: white;
                box-shadow: var(--shadow-elevation-2dp_-_box-shadow);
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            paper-card {
                width: 100%;
            }

            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--app-primary-color);
            }

            #filters .card-content {
                display: grid;
                grid-gap: 5px;
                grid-template-columns: repeat(auto-fill, minmax(15em, 1fr));
            }

            .citas td {
                padding: 5px 0px;
            }

            .citas tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        `;
    }

    render() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, loading, tratamientos } = this;

        return html`
            <section id="filters">
                <paper-card>
                    <div class="card-content">
                        <pacientes-combo required @change="${(e) => { this.paciente = e.target.selectedItem; }}"></pacientes-combo>
                        <lit-datepicker-input .dateFrom="${dateToUnixTimeStamp(desde)}" .dateTo="${dateToUnixTimeStamp(hasta)}"
                            @date-from-changed="${e => this.desde = unixTimeStampToJsDate(e.detail.value)}"
                            @date-to-changed="${e => this.hasta = unixTimeStampToJsDate(e.detail.value)}">
                        </lit-datepicker-input>
                    </div>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                </paper-card>
            </section>
            <section id="report">
                <ul>
                    ${tratamientos.map(tratamiento => html`
                        <li>
                            <table>
                                <tr>
                                    <td># orden</td>
                                    <td>Servicio</td>
                                    <td>Cliente</td>
                                    <td>Coopago: ${formatMoney(tratamiento.coopago)}</td>
                                    <td># sesiones: ${tratamiento.cantidad}</td>
                                    <td>Valor pagado: ${formatMoney(tratamiento.totalPagado)}</td>
                                </tr>
                                <tr>
                                    <th><a href="${tratamiento.ordenUrl}">${tratamiento.orden.id}</a></th>
                                    <th>${tratamiento.servicio.nombre}</th>
                                    <th>${tratamiento.convenio.nombreCompleto}</th>
                                    <td></td>
                                    <td># atendidas: ${tratamiento.sesionesAtendidas}</td>
                                    <td>${tratamiento.saldoSesiones > 0 ? 'Saldo a favor' : 'Valor por pagar'}: ${formatMoney(tratamiento.saldoSesiones)}</td>
                                </tr>
                            </table>
                            <hr>
                            <table class="citas">
                                ${tratamiento.detalles.map(detalle => html`
                                    <tr>
                                        <td>${formatISODate(detalle.fecha, { ...DateTime.DATETIME_SHORT, hour12: true })}</td>
                                        <td>${detalle.medico}</td>
                                        <td>${detalle.estado}</td>
                                        <td>${formatMoney(detalle.pago)}</td>
                                        <td>Aut# ${detalle.autorizacion}</td>
                                    </tr>
                                `)}
                            </table>
                        </li>
                    `)}
                </ul>
            </section>
        `;
    }

    constructor() {
        super();
        this.desde = '';
        this.hasta = '';
        this.paciente = {};
        this.tratamientos = [];
        this.query = gql`
            query TratamientosPaciente($paciente: ID!, $entre: String!) {
                tratamientos(paciente: $paciente, citasEntre: $entre) {
                    results {
                        id
                        coopago
                        cantidad
                        ordenUrl
                        totalPagado
                        orden { id }
                        saldoSesiones
                        sesionesAtendidas
                        servicio { id, nombre @title_case }
                        convenio { id, nombreCompleto @title_case }
                        recibos: recibosCaja { id, fecha, valor, anuladoPor { id } }
                        citas {
                            id
                            inicio
                            autorizacion
                            estadoDisplay
                            medico { id, nombreCompleto @title_case }
                        }
                    }
                }
            }
        `;
        this._setFiltersFromUrl();
    }

    get data() {
        return this._data;
    }

    set data(value) {
        this._data = value;
        this._setData(value);
    }

    // Lifecycles

    shouldUpdate() {
        return true;
    }

    updated(changedProps) {
        const shouldFetch = changedProps.has('desde') || changedProps.has('hasta') || changedProps.has('paciente');
        if (shouldFetch) this._fetchData();
    }

    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta } = urlQueryToDict();
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
    }

    _setQueryParams(desde, hasta, paciente) {
        const filtros = {
            ...(paciente && { paciente }),
            ...(desde && { desde: formatDateToISO(desde) }),
            ...(hasta && { hasta: formatDateToISO(hasta) }),
        };
        console.log(filtros);
        updateFiltersOnUrl(filtros, true);
    }

    _fetchData() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, paciente: { id } } = this;
        console.log('fecth');
        console.log(desde, hasta);
        this._setQueryParams(desde, hasta, id);
        if (!desde || !hasta || !id) {
            this.tratamientos = [];
            return;
        }

        this.variables = {
            ...(id && { paciente: id }),
            entre: `${formatDateToISO(desde)},${formatDateToISO(hasta)}`,
        };
        this.subscribe();
    }

    _setData() {
        const { tratamientos: { results: tratamientos } } = this.data;
        this.tratamientos = tratamientos.map(formatReportData);
    }
}

customElements.define('mh-relacion-citas-paciente', MedhisRelacionCitasPaciente);
