import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import { formatMoney, updateFiltersOnUrl, urlQueryToDict } from '../utils';
import tarifaFormInstance from '../components/tarifa-form';

import '@vaadin/vaadin-grid/theme/material/vaadin-grid-filter-column';
import '@vaadin/vaadin-grid/theme/material/vaadin-grid';
import '@polymer/paper-icon-button/paper-icon-button';
import '@apollo-elements/polymer/apollo-mutation';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/paper-card/paper-card';
import '@polymer/paper-fab/paper-fab';
import '../components/instituciones-combo';
import '../components/convenios-combo';
import '../components/clientes-combo';
import '../elements';

const DELETE_TARIFA_MUTATION = gql`
    mutation BorrarTarifa($tarifa: ID!) {
        borrarTarifa(id: $tarifa) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `mh-tarifas` Lista de tarifas.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisTarifas extends PolymerElement {
    static get properties() {
        return {
            /** Id del cliente */
            cliente: String,

            /** Id del convenio */
            convenio: String,

            /** Id de la institucion */
            institucion: String,

            /**
             * Tarifas.
             */
            tarifas: {
                type: Array,
                value: () => [],
            },
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                paper-card {
                    width: 100%;
                }

                paper-fab {
                    position: absolute;
                    right: 30px;
                    bottom: 10px;
                }

                #filtros .card-content {
                    display: grid;
                    grid-gap: 5px;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                }
            </style>

            <apollo-mutation mutation="[[mutation]]"></apollo-mutation>
            <apollo-query query="[[query]]" on-data-changed="_tarifasFetched"></apollo-query>
            <paper-card id="filtros">
                <div class="card-content">
                    <clientes-combo autofocus value="{{cliente}}"></clientes-combo>
                    <convenios-combo query="[[convenioQuery]]" variables="[[_convenioVariables(cliente)]]" value="{{convenio}}">
                    </convenios-combo>
                    <instituciones-combo value="{{institucion}}"></instituciones-combo>
                </div>
            </paper-card>
            <br><br>
            <vaadin-grid id="table" items="[[tarifas]]" on-active-item-changed="edit">
                <vaadin-grid-filter-column header="Servicio" path="servicio.nombre" flex-grow="2"></vaadin-grid-filter-column>
                <vaadin-grid-column header="Valor">
                    <template>[[_formatMoney(item.valor)]]</template>
                </vaadin-grid-column>
                <vaadin-grid-column header="Coopago">
                    <template>[[_formatMoney(item.coopago)]]</template>
                </vaadin-grid-column>
                <vaadin-grid-column header="Iva Coopago">
                    <template>[[_formatMoney(item.ivaCoopago)]]</template>
                </vaadin-grid-column>
                <vaadin-grid-column flex-grow="0">
                    <template>
                        <paper-icon-button icon="my-icons:delete" on-click="delete"></paper-icon-button>
                    </template>
                </vaadin-grid-column>
            </vaadin-grid>
            <paper-fab icon="my-icons:add" elevation="3" on-click="create"></paper-fab>
        `;
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_fetchTarifas(convenio, institucion)',
            '_setQueryParams(cliente, convenio, institucion)',
        ];
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        this.convenioQuery = gql`
            query ConveniosCliente($cliente: ID!) {
                convenios: planes(cliente: $cliente) {
                    results {
                        id
                        nombre @title_case
                    }
                }
            }
        `;
        this.query = gql`
            query Tarifas($institucion: ID!, $convenio: ID!) {
                tarifas(institucion: $institucion, plan: $convenio) {
                    results {
                        id
                        valor
                        coopago
                        ivaCoopago
                        servicio { id, nombre @title_case }
                    }
                }
            }
        `;
    }

    /**
     * Use for one-time configuration of your component after local DOM is
     * initialized.
     */
    ready() {
        super.ready();
        this.allSet = true;
        this._setFiltersFromUrl();
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        const { cliente, convenio, institucion } = urlQueryToDict();
        this.cliente = cliente || this.cliente;
        this.convenio = convenio || this.convenio;
        this.institucion = institucion || this.institucion;
    }

    /**
     * Actualiza la url.
     */
    _setQueryParams(cliente, convenio, institucion) {
        if (!this.allSet) return;

        const filtros = Object.assign(
            {},
            cliente ? { cliente } : {},
            convenio ? { convenio } : {},
            institucion ? { institucion } : {},
        );
        updateFiltersOnUrl(filtros, true);
    }

    /**
     * Gets las variables para el query del convenio.
     * @param {String} cliente Id del cliente.
     */
    _convenioVariables(cliente) {
        return cliente ? { cliente } : null;
    }

    /**
     * Fetches las tarifas.
     * @param {String} convenio Id del convenio.
     * @param {String} institucion Id de la institucion.
     */
    _fetchTarifas(convenio, institucion) {
        if (!convenio || !institucion) {
            this.tarifas = [];
            return;
        }

        const queryElem = this.shadowRoot.querySelector('apollo-query');
        const variables = { convenio, institucion };
        if (!queryElem.refetch(variables)) {
            queryElem.variables = variables;
        }
    }

    /** Set las tarifas */
    _tarifasFetched(e) {
        const { tarifas } = e.detail.value;
        this.tarifas = tarifas.results;
    }

    /** Formato a valores de dinero */
    _formatMoney(value) {
        return formatMoney(value);
    }

    /** Crea una tarifa */
    create() {
        const form = tarifaFormInstance;
        form.id = null;
        form.opened = true;
        form.convenio = this.convenio;
        form.institucion = this.institucion;
    }

    /** Editar una tarifa */
    edit(e) {
        if (e.detail.value) {
            const { id } = e.detail.value;
            const form = tarifaFormInstance;
            this.$.table.activeItem = null;
            form.id = id;
            form.convenio = this.convenio;
            form.institucion = this.institucion;
            form.opened = true;
        }
    }

    /** Borra tarifas. */
    delete(e) {
        const { id } = e.model.item;
        this.mutation = DELETE_TARIFA_MUTATION;
        this.shadowRoot.querySelector('apollo-mutation').mutate({
            variables: { tarifa: id }, refetchQueries: ['Tarifas'],
        });
    }
}

customElements.define('mh-tarifas', MedhisTarifas);
