import { unixTimeStampToJsDate, jsDateToUnixTimeStamp, ISODateToJSDate, jsDateToISO, formatISODate, DATETIME_FORMAT } from '../date';
import { urlQueryToDict, updateFiltersOnUrl } from '../utils';
import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import { cardCss, progressCss } from '../components/common-css';
import '@doubletrade/lit-datepicker/lit-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-card/paper-card';
import '../components/clientes-combo';
import '../elements';

/**
 * `mh-tratamientos-no-facturados-entidad` Tratamientos no facturados por entidad
 */
class MedhisTratamientosNoFacturadosEntidad extends ApolloQuery {
    static get properties() {
        return {
            desde: { type: String },
            hasta: { type: String },
            cliente: { type: String },
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

            li.card {
                display: grid;
                grid-gap: 5px;
                align-items: center;
                grid-template-columns: repeat(auto-fit, minmax(12em, 1fr));
            }

            .label {
                color: #636060;
            }

            #filter .card-content {
                display: grid;
                grid-gap: 5px;
                grid-template-columns: repeat(auto-fill, minmax(15em, 1fr));
            }

            paper-card {
                width: 100%;
            }
        `;

        return [progressCss, cardCss, base];
    }

    render() {
        const { cliente, desde, hasta, loading, data = { tratamientos: {} } } = this;
        const tratamientos = data.tratamientos.results || [];

        return html`
            <section id="filter">
                <paper-card>
                    <div class="card-content">
                        <clientes-combo required value="${cliente}" @change="${(e) => { this.cliente = e.target.value; }}"></clientes-combo>
                        <lit-datepicker-input required .dateFrom="${jsDateToUnixTimeStamp(desde)}" .dateTo="${jsDateToUnixTimeStamp(hasta)}"
                            @date-from-changed="${e => this.desde = unixTimeStampToJsDate(e.detail.value)}"
                            @date-to-changed="${e => this.hasta = unixTimeStampToJsDate(e.detail.value)}">
                        </lit-datepicker-input>
                    </div>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                </paper-card>
            </section>
            <section>
                <ul>
                    ${tratamientos.map(tratamiento => html`
                        <li class="card">
                            <p>
                                ${tratamiento.paciente.nombreCompleto} <br>
                                ${tratamiento.paciente.tipoDocumento} ${tratamiento.paciente.numeroDocumento}
                            </p>
                            <p>
                                ${tratamiento.servicio.nombre} <br>
                                Orden <a href="${tratamiento.ordenUrl}">${tratamiento.orden.id}</a>
                            </p>
                            <p>
                                <span class="label">Inicio:</span> ${formatISODate(tratamiento.fechaInicioTratamiento, DATETIME_FORMAT)} <br>
                                <span class="label">Fin:</span> ${formatISODate(tratamiento.fechaFinTratamiento, DATETIME_FORMAT)}
                            </p>
                        </li>
                    `)}
                </ul>
            </section>
        `;
    }

    constructor() {
        super();
        this.notifyOnNetworkStatusChange = true;
        this.query = gql`
            query TratamientosNoFacturadosEntidad($cliente: ID! $entre: String!) {
                tratamientos(facturados: false, cliente: $cliente, iniciaronEntre: $entre) {
                    results {
                        id
                        ordenUrl
                        orden { id }
                        fechaFinTratamiento
                        fechaInicioTratamiento
                        servicio { id, nombre @title_case }
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

        this._setFiltersFromUrl();
    }

    shouldUpdate() {
        return true;
    }

    updated(changedProps) {
        const shouldFetch = changedProps.has('desde') || changedProps.has('hasta') || changedProps.has('cliente');
        if (shouldFetch) this._fetchData();
    }

    /**
     * Actualiza la url.
     * @param {string} desde
     * @param {string} hasta
     * @param {string} cliente
     */
    _setQueryParams(desde, hasta, cliente) {
        const filtros = {
            ...(cliente && { cliente }),
            ...(desde && { desde: jsDateToISO(desde) }),
            ...(hasta && { hasta: jsDateToISO(hasta) }),
        };
        updateFiltersOnUrl(filtros, true);
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, cliente } = urlQueryToDict();
        this.cliente = `${cliente || this.cliente}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
    }

    _fetchData() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, cliente } = this;
        this._setQueryParams(desde, hasta, cliente);

        if (!desde || !hasta || !cliente) {
            return;
        }

        const variables = {
            ...(cliente && { cliente }),
            entre: `${jsDateToISO(desde)},${jsDateToISO(hasta)}`,
        };

        this.subscribe({ variables, query: this.query });
    }
}

customElements.define('mh-tratamientos-no-facturados-entidad', MedhisTratamientosNoFacturadosEntidad);