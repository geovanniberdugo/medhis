import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import { ESTADOS_ARRAY } from '../utils';

import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@polymer/paper-toggle-button/paper-toggle-button';
import '@apollo-elements/polymer/apollo-mutation';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/iron-form/iron-form';
import './estado-cita-form';
import './recibo-caja-form';

const ACTUALIZAR_ESTADO_MUTATION = gql`
    mutation ActualizarEstadoCita($cita: EstadoCitaInput!) {
        actualizarEstadoCita(input: $cita) {
            ok
            errors { field, messages }
        }
    }
`;

const ACTUALIZAR_ESTADO_WITH_RECIBO_MUTATION = gql`
    mutation ActualizarEstadoCitaWithRecibo($cita: EstadoCitaInput!, $recibo: ReciboCajaCreateGenericType!) {
        actualizarEstadoCita(input: $cita) {
            ok
            errors { field, messages }
        }
        crearReciboCaja(input: $recibo) {
            ok
            errors { field, messages }
            reciboCaja { id, detalleUrl }
        }
    }
`;

/**
 * `estado-cita-orden` Cambiar el estado de la cita.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class EstadoCitaOrden extends PolymerElement {
    static get properties() {
        return {
            /** Indica si el modal se esta mostrando. */
            opened: {
                type: Boolean,
                value: false,
                reflectToAttribute: true,
            },

            /** Elemento al cual sera attached. */
            positionTarget: {
                type: Element,
            },

            /**
             * Datos de la cita.
             */
            cita: {
                type: Object,
                value: null,
                observer: '_citaChanged',
            },

            /** Indica si se va a crear recibo. */
            conRecibo: {
                type: Boolean,
                computed: '_calcSiRecibo(nuevoEstado, coopago, saldo, ingresarPago)',
            },

            /** Indica si se debe ingresar pago. */
            ingresarPago: {
                type: Boolean,
                value: false,
            },

            /** Indica si se muestra error por valor ingresado. */
            showValorError: {
                type: Boolean,
                value: false,
            },

            /** Id del servicio prestado */
            servicioPrestadoId: String,

            /** Valor del coopago */
            coopago: Number,

            /** Valor del saldo del paciente */
            saldo: Number,

            /** Lo que falta por pagar */
            restantePagar: Number,
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                *[hidden] {
                    display: none;
                }

                .error {
                    color: var(--error-color);
                }
            </style>

            <apollo-mutation mutation="[[mutation]]" loading="{{loading}}" on-data-changed="_estadoGuardado"></apollo-mutation>
            <paper-dialog opened="{{opened}}" position-target="[[positionTarget]]" no-overlap>
                <paper-dialog-scrollable>
                    <iron-form>
                        <form>
                            <estado-cita-form id="estadoCita" estado="{{nuevoEstado}}" required estados="[[estadosDisponibles]]"></estado-cita-form>
                            <paper-toggle-button checked="{{ingresarPago}}" hidden$="[[!_mostrarPagoButton(nuevoEstado, saldo, coopago)]]">Ingresar pago</paper-toggle-button>
                            <div class="error" hidden$="[[!showValorError]]">El valor ingresado es mayor al restante por pagar.</div>
                            <recibo-caja-form id="reciboCaja" hidden$="[[!conRecibo]]"></recibo-caja-form>
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss>cancelar</paper-button>
                    <paper-button on-click="save" disabled="[[loading]]">guardar</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    /**
     * Use for one-time configuration of your component after local
     * DOM is initialized.
     */
    ready() {
        super.ready();
        this._form = this.shadowRoot.querySelector('iron-form');
    }

    /** Observer cita */
    _citaChanged(newValue) {
        if (newValue) {
            const { estadosDisponibles } = newValue;
            this.estadosDisponibles = ESTADOS_ARRAY.filter(e => estadosDisponibles.includes(e.value) && e.value !== 'TE');
        }
    }

    /** Indica si debe ingresar recibo. */
    _calcSiRecibo(estado, coopago, saldo, ingresarPago) {
        const saldoInsuficiente = saldo < coopago;
        const mostrarBotonPago = this._mostrarPagoButton(estado, saldo, coopago);
        return estado === 'CU' && !!coopago && (saldoInsuficiente || (mostrarBotonPago && ingresarPago));
    }

    /** Indica si debe mostrar el boton de agregar pago */
    _mostrarPagoButton(estado, saldo, coopago) {
        return estado === 'CU' && !!coopago && saldo >= coopago;
    }

    /** Valida el recibo de caja. */
    _validateRecibo() {
        const valid = !this.conRecibo || (this.$.reciboCaja.validate() && Number(this.$.reciboCaja.recibo.valor) <= this.restantePagar);
        if (this.conRecibo && this.$.reciboCaja.validate()) {
            this.showValorError = Number(this.$.reciboCaja.recibo.valor) > this.restantePagar;
        }
        return valid;
    }

    /** Actual call to mutation. */
    _executeMutation(cita, recibo) {
        this.mutation = this.conRecibo ? ACTUALIZAR_ESTADO_WITH_RECIBO_MUTATION : ACTUALIZAR_ESTADO_MUTATION;
        const variables = this.conRecibo ? { cita, recibo } : { cita };
        this.shadowRoot.querySelector('apollo-mutation').mutate({
            variables,
            refetchQueries: ['OrdenDetalle'],
        });
    }

    /** Estado guardado. */
    _estadoGuardado(e) {
        if (!e.detail.value) return;

        const { actualizarEstadoCita: estado, crearReciboCaja: recibo } = e.detail.value;
        if (recibo && recibo.ok) {
            window.location = recibo.reciboCaja.detalleUrl;
        }

        if (estado.ok) {
            this.opened = false;
            this.reset();
        }
    }

    /** Resets el formulario. */
    reset() {
        this.servicioPrestadoId = '';
        this.$.estadoCita.reset();
        this.$.reciboCaja.reset();
        this.nuevoEstado = '';
        this.cita = null;
    }

    /** Valida el formulario. */
    validate() {
        return this.$.estadoCita.validate() && this._validateRecibo();
    }

    /** Guarda el estado. */
    save() {
        if (this.validate()) {
            const { estado, motivo, reagendar } = this.$.estadoCita.value;
            const recibo = { 
                ...this.$.reciboCaja.recibo,
                sucursal: this.cita.sucursal.id,
                servicioPrestado: this.servicioPrestadoId,
            };
            const cita = { estado, id: this.cita.id };
            cita.reagendar = reagendar;
            if (motivo) cita.motivo = motivo;
            this._executeMutation(cita, recibo);
        }
    }
}

customElements.define('estado-cita-orden', EstadoCitaOrden);

EstadoCitaOrden.fragment = gql`
    fragment EstadoCitaOrden on Cita {
        id
        estadosDisponibles
    }
`;

export default EstadoCitaOrden;
