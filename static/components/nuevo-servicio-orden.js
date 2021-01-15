import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import { DateTime } from 'luxon';
import gql from 'graphql-tag';

import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker';
import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import 'paper-money-input-ench/paper-money-input-ench';
import '@apollo-elements/polymer/apollo-mutation';
import '@polymer/paper-checkbox/paper-checkbox';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-input/paper-input';
import '@polymer/iron-form/iron-form';
import './horas-atencion-combo';
import './sucursales-combo';
import './servicios-combo';
import './es-date-picker';
import './duracion-combo';
import './medicos-combo';

const AGREGAR_SERVICIO_MUTATION = gql`
    mutation agregarServicioOrden($servicio: AddServicioOrdenInput!){
        agregarServicioOrden(input: $servicio) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `nuevo-servicio-orden` Formulario para agregar nuevo servicio a la orden.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class NuevoServicioOrden extends PolymerElement {
    static get properties() {
        return {
            /** Indica si se debe mostrar el modal. */
            opened: {
                type: Boolean,
                value: false,
            },

            /** Datos de la orden. */
            orden: {
                type: Object,
                value: () => ({}),
            },

            /**
             * Datos del formulario.
             */
            formData: {
                type: Object,
                value: () => ({}),
            },
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                paper-dialog {
                    width: 80%;
                }

                vaadin-date-picker {
                    width: 100%;
                }

                form {
                    display: grid;
                    grid-template-columns: 1fr;
                }

                .disponibilidad {
                    color: var(--error-color);
                }

                @media (min-width: 1024px) {
                    paper-dialog {
                        width: 60%;
                    }

                    form {
                        display: grid;
                        grid-gap: 10px;
                        grid-template-columns: repeat(6, 1fr);
                    }

                    .full {
                        grid-column: 1 / -1;
                    }

                    .half {
                        grid-column: span 3;
                    }

                    .third {
                        grid-column: span 2;
                    }
                }
            </style>

            <apollo-mutation mutation="[[mutation]]" loading="{{loading}}" on-data-changed="_servicioAgregado"></apollo-mutation>
            <paper-dialog modal opened="{{opened}}">
                <h2>Nuevo Servicio</h2>
                <paper-dialog-scrollable>
                    <iron-form id="form">
                        <form>
                            <servicios-combo name="servicio" class="full" autofocus required with-tarifas
                                convenio="[[orden.convenio.id]]" institucion="[[orden.institucion.id]]"
                                on-change="_servicioChanged" value="{{formData.servicio}}">
                            </servicios-combo>
                            <sucursales-combo name="sucursal" class="half" required value="{{formData.sucursal}}"></sucursales-combo>
                            <medicos-combo name="medico" class="half" required activos sucursal="[[formData.sucursal]]"
                                selected-item="{{medicoItem}}" value="{{formData.medico}}"></medicos-combo>
                            <es-date-picker class="third">
                                <vaadin-date-picker name="fecha" label="Fecha" required value="{{formData.fecha}}"></vaadin-date-picker>
                            </es-date-picker>
                            <horas-atencion-combo name$="hora" class="third" sucursal="[[formData.sucursal]]" required
                                fecha="[[formData.fecha]]" medico="[[formData.medico]]"
                                value="{{formData.hora}}">
                            </horas-atencion-combo>
                            <duracion-combo label="Duración cita" required class="third" name="duracion" value="{{formData.duracion}}"></duracion-combo>
                            <paper-input name="autorizacion" label="Autorización" class="half" value="{{formData.autorizacion}}"
                                hidden$=[[!orden.convenio.requiereAutorizacion]]>
                            </paper-input>
                            <es-date-picker class="half" hidden$=[[!orden.convenio.requiereAutorizacion]]>
                                <vaadin-date-picker name="fechaAutorizacion" label="Fecha de autorización"
                                    value="{{formData.fechaAutorizacion}}">
                                </vaadin-date-picker>
                            </es-date-picker>
                            <div class="third">
                                <paper-input name="cantidad" label="Cantidad *" type="number" min="1" auto-validate 
                                    required value="{{formData.cantidad}}">
                                </paper-input>
                                <paper-checkbox name="isUnaCita" checked="{{formData.isUnaCita}}">Solo una cita</paper-checkbox>
                            </div>
                            <paper-money-input-ench class="third" label="Valor sesión" name="valor" disabled
                                precision="0" max-value="99999999999999" value="{{formData.valor}}">
                            </paper-money-input-ench> 
                            <div class="third">
                                <paper-money-input-ench label="Coopago *" name="coopago" required precision="0" 
                                    max-value="99999999999999" value="{{formData.coopago}}">
                                </paper-money-input-ench>
                                <paper-checkbox name="isCoopagoTotal" checked="{{formData.isCoopagoTotal}}">Valor del coopago por todas las sesiones</paper-checkbox>
                            </div>
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button on-click="agregarServicio" disabled="[[loading]]">agregar</paper-button>
                    <paper-button dialog-dismiss>cancelar</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        this.mutation = AGREGAR_SERVICIO_MUTATION;
        if (!NuevoServicioOrden.instance) NuevoServicioOrden.instance = this;
    }

    /**
     * Use for one-time configuration of your component after local
     * DOM is initialized.
     */
    ready() {
        super.ready();
        this._form = this.shadowRoot.querySelector('iron-form');
    }

    /** Llena los campos de coopago y valor. */
    _servicioChanged(e) {
        const { selectedItem: servicio } = e.target;
        if (!servicio) return;

        const { tarifas: [{ valor, coopago }] } = servicio;
        this.set('formData.valor', valor);
        this.set('formData.coopago', coopago);
    }

    /** Servicio agregado. */
    _servicioAgregado(e) {
        if (!e.detail.value) return;

        const { agregarServicioOrden: { ok } } = e.detail.value;
        if (ok) {
            this.reset();
            this.opened = false;
        }
    }

    /** Crear input para la mutación. */
    _composeAgregarServicioInput(orden, {
        servicio, sucursal, autorizacion, fechaAutorizacion, cantidad,
        coopago, fecha, hora, medico, isCoopagoTotal, isUnaCita, duracion
    } = {}) {
        const { id, convenio } = orden;
        const aut = convenio.requiereAutorizacion ? { autorizacion, fechaAutorizacion } : {};
        return Object.assign(aut, {
            medico,
            coopago,
            duracion,
            servicio,
            cantidad,
            sucursal,
            orden: id,
            isUnaCita,
            isCoopagoTotal,
            fecha: DateTime.fromFormat(`${fecha} ${hora}`, 'yyyy-LL-dd h:mm a').toISO(),
        });
    }

    /** Resetea el formulario. */
    reset() {
        this._form.reset();
    }

    /** Agrega el servicio a la orden. */
    agregarServicio() {
        if (this._form.validate()) {
            const servicio = this._composeAgregarServicioInput(this.orden, this.formData);
            this.shadowRoot.querySelector('apollo-mutation').mutate({
                variables: { servicio },
                refetchQueries: ['OrdenDetalle'],
            });
        }
    }
}

customElements.define('nuevo-servicio-orden', NuevoServicioOrden);

NuevoServicioOrden.fragment = gql`
    fragment NuevoServicioOrden on Plan {
        id
        requiereAutorizacion
    }
`;

export default NuevoServicioOrden;
