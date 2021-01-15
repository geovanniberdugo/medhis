import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `roles-combo` Combobox para las sucursales
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class RolesCombo extends PolymerElement {
    static get properties() {
        return {
            /** Nombre del combo. */
            name: String,

            /**
             * Escoge automaticamente la sucursal.
             */
            auto: {
                type: Boolean,
                value: false,
            },

            /**
             * Indica si el combo es requerido
             */
            required: {
                type: Boolean,
                value: false,
            },

            /**
             * Indica si el combo obtine el focus automaticamente
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
            <vaadin-combo-box label="Rol" required="[[required]]" hidden$="[[hidden]]"
                autofocus="[[autofocus]]" item-label-path="name" item-value-path="id"
                items="[[data.roles.results]]" value="{{value}}" on-change="_changed"
                selected-item="{{selectedItem}}">
            </vaadin-combo-box>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query Roles {
                roles {
                    results { id, name }
                }
            }
        `;
    }

    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }

    validate() {
        return this.shadowRoot.querySelector('vaadin-combo-box').validate();
    }
}

customElements.define('roles-combo', RolesCombo);
