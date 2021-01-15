import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
// eslint-disable-next-line object-curly-newline
import { formatDateToISO, formatMoney, urlQueryToDict, updateFiltersOnUrl, ISODateToJSDate } from '../utils';

import { progressCss, cardCss } from '../components/common-css';
import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '../components/instituciones-combo';
import '@polymer/paper-card/paper-card';
import '../components/medicos-combo';
import '../elements';

/**
 * `mh-tratamientos-pago-terapeutas` Relacion de tratamientos para pago de terapeutas.
 *
 * @customElement
 * @demo
 * 
 */
class MedhisTratamientosPagoTerapeutas extends ApolloQuery {
    static get properties() {
        return {
            desde: { type: String },
            hasta: { type: String },
            medico: { type: String },
            reportData: { type: Array },
            totalPagar: { type: Number },
            institucion: { type: String },
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

            h2 span {
                font-weight: normal;
            }

            p {
                margin: 0;
            }

            paper-card {
                width: 100%;
            }

            .label {
                color: #636060;
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

            #report {
                margin-block-end: 65px;
            }

            #total {
                left: 0;
                bottom: 0;
                width: 100%;
                padding: 0 20px;
                position: fixed;
                background-color: white;
            }

            #total h2 {
                color: green;
                font-weight: bolder;
                margin-block-end: 20px;
                margin-block-start: 20px;
            }
        `;

        return [progressCss, cardCss, base];
    }

    render() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, institucion, medico, loading, reportData, totalPagar } = this;

        return html`
            <section id="filters">
                <paper-card>
                    <div class="card-content">
                        <instituciones-combo required value="${institucion}"
                            @change="${(e) => { this.institucion = e.target.value; }}">
                        </instituciones-combo>
                        <medicos-combo required value="${medico}"
                            @change="${(e) => { this.medico = e.target.value; }}">
                        </medicos-combo>
                        <range-datepicker-input .dateFrom="${desde}" .dateTo="${hasta}"
                            @date-from-changed="${(e) => { this.desde = e.detail.value; }}"
                            @date-to-changed="${(e) => { this.hasta = e.detail.value; }}">
                            <template>
                                <div style="display: grid; grid-gap: 10px; grid-template-columns: 1fr 1fr;">
                                    <paper-input required label="Recibidos desde *" value="[[dateFrom]]"></paper-input>
                                    <paper-input required label="Recibidos hasta *" value="[[dateTo]]"></paper-input>
                                </div>
                            </template>
                        </range-datepicker-input>
                    </div>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                </paper-card>
            </section>
            <section id="report">
                ${reportData.map(cliente => html`
                    <h2>${cliente.nombre} - <span>Valor sesión: ${formatMoney(cliente.valor)}</span></h2>
                    <h3>
                        <span class="label">Total citas:</span> ${cliente.totalCitas} -
                        <span class="label">Valor a pagar por sesión:</span> ${formatMoney(cliente.valorPagarMedico)} -
                        <span class="label">Total a pagar:</span> ${formatMoney(cliente.totalPagar)}
                    </h3>
                    <ul>
                        ${cliente.tratamientos.map(tratamiento => html`
                            <li class="card">
                                <p>${tratamiento.servicio.nombre} <br> Orden <a href="${tratamiento.ordenUrl}">${tratamiento.orden.id}</a></p>
                                <p><span class="label">Terminado el:</span> <br> ${tratamiento.fechaFinTratamiento}</p>
                                <p><span class="label">Recibido el:</span> <br> ${tratamiento.recibidoAt}</p>
                                <p>${tratamiento.paciente.nombreCompleto}<br>${tratamiento.paciente.tipoDocumento} ${tratamiento.paciente.numeroDocumento}</p>
                                <p>
                                    <span class="label">cantidad:</span> ${tratamiento.cantidad} <br>
                                    <span class="label"># atendidas:</span> ${tratamiento.sesionesAtendidas}
                                </p>
                                <p>
                                    ${tratamiento.facturas.length > 0
                                        ? (
                                            html`
                                                <span class="label">Factura</span> <br>
                                                ${tratamiento.facturas.map(factura => html`<a href="${factura.detalleUrl}">${factura.numero}</a>`)}
                                            `
                                        )
                                        : ''
                                    }
                                </p>
                            </li>
                        `)}
                    </ul>
                `)}
            </section>
            <section id="total">
                <h2>Total a pagar: ${formatMoney(totalPagar)}</h2>
            </section>
        `;
    }

    constructor() {
        super();
        this.medico = '';
        this.reportData = [];
        this.institucion = '';
        this.query = gql`
            query TratamientosPagoProfesional($institucion: ID!, $medico: ID!, $entre: String!) {
                tratamientos(auditoriaFinal: true, medico: $medico, institucion: $institucion, recibidosEntre: $entre) {
                    results {
                        id
                        valor
                        ordenUrl
                        cantidad
                        orden { id }
                        valorPagarMedico(medico: $medico)
                        sesionesAtendidas(medico: $medico)
                        entidad { id, nombre @title_case }
                        servicio { id, nombre @title_case }
                        facturas { id, numero, detalleUrl }
                        recibidoAt @date(format: "DD/MM/YYYY")
                        fechaFinTratamiento @date(format: "DD/MM/YYYY")
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
        const shouldFetch = changedProps.has('desde') || changedProps.has('hasta') || changedProps.has('institucion') || changedProps.has('medico');
        if (shouldFetch) this._fetchData();
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { medico, desde, hasta, institucion } = urlQueryToDict();
        this.medico = `${medico || this.medico}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
        this.institucion = `${institucion || this.institucion}`;
    }

    /**
     * Actualiza la url.
     * @param {string} desde
     * @param {string} hasta
     * @param {string} medico
     * @param {string} institucion
     */
    _setQueryParams(desde, hasta, medico, institucion) {
        const filtros = {
            ...(medico && { medico }),
            ...(institucion && { institucion }),
            ...(desde && { desde: formatDateToISO(desde) }),
            ...(hasta && { hasta: formatDateToISO(hasta) }),
        };
        updateFiltersOnUrl(filtros, true);
    }

    _fetchData() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, medico, institucion } = this;
        this._setQueryParams(desde, hasta, medico, institucion);
        if (!desde || !hasta || !medico || !institucion) {
            this.reportData = [];
            return;
        }

        this.variables = {
            ...(medico && { medico }),
            ...(institucion && { institucion }),
            entre: `${formatDateToISO(desde)},${formatDateToISO(hasta)}`,
        };
        this.subscribe();
    }

    _setData(data) {
        const { tratamientos: { results: tratamientos } } = data;
        this.reportData = Object.values(tratamientos.reduce(this._groupByCliente, {}));
        this.totalPagar = this.reportData.reduce((total, actual) => total + actual.totalPagar, 0);
    }

    _groupByCliente(obj, tratamiento) {
        // eslint-disable-next-line object-curly-newline
        const { entidad, valor, valorPagarMedico, sesionesAtendidas } = tratamiento;
        const key = `${entidad.id}-${valor}`;
        if (!obj[key]) {
            // eslint-disable-next-line no-param-reassign
            obj[key] = {
                valor,
                valorPagarMedico,
                nombre: entidad.nombre,
                tratamientos: [tratamiento],
                totalCitas: sesionesAtendidas,
                totalPagar: valorPagarMedico * sesionesAtendidas,
            };
        } else {
            // eslint-disable-next-line no-param-reassign
            obj[key].tratamientos = [...obj[key].tratamientos, tratamiento];
            // eslint-disable-next-line no-param-reassign
            obj[key].totalCitas += sesionesAtendidas;
            // eslint-disable-next-line no-param-reassign
            obj[key].totalPagar += valorPagarMedico * sesionesAtendidas;
        }

        return obj;
    };
}

customElements.define('mh-tratamientos-pago-terapeutas', MedhisTratamientosPagoTerapeutas);
