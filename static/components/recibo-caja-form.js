import { PolymerElement, html } from '@polymer/polymer/polymer-element';

import 'paper-money-input-ench/paper-money-input-ench';
import '@polymer/paper-input/paper-textarea';
import '../components/sucursales-combo';
import '@polymer/iron-form/iron-form';
import './formas-pago-combo';

/**
 * `recibo-caja-form` Formulario para ingresar recibo de caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class ReciboCajaForm extends PolymerElement {
    static get properties() {
        return {
            /** Datos del recibo. */
            recibo: {
                type: Object,
                value: () => ({}),
            },

            /** Indica si se debe preguntar por la sucursal */
            withSucursal: {
                type: Boolean,
                value: false,
            },
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                :host[hidden] {
                    display: none;
                }

                form {
                    display: grid;
                    grid-template-columns: 1fr;
                }

                .full {
                    grid-column: 1 / -1;
                }

                @media (min-width: 40em) {
                    form {
                        display: grid;
                        grid-gap: 5px;
                        align-items: end;
                        grid-template-columns: 1fr 1fr;
                    }
                }
            </style>

            <iron-form>
                <form>
                    <formas-pago-combo required name="formaPago" value="{{recibo.formaPago}}"></formas-pago-combo>
                    <paper-money-input-ench label="Abono *" name="valor" precision="0" max-value="99999999999999"
                        required value="{{recibo.valor}}">
                    </paper-money-input-ench>
                    <sucursales-combo hidden="[[!withSucursal]]" required="[[withSucursal]]" name="sucursal" value="{{recibo.sucursal}}"></sucursales-combo>
                    <paper-textarea label="Detalle" class="full" name="detalle" value="{{recibo.detalle}}"></paper-textarea>
                </form>
            </iron-form>
        `;
    }

    /**
     * Use for one-time configuration of your component after local
     * DOM is initialized.
     */
    ready() {
        super.ready();
        this._form = this.shadowRoot.querySelector('iron-form');
    }

    get value() {
        return this.recibo;
    }

    /** Resetea el formulario. */
    reset() {
        this.recibo = {};
        this._form.reset();
        this.shadowRoot.querySelector('paper-money-input-ench').clean();
    }

    /** Valida el formulario. */
    validate() {
        return this._form.validate();
    }
}

customElements.define('recibo-caja-form', ReciboCajaForm);
