import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import 'paper-money-input-ench/paper-money-input-ench';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import '@polymer/iron-form/iron-form';
import './sucursales-combo';
import './es-date-picker';
import './modal-spinner';

const CERRAR_CAJA_MUTATION = gql`
    mutation CerrarCaja($caja: CajaInput!) {
        cerrarCaja(input: $caja) {
            ok
        }
    }
`;

const EDITAR_CAJA_MUTATION = gql`
    mutation EditarCaja($caja: EditCajaInput!) {
        editarCaja(input: $caja) {
            ok
            caja {
                id
                total
                sucursal { id }
                fecha @date(format: "DD/MM/YYYY")
            }
        }
    }
`;

/**
 * `cerrar-caja` Mutacion para cerrar o editar una caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class CerrarCaja extends ApolloMutation {
    static get properties() {
        return {
            /** Indica si se esta editando una caja. */
            edit: { type: Boolean },
        };
    }

    render() {
        const { loading, edit } = this;

        return html`
            <paper-button ?disabled="${loading}">${edit ? 'editar' : 'cerrar'}</paper-button>
        `;
    }

    constructor() {
        super();
        this.edit = false;
    }

    onCompleted(data) {
        const ok = this.edit ? data.editarCaja.ok : data.cerrarCaja.ok;
        if (ok) this.dispatchEvent(new CustomEvent('mutation-done', { detail: null }));
    }

    /** Ejecuta la mutación. */
    execute(caja) {
        const opts = this.edit ? { mutation: EDITAR_CAJA_MUTATION } : { mutation: CERRAR_CAJA_MUTATION, refetchQueries: ['Cajas'] };
        this.mutate({
            ...opts,
            variables: { caja },
        });
    }
}

customElements.define('cerrar-caja', CerrarCaja);

/**
 * `cierre-caja-form` Formulario para el cierre/edición de caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class CierreCajaForm extends ApolloQuery {
    static get properties() {
        return {
            /** Indica si el modal se esta mostrando. */
            opened: {
                type: Boolean,
                reflect: true,
            },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            label {
                font-weight: bold;
                text-transform: uppercase;
            }

            @media (min-width: 40em) {
                paper-dialog {
                    width: 60%;
                }

                es-date-picker {
                    align-self: end;
                }

                form {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                }

                form label {
                    align-self: center;
                }

                form paper-money-input-ench {
                    align-self: center;
                }
            }
        `;
    }

    render() {
        const { data = {}, loading, opened } = this;
        const formasPago = data.formasPago.enumValues || [];
        const caja = data.caja || '';

        return html`
            <paper-dialog modal ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                ${loading ? html`<modal-spinner ?active="${loading}"></modal-spinner>` : ''}
                <h2>CIERRE CAJA ${caja ? html`# ${caja.id}` : ''}</h2>
                <paper-dialog-scrollable>
                    <iron-form>
                        <form>
                            ${caja ? html`<es-date-picker><vaadin-date-picker required name="fecha" value="${caja.fecha}"></vaadin-date-picker></es-date-picker>` : ''}
                            <sucursales-combo autofocus required name="sucursal" value="${caja && caja.sucursal.id}"></sucursales-combo>
                            ${caja ? '' : html`<b></b>`}
                            ${formasPago.map(formaPago => html`
                                <label for="${formaPago.name}">${formaPago.description}</label>
                                <paper-money-input-ench label="" name="${formaPago.name}"
                                    precision="0" max-value="99999999999999" value="${caja && this._getFormaPagoValue(formaPago.name, caja.detalles)}">
                                </paper-money-input-ench>
                            `)}
                            <paper-money-input-ench name="pagos" label="Pagos hechos"
                                precision="0" max-value="99999999999999" value="${caja && caja.pagos}">
                            </paper-money-input-ench>
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <cerrar-caja ?edit="${!!caja}" @click="${this._mutate}" @mutation-done="${() => { this.opened = false; }}"></cerrar-caja>
                    <paper-button dialog-dismiss>Cancelar</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.opened = false;
        this._boundOpenListener = this._open.bind(this);
        this.query = gql`
            query CajaForm($caja: ID!, $withCaja: Boolean!) {
                formasPago: __type(name: "DetalleCajaFormaPagoEnum") {
                    enumValues { name, description }
                }
                caja(id: $caja) @include(if: $withCaja) {
                    id
                    pagos
                    fecha
                    sucursal { id }
                    detalles {
                        id
                        valor
                        formaPago
                    }
                }
            }
        `;
    }

    get id() {
        return this._id;
    }

    set id(value) {
        this._id = value;
        this._fetchData(value);
    }

    // lifecycles

    connectedCallback() {
        super.connectedCallback();
        window.addEventListener('show-cierre-caja-form', this._boundOpenListener);
    }

    disconnectedCallback() {
        window.removeEventListener('show-cierre-caja-form', this._boundOpenListener);
        super.disconnectedCallback();
    }

    /** Show modal */
    _open({ detail: { caja } }) {
        this.id = caja;
        this.opened = true;
    }

    /**
     * Valor del detalle de la caja segun la forma de pago.
     * @param {String} forma forma de pago
     * @param {Array} detalles Detalles de la caja.
     */
    _getFormaPagoValue(forma, detalles) {
        const detalle = detalles.filter(det => det.formaPago === forma);
        return detalle.length > 0 ? detalle[0].valor : 0;
    }

    /**
     * Fetches los datos del formulario.
     * @param {String} id Id de la caja.
     */
    _fetchData(id) {
        this.variables = { caja: id || "", withCaja: !!id };
        this.subscribe();
    }

    /** Serialize detalle. */
    _serializeDetalle(detalles) {
        return Object.entries(detalles)
            .map(e => ({ formaPago: e[0], valor: e[1] }))
            .filter(e => !!e.valor);
    }

    /** Cierra o edita la caja. */
    _mutate({ target }) {
        const form = this.shadowRoot.querySelector('iron-form');
        if (!form.validate()) return;

        // eslint-disable-next-line object-curly-newline
        const { pagos, sucursal, fecha, ...detalle } = form.serializeForm();
        const extraVars = this.id ? { id: this.id, fecha } : {};
        target.execute({
            pagos,
            sucursal,
            ...extraVars,
            detalles: this._serializeDetalle(detalle),
        });
    }
}

customElements.define('cierre-caja-form', CierreCajaForm);
