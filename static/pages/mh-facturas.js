import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import { formatISODate, formatMoney, updateFiltersOnUrl, urlQueryToDict } from '../utils';

import '@polymer/paper-icon-button/paper-icon-button';
import FacturaItem from '../components/factura-item';
import '@polymer/polymer/lib/elements/dom-repeat';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/paper-button/paper-button';
import '../components/instituciones-combo';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '../components/pacientes-combo';
import '@polymer/paper-fab/paper-fab';
import '../components/clientes-combo';
import '../components/nueva-factura';
import '../elements';

/**
 * `mh-facturas` Lista las facturas
 *
 * @customElement
 * @polymer
 * @demo
 */
class MedhisFacturas extends PolymerElement {
    static get properties() {
        return {
            /**
             * Cliente
             */
            cliente: {
                type: Object,
                value: () => ({}),
            },

            /**
             * Institucion
             */
            institucion: {
                type: Object,
                value: () => ({}),
            },

            /**
             * Paciente
             */
            paciente: {
                type: Object,
                value: () => ({}),
            },

            /** Numero de la factura */
            numero: {
                type: Number,
            },

            /**
             * Facturas.
             */
            facturas: {
                type: Array,
                value: () => [],
            },

            /**
             * Indica si la factura de ser a nombre del paciente.
             */
            _facturarPaciente: {
                type: Boolean,
                computed: '_debeFacturarPaciente(cliente.facturaPaciente)',
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

                ul {
                    padding: 0px;
                }

                paper-fab {
                    position: fixed;
                    bottom: 10px;
                    right: 10px;
                }

                paper-progress {
                    width: 100%;
                    --paper-progress-active-color: var(--app-primary-color);
                }

                #filtros .card-content {
                    display: grid;
                    grid-gap: 5px;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                }

                #filtros h2 {
                    align-self: end;
                    justify-self: center;
                }

                #more {
                    text-align: center;
                }
            </style>
            <apollo-query query="[[query]]" on-data-changed="_facturasFetched"></apollo-query>
            <paper-card id="filtros">
                <div class="card-content">
                    <instituciones-combo autofocus on-selected-item-changed="_changeInstitucion"></instituciones-combo>
                    <clientes-combo on-selected-item-changed="_changeCliente"></clientes-combo>
                    <pacientes-combo required="[[_facturarPaciente]]" hidden="[[!_facturarPaciente]]"
                        on-selected-item-changed="_changePaciente">
                    </pacientes-combo>
                    <h2>ó</h2>
                    <paper-input label="Número factura" type="number" on-blur="_changeNumero"></paper-input>
                </div>
            </paper-card>
            <ul>
                <template is="dom-repeat" items="[[facturas]]" as="factura">
                    <factura-item factura="[[factura]]"></factura-item>
                </template>
            </ul>
            <div id="more"><paper-button hidden$="[[!_hayMasFacturas(facturas, totalDisponibles)]]" on-click="_getMore">ver más</paper-button></div>
            <paper-fab disabled="[[!_canAddFactura(institucion.id, cliente.id, cliente.facturaPaciente, paciente.id)]]" icon="my-icons:add" on-click="_newFactura"></paper-fab>
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
            query Facturas($institucion: ID, $cliente: ID, $paciente: ID, $numero: Int, $offset: Int) {
                facturas(institucion: $institucion, cliente: $cliente, paciente: $paciente, numero: $numero) {
                    totalCount
                    results(ordering: "-numero", limit: 10, offset: $offset) {
                        id
                        ...FacturaItem
                    }
                }
            }
            ${FacturaItem.fragment}
        `;
    }

    /**
     * Use for one-time configuration of your component after local DOM is
     * initialized.
     */
    ready() {
        super.ready();
        this.allSet = true;
        this._facturarPaciente = false;
        this._queryElem = this.shadowRoot.querySelector('apollo-query');
        this._setFiltersFromUrl();
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_fetchFacturas(institucion.id, cliente.id, cliente.facturaPaciente, paciente.id, numero)',
            '_setQueryParams(cliente.id, institucion.id, numero)',
        ];
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        const institucionesCombo = this.shadowRoot.querySelector('instituciones-combo');
        const numeroInput = this.shadowRoot.querySelector('#filtros paper-input');
        const clientesCombo = this.shadowRoot.querySelector('clientes-combo');
        const { cliente, institucion, numero } = urlQueryToDict();

        this.numero = numero;
        numeroInput.value = numero || this.numero;
        clientesCombo.value = cliente || this.cliente.id;
        institucionesCombo.value = institucion || this.institucion.id;
    }

    /**
     * Actualiza la url.
     */
    _setQueryParams(cliente, institucion, numero) {
        if (!this.allSet) return;

        const filtros = numero ? { numero } : {
            ...(cliente && { cliente }),
            ...(institucion && { institucion }),
        }
        updateFiltersOnUrl(filtros, true);
    }

    /** Actualiza la institucion */
    _changeInstitucion(e) {
        this.institucion = { ...e.detail.value };
        if (this.institucion.id) {
            this._resetNumero();
        }
    }

    /** Actualiza el cliente */
    _changeCliente(e) {
        this.cliente = { ...e.detail.value };
        if (this.cliente.id) {
            this._resetNumero();
            if (!this.cliente.facturaPaciente) {
                this.shadowRoot.querySelector('pacientes-combo').value = '';
            }
        }
    }

    /** Actualiza el paciente */
    _changePaciente(e) {
        this.paciente = { ...e.detail.value };
    }

    _resetNumero() {
        this.numero = '';
        this.shadowRoot.querySelector('#filtros paper-input').value = '';
    }

    /** Actualiza el numero de la factura */
    _changeNumero(e) {
        this.numero = e.target.value;
        if (this.numero) {
            [...this.shadowRoot.querySelectorAll('instituciones-combo, clientes-combo, pacientes-combo')].map(
                e => e.value = ''
            );
        }
    }

    /**
     * Returns las variables para el query.
     * @param {String} institucion Id de la institucion
     * @param {String} cliente Id del cliente
     * @param {Boolean} conPaciente Si factura paciente
     * @param {String} paciente Id del paciente
     */
    _qlVariables(institucion, cliente, conPaciente, paciente, numero) {
        if (numero) return { numero };

        return { 
            cliente,
            institucion,
            ...(conPaciente && { paciente }),
        };
    }

    /**
     * Gets las facturas
     * @param {String} institucion Id de la institucion
     * @param {String} cliente Id del cliente
     * @param {Boolean} conPaciente Indica si se deben filtrar facturas por paciente
     * @param {String} paciente Id del paciente
     */
    _fetchFacturas(institucion, cliente, conPaciente, paciente, numero) {
        const noFetch = numero ? false : conPaciente ? !institucion || !cliente || !paciente : !institucion || !cliente;
        if (noFetch) {
            this.facturas = [];
            return;
        }

        this._queryElem.variables = this._qlVariables(institucion, cliente, conPaciente, paciente, numero);
        this._queryElem.subscribe();
    }

    /** Sets facturas */
    _facturasFetched(e) {
        const { facturas } = e.detail.value;
        this.facturas = facturas.results;
        this.totalDisponibles = facturas.totalCount;
    }

    /**
     * Obtiene mas facturas.
     */
    _getMore() {
        const { institucion, cliente, paciente, numero } = this;
        this._queryElem.fetchMore({
            variables: { ...this._qlVariables(institucion.id, cliente.id, cliente.facturaPaciente, paciente.id, numero), offset: this.facturas.length },
            updateQuery: (prev, { fetchMoreResult }) => {
                if (!fetchMoreResult) return prev;
                return Object.assign({}, prev, {
                    facturas: {
                        totalCount: prev.totalCount,
                        results: [...prev.facturas.results, ...fetchMoreResult.facturas.results],
                        __typename: prev.facturas.__typename,
                    },
                });
            },
        });
    }

    /**
     * Muestra el formulario para crear nueva factura.
     */
    _newFactura({ target }) {
        this.dispatchEvent(new CustomEvent('show-nueva-factura', {
            bubbles: true,
            composed: true,
            detail: {
                cliente: this.cliente,
                paciente: this.paciente,
                institucion: this.institucion,
            }
        }));
    }

    /**
     * Indica si hay mas facturas para cargar.
     * @param {Array} facturas Lista de facturas.
     * @param {Number} total Total de facturas.
     */
    _hayMasFacturas(facturas, total) {
        return facturas.length > 0 && facturas.length < total;
    }

    /**
     * Indica si se puede crear facturas.
     * @param {String} institucion Id de la institucion.
     * @param {String} cliente Id del cliente
     * @param {Boolean} conPaciente Si se debe usar paciente en la factura
     * @param {String} paciente Id del paciente
     */
    _canAddFactura(institucion, cliente, conPaciente, paciente) {
        return conPaciente ? institucion && cliente && paciente : institucion && cliente;
    }

    /**
     * Formatea la fecha dd/mm/yyyy
     * @param {Date} fecha
     */
    _formatFecha(fecha) {
        return formatISODate(fecha);
    }

    /**
     * Formatea valores númericos a dinero.
     * @param {String|Number} value Valor a formatear.
     */
    _formatMoney(value) {
        return formatMoney(value);
    }

    /**
     * Indica si se debe facturar a nombre del paciente.
     * @param {Boolena} facturar
     */
    _debeFacturarPaciente(facturar) {
        return !!facturar;
    }
}

customElements.define('mh-facturas', MedhisFacturas);
