import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `sucursales-combo` Combobox para las sucursales
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class SucursalesCombo extends PolymerElement {
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

            <apollo-query query="[[query]]" on-data-changed="_sucursalesFetched"></apollo-query>
            <vaadin-combo-box label="Sucursal" required="[[required]]" hidden$="[[hidden]]"
                autofocus="[[autofocus]]" item-label-path="nombre" item-value-path="id"
                items="[[sucursales]]" value="{{value}}" on-change="_changed"
                selected-item="{{selectedItem}}">
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
            query Sucursales {
                sucursales {
                    results {
                        id
                        nombre @title_case
                    }
                }
            }
        `;
    }

    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }

    /** Sets medicos */
    _sucursalesFetched(e) {
        const { sucursales } = e.detail.value;
        this.sucursales = sucursales.results;

        // eslint-disable-next-line prefer-destructuring
        if (this.sucursales.length > 0 && this.auto && !this.value) this.value = this.sucursales[0].id;
    }

    /** Valida el combobox */
    validate() {
        return this.shadowRoot.querySelector('vaadin-combo-box').validate();
    }
}

customElements.define('sucursales-combo', SucursalesCombo);
