import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import CRUFormMixin from './cru-form-mixin';

import 'paper-money-input-ench/paper-money-input-ench';
import './servicios-combo';

// eslint-disable-next-line import/no-mutable-exports
let tarifaFormInstance = null;

const EDIT_MUTATION = gql`
    mutation EditarTarifa($tarifa: TarifaUpdateGenericType!) {
        editarTarifa(input: $tarifa) {
            ok
            errors { field, messages }
            tarifa {
                id
                valor
                coopago
                ivaCoopago
                servicio { id, nombre @title_case }
            }
        }
    }
`;

const CREATE_MUTATION = gql`
    mutation CrearTarifa($tarifa: TarifaCreateGenericType!) {
        crearTarifa(input: $tarifa) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `tarifa-form` Formulario de creación y edición de tarifas.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class TarifaForm extends CRUFormMixin(PolymerElement) {
    static get properties() {
        return {
            /** Id del convenio */
            convenio: String,

            /** Id de la institucion */
            institucion: String,

            /**
             * Titulo del dialogo.
             */
            title: {
                type: String,
                value: 'Tarifa',
            },
        };
    }

    static get template() {
        return html`
            ${this.baseTemplate}
        `;
    }

    static get formTemplate() {
        return html`
            <servicios-combo name="servicio" required value="[[value.servicio]]"></servicios-combo>
            <paper-money-input-ench name="valor" label="Valor" required precision="0" max-value="99999999999999"
                value="[[value.valor]]">
            </paper-money-input-ench> 
            <paper-money-input-ench name="coopago" label="Coopago" precision="0" max-value="99999999999999"
                value="[[value.coopago]]">
            </paper-money-input-ench> 
            <paper-money-input-ench name="ivaCoopago" label="Iva Coopago" precision="0" max-value="99999999999999"
                value="[[value.ivaCoopago]]">
            </paper-money-input-ench> 
        `;
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        if (!tarifaFormInstance) tarifaFormInstance = this;
        this.editMutation = EDIT_MUTATION;
        this.createMutation = CREATE_MUTATION;
        this.query = gql`
            query Tarifa($id: ID!) {
                tarifa(id: $id) {
                    id
                    valor
                    coopago
                    ivaCoopago
                    servicio { id }
                }
            }
        `;
    }

    /** Create mutation options */
    _createOptions(value) {
        this.resultName = 'crearTarifa';
        return {
            variables: { tarifa: { institucion: this.institucion, plan: this.convenio, ...value }},
            refetchQueries: ['Tarifas'],
        };
    }

    /** Edit mutation options */
    _editOptions(id, value) {
        this.resultName = 'editarTarifa';
        return {
            variables: { tarifa: { id, institucion: this.institucion, plan: this.convenio, ...value }},
        };
    }

    /** @override */
    clean() {
        super.clean();
        [...this.shadowRoot.querySelectorAll('paper-money-input-ench')].map(e => e.clean());
    }

    /** Llena el formulario. */
    fillForm(data) {
        if (data) {
            // eslint-disable-next-line object-curly-newline
            const { tarifa: { coopago, servicio, ivaCoopago, valor } } = data;
            this.value = {
                valor,
                coopago,
                ivaCoopago,
                servicio: servicio.id,
            };
        } else {
            this.clean();
        }
    }
}

customElements.define('tarifa-form', TarifaForm);

export default tarifaFormInstance;
