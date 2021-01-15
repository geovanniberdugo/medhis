import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
// eslint-disable-next-line object-curly-newline
import { formatDateToISO, urlQueryToDict, updateFiltersOnUrl, ISODateToJSDate, formatISODate, DATETIME_FORMAT } from '../utils';


import { cardCss, progressCss } from '../components/common-css';
import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '../components/instituciones-combo';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '../components/clientes-combo';
import '../elements';

/**
 * `mh-medicos-ordenan-tratamiento` Reporte de medicos que ordenan tratamiento.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisMedicosOrdenanTratamiento extends ApolloQuery {
    static get properties() {
        return {
            desde: { type: String },
            hasta: { type: String },
            clienteId: { type: String },
            institucionId: { type: String },
        };
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
        const { desde, hasta, clienteId, institucionId, loading, data } = this;
        const { tratamientos: { results: tratamientos = [] } } = data || { tratamientos: {}};

        return html`
            <section id="filters">
                <paper-card>
                    <div class="card-content">
                        <range-datepicker-input .dateFrom="${desde}" .dateTo="${hasta}"
                            @date-from-changed="${(e) => { this.desde = e.detail.value; }}"
                            @date-to-changed="${(e) => { this.hasta = e.detail.value; }}">
                            <template>
                                <div style="display: grid; grid-gap: 10px; grid-template-columns: 1fr 1fr;">
                                    <paper-input required label="Desde *" value="[[dateFrom]]"></paper-input>
                                    <paper-input required label="Hasta *" value="[[dateTo]]"></paper-input>
                                </div>
                            </template>
                        </range-datepicker-input>
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
                    ${tratamientos.map(tratamiento => html`
                        <li class="card">
                            <p><span class="label">Medico que ordena</span><br> ${tratamiento.orden.medicoOrdena || 'No indicado'}</p>
                            <p>${tratamiento.servicio.nombre} <br> ${tratamiento.convenio.cliente.nombre}</p>
                            <p>
                                ${tratamiento.paciente.nombreCompleto} <br>
                                ${tratamiento.paciente.tipoDocumento} ${tratamiento.paciente.numeroDocumento}
                            </p>
                            <p>
                                <span class="label">Medicos:</span><br>
                                ${tratamiento.medicos.map(medico => html`${medico.nombreCompleto}<br>`)}
                            </p>
                            <p>
                                <span class="label">Cantidad:</span> ${tratamiento.cantidad} <br>
                                <span class="label"># atendidas:</span> ${tratamiento.sesionesAtendidas}
                            </p>
                        </li>
                    `)}
                </ul>
            </section>
        `;
    }

    constructor() {
        super();
        this.clienteId = '';
        this.institucionId = '';
        this.notifyOnNetworkStatusChange = true;
        this._setFiltersFromUrl();

        this.query = gql`
            query MedicosOrdenanTratamiento($entre: String!, $institucion: ID!, $cliente: ID) {
                tratamientos(citasEntre: $entre, institucion: $institucion, cliente: $cliente) {
                    results {
                        id
                        cantidad
                        sesionesAtendidas
                        servicio { id, nombre @title_case }
                        orden { id, medicoOrdena @title_case }
                        medicos { id, nombreCompleto @title_case }
                        convenio { id, cliente { id, nombre @title_case}}
                        paciente { id, nombreCompleto @title_case tipoDocumento numeroDocumento }
                    }
                }
            }
        `;
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
            this.data = null;
            return;
        }

        this.variables = {
            ...(clienteId && { cliente: clienteId }),
            ...(institucionId && { institucion: institucionId }),
            entre: `${formatDateToISO(desde)},${formatDateToISO(hasta)}`,
        };
        this.subscribe();
    }
}

customElements.define('mh-medicos-ordenan-tratamiento', MedhisMedicosOrdenanTratamiento);
