import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import { formatMoney, formatISODate, formatISOTime, ESTADOS, notifyErrorMessage } from '../utils';

import EditarTratamiento from './editar-tratamiento';
import EstadoCitaOrden from './estado-cita-orden';
import '@polymer/paper-toggle-button/paper-toggle-button';
import 'paper-money-input-ench/paper-money-input-ench';
import '@polymer/paper-icon-button/paper-icon-button';
import '@apollo-elements/polymer/apollo-mutation';
import '@polymer/polymer/lib/elements/dom-repeat';
import '@polymer/paper-checkbox/paper-checkbox';
import '@polymer/polymer/lib/elements/dom-if';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import './editar-tratamiento';
import './autorizacion-cita';
import './mover-cita-orden';
import './servicios-combo';

const UPDATE_TRATAMIENTO_MUTATION = gql`
    mutation ActualizarTratamiento($tratamiento: EditarTratamientoInput!) {
        editarTratamiento(input: $tratamiento) {
            ok
            errors { field, messages }
        }
    }
`;

const VERIFICAR_INICIO_TRATAMIENTO_MUTATION = gql`
    mutation VerificarInicioTratamiento($tratamiento: VerificarInicioTratamientoInput!) {
        verificarInicioTratamiento(input: $tratamiento) {
            tratamiento: servicioRealizar {
                id
                verificadoInicioPor { id, nombreCompleto @title_case }
            }
        }
    }
`;

const REAGENDAR_CITAS_MUTATION = gql`
    mutation ReagendarCitas($tratamiento: ReagendarCitasInput!) {
        reagendarCitas(input: $tratamiento) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `servicios-orden` Lista servicios/tratamientos de una orden.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class ServiciosOrden extends PolymerElement {
    static get properties() {
        return {
            /** Id del convenio. */
            convenio: String,
            
            /** Id de la institución. */
            institucion: String,

            /**
             * Tratamientos de la orden.
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

                paper-card {
                    width: 100%;
                    margin-bottom: 10px;
                }
                
                paper-icon-button {
                    float: right;
                    color: var(--app-primary-color);
                }

                .label {
                    color: #616161;
                }

                .card-content h3 {
                    margin-bottom: 0;
                }

                .card-content .inicio {
                    margin: 0;
                }

                .citas-link {
                    display: flex;
                }

                .citas-link a {
                    text-decoration: none;
                    color: var(--app-primary-color);
                }

                .servicio-info {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(9.4rem, 1fr));
                }

                .saldo-sesion {
                    align-self: center;
                    justify-self: center;
                }

                .saldo-sesion > div {
                    color: white;
                    padding: 1em;
                    font-weight: bold;
                    text-align: center;
                    text-transform: uppercase;
                    background-color: var(--servicio-orden-estado-saldo, #ffc107);
                }

                .saldo-sesion > div.debt {
                    --servicio-orden-estado-saldo: #dd2c00;
                }

                .saldo-sesion > div.favor {
                    --servicio-orden-estado-saldo: #0f9d58;
                }

                .cita-info {
                    display: grid;
                    padding: 0 15px;
                    grid-template-columns: repeat(auto-fit, minmax(9.4rem, 1fr));
                    border-bottom: 0.5px solid lightgrey;
                }

                .cita-info p, .cita-info .estado-cita {
                    cursor: pointer;
                }

                .estado-cita {
                    text-align: center;
                    align-self: center;
                    justify-self: center;
                    text-transform: uppercase;
                }

                .circle {
                    height: 1.5em;
                    width: 1.5em;
                    border-radius: 50%;
                    display: inline-block;
                }

                .verificacion-inicio {
                    align-self: center;
                    justify-self: center;
                }       

                div[hidden] {
                    display: none;
                }
            </style>
            <apollo-mutation mutation="[[mutation]]" on-error-changed="_errorMutation"></apollo-mutation>
            <template is="dom-repeat" items="[[tratamientos]]" as="tratamiento">
                <paper-card>
                    <div class="card-content">
                        <paper-icon-button hidden$="[[!tratamiento.canEdit]]" icon="my-icons:edit" on-click="_editServicio"></paper-icon-button>
                        <a href="[[tratamiento.controlCitasUrl]]"><paper-icon-button alt="Control de citas" icon="my-icons:print"></paper-icon-button></a>
                        <h3>[[tratamiento.servicio.nombre]]</h3>
                        <p class="inicio"><b class="label">Inicio: [[_formatDate(tratamiento.fechaInicioTratamiento)]]</b></p>
                        <div class="servicio-info">
                            <p>
                                <b class="label">Cantidad:</b> [[tratamiento.cantidad]] <br>
                                <b class="label">Atendidas:</b> [[tratamiento.sesionesAtendidas]] <br>
                                <b class="label">Faltantes:</b> [[tratamiento.sesionesFaltantes]]<br>
                            </p>
                            <p>
                                <b class="label">Valor sesión:</b> [[_formatMoney(tratamiento.valor)]] <br>
                                <b class="label">Valor total:</b> [[_formatMoney(tratamiento.valorTotal)]] <br>
                                <b class="label">Coopago:</b> [[_formatMoney(tratamiento.coopago)]] <br>
                            </p>
                            <p>
                                <b class="label">Valor a pagar:</b> [[_formatMoney(tratamiento.coopagoTotal)]] <br>
                                <b class="label">Valor pagado:</b> [[_formatMoney(tratamiento.totalPagado)]] <br>
                                <b class="label">Saldo actual:</b> [[_formatMoney(tratamiento.saldoPaciente)]] <br>
                            </p>
                            <div class="saldo-sesion" hidden$="[[_sinSaldo(tratamiento.saldoSesiones)]]">
                                <div class$="[[_estadoSaldoSesionesClass(tratamiento.saldoSesiones)]]">
                                    [[_estadoSaldoSesiones(tratamiento.saldoSesiones)]] <br>
                                    [[_formatMoney(tratamiento.saldoSesiones)]]
                                </div>
                            </div>
                            <div class="verificacion-inicio" hidden$="[[!tratamiento.canVerificarOrdenInicioTratamiento]]">
                                <template is="dom-if" if="[[tratamiento.verificadoInicioPor]]">
                                    <span class="label">Verificado por</span> <br>
                                    [[tratamiento.verificadoInicioPor.nombreCompleto]] <br>
                                </template>
                                <template is="dom-if" if="[[!tratamiento.verificadoInicioPor]]">
                                    <paper-checkbox on-change="verificarInicioTratamiento">Verificar</paper-checkbox>
                                </template>
                            </div>
                        </div>
                        <p class="citas-link">
                            <a href="#" hidden$="[[!tratamiento.canReagendarCitas]]" on-click="reagendarCitas">Reagendar citas</a>
                            <span style="flex: 1"></span>
                            <a href="#" on-click="_showCitas">Ver citas</a>
                        </p>
                        <iron-collapse>
                            <hr>
                            <h4>Citas</h4>
                            <template is="dom-repeat" items="[[tratamiento.citas]]" as="cita">
                                <div class="cita-info">
                                    <p on-click="_showMoverCita">
                                        [[_formatHora(cita.inicio)]] <br>
                                        [[_formatDate(cita.inicio)]] <br>
                                        [[cita.medico.nombreCompleto]] - [[cita.sucursal.nombre]]
                                    </p>
                                    <p on-click="_showAddAutorizacion">
                                        <b class="label">Autorización</b> <br>
                                        <template is="dom-if" if="[[cita.autorizacion]]">
                                        [[cita.autorizacion]] <br>
                                        [[cita.fechaAutorizacion]] <br>
                                        [[cita.autorizadoPor]]
                                        </template>
                                        <template is="dom-if" if="[[!cita.autorizacion]]">
                                        No tiene número de autorización ingresado.
                                        </template>
                                    </p>
                                    <div class="estado-cita" on-click="_showCambiarEstado">
                                        <span class="circle" style$="background-color: [[_colorEstadoCita(cita.historialActual.estado)]]"></span> <br>
                                        <b class="label">[[cita.historialActual.estadoLabel]]</b>
                                    </div>
                                </div>
                            </template>
                        </iron-collapse>
                    </div>
                </paper-card>
            </template>

            <mover-cita-orden id="moverCita" institucion="[[institucion]]"></mover-cita-orden>
            <autorizacion-cita id="autorizacionCita"></autorizacion-cita>
            <estado-cita-orden id="estadoCita"></estado-cita-orden>
        `;
    }

    /** Formatea valores de dinero. */
    _formatMoney(value) {
        return formatMoney(value);
    }

    /** Formatea. */
    _formatDate(value) {
        return formatISODate(value);
    }

    /** Formatea */
    _formatHora(value) {
        return formatISOTime(value);
    }

    /**
     * Indica si el paciente se encuentra al dia.
     * @param {number} saldo
     */
    _sinSaldo(saldo) {
        return saldo === 0;
    }

    /** Indica si el paciente esta en deuda, al día o con saldo a favor. */
    _estadoSaldoSesiones(valor) {
        if (valor < 0) return 'deuda';
        if (valor > 0) return 'saldo a favor';
        return 'al día';
    }

    /** Indica el color a mostrar dependido del estado del saldo del paciente. */
    _estadoSaldoSesionesClass(valor) {
        if (valor < 0) return 'debt';
        if (valor > 0) return 'favor';
        return '';
    }

    /** Indica el color del estado de la cita. */
    _colorEstadoCita(estadoActual) {
        const actual = ESTADOS[estadoActual];
        return actual ? actual.color : '';
    }

    /** Muestra las citas asociadas al tratamiento. */
    _showCitas(e) {
        const collapseElement = e.currentTarget.closest('paper-card').querySelector('iron-collapse');
        collapseElement.toggle();
        e.currentTarget.innerText = collapseElement.opened ? 'Ocultar citas' : 'Ver citas';
    }

    /** Muestra el formulario para mover una cita de horario */
    _showMoverCita(e) {
        const { cita } = e.model;
        if (cita.canMove) {
            const element = this.$.moverCita;
            element.positionTarget = e.currentTarget;
            element.cita = cita;
            element.opened = true;
        }
    }

    /** Muestra el formulario para agregar autorizacion a cita. */
    _showAddAutorizacion(e) {
        const { cita } = e.model;
        if (cita.canEdit) {
            const element = this.$.autorizacionCita;
            element.positionTarget = e.currentTarget;
            element.cita = cita;
            element.opened = true;
        }
    }

    /** Muestra el formulario para cambiar el estado de la cita. */
    _showCambiarEstado(e) {
        const { cita } = e.model;
        const { tratamiento } = e.model.parentModel;
        const element = this.$.estadoCita;
        element.reset();
        element.positionTarget = e.currentTarget;
        element.opened = true;
        element.cita = cita;
        element.coopago = tratamiento.coopago;
        element.saldo = tratamiento.saldoSesiones;
        element.servicioPrestadoId = tratamiento.id;
        element.restantePagar = tratamiento.saldoPaciente;
    }

    /** Muestra formulario para edición del servicio seleccionado. */
    _editServicio(e) {
        e.stopPropagation();
        this.dispatchEvent(new CustomEvent('show-editar-tratamiento-form', {
            bubbles: true,
            composed: true,
            detail: { tratamiento: e.model.tratamiento, convenioId: this.convenio, institucionId: this.institucion },
        }));
    }

    /** Verifica que los datos del tratamiento sean correctos. */
    verificarInicioTratamiento(e) {
        e.stopPropagation();
        if (e.target.checked) {
            const tratamiento = { id: e.model.tratamiento.id };
            this.mutation = VERIFICAR_INICIO_TRATAMIENTO_MUTATION;
            this.shadowRoot.querySelector('apollo-mutation').mutate({variables: { tratamiento }});
        }
    }

    /** Reagendar citas */
    reagendarCitas(e) {
        e.stopPropagation();
        const tratamiento = { id: e.model.tratamiento.id };
        this.mutation = REAGENDAR_CITAS_MUTATION;
        this.shadowRoot.querySelector('apollo-mutation').mutate({
            variables: { tratamiento },
            refetchQueries: ['OrdenDetalle'],
        });
    }

    _errorMutation({ detail }) {
        if (!detail.value) return;

        const msg = detail.value.graphQLErrors.map(e => e.message).join('.');
        notifyErrorMessage(this, msg);
    }
}

customElements.define('servicios-orden', ServiciosOrden);

ServiciosOrden.fragment = gql`
    fragment ServiciosOrden on ServicioRealizar {
        id
        valor
        coopago
        canEdit
        cantidad
        isUnaCita
        valorTotal
        totalPagado
        coopagoTotal
        canEditValor
        saldoPaciente
        saldoSesiones
        isCoopagoTotal
        controlCitasUrl
        sesionesAtendidas
        sesionesFaltantes
        canReagendarCitas
        ...EditarTratamiento
        fechaInicioTratamiento
        servicio { id, nombre }
        canVerificarOrdenInicioTratamiento
        verificadoInicioPor { id, nombreCompleto @title_case }
        citas {
            id
            inicio
            canEdit
            canMove
            autorizacion
            autorizadoPor
            fechaAutorizacion
            ...EstadoCitaOrden
            sucursal { id, nombre @title_case }
            medico { id, nombreCompleto @title_case }
            historialActual { id, estado, estadoLabel }
        }
    }
    ${EstadoCitaOrden.fragment}
    ${EditarTratamiento.fragment}
`;

export default ServiciosOrden;
