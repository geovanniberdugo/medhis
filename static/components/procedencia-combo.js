import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `procedencias-combo` Combobox con las opciones de como se entero de la IPS.
 *
 * @customElement
 * @polymer
 * @demo
 */
class ProcedenciaCombo extends PolymerElement {
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

            <vaadin-combo-box label="Como se entero" required="[[required]]" hidden$="[[hidden]]"
                item-label-path="description" item-value-path="name" disabled="[[disabled]]"
                items="[[data.procedencia.enumValues]]" value="{{value}}"
                selected-item="{{selectedItem}}" autofocus="[[autofocus]]">
            </vaadin-combo-box>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query Procedencia {
                procedencia: __type(name: "PacienteProcedenciaEnumCreate") { 
                    enumValues { name, description } 
                }
            }
        `;
    }
}

customElements.define('procedencias-combo', ProcedenciaCombo);
