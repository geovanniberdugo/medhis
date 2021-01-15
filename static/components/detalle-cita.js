import { html, css } from 'lit-element/lit-element';
import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { DateTime } from 'luxon';
import gql from 'graphql-tag';
import { formatISODate, ESTADOS_ARRAY } from '../utils';

import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@polymer/paper-spinner/paper-spinner-lite';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import './estado-cita-form';
import './modal-spinner';

const ACTUALIZAR_ESTADO_MUTATION = gql`
    mutation CambiarEstadoCita($cita: EstadoCitaInput!) {
        actualizarEstadoCita(input: $cita) {
            ok
            errors { field, messages }
            cita {
                id
                canMove
                category
                estadoActual
                redireccionaUrl
                estadosDisponibles
                historialActual { id, estado, estadoLabel }
            }
        }
    }
`;

/**
 * `cambiar-estado-cita` Mutacion para cambiar el estado de la cita.
 * 
 * @customElement
 * @polymer
 * @demo
 *
 */
class CambiarEstadoCita extends ApolloMutation {
    render() {
        const { loading } = this;
        return html`
            <paper-button ?disabled="${loading}">Guardar</paper-button>
        `;
    }

    onCompleted(data) {
        const { actualizarEstadoCita: { ok } } = data;
        if (ok) this.dispatchEvent(new CustomEvent('estado-changed', { detail: null }));
    }
}

customElements.define('cambiar-estado-cita', CambiarEstadoCita);

/**
 * `detalle-cita` Muestra el detalle de una cita.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class DetalleCita extends ApolloQuery {
    static get properties() {
        return {
            /** Indica si el modal se esta mostrando. */
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

            paper-dialog {
                width: 70%;
            }

            .buttons .space {
                margin-right: auto;
            }
        `;
    }

    render() {
        const { opened, data, loading } = this;
        const { cita = {} } = data || {};
        return html`
            <paper-dialog modal ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                ${loading ? html`<modal-spinner ?active="${loading}"></modal-spinner>` : ''}
                <h2>DATOS DE LA CITA</h2>
                <paper-dialog-scrollable>
                    <p><strong>Fecha:</strong> ${formatISODate(cita.inicio, Object.assign({}, DateTime.DATETIME_SHORT, { hour12: true }))}</p>
                    <p><strong>IPS:</strong> ${cita.institucion.nombre}</p>
                    <p><strong>Empresa:</strong> ${cita.empresa.nombreCompleto}</p>
                    <p><strong>Servicio:</strong> ${cita.servicio.nombre}</p>
                    <p><strong>Medico:</strong> ${cita.medico.nombreCompleto}</p>
                    <p><strong>Paciente:</strong> ${cita.paciente.nombreCompleto}</p>
                    <p><strong>Documento:</strong> ${cita.paciente.tipoDocumento} ${cita.paciente.numeroDocumento}</p>
                    <p><strong>Teléfono del domicilio:</strong> ${cita.paciente.telefono}</p>
                    <p><strong>Celular:</strong> ${cita.paciente.celular}</p>
                    <p><strong>Telefono 2:</strong> ${cita.paciente.telefono2}</p>
                    <p><strong>Estado actual:</strong> ${cita.historialActual.estadoLabel}</p>
                    <estado-cita-form required .estados="${this._estadosDisponibles(cita.estadosDisponibles)}"></estado-cita-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss ?hidden="${!cita.canMove}" @click="${this.moverCita}">Mover cita</paper-button>
                    <a ?hidden="${!cita.ordenUrl}" href="${cita.ordenUrl}" tabindex="-1"><paper-button>Ver orden</paper-button></a>
                    <a ?hidden="${!cita.estadosDisponibles.includes('CU')}" href="${cita.redireccionaUrl}" tabindex="-1"><paper-button>Paciente llegó</paper-button></a>
                    <div class="space"></div>
                    <paper-button dialog-dismiss>Cancelar</paper-button>
                    <cambiar-estado-cita @click="${this.cambiarEstado}" @estado-changed="${() => { this.opened = false; }}"></cambiar-estado-cita>
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
        this.opened = false;
        if (!DetalleCita.instance) DetalleCita.instance = this;
        this.query = gql`
            query DetalleCita($cita: ID!) {
                cita(id: $cita) {
                    id
                    inicio
                    canMove
                    ordenUrl
                    redireccionaUrl
                    estadosDisponibles
                    servicio { id, nombre }
                    institucion { id, nombre @title_case }
                    medico { id, nombreCompleto @title_case }
                    empresa { id, nombreCompleto @title_case }
                    historialActual { id, estado, estadoLabel }
                    paciente { 
                        id
                        celular
                        telefono
                        telefono2
                        tipoDocumento
                        numeroDocumento
                        nombreCompleto @title_case
                    }
                }
            }
        `;
    }

    get id() {
        return this._id;
    }

    set id(value) {
        this._id = value;
        this._fetchData(value);
    }

    get estadoForm() {
        return this.shadowRoot.querySelector('estado-cita-form');
    }

    /** Fetch el detalle de la cita. */
    _fetchData(id) {
        if (!id) return;

        const variables = { cita: id };
        if (!this.refetch(variables)) {
            this.variables = variables;
        }
    }

    /**
     * Indica los estados que puede tener la cita.
     * @param {Array} disponibles Estados que puede tener la cita.
     */
    _estadosDisponibles(disponibles) {
        return ESTADOS_ARRAY.filter(estado => estado.value !== 'CU' && disponibles.includes(estado.value));
    }

    /** Actualiza el estado de la cita. */
    cambiarEstado(e) {
        const estadoForm = this.estadoForm;
        if (!estadoForm.validate()) return;
        
        const { motivo, ...data } = estadoForm.value;
        const _motivo = motivo ? { motivo } : {};
        const cita = {id: this.id, ..._motivo, ...data};
        
        const _cambiarEstado = e.target;
        _cambiarEstado.mutate({
            variables: { cita },
            refetchQueries: ['AgendaCitas'],
            mutation: ACTUALIZAR_ESTADO_MUTATION,
        });
    }

    /** Despacha evento que indica que se va a mover la cita. */
    moverCita() {
        this.dispatchEvent(new CustomEvent('mover-cita', { detail: { cita: this.id } }));
    }
}

customElements.define('detalle-cita', DetalleCita);
export default DetalleCita;
