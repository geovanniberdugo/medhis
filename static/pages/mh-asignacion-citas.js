import { jsDateToUnixTimeStamp, unixTimeStampToJsDate, ISODateToJSDate, formatDateToISO, formatISODate, DATETIME_FORMAT } from '../date';
import { urlQueryToDict, updateFiltersOnUrl } from '../utils';
import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import { cardCss, progressCss } from '../components/common-css';
import '@doubletrade/lit-datepicker/lit-datepicker-input';
import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '../components/instituciones-combo';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '../components/clientes-combo';
import '../elements';

/**
 * `mh-asignacion-citas` Reporte de asignacion de citas.
 *
 * @customElement
 * @demo
 * 
 */
class MedhisAsignacionCitas extends ApolloQuery {
    static get properties() {
        return {
            citas: { type: Array },
            desde: { type: String },
            hasta: { type: String },
            clienteId: { type: String },
            institucionId: { type: String },
        }
    }

    static get styles() {
        const base = css`
            :host {
                display: block;
            }

            ul {
                padding: 0;
            }

            p {
                margin: 0;
            }

            paper-card {
                width: 100%;
            }

            .label {
                color: #616161;
            }

            .card {
                display: grid;
                padding: 20px;
                grid-gap: 10px;
                list-style: none;
                align-items: center;
                margin-block-end: 10px;
                grid-template-columns: repeat(auto-fit, minmax(12em, 1fr));
            }

            #filters .card-content {
                display: grid;
                grid-gap: 5px;
                grid-template-columns: repeat(auto-fill, minmax(15em, 1fr));
            }
        `;

        return [cardCss, progressCss, base];
    }

    render() {
        const { desde, hasta, clienteId, institucionId, loading, citas } = this;

        return html`
            <section id="filters">
                <paper-card>
                    <div class="card-content">
                    <lit-datepicker-input .dateFrom="${jsDateToUnixTimeStamp(desde)}" .dateTo="${jsDateToUnixTimeStamp(hasta)}"
                            @date-from-changed="${e => this.desde = unixTimeStampToJsDate(e.detail.value)}"
                            @date-to-changed="${e => this.hasta = unixTimeStampToJsDate(e.detail.value)}">
                        </lit-datepicker-input>
                        <instituciones-combo required value="${institucionId}"
                            @change="${(e) => { this.institucionId = e.target.value; }}">
                        </instituciones-combo>
                        <clientes-combo value="${clienteId}"
                            @change="${(e) => { this.clienteId = e.target.value; }}">
                        </clientes-combo>
                    </div>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                </paper-card>
            </section>
            <section id="report">
                <ul>
                    ${citas.map(cita => html`
                        <li class="card">
                            <p>
                                ${cita.paciente.nombreCompleto} <br>
                                ${cita.paciente.tipoDocumento} ${cita.paciente.numeroDocumento}
                            </p>
                            <p>${cita.servicio.nombre} <br> <span class="label">Cliente:</span> ${cita.convenio.cliente.nombre}</p>
                            <p>
                                <span class="label">Fecha llamada:</span> <br>
                                ${formatISODate(cita.creadaEl, DATETIME_FORMAT)}
                            </p>
                            <p>
                                <span class="label">Fecha deseada:</span> <br>
                                ${cita.fechaDeseada}
                            </p>
                            <p>
                                <span class="label">Fecha cita:</span> <br>
                                ${formatISODate(cita.inicio, DATETIME_FORMAT)}
                            </p>
                        </li>    
                    `)}
                </ul>
            </section>
        `;
    }

    constructor() {
        super();
        this.citas = [];
        this.clienteId = '';
        this.institucionId = '';
        this.notifyOnNetworkStatusChange = true;
        this._setFiltersFromUrl();

        this.query = gql`
            query AsignacionCitas($entre: String!, $institucion: ID!, $cliente: ID) {
                citas(fechaEntre: $entre, institucion: $institucion, empresa: $cliente) {
                    results {
                        id
                        inicio
                        creadaEl
                        servicio { id, nombre @title_case }
                        fechaDeseada @date(format: "DD/MM/YYYY")
                        convenio { id, cliente { id, nombre @title_case }}
                        paciente { 
                            id
                            tipoDocumento
                            numeroDocumento
                            nombreCompleto @title_case
                        }
                    }
                }
            }
        `;
    }

    get data() {
        return this._data;
    }

    set data(value) {
        this._data = value;
        this._setData(value);
    }

    shouldUpdate() {
        return true;
    }

    updated(changedProps) {
        const shouldFetch = changedProps.has('desde') || changedProps.has('hasta') || changedProps.has('institucionId') || changedProps.has('clienteId');
        if (shouldFetch) this._fetchData();
    }

    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { hasta, desde, cliente, institucion } = urlQueryToDict();
        this.clienteId = `${cliente || this.clienteId}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
        this.institucionId = `${institucion || this.institucionId}`;
    }

    _setQueryParams(desde, hasta, cliente, institucion) {
        const filtros = {
            ...(cliente && { cliente }),
            ...(institucion && { institucion }),
            ...(desde && { desde: formatDateToISO(desde) }),
            ...(hasta && { hasta: formatDateToISO(hasta) }),
        };
        updateFiltersOnUrl(filtros, true);
    }

    _fetchData() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, clienteId, institucionId } = this;
        this._setQueryParams(desde, hasta, clienteId, institucionId);
        if (!desde || !hasta || !institucionId) {
            this.citas = [];
            return;
        }

        this.variables = {
            ...(clienteId && { cliente: clienteId }),
            ...(institucionId && { institucion: institucionId }),
            entre: `${formatDateToISO(desde)},${formatDateToISO(hasta)}`,
        };
        this.subscribe();
    }

    _setData(data) {
        const { citas: { results: citas } } = data;
        this.citas = citas;
    }
}

customElements.define('mh-asignacion-citas', MedhisAsignacionCitas);
