import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { formatMoney } from '../utils';

import '@polymer/paper-toggle-button/paper-toggle-button';
import '@polymer/paper-icon-button/paper-icon-button';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-checkbox/paper-checkbox';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-card/paper-card';
import '../components/transacciones-caja';
import '../components/cierre-caja-form';
import '../elements';

const RECIBIR_CAJA_MUTATION = gql`
    mutation RecibirCaja($caja: RecibirCajaInput!) {
        recibirCaja(input: $caja) {
            caja {
                id
                recibidoPor { id, nombreCompleto @title_case }
            }
        }
    }
`;

/**
 * `caja-pago-recibido` Audita si se recibio el pago de la caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class CajaPagoRecibido extends ApolloMutation {
    static get properties() {
        return {
            /** Caja. */
            caja: { type: Object },

            /** Indica si puede recibir el dinero. */
            canRecibir: { type: Boolean },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            .label {
                color: grey;
            }
        `;
    }

    render() {
        const { canRecibir, caja: { recibidoPor } } = this;
        return html`
            ${recibidoPor
                ? html`<span class="label">Pago recibido por</span><br>${recibidoPor.nombreCompleto}<br>`
                : html`<paper-checkbox ?disabled="${!canRecibir}" @change="${this.recibirCaja}">Pago recibido</paper-checkbox>`
            }
        `;
    }

    constructor() {
        super();
        this.mutation = RECIBIR_CAJA_MUTATION;
    }

    /** Recibir caja. */
    recibirCaja({ target: { checked } }) {
        if (checked) {
            this.variables = { caja: { id: this.caja.id } };
            this.mutate();
        }
    }
}

customElements.define('caja-pago-recibido', CajaPagoRecibido);

/** Muestra el formulario para el cierre/edición de caja. */
const showCajaForm = ({ target }, id) => {
    target.dispatchEvent(new CustomEvent('show-cierre-caja-form', {
        bubbles: true,
        composed: true,
        detail: { caja: id },
    }));
};

/** Muestra las transacciones de una caja */
const showTransacciones = ({ target }, id) => {
    target.dispatchEvent(new CustomEvent('show-transacciones-caja', {
        bubbles: true,
        composed: true,
        detail: { caja: id },
    }));
};

// Templates
const cajaItem = (caja, canRecibir, canVerTransacciones) => html`
    <li>
        <paper-card>
            <div class="card-content">
                <h3>${caja.empleado.nombreCompleto}</h3>
                <p>${caja.fecha} <br> ${caja.sucursal.nombre}</p>
                <p>
                    <span>Total</span><br>
                    ${formatMoney(caja.total)}
                </p>
                <div><caja-pago-recibido ?canRecibir="${canRecibir}" .caja="${caja}"></caja-pago-recibido></div>
                <div>
                    <paper-icon-button ?hidden="${!canVerTransacciones}" icon="my-icons:remove-red-eye"
                        @click="${e => showTransacciones(e, caja.id)}">
                    </paper-icon-button>
                    <paper-icon-button ?hidden="${!caja.canEdit}" icon="my-icons:edit"
                        @click="${e => showCajaForm(e, caja.id)}">
                    </paper-icon-button>
                    <a href="${caja.detalleUrl}"><paper-icon-button icon="my-icons:print"></paper-icon-button></a>
                </div>
            </div>
        </paper-card>
    </li>
`;

/**
 * `mh-cajas` Pagina que lista las cajas cerradas
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisCajas extends ApolloQuery {
    static get properties() {
        return {
            /** Indica si puede recibir el dinero. */
            canRecibir: { type: Boolean },

            /** Indica si puede cerrar la caja. */
            canCerrarCaja: { type: Boolean },

            /** Indica si puede ver las transacciones de una caja. */
            canVerTransacciones: { type: Boolean },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            section {
                display: flex;
            }

            ul {
                margin: 0;
                padding: 0;
            }

            li {
                list-style: none;
            }

            span {
                color: gray;
            }

            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--app-primary-color);
            }

            paper-button.primary {
                color: white;
                margin-left: auto;
                background-color: var(--app-secondary-color);
            }

            paper-card {
                width: 100%;
                margin-bottom: 10px;
            }

            paper-card .card-content {
                display: grid;
                align-items: center;
                grid-template-columns: repeat(auto-fit, minmax(9.4rem, 1fr));
            }

            #more {
                text-align: center;
            }
        `;
    }

    render() {
        // eslint-disable-next-line object-curly-newline
        const { loading, data, auditadas, canRecibir, canCerrarCaja, canVerTransacciones, updateQuery } = this;
        const cajas = data.cajas.results || [];
        const total = data.cajas.totalCount || 0;
        const variables = { auditadas, offset: cajas.length };

        return html`
            <section>
                <paper-toggle-button @checked-changed="${(e) => { this.auditadas = e.detail.value; }}">Mostrar auditados</paper-toggle-button>
                <paper-button class="primary" raised ?hidden="${!canCerrarCaja}" @click="${e => showCajaForm(e, null)}">cerrar caja</paper-button>
            </section>
            <br>
            <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
            <ul>
                ${cajas.map(caja => cajaItem(caja, canRecibir, canVerTransacciones))}
            </ul>
            <div id="more">
                <paper-button ?hidden="${cajas.length === 0 || cajas.length === total}"
                    @click="${() => this.fetchMore({ updateQuery, variables })}">
                    ver mas
                </paper-button>
            </div>
        `;
    }

    constructor() {
        super();
        this.notifyOnNetworkStatusChange = true;
        this.auditadas = false;
        this.query = gql`
            query Cajas($auditadas: Boolean!, $offset: Int) {
                cajas(verificadas: $auditadas) {
                    totalCount
                    results(limit: 10, offset: $offset) {
                        id
                        total
                        canEdit
                        detalleUrl
                        fecha @date(format: "DD/MM/YYYY")
                        sucursal { id, nombre @title_case }
                        empleado { id, nombreCompleto @title_case }
                        recibidoPor { id, nombreCompleto @title_case }
                    }
                }
            }
        `;
    }

    get auditadas() {
        return this._auditadas;
    }

    set auditadas(value) {
        this._auditadas = value;
        this._fetchData(value);
    }

    /** Fetch las cajas */
    _fetchData(auditadas) {
        const variables = { auditadas };
        this.variables = variables;
        this.subscribe();
    }

    /** */
    updateQuery(prev, { fetchMoreResult }) {
        if (!fetchMoreResult) return prev;
        return Object.assign({}, prev, {
            cajas: {
                totalCount: fetchMoreResult.cajas.totalCount,
                results: [...prev.cajas.results, ...fetchMoreResult.cajas.results],
                __typename: prev.cajas.__typename,
            },
        });
    }
}

customElements.define('mh-cajas', MedhisCajas);
