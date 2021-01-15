import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `profesiones-combo` Combobox con las profesiones.
 *
 * @customElement
 * @polymer
 * @demo
 */
class ProfesionesCombo extends PolymerElement {
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

            <vaadin-combo-box label="Ocupación" required="[[required]]" hidden$="[[hidden]]" value="{{value}}"
                item-label-path="nombre" item-value-path="id" items="[[data.profesiones.results]]"
                selected-item="{{selectedItem}}" autofocus="[[autofocus]]" disabled="[[disabled]]">
            </vaadin-combo-box>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query Profesiones {
                profesiones {
                    results {
                        id
                        nombre @capitalize
                    }
                }
            }
        `;
    }
}

customElements.define('profesiones-combo', ProfesionesCombo);
