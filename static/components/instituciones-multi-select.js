import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import 'multiselect-combo-box/theme/material/multiselect-combo-box';

/**
 * `instituciones-multi-select` Description
 *
 * @customElement
 * @demo
 * 
 */
class InstitucionesMultiSelect extends ApolloQuery {
    static get properties() {
        return {
            name: { type: String },
            hidden: { type: Boolean },
            required: { type: Boolean },
            autofocus: { type: Boolean },
            selectedItems: { type: Array },
            _instituciones: { type: Array },
        }
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            multiselect-combo-box {
                width: 100%;
            }
        `;
    }

    render() {
        const { required, hidden, autofocus, selectedItems, instituciones } = this;

        return html`
            <multiselect-combo-box label="Instituciones" ?required="${required}" ?hidden="${hidden}"
                ?autofocus="${autofocus}" .selectedItems="${selectedItems}" .items="${instituciones}"
                item-id-path="id" item-value-path="id" item-label-path="nombre"
                @selected-items-changed="${({ detail }) => this.selectedItems = detail.value}">
            </multiselect-combo-box>
        `;
    }

    constructor() {
        super();
        this.selectedItems = [];
        this.instituciones = [];
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

    get data() {
        return this._data;
    }

    set data(value) {
        this._data = value;
        this.instituciones = value.instituciones.results || [];
    }

    get value() {
        return this.selectedItems.map(item => item.id);
    }

    set value(value) {
        this._selectedItemsTemp = this.instituciones.length === 0 ? value : null;
        this.selectedItems = this.instituciones.filter(institucion => value.includes(institucion.id))
    }

    get instituciones() {
        return this._instituciones;
    }

    set instituciones(value) {
        this._instituciones = value;
        if (this._selectedItemsTemp) this.value = this._selectedItemsTemp;
    }

    validate() {
        return this.shadowRoot.querySelector('multiselect-combo-box').validate();
    }
}

customElements.define('instituciones-multi-select', InstitucionesMultiSelect);
