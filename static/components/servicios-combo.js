import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `servicios-combo` Combobox de servicios
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class ServiciosCombo extends PolymerElement {
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

            /**
             * Indica si se deben traer las tarifas de los servicios.
             */
            withTarifas: {
                type: Boolean,
                value: false,
            },

            /** Id del convenio. */
            convenio: String,

            /** Id de la institucion. */
            institucion: String,
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

            <apollo-query query="[[query]]" on-data-changed="_itemsFetched" loading="{{loading}}"></apollo-query>
            <vaadin-combo-box label="Servicio" required="[[required]]" hidden$="[[hidden]]" autofocus="[[autofocus]]"
                item-label-path="nombre" item-value-path="id" items="[[items]]" loading="[[loading]]"
                value="{{value}}" selected-item="{{selectedItem}}" on-change="_changed">
            </vaadin-combo-box>
        `;
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_fetchItems(withTarifas, convenio, institucion)',
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
            query Servicios($withTarifas: Boolean!, $convenio: ID, $institucion: ID) {
                servicios(planes: [$convenio], institucion: $institucion) {
                    results {
                        ...ServiciosCombo
                        tarifas(plan: $convenio, institucion: $institucion) @include(if: $withTarifas) {
                            id
                            valor
                            coopago
                        }
                    }
                }
            }
            ${ServiciosCombo.fragment}
        `;
    }

    /** Propagates event. */
    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }

    /**
     * Gets los servicios del combobox.
     * @param {boolean} withTarifas Indica si se deben traer tarifas.
     * @param {string} convenio Id del convenio.
     * @param {string} institucion Id de la institución.
     */
    _fetchItems(withTarifas, convenio, institucion) {
        const _convenio = convenio ? { convenio } : {};
        const _institucion = institucion ? { institucion } : {};
        
        const variables = { withTarifas, ..._convenio, ..._institucion };
        const queryElem = this.shadowRoot.querySelector('apollo-query');
        if (!queryElem.refetch(variables)) {
            queryElem.variables = variables;
        }
    }

    /** Sets los items */
    _itemsFetched(e) {
        const { servicios } = e.detail.value;
        this.items = servicios.results;
    }

    /** Valida el combobox */
    validate() {
        return this.shadowRoot.querySelector('vaadin-combo-box').validate();
    }
}

customElements.define('servicios-combo', ServiciosCombo);

ServiciosCombo.fragment = gql`
    fragment ServiciosCombo on Servicio {
        id
        nombre @title_case
    }
`;

export default ServiciosCombo;
