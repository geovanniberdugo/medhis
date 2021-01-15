import { ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import 'paper-money-input-ench/paper-money-input-ench';
import '@polymer/paper-checkbox/paper-checkbox';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-input/paper-input';
import '@polymer/iron-form/iron-form';
import './servicios-combo';

const UPDATE_TRATAMIENTO_MUTATION = gql`
    mutation ActualizarTratamiento($tratamiento: EditarTratamientoInput!) {
        editarTratamiento(input: $tratamiento) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `editar-tratamiento`
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class EditarTratamiento extends ApolloMutation {
    static get properties() {
        return {
            opened: {
                type: Boolean,
                reflect: true,
            },

            convenioId: { type: String },
            tratamiento: { type: Object },
            institucionId: { type: String },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }
        `;
    }

    render() {
        const { opened, tratamiento, convenioId, institucionId, loading } = this;

        return html`
            <paper-dialog modal ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                <h2>EDITAR TRATAMIENTO</h2>
                <paper-dialog-scrollable>
                    <iron-form>
                        <form>
                            <servicios-combo required name="servicio" convenio="${convenioId}" institucion="${institucionId}"
                                value="${tratamiento.servicio && tratamiento.servicio.id}" with-tarifas
                                @change="${this._servicioChanged}">
                            </servicios-combo>
                            <paper-input required name="cantidad" label="Cantidad *" type="number" min="1"
                                value="${tratamiento.cantidad}">
                            </paper-input>
                            <paper-checkbox name="isUnaCita" ?checked="${tratamiento.isUnaCita}">Solo una cita</paper-checkbox>
                            <paper-money-input-ench label="Valor de la sesión *" name="valor" precision="0"
                                max-value="99999999999999" value="${tratamiento.valor}" ?disabled="${!tratamiento.canEditValor}">
                            </paper-money-input-ench>
                            <paper-money-input-ench required label="Coopago *" name="coopago" precision="0"
                                max-value="99999999999999" value="${tratamiento.coopago}">
                            </paper-money-input-ench>
                            <paper-checkbox name="isCoopagoTotal" ?checked="${tratamiento.isCoopagoTotal}"
                                @change="${this._isCoopagoTotalChanged}">
                                Valor del coopago por todas las sesiones
                            </paper-checkbox>
                            <paper-input name="numSesionesCoopago" label="Número de sesiones por coopago" type="number" min="1"
                                value="${tratamiento.numSesionesCoopago || ''}" @blur="${this._numSesionesCoopagoChanged}">
                            </paper-input>
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss>Cancelar</paper-button>
                    <paper-button ?disabled="${loading}" @click="${this._editar}">Editar</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.opened = false;
        this.convenioId = '';
        this.tratamiento = {};
        this.institucionId = '';
        this._boundOpenListener = this._open.bind(this);
    }

    // lifecycles

    connectedCallback() {
        super.connectedCallback();
        window.addEventListener('show-editar-tratamiento-form', this._boundOpenListener);
    }

    disconnectedCallback() {
        window.removeEventListener('show-editar-tratamiento-form', this._boundOpenListener);
        super.disconnectedCallback();
    }

    _open({ detail: { tratamiento, convenioId, institucionId } }) {
        this.convenioId = convenioId;
        this.tratamiento = tratamiento;
        this.institucionId = institucionId;
        this.opened = true;
    }

    _numSesionesCoopagoChanged({ target }) {
        if (!target.value) return;
        this.shadowRoot.querySelector('paper-checkbox[name="isCoopagoTotal"]').checked = false;
    }

    _isCoopagoTotalChanged({ target }) {
        if (!target.checked) return;
        this.shadowRoot.querySelector('paper-input[name="numSesionesCoopago"]').value = '';
    }

    _servicioChanged({ target }) {
        const { selectedItem: servicio } = target;
        if (!servicio) return;

        const { tarifas: [{ valor, coopago }] } = servicio;
        this.tratamiento = { ...this.tratamiento, valor, coopago };
    }

    _editar() {
        const form = this.shadowRoot.querySelector('iron-form');
        if (!form.validate()) return;

        this.mutate({
            refetchQueries: ['OrdenDetalle'],
            mutation: UPDATE_TRATAMIENTO_MUTATION,
            variables: { tratamiento: this._buildInput(this.tratamiento.id, form.serializeForm()) },
        });
    }

    _buildInput(tratamientoId, data) {
        const { cantidad, valor, coopago, isCoopagoTotal, isUnaCita, numSesionesCoopago, servicio } = data;
        return {
            servicio,
            id: tratamientoId,
            coopago: Number(coopago),
            cantidad: Number(cantidad),
            isUnaCita: !!isUnaCita || false,
            isCoopagoTotal: !!isCoopagoTotal || false,
            numSesionesCoopago: numSesionesCoopago || null,
            ...(this.tratamiento.canEditValor && { valor: Number(valor) }),
        }
    }

    onCompleted({ editarTratamiento }) {
        const { ok, errors } = editarTratamiento
        if (ok) this.opened = false;
    }
}

customElements.define('editar-tratamiento', EditarTratamiento);

EditarTratamiento.fragment = gql`
    fragment EditarTratamiento on ServicioRealizar {
        id
        valor
        coopago
        cantidad
        isUnaCita
        canEditValor
        isCoopagoTotal
        servicio { id }
        numSesionesCoopago
    }
`;

export default EditarTratamiento;