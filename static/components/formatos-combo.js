import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `formatos-combo` Combobox para los tipos de documento.
 *
 */
class FormatosCombo extends PolymerElement {
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

            <vaadin-combo-box label="Formato" required="[[required]]" hidden$="[[hidden]]" disabled="[[disabled]]"
                item-label-path="nombre" item-value-path="id" items="[[data.formatos.results]]"
                value="{{value}}" selected-item="{{selectedItem}}" autofocus="[[autofocus]]"
                on-change="_changed">
            </vaadin-combo-box>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query Formatos {
                formatos {
                    results(ordering: "nombre") {
                        id
                        nombre @capitalize
                    }
                }
            }
        `;
    }

    _changed() {
        this.dispatchEvent(new CustomEvent('change', { detail: null }));
    }

    /** Valida el combobox */
    validate() {
        return this.shadowRoot.querySelector('vaadin-combo-box').validate();
    }
}

customElements.define('formatos-combo', FormatosCombo);
