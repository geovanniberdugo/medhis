import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@apollo-elements/polymer/apollo-mutation';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-input/paper-input';
import '@polymer/iron-form/iron-form';
import './es-date-picker';

const ADD_AUTORIZACION_MUTATION = gql`
    mutation AgregarAutorizacionCita($cita: AgregarAutorizacionCitaInput!){
        agregarAutorizacionCita(input: $cita) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `autorizacion-cita` Permite modificar la autorización de una cita.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class AutorizacionCita extends PolymerElement {
    static get properties() {
        return {
            /**
                * Indica si el modal se esta mostrando.
                */
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
            </style>

            <apollo-mutation mutation="[[mutation]]" loading="{{loading}}" on-data-changed="_autorizacionGuardada"></apollo-mutation>
            <paper-dialog opened="{{opened}}" position-target="[[positionTarget]]" no-overlap>
                <paper-dialog-scrollable>
                    <iron-form>
                        <form>
                            <paper-input autofocus label="Autorización" name="autorizacion" required value="[[cita.autorizacion]]"></paper-input>
                            <es-date-picker>
                                <vaadin-date-picker label="Fecha de la autorización" name="fechaAutorizacion" required
                                    value="[[cita.fechaAutorizacion]]">
                                </vaadin-date-picker>
                            </es-date-picker>
                            <paper-input label="Autorizado por" name="autorizadoPor" value="[[cita.autorizadorPor]]"></paper-input>
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss>cancelar</paper-button>
                    <paper-button on-click="agregarAutorizacion" disabled="[[loading]]">aceptar</paper-button>
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
        this.mutation = ADD_AUTORIZACION_MUTATION;
    }

    /** Resultado mutación */
    _autorizacionGuardada(e) {
        if (!e.detail.value) return;

        const { agregarAutorizacionCita: { ok } } = e.detail.value;
        if (ok) {
            this.reset();
            this.opened = false;
        }
    }

    /** Resetea el formulario */
    reset() {
        this.cita = {};
    }

    /** Guarda la autoriacion. */
    agregarAutorizacion() {
        const form = this.shadowRoot.querySelector('iron-form');
        if (form.validate()) {
            const cita = { id: this.cita.id, ...form.serializeForm()};
            this.shadowRoot.querySelector('apollo-mutation').mutate({
                variables: { cita },
                refetchQueries: ['OrdenDetalle'],
            });
        }
    }
}

customElements.define('autorizacion-cita', AutorizacionCita);

AutorizacionCita.fragment = gql`
    fragment AutorizacionCita on Cita {
        id
        autorizacion
        autorizadoPor
        fechaAutorizacion
    }
`;

export default AutorizacionCita;
