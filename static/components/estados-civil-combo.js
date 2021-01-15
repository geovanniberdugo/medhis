import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `estados-civil-combo` Combobox para los estado civil.
 *
 * @customElement
 * @polymer
 * @demo
 */
class EstadosCivilCombo extends PolymerElement {
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

            <vaadin-combo-box label="Estado Civil" required="[[required]]" hidden="[[hidden]]" disabled="[[disabled]]"
                item-label-path="description" item-value-path="name" auto-validate value="{{value}}"
                items="[[data.estadosCiviles.enumValues]]" selected-item="{{selectedItem}}" autofocus="[[autofocus]]">
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
            query EstadoCivil {
                estadosCiviles: __type(name: "PacienteEstadoCivilEnumCreate") { 
                    enumValues { name, description } 
                }
            }
        `;
    }
}

customElements.define('estados-civil-combo', EstadosCivilCombo);
