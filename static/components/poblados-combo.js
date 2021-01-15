import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import { Debouncer } from '@polymer/polymer/lib/utils/debounce';
import { timeOut } from '@polymer/polymer/lib/utils/async';
import gql from 'graphql-tag';

import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@apollo-elements/polymer/apollo-query';

/**
 * `poblados-combo` Combobox con los poblados.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class PobladosCombo extends PolymerElement {
    static get properties() {
        return {
            name: String,

            label: {
                type: String,
                value: 'Poblados',
            },

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
                observer: '_valueChanged'
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

            <apollo-query query="[[query]]"on-data-changed="_itemsFetched" loading="{{loading}}"></apollo-query>
            <vaadin-combo-box label="[[label]]" required="[[required]]" hidden$="[[hidden]]" item-label-path="nombre" 
                item-value-path="id" value="{{value}}" disabled="[[disabled]]" loading="{{loading}}"
                selected-item="{{selectedItem}}" autofocus="[[autofocus]]" on-filter-changed="_search">
                <template>
                    [[item.nombre]] - [[item.municipio.nombre]]
                </template>
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
            query Poblados($term: String!) {
                poblados(search: $term) {
                    results {
                        id
                        nombre @capitalize
                        municipio {
                            id
                            nombre @capitalize
                        }
                    }
                }
            }
        `;
    }

    _search(e) {
        const term = e.detail.value;
        this._debouncer = Debouncer.debounce(
            this._debouncer,
            timeOut.after(500),
            () => { this._fetch(term); },
        );
    }

    _valueChanged(newValue, oldValue) {
        const items = this.shadowRoot.querySelector('vaadin-combo-box').filteredItems || [];
        if (newValue && items.length == 0) {
            this._fetch(newValue);
        }
    }

    _fetch(term) {
        const queryElem = this.shadowRoot.querySelector('apollo-query');
        if (term) {
            queryElem.variables = { term }
            queryElem.subscribe();
        }
    }

    _itemsFetched(e) {
        const { poblados: { results: poblados} } = e.detail.value;
        const combo = this.shadowRoot.querySelector('vaadin-combo-box');

        combo.filteredItems = poblados;
        if (poblados.length > 0 && this.value && !combo.selectedItem) {
            const _value = this.value;
            combo.value = '';
            combo.value = _value;
        }
    }

    /** Valida el combobox */
    validate() {
        return this.shadowRoot.querySelector('vaadin-combo-box').validate();
    }
}

customElements.define('poblados-combo', PobladosCombo);
