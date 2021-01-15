import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `grupos-etnicos-combo` Combobox para los grupos sanguineos.
 *
 * @customElement
 * @polymer
 * @demo
 */
class GruposEtnicosCombo extends PolymerElement {
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

            <vaadin-combo-box label="Grupo Etnico" required="[[required]]" hidden="[[hidden]]"
                item-label-path="description" item-value-path="name" disabled="[[disabled]]"
                items="[[data.gruposEtnicos.enumValues]]" value="{{value}}"
                selected-item="{{selectedItem}}" autofocus="[[autofocus]]">
            </vaadin-combo-box>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query GruposEtnicos {
                gruposEtnicos: __type(name: "PacienteGrupoEtnicoEnumCreate") { 
                    enumValues { name, description } 
                }
            }
        `;
    }
}

customElements.define('grupos-etnicos-combo', GruposEtnicosCombo);
