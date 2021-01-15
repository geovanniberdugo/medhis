import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
// eslint-disable-next-line object-curly-newline
import { formatDateToISO, urlQueryToDict, updateFiltersOnUrl, ISODateToJSDate, formatISODate, DATETIME_FORMAT } from '../utils';

import { cardCss, progressCss } from '../components/common-css';
import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-input/paper-textarea';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-dialog/paper-dialog';
import '../components/instituciones-combo';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '../components/sucursales-combo';
import '../components/medicos-combo';
import '../elements';

const CAMBIAR_MOTIVO_MUTATION = gql`
    mutation CambiarMotivoEstadoCita($input: HistorialEstadoUpdateGenericType!) {
        cambiarMotivoEstadoCita(input: $input) {
            ok
            historialEstado {
                id
                motivo
            }
        }
    }
`;

/**
 * `cambiar-motivo-estado` Cambiar motivo del estado.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class CambiarMotivoEstado extends ApolloMutation {
    static get properties() {
        return {

        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            paper-dialog {
                margin: 10px;
                width: 250px;
            }
        `;
    }

    render() {
        const { loading } = this;

        return html`
            <paper-dialog no-overlap horizontal-align="center" vertical-align="auto" dynamic-align scroll-action="lock">
                <paper-textarea autofocus required label="Motivo"></paper-textarea>
                <div class="buttons">
                    <paper-button dialog-dismiss>Cancelar</paper-button>
                    <paper-button ?disabled="${loading}" @click="${this._cambiar}">Cambiar</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    firstUpdated() {
        this.textElem = this.shadowRoot.querySelector('paper-textarea');
        this.dialogElem = this.shadowRoot.querySelector('paper-dialog');
    }

    _cambiar() {
        if (!this.textElem.validate()) return;

        const variables = { input: { id: this.estado, motivo: this.textElem.value } };
        this.mutate({
            variables,
            mutation: CAMBIAR_MOTIVO_MUTATION,
        });
    }

    onCompleted({ cambiarMotivoEstadoCita: { ok } }) {
        if (ok) {
            this.textElem.value = '';
            this.dialogElem.close();
        }
    }

    open({ element, estado }) {
        this.dialogElem.positionTarget = element;
        this.estado = estado;
        this.dialogElem.open();
    }
}

customElements.define('cambiar-motivo-estado', CambiarMotivoEstado);

/**
 * `mh-citas-no-cumplidas` Reporte de citas no cumplidas.
 *
 * @customElement
 * @demo
 * 
 */
class MedhisCitasNoCumplidas extends ApolloQuery {
    static get properties() {
        return {
            citas: { type: Array },
            desde: { type: String },
            hasta: { type: String },
            medicoId: { type: String },
            sucursalId: { type: String },
            institucionId: { type: String },
        }
    }

    static get styles() {
        const base = css`
            :host {
                display: block;
            }

            ul {
                padding: 0;
            }

            p {
                margin: 0;
            }

            paper-card {
                width: 100%;
            }

            .card {
                display: grid;
                padding: 20px;
                grid-gap: 10px;
                list-style: none;
                align-items: center;
                margin-block-end: 10px;
                grid-template-columns: repeat(auto-fit, minmax(12em, 1fr));
            }

            #filters .card-content {
                display: grid;
                grid-gap: 5px;
                grid-template-columns: repeat(auto-fill, minmax(15em, 1fr));
            }
        `;

        return [cardCss, progressCss, base];
    }

    render() {
        const { desde, hasta, institucionId, medicoId, sucursalId, loading, citas } = this;

        return html`
            <section id="filters">
                <paper-card>
                    <div class="card-content">
                        <range-datepicker-input .dateFrom="${desde}" .dateTo="${hasta}"
                            @date-from-changed="${(e) => { this.desde = e.detail.value; }}"
                            @date-to-changed="${(e) => { this.hasta = e.detail.value; }}">
                            <template>
                                <div style="display: grid; grid-gap: 10px; grid-template-columns: 1fr 1fr;">
                                    <paper-input required label="Desde *" value="[[dateFrom]]"></paper-input>
                                    <paper-input required label="Hasta *" value="[[dateTo]]"></paper-input>
                                </div>
                            </template>
                        </range-datepicker-input>
                        <instituciones-combo value="${institucionId}"
                            @change="${(e) => { this.institucionId = e.target.value; }}">
                        </instituciones-combo>
                        <medicos-combo value="${medicoId}"
                            @change="${(e) => { this.medicoId = e.target.value; }}">
                        </medicos-combo>
                        <sucursales-combo value="${sucursalId}"
                            @change="${(e) => { this.sucursalId = e.target.value; }}">
                        </sucursales-combo>
                    </div>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                </paper-card>
            </section>
            <section id="report">
                <ul>
                    ${citas.map(cita => html`
                        <li class="card">
                            <p>
                                ${cita.paciente.nombreCompleto} <br>
                                ${cita.paciente.tipoDocumento} ${cita.paciente.numeroDocumento}
                            </p>
                            <p>${cita.convenio.nombreCompleto}</p>
                            <p>${formatISODate(cita.inicio, DATETIME_FORMAT)}</p>
                            <p>${cita.servicio.nombre}</p>
                            <p>${cita.historialActual.estadoLabel}</p>
                            <p @click="${e => this._showCambiarMotivo({ element: e.target, estado: cita.historialActual.id})}">
                                ${cita.historialActual.motivo}
                            </p>
                        </li>    
                    `)}
                </ul>
            </section>
            <cambiar-motivo-estado></cambiar-motivo-estado>
        `;
    }

    constructor() {
        super();
        this.citas = [];
        this.medicoId = '';
        this.sucursalId = '';
        this.notifyOnNetworkStatusChange = true;
        this._setFiltersFromUrl();
        this.query = gql`
            query CitasNoCumplidas($entre: String!, $institucion: ID, $medico: ID, $sucursal: ID) {
                citas(noCumplidas: true, fechaEntre: $entre, institucion: $institucion, medico: $medico, sucursal: $sucursal) {
                    results {
                        id
                        inicio
                        servicio { id, nombre @title_case }
                        convenio { id, nombreCompleto @title_case}
                        historialActual { id, estadoLabel, motivo }
                        paciente { 
                            id
                            tipoDocumento
                            numeroDocumento
                            nombreCompleto @title_case
                        }
                    }
                }
            }
        `;
    }

    get data() {
        return this._data;
    }

    set data(value) {
        this._data = value;
        this._setData(value);
    }

    // Lifecycles

    shouldUpdate() {
        return true;
    }

    updated(changedProps) {
        const shouldFetch = changedProps.has('desde') || changedProps.has('hasta') || changedProps.has('sucursalId') || changedProps.has('institucionId') || changedProps.has('medicoId');
        if (shouldFetch) this._fetchData();
    }

    _setFiltersFromUrl() {
        // eslint-disable-next-line object-curly-newline
        const { hasta, desde, medico, sucursal, institucion } = urlQueryToDict();
        this.medicoId = `${medico || this.medicoId}`;
        this.desde = ISODateToJSDate(desde || this.desde);
        this.hasta = ISODateToJSDate(hasta || this.hasta);
        this.sucursalId = `${sucursal || this.sucursalId}`;
        this.institucionId = `${institucion || this.institucionId}`;
    }

    _setQueryParams(desde, hasta, institucion, medico, sucursal) {
        const filtros = {
            ...(medico && { medico }),
            ...(sucursal && { sucursal }),
            ...(institucion && { institucion }),
            ...(desde && { desde: formatDateToISO(desde) }),
            ...(hasta && { hasta: formatDateToISO(hasta) }),
        };
        updateFiltersOnUrl(filtros, true);
    }

    _fetchData() {
        // eslint-disable-next-line object-curly-newline
        const { desde, hasta, institucionId, sucursalId, medicoId } = this;
        this._setQueryParams(desde, hasta, institucionId, medicoId, sucursalId);
        if (!desde || !hasta) {
            this.citas = [];
            return;
        }

        this.variables = {
            ...(medicoId && { medico: medicoId }),
            ...(sucursalId && { sucursal: sucursalId }),
            ...(institucionId && { institucion: institucionId }),
            entre: `${formatDateToISO(desde)},${formatDateToISO(hasta)}`,
        };
        this.subscribe();
    }

    _setData(data) {
        const { citas: { results: citas } } = data;
        this.citas = citas;
    }

    _showCambiarMotivo({ element, estado }) {
        this.shadowRoot.querySelector('cambiar-motivo-estado').open({ element, estado });
    }
}

customElements.define('mh-citas-no-cumplidas', MedhisCitasNoCumplidas);
