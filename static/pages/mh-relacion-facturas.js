import { formatMoney, urlQueryToDict, updateFiltersOnUrl, groupBy, mapObject, totalizeBy } from '../utils';
import { unixTimeStampToJsDate, jsDateToUnixTimeStamp, ISODateToJSDate, jsDateToISO } from '../date';
import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import { progressCss, cardCss } from '../components/common-css';
import '@doubletrade/lit-datepicker/lit-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-card/paper-card';
import '../components/clientes-combo';
import '../elements';

/**
 * `mh-relacion-facturas` Relacion de facturas
 */
class MedhisRelacionFacturas extends ApolloQuery {
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

            h2 {
                color: grey;
                font-size: 1.2em;
                text-transform: uppercase;
            }

            paper-card {
                width: 100%;
            }

            #filter .card-content {
                display: grid;
                grid-gap: 5px;
                align-items: end;
                grid-template-columns: repeat(auto-fill, minmax(15em, 1fr));
            }

            #summary ul {
                text-transform: uppercase;
                display: grid;
                grid-gap: 15px;
                align-items: center;
                grid-template-columns: repeat(auto-fit, minmax(15em, 1fr));
            }

            #summary li {
                padding: 15px;
                display: flex;
                align-items: center;
                flex-direction: column;
                justify-content: center;
            }

            #summary li span:last-child {
                color: green;
                font-size: 20px;
                font-weight: bold;
            }

            #detail .card {
                display: grid;
                grid-gap: 5px;
                align-items: center;
                justify-items: center;
                grid-template-columns: repeat(auto-fit, minmax(12em, 1fr));
            }
        `;

        return [progressCss, cardCss, base];
    }

    render() {
        const { loading, data = {}, desde, hasta, cliente } = this;
        const instituciones = data.instituciones && data.instituciones.results || [];
        const facturas = data.facturas && data.facturas.results || [];
        const reportData = this._setData(facturas);
        const detailData = Object.values(reportData);

        return html`
            <section id="filter">
                <paper-card>
                    <div class="card-content">
                        <lit-datepicker-input .dateFrom="${jsDateToUnixTimeStamp(desde)}" .dateTo="${jsDateToUnixTimeStamp(hasta)}"
                            @date-from-changed="${e => this.desde = unixTimeStampToJsDate(e.detail.value)}"
                            @date-to-changed="${e => this.hasta = unixTimeStampToJsDate(e.detail.value)}">
                        </lit-datepicker-input>
                        <clientes-combo value="${cliente}" @change="${e => this.cliente = e.target.value}"></clientes-combo>
                    </div>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                </paper-card>
            </section>
            <section id="summary">
                <ul>
                    ${instituciones.map(institucion => html`
                        <li class="card"><span class="label">${institucion.nombre}</span> <span>${formatMoney((reportData[institucion.id] && reportData[institucion.id].total) || 0)}</span></li>
                    `)}
                </ul>
            </section>
            <section id="detail">
                ${detailData.map(institucion => html`
                    <h2>${institucion.nombre}</h2>
                    <ul>
                        ${institucion.items.map(item => html`
                            <li class="card">
                                <a href="${item.detalleUrl}" target="_blank">#${item.numero}</a>
                                <p>${item.fechaExpedicion}</p>
                                <p>${item.cliente.nombre}</p>
                                <p>${formatMoney(item.total)}</p>
                            </li>
                        `)}
                    </ul>
                `)}
            </section>
        `;
    }

    constructor() {
        super();
        this.cliente = '';
        this.notifyOnNetworkStatusChange = true;
        this.query = gql`
            query RelacionFacturas($entre: String!, $cliente: ID) {
                instituciones {
                    results { id, nombre }
                }
                facturas(anuladas: false, expedidaEntre: $entre, cliente: $cliente) {
                    results {
                        id
                        total
                        numero
                        detalleUrl
                        cliente { id, nombre @title_case }
                        institucion { id, nombre @title_case }
                        fechaExpedicion @date(format: "DD/MM/YYYY")
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

    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, cliente } = urlQueryToDict();
        this.cliente = `${cliente || this.cliente}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
    }

    _setQueryParams(desde, hasta, cliente) {
        const filtros = {
            ...(cliente && { cliente }),
            ...(desde && { desde: jsDateToISO(desde) }),
            ...(hasta && { hasta: jsDateToISO(hasta) }),
        };
        updateFiltersOnUrl(filtros, true);
    }

    _fetchData() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, cliente } = this;
        this._setQueryParams(desde, hasta, cliente);
        if (!desde || !hasta) {
            this.reportData = {};
            this.instituciones = [];
            return;
        }

        if (this.observableQuery && this.observableQuery.getCurrentResult().loading) {
            this.client.queryManager.stopQueryNoBroadcast(this.observableQuery.queryId);
        }

        const variables = {
            ...(cliente && { cliente }),
            entre: `${jsDateToISO(desde)},${jsDateToISO(hasta)}`,
        };

        this.subscribe({ variables, query: this.query });
    }

    _setData(facturas) {
        return this._summarize(groupBy(facturas, factura => factura.institucion.id));
    }

    _summarize(facturasAgrupadas) {
        return mapObject(facturasAgrupadas, (key, value) => {
            const { institucion } = value[0];

            return {
                key,
                items: value,
                nombre: institucion.nombre,
                total: totalizeBy(value, item => item.total),
            };
        });
    }
}

customElements.define('mh-relacion-facturas', MedhisRelacionFacturas);