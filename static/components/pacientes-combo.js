import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import { Debouncer } from '@polymer/polymer/lib/utils/debounce';
import { timeOut } from '@polymer/polymer/lib/utils/async';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `pacientes-combo` Combobox para filtrar pacientes.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class PacientesCombo extends PolymerElement {
    static get properties() {
        return {
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

            <vaadin-combo-box label="Paciente" required="[[required]]" hidden$="[[hidden]]"
                item-label-path="nombreCompleto" item-value-path="id" autofocus="[[autofocus]]"
                on-filter-changed="_debounceSearch" filtered-items="[[data.pacientes.results]]"
                value="{{value}}" selected-item="{{selectedItem}}" on-change="_changed">
                <template>[[item.numeroDocumento]] - [[item.nombreCompleto]]</template>
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
            query Pacientes($term: String!) {
                pacientes(search: $term) {
                    results {
                        id
                        nombreCompleto
                        numeroDocumento
                    }
                }
            }
        `;
    }

    /** Propagates event. */
    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }

    /**
     * Busca paciente.
     */
    _searchPaciente(term) {
        if (!term) return;

        const query = this.shadowRoot.querySelector('apollo-query');
        const variables = { term };
        if (!query.refetch(variables)) {
            query.variables = variables;
        }
    }

    /** Debounce search after 500. */
    _debounceSearch(e) {
        const term = e.detail.value;
        this._debouncer = Debouncer.debounce(
            this._debouncer,
            timeOut.after(500),
            () => this._searchPaciente(term),
        );
    }
}

customElements.define('pacientes-combo', PacientesCombo);
