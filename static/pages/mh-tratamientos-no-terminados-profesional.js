import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
// eslint-disable-next-line object-curly-newline
import { formatDateToISO, formatISODate, DATETIME_FORMAT, urlQueryToDict, updateFiltersOnUrl, ISODateToJSDate } from '../utils';

import { progressCss, cardCss } from '../components/common-css';
import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-card/paper-card';
import '../components/sucursales-combo';
import '../components/medicos-combo';
import '../elements';

/**
 * `mh-tratamientos-no-terminados-profesional` Reporte de tratamientos no terminados por profesional.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisTratamientosNoTerminadosProfesional extends ApolloQuery {
    static get properties() {
        return {
            desde: { type: String },
            hasta: { type: String },
            medico: { type: String },
            sucursal: { type: String },
            reportData: { type: Array },
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

            li {
                list-style: none;
                margin-bottom: 10px;
            }

            h2 {
                color: grey;
                font-size: 1.2em;
                text-transform: uppercase;
            }

            paper-card {
                width: 100%;
            }

            .label {
                color: #636060;
            }

            #filter .card-content {
                display: grid;
                grid-gap: 5px;
                align-items: end;
                grid-template-columns: repeat(auto-fill, minmax(15em, 1fr));
            }

            #data .card {
                display: grid;
                grid-gap: 5px;
                align-items: center;
                grid-template-columns: repeat(auto-fit, minmax(12em, 1fr));
            }
        `;

        return [progressCss, cardCss, base];
    }

    render() {
        const { desde, hasta, medico, sucursal, reportData, loading } = this;

        return html`
            <section id="filter">
                <paper-card>
                    <div class="card-content">
                        <medicos-combo required value="${medico}" @change="${(e) => { this.medico = e.target.value; }}"></medicos-combo>
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
                        <sucursales-combo clear-button-visible value="${sucursal}" @change="${(e) => { this.sucursal = e.target.value; }}"></sucursales-combo>
                    </div>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                </paper-card>
            </section>
            <section id="data">
                ${reportData.map(group => html`
                    <h2>${group.nombre}</h2>
                    <ul>
                        ${group.tratamientos.map(tratamiento => html`
                            <li class="card">
                                <p>
                                    ${tratamiento.paciente.nombreCompleto} <br>
                                    ${tratamiento.paciente.tipoDocumento} ${tratamiento.paciente.numeroDocumento}
                                </p>
                                <p>
                                    ${tratamiento.entidad.nombre} <br>
                                    Orden <a href="${tratamiento.ordenUrl}">${tratamiento.orden.id}</a>
                                </p>
                                <p>
                                    <span class="label"># Citas:</span> ${tratamiento.cantidad} <br>
                                    <span class="label"># Atendidas:</span> ${tratamiento.sesionesAtendidas}
                                </p>
                                <p>
                                    <span class="label">Inicio:</span> ${formatISODate(tratamiento.fechaInicioTratamiento, DATETIME_FORMAT)} <br>
                                    <span class="label">Fin:</span> ${formatISODate(tratamiento.fechaFinTratamiento, DATETIME_FORMAT)}
                                </p>
                            </li>
                        `)}
                    </ul>
                `)}
            </section>
        `;
    }

    constructor() {
        super();
        this.medico = '';
        this.sucursal = '';
        this.reportData = [];
        this.query = gql`
            query TratamientosNoTerminadosProfesional($medico: ID!, $entre: String!, $sucursal: ID) {
                tratamientos: serviciosPrestados(terminados: false, medico: $medico, citasEntre: $entre, sucursal: $sucursal) {
                    results {
                        id
                        cantidad
                        ordenUrl
                        orden { id }
                        sesionesAtendidas
                        fechaFinTratamiento
                        fechaInicioTratamiento
                        entidad { id, nombre @title_case }
                        servicio { id, nombre @title_case }
                        paciente { id, tipoDocumento, numeroDocumento, nombreCompleto @title_case }
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
        const shouldFetch = changedProps.has('desde') || changedProps.has('hasta') || changedProps.has('medico') || changedProps.has('sucursal');
        if (shouldFetch) this._fetchData();
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, medico, sucursal } = urlQueryToDict();
        this.medico = `${medico || this.medico}`;
        this.sucursal = `${sucursal || this.sucursal}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
    }

    /**
     * Actualiza la url.
     * @param {string} desde
     * @param {string} hasta
     * @param {string} medico
     * @param {string} sucursal
     */
    _setQueryParams(desde, hasta, medico, sucursal) {
        const filtros = {
            ...(medico && { medico }),
            ...(sucursal && { sucursal }),
            ...(desde && { desde: formatDateToISO(desde) }),
            ...(hasta && { hasta: formatDateToISO(hasta) }),
        };
        updateFiltersOnUrl(filtros, true);
    }

    _fetchData() {
        // eslint-disable-next-line-object-curly-newline
        const { desde, hasta, medico, sucursal } = this;
        this._setQueryParams(desde, hasta, medico, sucursal);
        if (!desde || !hasta || !medico) {
            this.reportData = [];
            return;
        }

        this.variables = {
            ...(medico && { medico }),
            ...(sucursal && { sucursal }),
            entre: `${formatDateToISO(desde)},${formatDateToISO(hasta)}`,
        };
        this.subscribe();
    }

    _setData() {
        const { tratamientos: { results: tratamientos } } = this.data;
        this.reportData = Object.values(tratamientos.reduce(this._groupByServicioEntidad, {}));
    }

    _groupByServicioEntidad(obj, tratamiento) {
        const { servicio, entidad } = tratamiento;
        const key = `${servicio.id}-${entidad.id}`;
        if (!obj[key]) {
            // eslint-disable-next-line no-param-reassign
            obj[key] = {
                tratamientos: [tratamiento],
                nombre: `${servicio.nombre} - ${entidad.nombre}`,
            };
        } else {
            // eslint-disable-next-line no-param-reassign
            obj[key].tratamientos = [...obj[key].tratamientos, tratamiento];
        }

        return obj;
    };
}

customElements.define('mh-tratamientos-no-terminados-profesional', MedhisTratamientosNoTerminadosProfesional);