import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { formatMoney } from '../utils';

import BasePacientePerfil from '../components/base-paciente-perfil';
import { progressCss } from '../components/common-css';
import '@polymer/paper-icon-button/paper-icon-button';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-tooltip/paper-tooltip';
import '@polymer/paper-input/paper-textarea';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '@polymer/iron-icon/iron-icon';
import '../components/nuevo-pago';
import '../elements';

const ANULAR_RECIBO_MUTATION = gql`
    mutation AnularReciboCaja($input: AnularReciboCajaInput!) {
        anularReciboCaja(input: $input) {
            ok
            reciboCaja {
                id
                razonAnulacion
                anuladoEl @date(format: "DD/MM/YYYY")
                anuladoPor { id, nombreCompleto @title_case }
            }
        }
    }
`;

/**
 * `anular-recibo-caja` Anular recibo de caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class AnularReciboCaja extends ApolloMutation {
    static get properties() {
        return {

        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            paper-dialog {
                margin: 5px;
                width: 250px;
            }
        `;
    }

    render() {
        const { loading } = this;

        return html`
            <paper-dialog no-overlap horizontal-align="center" vertical-align="auto" scroll-action="lock">
                <paper-textarea autofocus required label="Razón"></paper-textarea>
                <div class="buttons">
                    <paper-button ?disabled="${loading}" @click="${this._anular}">anular</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    firstUpdated() {
        this.textElem = this.shadowRoot.querySelector('paper-textarea');
        this.dialogElem = this.shadowRoot.querySelector('paper-dialog');
    }

    _anular() {
        if (!this.textElem.validate()) return;

        const variables = { input: { id: this.recibo, razonAnulacion: this.textElem.value } };
        this.mutate({
            variables,
            mutation: ANULAR_RECIBO_MUTATION,
            refetchQueries: ['TratamientosPorPagar'],
        });
    }

    onCompleted({ anularReciboCaja: { ok } }) {
        if (ok) {
            this.textElem.value = '';
            this.dialogElem.close();
        }
    }

    open({ element, recibo }) {
        this.dialogElem.positionTarget = element;
        this.recibo = recibo;
        this.dialogElem.open();
    }
}

customElements.define('anular-recibo-caja', AnularReciboCaja);

// Templates

// eslint-disable-next-line object-curly-newline
const pagoItem = ({ id, numero, tratamiento, fecha, valor, formaPagoLabel, detalleUrl, canAnular, anuladoEl, anuladoPor, razonAnulacion }, showAnularDialog) => html`
    <li>
        <paper-card>
            <div class="card-content">
                <p>
                    <span class="numero-recibo"># ${numero}</span> <br>
                    <a href="${tratamiento.ordenUrl}" class="orden-url"># ${tratamiento.id} ${tratamiento.servicio.nombre}</a>
                </p>
                <p>${fecha}</p>
                <p>${formatMoney(valor)}</p>
                <p>
                    ${formaPagoLabel} <br>
                </p>
                ${anuladoPor && html`
                    <p class="anulado">
                        <span>ANULADO</span><br>
                        <span class="label">${anuladoEl}</span><br>
                        <span class="label">${anuladoPor.nombreCompleto}</span><br>
                        <paper-tooltip>${razonAnulacion}</paper-tooltip>
                    </p>
                `}
                <div ?hidden="${anuladoPor}">
                    <a href="${detalleUrl}"><iron-icon icon="my-icons:print"></iron-icon></a>
                    <paper-icon-button ?hidden="${!canAnular}" icon="my-icons:delete"
                        @click="${e => showAnularDialog({ elem: e.target, recibo: id })}">
                    </paper-icon-button>
                </div>
            </div>
        </paper-card>
    </li> 
`;

/**
 * `mh-pagos-paciente` Muestra los pagos de un paciente
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisPagosPaciente extends ApolloQuery {
    static get properties() {
        return {
            /** Id del paciente */
            paciente: { type: String },
        };
    }

    static get styles() {
        const base = css`
            :host {
                display: block;
            }

            a {
                text-decoration: none;
                color: var(--app-primary-color);
            }

            ul {
                margin: 0;
                padding: 0;
            }

            li {
                list-style: none;
                margin-bottom: 5px;
            }

            section {
                display: flex;
                margin-bottom: 10px;
                align-items: flex-end;
            }

            section paper-button {
                height: 40px;
                color: white;
                margin-left: auto;
                background-color: var(--accent-color);
            }

            paper-card {
                width: 100%;
            }

            paper-card:hover {
                background-color: #f5f2f2;
            }

            iron-icon, paper-icon-button {
                padding: 5px;
                color: initial;
                border: 1px solid;
                border-radius: 20px;
            }

            .card-content {
                display: grid;
                grid-gap: 5px;
                align-items: center;
                grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
            }

            .numero-recibo {
                font-size: 22px;
                font-weight: bold;
            }
            
            .anulado span:first-child {
                color: red;
            }

            .order-url {
                font-size: 15px;
            }

            #more {
                text-align: center;
            }

            @media (min-width: 40em) {
                paper-input {
                    width: 20%;
                }
            }
        `;

        return [BasePacientePerfil.headerStyles, progressCss, base];
    }

    render() {
        const { loading, data, updateQuery } = this;
        const paciente = data.paciente || {};
        const pagos = data.pagos.results || [];
        const total = data.pagos.totalCount || 0;
        const variables = { paciente: paciente.id, offset: pagos.length };

        return html`
            <base-paciente-perfil selected-menu="pagos" .paciente="${paciente}">
                <header>
                    <h1>Pagos</h1>
                </header>

                <section>
                    <paper-input label="No. recibo" type="number" @blur="${this._filterByNumero}"></paper-input>
                    <paper-button @click="${this._showNuevoPago}">agregar pago</paper-button>
                </section>
                <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                <ul>
                    ${pagos.map(pago => pagoItem(pago, this._showAnularDialog.bind(this)))}
                </ul>
                <div id="more">
                    <paper-button ?hidden="${pagos.length === 0 || pagos.length === total}"
                        @click="${() => this.fetchMore({ updateQuery, variables })}">
                        ver mas
                    </paper-button>
                </div>
                <anular-recibo-caja></anular-recibo-caja>
            </base-paciente-perfil>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query PagosPaciente($paciente: ID!, $offset: Int, $numero: Int) {
                paciente(id: $paciente) {
                    ...BasePacientePerfil
                }
                pagos: recibosCaja(paciente: $paciente, numero: $numero) {
                    totalCount
                    results(ordering: "-numero", limit: 10, offset: $offset) {
                        id
                        valor
                        numero
                        canAnular
                        detalleUrl
                        formaPagoLabel
                        razonAnulacion
                        fecha @date(format: "DD/MM/YYYY")
                        anuladoEl @date(format: "DD/MM/YYYY")
                        anuladoPor { id, nombreCompleto @title_case }
                        tratamiento: servicioPrestado {
                            id
                            ordenUrl
                            servicio { id, nombre @title_case }
                        }
                    }
                }
            }
            ${BasePacientePerfil.fragment}
        `;
    }

    get paciente() {
        return this._paciente;
    }

    set paciente(value) {
        this._paciente = value;
        this._fetchData(value);
    }

    /** Fetch los datos */
    _fetchData(id) {
        this.variables = { paciente: id };
        this.subscribe();
    }

    /** Filtra los recibos por número del recibo. */
    _filterByNumero(e) {
        const { paciente } = this;
        const { value } = e.target;
        this.variables = value ? { paciente, numero: value } : { paciente };
        this.subscribe();
    }

    _showNuevoPago() {
        this.dispatchEvent(new CustomEvent('show-nuevo-pago', {
            bubbles: true,
            composed: true,
            detail: null,
        }));
    }

    _showAnularDialog({ elem, recibo }) {
        this.shadowRoot.querySelector('anular-recibo-caja').open({ element: elem, recibo });
    }

    /** Pagination */
    updateQuery(prev, { fetchMoreResult }) {
        if (!fetchMoreResult) return prev;
        return Object.assign({}, prev, {
            pagos: {
                totalCount: fetchMoreResult.pagos.totalCount,
                results: [...prev.pagos.results, ...fetchMoreResult.pagos.results],
                __typename: prev.pagos.__typename,
            },
        });
    }
}

customElements.define('mh-pagos-paciente', MedhisPagosPaciente);
