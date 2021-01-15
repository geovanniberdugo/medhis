import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `instituciones-combo` Combobox con las instituciones.
 *
 * @customElement
 * @polymer
 * @demo
 */
class InstitucionesCombo extends PolymerElement {
    static get properties() {
        return {
            /** Nombre del combo. */
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
            <vaadin-combo-box label="Institución" required="[[required]]" hidden$="[[hidden]]" on-change="_changed"
                item-label-path="nombre" item-value-path="id" items="[[data.instituciones.results]]"
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
            query Instituciones {
                instituciones {
                    results {
                        id
                        nombre @title_case
                    }
                }
            }
        `;
    }

    /** Propagates event. */
    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }

    /** Valida el combobox */
    validate() {
        return this.shadowRoot.querySelector('vaadin-combo-box').validate();
    }
}

customElements.define('instituciones-combo', InstitucionesCombo);
