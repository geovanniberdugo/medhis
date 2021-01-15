import { html } from '@polymer/polymer/polymer-element';
import { setErrorsOnForm } from '../utils';

import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@apollo-elements/polymer/apollo-mutation';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/iron-form/iron-form';

/**
 * CRUFormMixin - Usado en los formularios de creación y edición
 * @polymerMixin
 * @mixinFunction
 */
const CRUFormMixin = superClass => class extends superClass {
    /**
      * Object describing property-related metadata used by Polymer features
      */
    static get properties() {
        return {
            /** Indica si el formulario se esta mostrando. */
            opened: {
                type: Boolean,
                value: false,
                reflectToAttribute: true,
            },

            /** Acción a realizar en el formulario. Puede ser Crear o Editar dependiendo del valor de id. */
            accion: {
                type: String,
                computed: '_accionValue(id)',
            },

            /** ID del objeto a editar. */
            id: {
                type: String,
                value: '',
                observer: '_idChanged',
            },

            /** Datos del formulario. */
            value: {
                type: Object,
                value: () => ({}),
            },
        };
    }

    static get baseTemplate() {
        return html`
            ${this.cssStyles}
            <apollo-mutation mutation="[[mutation]]" on-data-changed="_dataUpdated"></apollo-mutation>
            <apollo-query query="[[query]]" on-data-changed="_dataFetched"></apollo-query>
            <paper-dialog modal opened="{{opened}}">
                <h2>[[title]]</h2>
                <paper-dialog-scrollable>
                    <iron-form id="form">
                        <form>
                            ${this.formTemplate}
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss>Cancelar</paper-button>
                    <paper-button on-click="save">[[accion]]</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    static get cssStyles() {
        return html`
            <style>
                :host {
                    display: block;
                }

                * {
                    box-sizing: border-box;
                }

                paper-dialog {
                    width: 60%;
                }

                vaadin-combo-box {
                    width: 100%;
                }
            </style>
        `;
    }

    /** Indica que acción se va a ejecutar. */
    _accionValue(id) {
        return id ? 'Editar' : 'Crear';
    }

    /** Observer cuando id cmabia */
    _idChanged(newValue) {
        if (newValue) {
            this._fetchObjectData(newValue);
        } else {
            this.clean();
        }
    }

    /**
     * Gets los datos del formulario.
     * @param {String} id Id del objeto.
     */
    _fetchObjectData(id) {
        if (!id) {
            this.clean();
            return;
        }

        const queryElem = this.shadowRoot.querySelector('apollo-query');
        const variables = { id };
        if (!queryElem.refetch(variables)) {
            queryElem.variables = variables;
        }
    }

    /** Datos obtenidos */
    _dataFetched(e) {
        this.fillForm(e.detail.value);
    }

    /** Datos guardados */
    _dataUpdated(e) {
        if (e.detail.value) {
            const data = e.detail.value[this.resultName];
            if (data.ok) {
                this.id = '';
                this.opened = false;
            } else {
                setErrorsOnForm(this.shadowRoot.querySelector('form'), data.errors);
            }
        }
    }

    /**
     * Normaliza valores númericos. Si el valor es un string vacío se convierte a null.
     *
     * @param {string|number} value Valor a normalizar.
     * @return {string|number|null} El valor normalizado.
     */
    _cleanNumber(value) {
        return value === '' ? null : value;
    }

    /** Gets form data. */
    _formData() {
        const form = this.shadowRoot.querySelector('form');
        return [...form.querySelectorAll('*')].reduce((obj, elem) => {
            const { name, value } = elem;
            return Object.assign({}, obj, { [name]: value });
        }, {});
    }

    /** Limpia el formulario. */
    clean() {
        const form = this.shadowRoot.querySelector('form');
        // eslint-disable-next-line no-return-assign
        [...form.querySelectorAll('*')].map(e => e.value = '');
    }

    /** Valida el formulario. */
    validate() {
        return this.shadowRoot.querySelector('iron-form').validate();
    }

    /** Guarda el formulario. */
    save() {
        if (this.validate()) {
            const { id } = this;
            const value = this._formData();
            this.mutation = id ? this.editMutation : this.createMutation;
            const options = id ? this._editOptions(id, value) : this._createOptions(value);
            this.shadowRoot.querySelector('apollo-mutation').mutate(options);
        }
    }
};

export default CRUFormMixin;
