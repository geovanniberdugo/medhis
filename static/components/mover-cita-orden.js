import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import { DateTime } from 'luxon';
import gql from 'graphql-tag';
import { formatISOTime } from '../utils';

import MedicosCombo from './medicos-combo';
import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker';
import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@apollo-elements/polymer/apollo-mutation';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import '@polymer/iron-form/iron-form';
import './horas-atencion-combo';
import './sucursales-combo';
import './es-date-picker';

window.Luxon = DateTime;
const MOVER_CITA_MUTATION = gql`
    mutation MoverCita($cita: CitaUpdateGenericType!) {
        moverCita(input: $cita) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `mover-cita-orden` Permite mover la cita a un nuevo horario.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MoverCitaOrden extends PolymerElement {
    static get properties() {
        return {
            /** Id de la institución. */
            institucion: String,

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

            /** Datos de la cita. */
            cita: {
                type: Object,
                value: null,
                observer: '_citaChanged',
            },
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                form {
                    display: grid;
                    grid-template-columns: 1fr;
                }

                @media (min-width: 600px) {
                    form {
                        grid-gap: 10px;
                        grid-template-columns: 1fr 1fr;
                    }
                }
            </style>

            <apollo-mutation mutation="[[mutation]]" loading="{{loading}}" on-data-changed="_citaMovida"></apollo-mutation>
            <paper-dialog opened="{{opened}}" position-target="[[positionTarget]]" no-overlap no-cancel-on-outside-click>
                <paper-dialog-scrollable>
                    <iron-form id="form">
                        <form>
                            <medicos-combo name="medico" with-sucursales activos institucion="[[institucion]]"
                                selected-item="{{medicoItem}}" value="{{formData.medico}}">
                            </medicos-combo>
                            <vaadin-combo-box name="Sucursal" label="Sucursal" required auto-validate value="{{formData.sucursal}}"
                                items="[[medicoItem.sucursales]]" item-label-path="nombre" item-value-path="id">
                            </vaadin-combo-box>
                            <es-date-picker>
                                <vaadin-date-picker name="fecha" label="Fecha" required auto-validate value="{{formData.fecha}}">
                                </vaadin-date-picker>
                            </es-date-picker>
                            <horas-atencion-combo name="hora" value="{{formData.hora}}"
                                fecha="[[formData.fecha]]" medico="[[formData.medico]]" sucursal="[[formData.sucursal]]">
                            </horas-atencion-combo>
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss>cancelar</paper-button>
                    <paper-button on-click="moverCita" disabled="[[loading]]">mover</paper-button>
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
        this.mutation = MOVER_CITA_MUTATION;
    }

    /** Observer. */
    _citaChanged(newValue) {
        if (!newValue) return;

        const { inicio, medico, sucursal } = newValue;
        this.formData = {
            medico: medico.id,
            sucursal: sucursal.id,
            hora: formatISOTime(inicio),
            fecha: DateTime.fromISO(inicio).toISODate(),
        };
    }

    /** Cita movida */
    _citaMovida(e) {
        if (!e.detail.value) return;

        const { moverCita: { ok } } = e.detail.value;
        if (ok) {
            this.reset();
            this.opened = false;
        }
    }

    /**
     * Retorna el input para la mutación.
     * @param {string} id Id de la cita.
     * @param {object} data Datos del formulario.
     */
    _buildCitaInput(id, data) {
        // eslint-disable-next-line object-curly-newline
        const { fecha, hora, sucursal, medico } = data;
        return {
            id,
            medico,
            sucursal,
            inicio: DateTime.fromFormat(`${fecha} ${hora}`, 'yyyy-LL-dd h:mm a').toISO(),
        };
    }

    /** Resetea el formulario */
    reset() {
        this.cita = null;
        this.formData = {};
    }

    /** Mover cita. */
    moverCita() {
        const form = this.shadowRoot.querySelector('iron-form');
        if (form.validate()) {
            const cita = this._buildCitaInput(this.cita.id, this.formData);
            this.shadowRoot.querySelector('apollo-mutation').mutate({
                variables: { cita },
                refetchQueries: ['OrdenDetalle'],
            });
        }
    }
}

customElements.define('mover-cita-orden', MoverCitaOrden);

MoverCitaOrden.fragment = gql`
    fragment MoverCitaOrden on Cita {
        id
        inicio
        medico { id }
        sucursal { id }
    }
`;

export default MoverCitaOrden;
