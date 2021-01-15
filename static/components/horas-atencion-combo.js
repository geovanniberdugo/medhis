import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import { formatISOTime } from '../utils';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `horas-atencion-combo` Combobox con las horas de atencion de un medico en una sucursal.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class HorasAtencionCombo extends PolymerElement {
    static get properties() {
        return {
            name: String,

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

            horasAtencion: {
                type: Array,
                value: () => [],
            },

            /** Id de la institución. */
            fecha: String,

            /** Id de la sucursal. */
            sucursal: String,

            /** Id del medico */
            medico: String,
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

            <apollo-query query="[[query]]" on-data-changed="_itemsFetched"></apollo-query>
            <vaadin-combo-box label="Hora" required="[[required]]" hidden$="[[hidden]]" autofocus="[[autofocus]]"
                items="[[horasAtencion]]" value="{{value}}">
            </vaadin-combo-box>
        `;
    }

    static get observers() {
        return [
            '_fetchItems(medico, sucursal, fecha)',
        ];
    }

    constructor() {
        super();
        this.query = gql`
            query HorasAtencionMedico($medico: ID!, $sucursal: ID!, $fecha: Date!) {
                medico: empleado(id: $medico) {
                    id
                    horasAtencion(sucursal: $sucursal, fecha: $fecha)
                }
            }
        `;
    }

    _fetchItems(medico, sucursal, fecha) {
        if (!medico || !sucursal || !fecha) return;

        const queryElem = this.shadowRoot.querySelector('apollo-query');
        queryElem.variables = { medico, sucursal, fecha };
        queryElem.subscribe();
    }

    _itemsFetched(e) {
        const { medico } = e.detail.value;
        this.horasAtencion = medico.horasAtencion.map(h => formatISOTime(h));
    }
}

customElements.define('horas-atencion-combo', HorasAtencionCombo);
