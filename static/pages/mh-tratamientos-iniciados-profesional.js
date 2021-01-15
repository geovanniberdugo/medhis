import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
// eslint-disable-next-line object-curly-newline
import { formatDateToISO, formatISODate, ISODateToJSDate, urlQueryToDict, updateFiltersOnUrl, DATETIME_FORMAT } from '../utils';

import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '../components/instituciones-combo';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '../components/medicos-combo';
import '../elements';

/**
 * `mh-tratamientos-iniciados-profesional` Reporte con los tratamientos de un profesional que iniciaron en el
 * rango de fechas escogido.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisTratamientosIniciadosProfesional extends ApolloQuery {
    static get properties() {
        return {
            /** Id del medico */
            medico: { type: String },

            /** Id de la institucion */
            institucion: { type: String },

            /** Fecha inicio reporte */
            desde: { type: String },

            /** Fecha fin reporte */
            hasta: { type: String },

            /** Tratamientos */
            tratamientos: { type: Array },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            p {
                margin: 0;
            }

            ul {
                padding: 0px;
            }

            ul li {
                list-style: none;
                margin-bottom: 10px;
            }

            ul .card-content {
                display: grid;
                grid-gap: 5px;
                grid-template-columns: repeat(auto-fit, minmax(15em, 1fr));
            }

            paper-card {
                width: 100%;
            }

            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--app-primary-color);
            } 

            #filtros .card-content {
                display: grid;
                grid-gap: 5px;
                grid-template-columns: repeat(auto-fill, minmax(15em, 1fr));
            }

            .label {
                color: grey;
            }

            @media print {
                ul li {
                    margin-bottom: 0px;
                }

                paper-card {
                    box-shadow: none;
                }
            }
        `;
    }

    render() {
        // eslint-disable-next-line object-curly-newline
        const { loading, tratamientos, medico, desde, hasta, institucion } = this;

        return html`
            <paper-card id="filtros">
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
                    <instituciones-combo value="${institucion}" @change="${(e) => { this.institucion = e.target.value; }}"></instituciones-combo>
                </div>
                <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
            </paper-card>
            <ul>
                ${tratamientos.map(tratamiento => html`
                    <li>
                        <paper-card class="data">
                            <div class="card-content">
                                <p>
                                    ${tratamiento.paciente.tipoDocumento} ${tratamiento.paciente.numeroDocumento}<br>
                                    ${tratamiento.paciente.nombreCompleto}
                                </p>
                                <p>${tratamiento.entidad.nombre}<br>${tratamiento.servicio.nombre}</p>
                                <p>
                                    <span class="label">Inicio:</span>${formatISODate(tratamiento.fechaInicioTratamiento, DATETIME_FORMAT)}<br>
                                    <span class="label">Fin:</span>${formatISODate(tratamiento.fechaFinTratamiento, DATETIME_FORMAT)}
                                </p>
                                <p>
                                    <span class="label"># citas:</span>${tratamiento.cantidad} <br>
                                    <a href="${tratamiento.ordenUrl}">Ver orden</a>
                                </p>
                            </div>
                        </paper-card>
                    </li>
                `)}
            </ul>
        `;
    }

    constructor() {
        super();
        this.medico = '';
        this.institucion = '';
        this.tratamientos = [];
        this.query = gql`
            query TratamientosInicidosProfesional($medico: ID!, $entre: String!, $institucion: ID) {
                tratamientos: serviciosPrestados(medico: $medico, iniciaronEntre: $entre, institucion: $institucion) {
                    results {
                        id
                        cantidad
                        ordenUrl
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

    updated(changedProperties) {
        if (changedProperties.has('medico') || changedProperties.has('desde') || changedProperties.has('hasta') || changedProperties.has('institucion')) this._fetchData();
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        const { medico, desde, hasta, institucion } = urlQueryToDict();
        this.medico = `${medico || this.medico}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
        this.institucion = `${institucion || this.institucion}`;
    }

    /**
     * Actualiza la url.
     * @param {string} medico
     * @param {string} desde
     * @param {string} hasta
     * @param {string} institucion
     */
    _setQueryParams(medico, desde, hasta, institucion) {
        const filtros = Object.assign(
            {},
            medico ? { medico } : {},
            institucion ? { institucion } : {},
            desde ? { desde: formatDateToISO(desde) } : {},
            hasta ? { hasta: formatDateToISO(hasta) } : {},
        );
        updateFiltersOnUrl(filtros, true);
    }

    /** Fetch los datos para el calendario */
    _fetchData() {
        // eslint-disable-next-line object-curly-newline
        const { medico, desde, hasta, institucion } = this;
        this._setQueryParams(medico, desde, hasta, institucion);
        const noFetch = !medico || !desde || !hasta;
        if (noFetch) {
            this.tratamientos = [];
            return;
        }

        const _vInstitucion = institucion ? { institucion } : {};
        this.variables = {
            medico,
            ..._vInstitucion,
            entre: `${formatDateToISO(desde)},${formatDateToISO(hasta)}`,
        };
        this.subscribe();
    }

    /** Sets los datos del reporte */
    _setData() {
        const { tratamientos: { results: tratamientos } } = this.data;
        this.tratamientos = tratamientos;
    }
}

customElements.define('mh-tratamientos-iniciados-profesional', MedhisTratamientosIniciadosProfesional);
