import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { urlQueryToDict, updateFiltersOnUrl, formatDateToISO, ISODateToJSDate, formatMoney } from '../utils';

import { cardCss } from '../components/common-css';
import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '../components/instituciones-combo';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '../components/clientes-combo';
import '../elements';

/**
 * `mh-tratamientos-facturados-entidad` Tratamientos facturados por entidad.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class TratamientosFacturadosEntidad extends ApolloQuery {
    static get properties() {
        return {
            desde: { type: String },
            hasta: { type: String },
            cliente: { type: String },
            reportData: { type: Array },
            institucion: { type: String },
            totalFacturado: { type: Number },
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

            h2 {
                color: grey;
                font-size: 1.2em;
                text-transform: uppercase;
            }

            paper-card {
                width: 100%;
            }

            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--app-primary-color);
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

            #filter .card-content {
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

        return [cardCss, base];
    }

    render() {
        const { institucion, cliente, desde, hasta, reportData, totalFacturado, loading } = this;

        return html`
            <section id="filter">
                <paper-card>
                    <div class="card-content">
                        <instituciones-combo required value="${institucion}"
                            @change="${(e) => { this.institucion = e.target.value; }}">
                        </instituciones-combo>
                        <clientes-combo required value="${cliente}"
                            @change="${(e) => { this.cliente = e.target.value; }}">
                        </clientes-combo>
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
                    </div>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                </paper-card>
            </section>
            <section id="report">
                ${reportData.map(servicio => html`
                    <h2>${servicio.nombre}</h2>
                    <h3>
                        <span class="label">Total de citas:</span> ${servicio.totalCitas} - 
                        <span class="label">Tarifa convenio:</span> ${formatMoney(servicio.valor)} - 
                        <span class="label">Facturado:</span> ${formatMoney(servicio.total)}
                    </h3>
                    <ul>
                        ${servicio.tratamientos.map(tratamiento => html`
                            <li class="card">
                                <p>Orden <br><a href="${tratamiento.ordenUrl}">${tratamiento.orden.id}</a></p>
                                <p>${tratamiento.paciente.nombreCompleto}<br>${tratamiento.paciente.numeroDocumento}</p>
                                <p>
                                    <span class="label"># citas:</span> ${tratamiento.cantidad} <br>
                                    <span class="label"># facturadas:</span> ${tratamiento.cantCitasFacturadas}
                                </p>
                                <p>
                                    Facturas <br> ${tratamiento.facturas.map(factura => html`
                                        <a href="${factura.detalleUrl}" target="_blank">#${factura.numero}</a> - ${factura.fechaExpedicion} <br>
                                    `)}
                                </p>
                            </li>
                        `)}
                    </ul>
                `)}
            </section>
            <section id="total">
                <h2>Total facturado: ${formatMoney(totalFacturado)}</h2>
            </section>
        `;
    }

    constructor() {
        super();
        this.desde = '';
        this.hasta = '';
        this.cliente = '';
        this.reportData = [];
        this.institucion = '';
        this.notifyOnNetworkStatusChange = true;
        this.query = gql`
            query TratamientosFacturadosEntidad($institucion: ID!, $cliente: ID!, $entre: String!) {
                tratamientos(institucion: $institucion, cliente: $cliente, facturadosEntre: $entre) {
                    results {
                        id
                        valor
                        ordenUrl
                        cantidad
                        orden { id }
                        servicio { id, nombre @title_case }
                        citas { id, detalleFactura { id, subtotal }}
                        paciente { id, numeroDocumento, nombreCompleto @title_case}
                        facturas { id, numero, fechaExpedicion @date(format: "DD/MM/YYYY"), detalleUrl }
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
        const shouldFetch = changedProps.has('desde') || changedProps.has('hasta') || changedProps.has('cliente') || changedProps.has('institucion');
        if (shouldFetch) this._fetchData();
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { institucion, desde, hasta, cliente } = urlQueryToDict();
        this.cliente = `${cliente || this.cliente}`;
        this.institucion = `${institucion || this.institucion}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
    }

    /**
     * Actualiza la url.
     * @param {string} desde
     * @param {string} hasta
     * @param {string} cliente
     * @param {string} institucion
     */
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
        const { desde, hasta, cliente, institucion } = this;
        this._setQueryParams(desde, hasta, cliente, institucion);
        if (!desde || !hasta || !cliente || !institucion) {
            return;
        }

        this.variables = {
            ...(cliente && { cliente }),
            ...(institucion && { institucion }),
            entre: `${formatDateToISO(desde)},${formatDateToISO(hasta)}`,
        };
        this.subscribe();
    }

    _setData() {
        const { tratamientos: { results: tratamientos } } = this.data;
        this.reportData = Object.values(this._summarize(this._groupBySevicioValor(tratamientos)));
        this.totalFacturado = this.reportData.reduce((total, servicio) => total + servicio.total, 0);
    }

    _groupBySevicioValor(tratamientos) {
        return tratamientos.reduce((obj, tratamiento) => {
            const { servicio, valor } = tratamiento;
            const key = `${servicio.id}-${valor}`;

            if (!obj[key]) {
                obj[key] = [tratamiento];
            } else {
                obj[key].push(tratamiento);
            }

            return obj;
        }, {});
    }

    _summarize(obj) {
        const totalFacturado = (citasFacturadas) => {
            const detalles = citasFacturadas.map(cita => cita.detalleFactura);
            const uniqueDetalles = [...new Set(detalles.map(det => det.id))].map(id => detalles.find(det => det.id === id));

            return uniqueDetalles.reduce((total, det) => total + det.subtotal, 0);
        }

        const result = {};
        Object.entries(obj).forEach(([key, value]) => {
            const { valor, servicio } = value[0];
            const tratamientos = value.map(tr => {
                const { citas, ...data } = tr;
                const citasFacturadas = citas.filter(cita => !!cita.detalleFactura);
                return {
                    ...data,
                    citasFacturadas,
                    cantCitasFacturadas: citasFacturadas.length,
                }
            });

            result[key] = {
                valor,
                tratamientos,
                nombre: servicio.nombre,
                totalCitas: tratamientos.reduce((total, tr) => total + tr.cantCitasFacturadas, 0),
                total: tratamientos.reduce((total, tr) => total + totalFacturado(tr.citasFacturadas), 0),
            };
        });
        return result;
    }
}

customElements.define('mh-tratamientos-facturados-entidad', TratamientosFacturadosEntidad);
