import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-grid/theme/material/vaadin-grid-filter-column';
import '@vaadin/vaadin-grid/theme/material/vaadin-grid';
import { progressCss } from '../components/common-css';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-fab/paper-fab';
import '@polymer/iron-icon/iron-icon';
import '../components/medico-form';
import '../elements';

/**
 * `mh-medicos` Lista, edita y crea medicos.
 *
 * @customElement
 * @demo
 * 
 */
class MedhisMedicos extends ApolloQuery {
    static get properties() {
        return {
            medicos: { type: Array },
        }
    }

    static get styles() {
        const base = css`
            :host {
                display: block;
            }

            paper-fab {
                position: absolute;
                right: 30px;
                bottom: 10px;
            }
        `;

        return [progressCss, base];
    }

    render() {
        const { loading, data } = this;
        const medicos = data.medicos.results || [];

        return html`
            <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
            <vaadin-grid .items=${medicos} @active-item-changed="${this._editar}">
                <vaadin-grid-filter-column header="Nombre" path="nombreCompleto"></vaadin-grid-filter-column>
                <vaadin-grid-filter-column header="Identificación" path="cedula"></vaadin-grid-filter-column>
                <vaadin-grid-column header="Registro medico" path="registroMedico"></vaadin-grid-column>
                <vaadin-grid-column header="Activo"></vaadin-grid-column>
            </vaadin-grid>
            <paper-fab icon="my-icons:add" elevation="3" @click="${this._crear}"></paper-fab>
        `;
    }

    constructor() {
        super();
        this.notifyOnNetworkStatusChange = true;
        this.query = gql`
            query TodosMedicos {
                medicos: empleados(medicos: true) {
                    results(ordering: "nombres") {
                        id
                        activo
                        cedula
                        registroMedico
                        nombreCompleto @title_case
                    }
                }
            }
        `;
    }

    // Lifecycles
    firstUpdated() {
        const columns = this.shadowRoot.querySelectorAll('vaadin-grid-column');

        columns[1].renderer = (root, column, rowData) => {
            root.innerHTML = `<iron-icon icon="my-icons:${this._estadoIcon(rowData.item.activo)}"></iron-icon>`;
        };
    }

    _estadoIcon(estado) {
        return estado ? 'done' : 'clear';
    }

    _crear() {
        this._showForm();
    }

    _editar({ target, detail }) {
        if (detail.value)  this._showForm(detail.value.id);
        target.activeItem = null;
    }

    _showForm(id = '') {
        this.dispatchEvent(new CustomEvent('show-medico-form', {
            bubbles: true,
            composed: true,
            detail: id ? { medicoId: id } : null,
        }));
    }
}

customElements.define('mh-medicos', MedhisMedicos);
