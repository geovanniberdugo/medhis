import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `medicos-combo` Combobox con los medicos.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedicosCombo extends PolymerElement {
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

            /**
             * Indica si se deben traer los horarios de atención.
             */
            withHorarios: {
                type: Boolean,
                value: false,
            },

            /**
             * Indica si se deben traer las sucursales.
             */
            withSucursales: {
                type: Boolean,
                value: false,
            },

            /** Medicos que no estan asociados a ninguna agenda. */
            individuales: {
                type: Boolean,
                value: false,
            },

            /** Medicos activos. */
            activos: {
                type: Boolean,
                value: false,
            },

            /** Id de la institución. */
            institucion: String,

            /** Id de la sucursal. */
            sucursal: String,
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                :host[hidden] {
                    display: none;
                }

                vaadin-combo-box {
                    width: 100%;
                }
            </style>

            <apollo-query query="[[query]]" on-data-changed="_medicosFetched"></apollo-query>
            <vaadin-combo-box label="Medico" required="[[required]]" hidden$="[[hidden]]" autofocus="[[autofocus]]"
                item-label-path="nombreCompleto" item-value-path="id" items="[[medicos]]"
                value="{{value}}" selected-item="{{selectedItem}}" on-change="_changed">
            </vaadin-combo-box>
        `;
    }

    static get observers() {
        return [
            '_fetchItems(withHorarios, withSucursales, individuales, institucion, sucursal, activos)',
        ];
    }

    /**
      * Instance of the element is created/upgraded. Useful for initializing
      * state, set up event listeners, create shadow dom.
      * @constructor
      */
    constructor() {
        super();
        this.query = gql`
            query Medicos($withHorarios: Boolean!, $withSucursales: Boolean!, $individuales: Boolean!, $institucion: ID, $sucursal: ID, $activo: Boolean) {
                medicos: empleados(medicos: true, individuales: $individuales, instituciones: [$institucion], sucursal: $sucursal, activo: $activo) {
                    results {
                        ...MedicosCombo
                        sucursales @include(if: $withSucursales) {
                            id
                            nombre @title_case
                        }
                        horariosAtencion @include(if: $withHorarios) {
                            id
                            dia
                            horasAtencion
                            sucursal { id }
                        }
                    }
                }
            }
            ${MedicosCombo.fragment}
        `;
    }

    /** Propagates event. */
    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }

    /**
     * Gets los medicos del combobox.
     * @param {boolean} withHorarios Indica si se deben traer los horarios de atención.
     * @param {boolean} withSucursales Indica si se deben traer las sucursales.
     * @param {boolean} individuales Indica si se deben traer las sucursales.
     * @param {string} institucion Id de la institución.
     * @param {string} sucursal Id de la sucursal.
     * @param {boolean} activos Indica si se deben mostrar solo los activos.
     */
    _fetchItems(withHorarios, withSucursales, individuales, institucion, sucursal, activos) {
        const _sucursal = sucursal ? { sucursal } : {};
        const _institucion = institucion ? { institucion } : {};
        const _activos = activos ? { activo: true } : {};

        const variables = { individuales, withHorarios, withSucursales, ..._sucursal, ..._institucion, ..._activos };
        const queryElem = this.shadowRoot.querySelector('apollo-query');
        if (!queryElem.refetch(variables)) {
            queryElem.variables = variables;
        }
    }

    /** Sets medicos */
    _medicosFetched(e) {
        const { medicos } = e.detail.value;
        this.medicos = medicos.results;

        // eslint-disable-next-line prefer-destructuring
        if (this.medicos.length > 0 && this.auto && !this.value) this.value = this.medicos[0].id;
    }
}

customElements.define('medicos-combo', MedicosCombo);

MedicosCombo.fragment = gql`
    fragment MedicosCombo on Empleado {
        id
        duracionCita
        nombreCompleto @title_case
    }
`;

export default MedicosCombo;
