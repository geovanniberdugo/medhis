import { PolymerElement, html } from '@polymer/polymer/polymer-element';

import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-button';
import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-group';
import '@polymer/paper-toggle-button/paper-toggle-button';
import '@polymer/polymer/lib/elements/dom-repeat';
import '@polymer/paper-input/paper-textarea';
import '@polymer/iron-form/iron-form';

/**
 * `estado-cita-form` Formulario para cambiar el estado de la cita.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class EstadoCitaForm extends PolymerElement {
    static get properties() {
        return {
            /**
             * Estados que puede tener la cita.
             */
            estados: {
                type: Array,
                value: () => [],
            },

            /** Indica si el combo es requerido. */
            required: {
                type: Boolean,
                value: false,
            },

            /** Indica si puede reagendar. */
            couldReagendar: {
                type: Boolean,
                value: false,
            },

            /** Indica si debe ingresar motivo de cancelación. */
            conMotivo: {
                type: Boolean,
                value: false,
            },

            /** Estado nuevo de la cita */
            estado: {
                type: String,
                notify: true,
                value: '',
            },
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
            </style>
            <iron-form>
                <form>
                    <vaadin-radio-group required="[[required]]" error-message="Escoge un estado" on-value-changed="_estadoChanged">
                        <template is="dom-repeat" items="[[estados]]" as="estado">
                            <vaadin-radio-button name="estado" value="[[estado.value]]">[[estado.label]]</vaadin-radio-button>
                        </template>
                    </vaadin-radio-group>
                    <paper-textarea label="Motivo" name="motivo" hidden$="[[!conMotivo]]" id="motivo"
                        required="[[conMotivo]]" auto-validate error-message="Debes ingresar un motivo">
                    </paper-textarea>
                    <br>
                    <paper-toggle-button id="reagendar" name="reagendar" hidden$="[[!couldReagendar]]">Reagendar cita automaticamente</paper-toggle-button>
                </form>
            </iron-form>
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

    get value() {
        return this._form ? this._form.serializeForm() : null;
    }

    /**  */
    _estadoChanged(e) {
        const { value } = e.detail;
        this.couldReagendar = ['EX', 'NT', 'NA'].includes(value);
        this.conMotivo = ['CA', 'EX', 'NA', 'NT'].includes(value);

        this.estado = value;
        if (this.conMotivo) this.$.motivo.focus();
        if (!this.conMotivo) this.$.motivo.value = '';
        if (!this.couldReagendar) this.$.reagendar.checked = false;
    }

    /** Resetea el formulario. */
    reset() {
        this._form.reset();
    }

    /** Valida el formulario. */
    validate() {
        return this._form.validate();
    }
}

customElements.define('estado-cita-form', EstadoCitaForm);
