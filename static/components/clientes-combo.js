import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `clientes-combo` Combobox con los clientes.
 *
 * @customElement
 * @polymer
 * @demo
 */
class ClientesCombo extends PolymerElement {
    static get properties() {
        return {
            /** Nombre del campo. */
            name: String,

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

            <vaadin-combo-box label="IPS/EPS" required="[[required]]" hidden$="[[hidden]]" on-change="_changed"
                item-label-path="nombre" item-value-path="id" items="[[data.clientes.results]]"
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
            query Clientes {
                clientes {
                    results {
                        id
                        discriminarIva
                        facturaPaciente
                        nombre @title_case
                    }
                }
            }
        `;
    }

    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }
}

customElements.define('clientes-combo', ClientesCombo);
