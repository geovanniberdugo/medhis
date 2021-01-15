import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `formas-pago-combo` Combobox para las formas de pago.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class FormasPagoCombo extends PolymerElement {
    static get properties() {
        return {
            /**
             * Indica si el combo es requerido
             */
            required: {
                type: Boolean,
                value: false,
            },

            /**
             * Indica si el combo debe tener el foco.
             */
            autofocus: {
                type: Boolean,
                value: false,
            },

            /**
             * Indica si el combo se muestra
             */
            hidden: {
                type: Boolean,
                value: false,
            },

            /** Valor seleccionado */
            value: {
                type: String,
                notify: true,
            },

            /**
             * Item seleccionado
             */
            selectedItem: {
                type: Object,
                notify: true,
            },
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                vaadin-combo-box {
                    width: 100%;
                }
            </style>

            <apollo-query query="[[query]]" data="{{data}}"></apollo-query>

            <vaadin-combo-box label="Forma de pago" required="[[required]]" hidden$="[[hidden]]"
                item-label-path="description" item-value-path="name" items="[[data.formasPago.enumValues]]"
                value="{{value}}" selected-item="{{selectedItem}}" autofocus="[[autofocus]]">
            </vaadin-combo-box>
        `;
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        this.query = gql`
            query FormasPago {
                formasPago: __type(name: "ReciboCajaFormaPagoEnum") {
                    enumValues { name, description }
                }
            }
        `;
    }
}

customElements.define('formas-pago-combo', FormasPagoCombo);
