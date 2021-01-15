import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `tipos-documento-combo` Combobox para los tipos de documento.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class TiposDocumentoCombo extends PolymerElement {
    static get properties() {
        return {
            name: String,

            required: {
                type: Boolean,
                value: false,
            },

            disabled: {
                type: Boolean,
                value: false,
            },

            autofocus: {
                type: Boolean,
                value: false,
            },

            hidden: {
                type: Boolean,
                value: false,
            },

            value: {
                type: String,
                notify: true,
            },

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

            <vaadin-combo-box label="Tipo de documento" required="[[required]]" hidden$="[[hidden]]" disabled="[[disabled]]"
                item-label-path="description" item-value-path="name" items="[[data.tiposDocumento.enumValues]]"
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
            query TiposDocumento {
                tiposDocumento: __type(name: "PacienteTipoDocumentoEnum") { 
                    enumValues { name, description } 
                }
            }
        `;
    }

    /** Valida el combobox */
    validate() {
        return this.shadowRoot.querySelector('vaadin-combo-box').validate();
    }
}

customElements.define('tipos-documento-combo', TiposDocumentoCombo);
