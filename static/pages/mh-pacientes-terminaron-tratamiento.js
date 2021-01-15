import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import { formatDateToISO } from '../utils';

import '@polymer/paper-toggle-button/paper-toggle-button';
import '@polymer/polymer/lib/elements/dom-repeat';
import '@apollo-elements/polymer/apollo-mutation';
import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-checkbox/paper-checkbox';
import '@polymer/paper-progress/paper-progress';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/polymer/lib/elements/dom-if';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '../components/pacientes-combo';
import '../components/medicos-combo';
import '../elements';

const RECIBIR_AUDITORIA_MUTATION = gql`
    mutation RecibirTratamientoTerminado($tratamiento: RecibirTratamientoTerminadoInput!) {
        recibirTratamientoTerminado(input: $tratamiento) {
            servicioRealizar {
                id
                recibidoPor { id, nombreCompleto }
            }
        }
    }
`;

const VERIFICAR_AUDITORIA_MUTATION = gql`
    mutation VerificarTratamientoTerminado($tratamiento: VerificarTratamientoTerminadoInput!) {
        verificarTratamientoTerminado(input: $tratamiento) {
            servicioRealizar {
                id
                verificadoPor { id, nombreCompleto }
            }
        }
    }
`;

/**
 * `mh-pacientes-terminaron-tratamiento` Auditoria de pacientes que terminaron tratamiento
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisPacientesTerminaronTratamiento extends PolymerElement {
    static get properties() {
        return {
            desde: String,
            hasta: String,

            /**
             * Indica si puede recibir la auditoria.
             */
            canRecibir: {
                type: Boolean,
                value: false,
            },

            /**
             * Indica si puede verificar la auditoria.
             */
            canVerificar: {
                type: Boolean,
                value: false,
            },

            /**
             * Indica si se muestran los auditados.
             */
            auditados: {
                type: Boolean,
                value: false,
            },

            /** Paciente */
            paciente: {
                type: Object,
                value: null,
            },

            /** Medico */
            medico: {
                type: String,
                value: '',
            },

            /**
             * Tratamientos terminados.
             */
            tratamientos: {
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

                h3 {
                    margin-bottom: 0;
                }

                ul {
                    padding: 0;
                }

                li {
                    list-style: none;
                }

                paper-card {
                    width: 100%;
                    margin-bottom: 10px;
                }

                paper-progress {
                    width: 100%;
                    --paper-progress-active-color: var(--app-primary-color);
                }

                #more {
                    text-align: center;
                }

                #filtros {
                    display: grid;
                    grid-gap: 5px;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                }

                .label {
                    color: #616161;
                }

                .info {
                    padding: 10px;
                    display: grid;
                    grid-gap: 10px;
                    grid-template-columns: repeat(auto-fit, minmax(10em, 1fr));
                }
            </style>

            <apollo-mutation mutation="[[mutation]]"></apollo-mutation>
            <apollo-query query="[[query]]" loading="{{loading}}" on-data-changed="_tratamientosFetched"></apollo-query>
            <div id="filtros">
                <paper-toggle-button checked="{{auditados}}">Mostrar auditados</paper-toggle-button>
                <pacientes-combo selected-item="{{paciente}}"></pacientes-combo>
                <medicos-combo value="{{medico}}"></medicos-combo>
                <range-datepicker-input date-from="{{desde}}" date-to="{{hasta}}">
                    <template>
                        <div style="display: grid; grid-gap: 10px; grid-template-columns: 1fr 1fr;">
                            <paper-input label="Desde" value="[[dateFrom]]"></paper-input>
                            <paper-input label="Hasta" value="[[dateTo]]"></paper-input>
                        </div>
                    </template>
                </range-datepicker-input>
            </div>
            <paper-progress indeterminate disabled="[[!loading]]"></paper-progress>
            <ul>
                <template is="dom-repeat" items="[[tratamientos]]" as="tratamiento">
                    <li>
                        <paper-card>
                            <div class="card-content">
                                <h3>[[tratamiento.orden.paciente.nombreCompleto]]</h3>
                                <span>[[tratamiento.orden.paciente.tipoDocumento]] [[tratamiento.orden.paciente.numeroDocumento]]</span>
                                <div class="info">
                                    <div>
                                        [[tratamiento.orden.convenio.nombreCompleto]] <br>
                                        [[tratamiento.servicio.nombre]] <br>
                                        <span class="label">Inicio</span>: [[tratamiento.fechaInicioTratamiento]] <br>
                                        <span class="label">Fin</span>: [[tratamiento.fechaFinTratamiento]]
                                    </div>
                                    <div>
                                        <span class="label">Atendido por</span> <br>
                                        <template is="dom-repeat" items="[[tratamiento.medicos]]" as="medico">
                                            [[medico.nombreCompleto]] <br>
                                        </template>
                                    </div>
                                    <div>
                                        <span class="label">Cantidad</span> <br>
                                        [[tratamiento.cantidad]] en total <br>
                                        [[tratamiento.sesionesAtendidas]] atendidas
                                    </div>
                                    <div>[[tratamiento.estadoLabel]]</div>
                                    <div>
                                        <template is="dom-if" if="[[tratamiento.recibidoPor]]">
                                            <span class="label">Recibido por</span> <br>
                                            [[tratamiento.recibidoPor.nombreCompleto]] <br>
                                        </template>
                                        <template is="dom-if" if="[[!tratamiento.recibidoPor]]">
                                            <paper-checkbox disabled="[[!canRecibir]]" on-change="_recibirTratmiento">Recibido</paper-checkbox>
                                            <br>
                                        </template>
                                        <template is="dom-if" if="[[tratamiento.verificadoPor]]">
                                            <span class="label">Verificado por</span> <br>
                                            [[tratamiento.verificadoPor.nombreCompleto]] <br>
                                        </template>
                                        <template is="dom-if" if="[[!tratamiento.verificadoPor]]">
                                            <paper-checkbox disabled="[[!canVerificar]]" on-change="_verificarTratamiento">Verificado</paper-checkbox>
                                            <br>
                                        </template>
                                    </div>
                                </div>
                            </div>
                        </paper-card>
                    </li>
                </template>
            </ul>
            <div id="more">
                <paper-button hidden$="[[!_hayMas(tratamientos, totalDisponibles)]]" on-click="_getMore">ver más</paper-button>
            </div>
        `;
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        this.loading = false;
        this.query = gql`
            query TratamientosTerminados($posibles: Boolean!, $auditados: Boolean!, $offset: Int, $paciente: String, $medico: ID, $entre: String) {
                tratamientos(tratamientosTerminadosPosiblesAuditar: $posibles, tratamientosTerminadosAuditados: $auditados, documentoPaciente: $paciente, medico: $medico, citasEntre: $entre) {
                    totalCount
                    results(limit: 10, offset: $offset) {
                        id
                        estado
                        cantidad
                        estadoLabel
                        sesionesAtendidas
                        fechaFinTratamiento @date(format: "DD/MM/YYYY")
                        fechaInicioTratamiento @date(format: "DD/MM/YYYY")
                        servicio { id, nombre }
                        medicos { id, nombreCompleto }
                        recibidoPor { id, nombreCompleto }
                        verificadoPor { id, nombreCompleto }
                        orden {
                            id
                            convenio: plan { id, nombreCompleto }
                            paciente { id, nombreCompleto, tipoDocumento, numeroDocumento }
                        }
                    }
                }
            }
        `;
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_fetchTratamientos(auditados, paciente.numeroDocumento, medico, desde, hasta)',
        ];
    }

    /**
     * Returns las variables para el query.
     * @param {Boolean} mostrarAuditados
     */
    _qlVariables(mostrarAuditados, paciente, medico, desde, hasta) {
        const entre = desde && hasta ? `${formatDateToISO(desde)},${formatDateToISO(hasta)}` : '';
        return { 
            ...(entre && { entre }),
            ...(medico && { medico }),
            posibles: !mostrarAuditados,
            auditados: mostrarAuditados,
            ...(paciente && { paciente }),
        };
    }

    /**
     * Gets los tratamientos
     * @param {Boolean} auditados
     */
    _fetchTratamientos(mostrarAuditados, paciente, medico, desde, hasta) {
        this._queryElem = this.shadowRoot.querySelector('apollo-query');
        this._queryElem.variables = this._qlVariables(mostrarAuditados, paciente, medico, desde, hasta);
        this._queryElem.subscribe();
    }

    /** Sets tratamientos */
    _tratamientosFetched(e) {
        const { tratamientos } = e.detail.value;
        this.tratamientos = tratamientos.results;
        this.totalDisponibles = tratamientos.totalCount;
    }

    /**
     * Indica si hay mas tratamientos para cargar.
     * @param {Array} tratamientos Lista de tratamientos.
     * @param {Number} total Total de tratamientos.
     */
    _hayMas(tratamientos, total) {
        return tratamientos.length > 0 && tratamientos.length < total;
    }

    /**
     * Obtiene mas tratamientos.
     */
    _getMore() {
        const { auditados: mostrarAuditados, paciente, medico, desde, hasta } = this;
        const _paciente = paciente ? paciente.numeroDocumento : null;
        const _medico = medico ? medico : null;
        this._queryElem.fetchMore({
            variables: { ...this._qlVariables(mostrarAuditados, _paciente, _medico, desde, hasta), offset: this.tratamientos.length },
            updateQuery: (prev, { fetchMoreResult }) => {
                if (!fetchMoreResult) return prev;
                return Object.assign({}, prev, {
                    tratamientos: {
                        totalCount: prev.tratamientos.totalCount,
                        results: [...prev.tratamientos.results, ...fetchMoreResult.tratamientos.results],
                        __typename: prev.tratamientos.__typename,
                    },
                });
            },
        });
    }

    /**
     * Auditar tratamiento.
     * @param {String} tratamiento Id del tratamiento.
     * @param {Boolean} verificar Indica si se va a verificar o recibir.
     */
    _auditar(tratamiento, verificar) {
        this.mutation = verificar ? VERIFICAR_AUDITORIA_MUTATION : RECIBIR_AUDITORIA_MUTATION;
        this.shadowRoot.querySelector('apollo-mutation').mutate({ variables: { tratamiento: { id: tratamiento } } });
    }

    /** Recibe el tratamiento */
    _recibirTratmiento(e) {
        if (e.target.checked) {
            this._auditar(e.model.tratamiento.id, false);
            e.target.checked = false;
        }
    }

    /** Verifica el tratamiento */
    _verificarTratamiento(e) {
        if (e.target.checked) {
            this._auditar(e.model.tratamiento.id, true);
            e.target.checked = false;
        }
    }
}

customElements.define('mh-pacientes-terminaron-tratamiento', MedhisPacientesTerminaronTratamiento);
