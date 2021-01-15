import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';

/**
 * `duracion-combo` Combobox con las duraciones.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class DuracionCombo extends PolymerElement {
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

            items: {
                type: Array,
                value: () => ([
                    {label: '10 Minutos', value: '00:10:00'},
                    {label: '15 Minutos', value: '00:15:00'},
                    {label: '20 Minutos', value: '00:20:00'},
                    {label: '25 Minutos', value: '00:25:00'},
                    {label: '30 Minutos', value: '00:30:00'},
                    {label: '35 Minutos', value: '00:35:00'},
                    {label: '40 Minutos', value: '00:40:00'},
                    {label: '45 Minutos', value: '00:45:00'},
                    {label: '50 Minutos', value: '00:50:00'},
                    {label: '1 Hora', value: '01:00:00'},
                ]),
            },
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

            <vaadin-combo-box label="Duración" required="[[required]]" hidden$="[[hidden]]" autofocus="[[autofocus]]"
                items="[[items]]" value="{{value}}" selected-item="{{selectedItem}}" on-change="_changed">
            </vaadin-combo-box>
        `;
    }

    /** Propagates event. */
    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }
}

customElements.define('duracion-combo', DuracionCombo);
