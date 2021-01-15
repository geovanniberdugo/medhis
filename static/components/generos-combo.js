import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `generos-combo` Combobox con los generos.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class GenerosCombo extends PolymerElement {
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
            <vaadin-combo-box label="Sexo" required="[[required]]" hidden$="[[hidden]]" disabled="[[disabled]]"
                item-label-path="description" item-value-path="name" items="[[data.generos.enumValues]]"
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
            query GenerosPaciente {
                generos: __type(name: "PacienteGeneroEnum") { 
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

customElements.define('generos-combo', GenerosCombo);
