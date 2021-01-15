import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `convenios-combo` Combobox para los convenios.
 *
 * @customElement
 * @polymer
 * @demo
 *
 * @attr {Boolean} nombre-completo
 */
class ConveniosCombo extends PolymerElement {
    static get properties() {
        return {
            /** Nombre del combo */
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

            /** Indica si se usa nombre completo */
            nombreCompleto: {
                type: Boolean,
                value: false,
            },

            /**
             * Label a usar en combobox.
             */
            labelPath: {
                type: String,
                computed: '_setLabel(nombreCompleto)',
            },

            /** Id de la institución. */
            institucion: String,

            /** gql query */
            query: Object,

            /** query variables */
            variables: {
                type: Object,
                observer: '_variablesChanged',
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

            <apollo-query query="[[query]]" loading="{{loading}}" on-data-changed="_itemsFetched"></apollo-query>
            <vaadin-combo-box label="Convenio" required="[[required]]" hidden$="[[hidden]]" loading="[[loading]]"
                item-label-path="[[labelPath]]" item-value-path="id" items="[[convenios]]" on-change="_changed"
                value="{{value}}" selected-item="{{selectedItem}}">
            </vaadin-combo-box>
        `;
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_fetchItems(institucion)',
        ];
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        this.query = gql`
            query Convenios($institucion: ID) {
                convenios: planes(institucion: $institucion) {
                    results {
                        ...ConveniosCombo
                    }
                }
            }
            ${ConveniosCombo.fragment}
        `;
    }

    /** Propagates event. */
    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }

    /**
     * Gets los convenios del combobox.
     * @param {string} institucion Id de la institución.
     */
    _fetchItems(institucion) {
        const _institucion = institucion ? { institucion } : {};

        const variables = { ..._institucion };
        const queryElem = this.shadowRoot.querySelector('apollo-query');
        if (!queryElem.refetch(variables)) {
            queryElem.variables = variables;
        }
    }

    /** Sets conveios */
    _itemsFetched(e) {
        const { convenios } = e.detail.value;
        this.convenios = convenios.results;

        // eslint-disable-next-line prefer-destructuring
        // if (this.convenios.length > 0 && this.auto && !this.value) this.value = this.convenios[0].id;
    }

    /** Observer. */
    _variablesChanged(variables) {
        this.__value = this.value;
        if (!variables) {
            this.value = '';
            this.__value = '';
            this.convenios = [];
            return;
        }

        if (variables) {
            const queryElem = this.shadowRoot.querySelector('apollo-query');
            if (!queryElem.refetch(variables)) {
                queryElem.variables = variables;
            }
        }
    }

    /** Sets convenios */
    _conveniosFetched(e) {
        const { convenios } = e.detail.value;
        this.convenios = convenios.results;
        this.value = this.__value;
    }

    /** Sets el label a mostrar */
    _setLabel(nombreCompleto) {
        return nombreCompleto ? 'nombreCompleto' : 'nombre';
    }

    /** Valida el combobox */
    validate() {
        return this.shadowRoot.querySelector('vaadin-combo-box').validate();
    }
}

customElements.define('convenios-combo', ConveniosCombo);

ConveniosCombo.fragment = gql`
    fragment ConveniosCombo on Plan {
        id
        cliente { id }
        nombre @title_case
        nombreCompleto @title_case
    }
`;

export default ConveniosCombo;
