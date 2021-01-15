import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-button';
import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-group';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import TratamientoInfo from './tratamiento-info';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import './paper-stepper/paper-stepper';
import '@polymer/iron-icon/iron-icon';
import './recibo-caja-form';

const CREAR_RECIBO_MUTATION = gql`
    mutation AbonarPago($recibo: ReciboCajaCreateGenericType!) {
        crearReciboCaja(input: $recibo) {
            ok
        }
    }
`;

/**
 * `tratamientos-por-pagar-list` Lista de tratamientos disponibles para abonar pago.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class TratamientosPorPagarList extends ApolloQuery {
    static get properties() {
        return {
            pacienteId: { type: String },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            ul {
                margin: 0;
                padding: 0;
            }

            li {
                list-style: none;
                margin-bottom: 5px;
            }

            tratamiento-info {
                width: calc(100vw * 0.8 - 120px);
            }
        `;
    }

    render() {
        const { data = {} } = this;
        const tratamientos = data.tratamientos.results || [];

        return html`
            <vaadin-radio-group required error-message="Escoje un tratamiento">
                ${tratamientos.map(tratamiento => html`
                    <vaadin-radio-button value="${tratamiento.id}">
                        <tratamiento-info .tratamiento="${tratamiento}"></tratamiento-info>
                    </vaadin-radio-button>
                `)}
            </vaadin-radio-group>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query TratamientosPorPagar($paciente: ID!) {
                tratamientos(paciente: $paciente disponiblePagar: true) {
                    results(ordering: "-id") {
                        ...TratamientoInfo
                    }
                }
            }
            ${TratamientoInfo.fragment}
        `;
    }

    get pacienteId() {
        return this._pacienteId;
    }

    set pacienteId(value) {
        this._pacienteId = value;
        this._fetchData(value);
    }

    get value() {
        return this.radioGroup.value;
    }

    get radioGroup() {
        return this.shadowRoot.querySelector('vaadin-radio-group');
    }

    _fetchData(id) {
        this.variables = { paciente: id };
        this.subscribe();
    }

    validate() {
        return this.radioGroup.validate();
    }
}

customElements.define('tratamientos-por-pagar-list', TratamientosPorPagarList);

/**
 * `nuevo-pago` Formulario para agregar pago de paciente.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class NuevoPago extends ApolloMutation {
    static get properties() {
        return {
            pacienteId: { type: String },

            opened: {
                type: Boolean,
                reflect: true,
            },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            header {
                display: flex;
                align-items: center;
            }

            paper-dialog {
                width: 80%;
            }

            iron-icon {
                margin-left: auto;
            }
        `;
    }

    render() {
        const { pacienteId, opened } = this;

        return html`
            <paper-dialog modal ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                <header>
                    <h2>NUEVO PAGO</h2>
                    <iron-icon dialog-dismiss icon="my-icons:clear"></iron-icon>
                </header>
                <paper-dialog-scrollable>
                    <paper-stepper linear horizontal open-first-step-on-startup @stepper-finished="${this.save}">
                        <paper-step editable label="Tratamiento a pagar" update-label="Actualizar"
                            continue-label="Continuar">
                            <tratamientos-por-pagar-list required pacienteid="${pacienteId}"></tratamientos-por-pagar-list>
                        </paper-step>
                        <paper-step label="Pago" finish-label="Guardar" back-button back-label="Atras">
                            <recibo-caja-form required with-sucursal></recibo-caja-form>
                        </paper-step>
                    </paper-stepper>
                </paper-dialog-scrollable>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this._boundOpenListener = this._open.bind(this);
    }

    // lifecycles

    connectedCallback() {
        super.connectedCallback();
        window.addEventListener('show-nuevo-pago', this._boundOpenListener);
    }

    disconnectedCallback() {
        window.removeEventListener('show-nuevo-pago', this._boundOpenListener);
        super.disconnectedCallback();
    }

    /** Show modal */
    _open() {
        this.opened = true;
    }

    save() {
        const { value: tratamientoId } = this.shadowRoot.querySelector('tratamientos-por-pagar-list');
        const { value: recibo } = this.shadowRoot.querySelector('recibo-caja-form');

        const variables = { recibo: { servicioPrestado: tratamientoId, ...recibo } };
        this.mutate({
            variables,
            mutation: CREAR_RECIBO_MUTATION,
            refetchQueries: ['PagosPaciente', 'TratamientosPorPagar'],
        });
    }

    onCompleted(data) {
        const { ok } = data.crearReciboCaja;
        if (ok) {
            this.opened = false;
            this.shadowRoot.querySelector('paper-stepper').reset();
        }
    }
}

customElements.define('nuevo-pago', NuevoPago);
