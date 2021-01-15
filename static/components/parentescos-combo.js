import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `parentescos-combo` Combobox para parentescos.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class ParentescosCombo extends PolymerElement {
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
            <vaadin-combo-box label="Parentesco" required="[[required]]" hidden$="[[hidden]]" disabled="[[disabled]]"
                item-label-path="description" item-value-path="name" items="[[data.parentescos.enumValues]]"
                value="{{value}}" selected-item="{{selectedItem}}">
            </vaadin-combo-box>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query Parentescos {
                parentescos: __type(name: "PacienteParentescoResponsableEnumCreate") {
                    enumValues { name, description }
                }
            }
        `;
    }
}

customElements.define('parentescos-combo', ParentescosCombo);
