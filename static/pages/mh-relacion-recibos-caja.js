import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
// eslint-disable-next-line object-curly-newline
import { formatMoney, urlQueryToDict, updateFiltersOnUrl, groupBy, mapObject, totalizeBy } from '../utils';
import { unixTimeStampToJsDate, jsDateToUnixTimeStamp, ISODateToJSDate, jsDateToISO } from '../date';

import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-button';
import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-group';
import '@doubletrade/lit-datepicker/lit-datepicker-input';
import { cardCss } from '../components/common-css';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-card/paper-card';
import '../components/sucursales-combo';
import '../components/clientes-combo';
import '../elements';

const _flattenRecibos = (recibo) => {
    const {
        tratamiento: {
            coopago,
            servicio,
            orden: { institucion, plan },
        },
        ...data
    } = recibo;

    return {
        plan,
        ...data,
        coopago,
        servicio,
        institucion,
    };
};

const detalladoItem = recibo => html`
    <li class="card">
        <h3><span>#</span><span>${recibo.numero}</span></h3>
        <div>${recibo.paciente.nombreCompleto} <br> ${recibo.paciente.numeroDocumento}</div>
        <div><span class="label">Valor:</span> ${formatMoney(recibo.valor)} <br><span class="label">Coopago:</span> ${formatMoney(recibo.coopago)}</div>
        <div>${recibo.fecha} <br> <span class="label">Sucursal:</span> ${recibo.sucursal.nombre}</div>
        <div>${recibo.servicio.nombre} <br> ${recibo.plan.nombreCompleto}</div>
    </li>
`;

const formaPagoItem = item => html`
    <li class="card">
        <h3>${item.nombre}</h3>
        <div>${formatMoney(item.total)}</div>
    </li>
`;

/**
 * `mh-relacion-recibos-caja` Relación con los recibos de caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisRelacionRecibosCaja extends ApolloQuery {
    static get properties() {
        return {
            desde: { type: String },
            hasta: { type: String },
            cliente: { type: String },
            sucursal: { type: String },
            tipoReporte: { type: String },
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

            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--app-primary-color);
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

            #detail h3 {
                display: flex;
                align-items: center;
                flex-direction: column;
            }

            #detail h3 span:last-child {
                font-size: 1.19em;
            }
        `;

        return [cardCss, base];
    }

    render() {
        // eslint-disable-next-line object-curly-newline
        const { loading, data = {}, desde, hasta, cliente, sucursal, tipoReporte } = this;
        const instituciones = data.instituciones && data.instituciones.results || [];
        const recibos = data.recibosCaja && data.recibosCaja.results || [];
        const reportData = this._setData(recibos, tipoReporte);
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
                        <sucursales-combo value="${sucursal}" @change="${e => this.sucursal = e.target.value}"></sucursales-combo>
                        <vaadin-radio-group label="Tipo de reporte" value="${tipoReporte}" @value-changed="${e => this.tipoReporte = e.detail.value}">
                            <vaadin-radio-button value="0">Detallado</vaadin-radio-button><br>
                            <vaadin-radio-button value="1">Forma de pago</vaadin-radio-button>
                        </vaadin-radio-group>
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
                        ${institucion.items.map(item => tipoReporte === '0' ? detalladoItem(item) : formaPagoItem(item))}
                    </ul>
                `)}
            </section>
        `;
    }

    constructor() {
        super();
        this.cliente = '';
        this.sucursal = '';
        this.tipoReporte = '0';
        this.query = gql`
            query RelacionRecibosCaja($entre: String!, $cliente: ID, $sucursal: Float) {
                instituciones {
                    results { id, nombre }
                }
                recibosCaja(fechaEntre: $entre, cliente: $cliente, sucursal: $sucursal, anulados: false) {
                    results(ordering: "-numero") {
                        id
                        valor
                        numero
                        formaPago
                        formaPagoLabel
                        fecha @date(format: "DD/MM/YYYY")
                        sucursal { id, nombre @lowercase }
                        paciente { id, numeroDocumento, nombreCompleto @title_case }
                        tratamiento: servicioPrestado {
                            id
                            coopago
                            servicio { id, nombre @capitalize }
                            orden {
                                id
                                institucion { id, nombre @capitalize }
                                plan { id, nombreCompleto @title_case }
                            }
                        }
                    }
                }
            }
        `;

        this._setFiltersFromUrl();
    }

    // Lifecycles

    shouldUpdate() {
        return true;
    }

    updated(changedProps) {
        const shouldFetch = changedProps.has('desde') || changedProps.has('hasta') || changedProps.has('cliente') || changedProps.has('sucursal');
        if (shouldFetch) this._fetchData();
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { sucursal, desde, hasta, cliente } = urlQueryToDict();
        this.cliente = `${cliente || this.cliente}`;
        this.sucursal = `${sucursal || this.sucursal}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
    }

    /**
     * Actualiza la url.
     * @param {string} desde
     * @param {string} hasta
     * @param {string} cliente
     * @param {string} sucursal
     */
    _setQueryParams(desde, hasta, cliente, sucursal) {
        const filtros = {
            ...(cliente && { cliente }),
            ...(sucursal && { sucursal }),
            ...(desde && { desde: jsDateToISO(desde) }),
            ...(hasta && { hasta: jsDateToISO(hasta) }),
        };
        updateFiltersOnUrl(filtros, true);
    }

    _fetchData() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, cliente, sucursal } = this;
        this._setQueryParams(desde, hasta, cliente, sucursal);
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
            ...(sucursal && { sucursal }),
            entre: `${jsDateToISO(desde)},${jsDateToISO(hasta)}`,
        };
        
        this.subscribe({ variables, query: this.query });
    }

    _setData(recibos, tipoReporte) {
        return this._summarize(groupBy(recibos.map(_flattenRecibos), recibo => recibo.institucion.id), tipoReporte);
    }

    _summarize(grouppedRecibos, tipoReporte) {
        return mapObject(grouppedRecibos, (key, value) => {
            const { institucion } = value[0];

            return {
                key,
                nombre: institucion.nombre,
                total: totalizeBy(value, item => item.valor),
                items: tipoReporte === '0' ? value : this._reportByFomaPago(value),
            };
        });
    }

    _reportByFomaPago(recibos) {
        const groupped = groupBy(recibos, recibo => recibo.formaPago);
        const data = mapObject(groupped, (key, value) => {
            return {
                key,
                nombre: value[0].formaPagoLabel,
                total: totalizeBy(value, item => item.valor),
            };
        });

        return Object.values(data);
    }
}

customElements.define('mh-relacion-recibos-caja', MedhisRelacionRecibosCaja);
