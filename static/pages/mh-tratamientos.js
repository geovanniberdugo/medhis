import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { notifyErrorMessage, createUrlQueryStringFromObject } from '../utils';

import BasePacientePerfil from '../components/base-paciente-perfil';
import '@vaadin/vaadin-combo-box/theme/material/vaadin-combo-box';
import '@vaadin/vaadin-checkbox/theme/material/vaadin-checkbox';
import TratamientoInfo from '../components/tratamiento-info';
import '@polymer/paper-icon-button/paper-icon-button';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '@polymer/paper-fab/paper-fab';
import '../elements';

// Templates

const tratamientoItem = tratamiento => html`
    <a href="${tratamiento.ordenUrl}">
        <li><tratamiento-info .tratamiento="${tratamiento}"></tratamiento-info></li>
    </a>
`;

const tratamientoItemWithCheck = tratamiento => html`
    <li class="with-checkbox">
        <vaadin-checkbox value="${tratamiento.id}"></vaadin-checkbox>
        <tratamiento-info .tratamiento="${tratamiento}"></tratamiento-info>
    </li>
`;

const optionsMenu = (opened, generarCertificado) => html`
    <paper-dialog id="options-menu" ?opened="${opened}" horizontal-align="right" vertical-align="top">
        <div class="card-content">
            <ul>
                <li @click="${generarCertificado}">Generar certificado de asistencia</li>
            </ul>
        </div>
    </paper-dialog>
`;

/**
 * `mh-tratamientos` Tratamientos de un paciente.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisTratamientos extends ApolloQuery {
    static get properties() {
        return {
            pacienteId: { type: String },
            menuOpened: { type: Boolean },
            certificado: { type: Boolean },
            certificadoAsistenciaUrl: { type: String },
        };
    }

    static get styles() {
        const base = css`
            :host {
                display: block;
            }

            a {
                color: inherit;
            }

            ul {
                margin: 0;
                padding: 0;
            }

            li {
                list-style: none;
                margin-bottom: 5px;
            }

            section {
                display: flex;
                align-items: flex-end;
            }

            section *:last-child {
                margin-left: auto;
            }

            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--app-primary-color);
            }

            paper-fab {
                right: 10px;
                bottom: 10px;
                position: fixed;
            }

            paper-fab[hidden] {
                display: none;
            }

            tratamiento-info:hover {
                --tratamiento-card-color: #f5f2f2;
            }

            .with-checkbox {
                display: flex;
                align-items: center;
            }

            .with-checkbox vaadin-checkbox {
                margin-right: 5px;
            }

            .with-checkbox tratamiento-info {
                flex: 1;
            }

            .with-checkbox tratamiento-info:hover {
                --tratamiento-card-color: white;
            }

            #more {
                text-align: center;
            }

            #options-menu .card-content {
                margin: 0;
                padding: 0;
            }

            #options-menu li {
                padding: 15px;
            }

            #options-menu li:hover {
                padding: 15px;
                cursor: pointer;
                background-color: lightgray;
            }

            #cert-asistencia {
                color: green;
                padding: 10px;
                border-radius: 2px;
                background-color: #bfecbf;
                border: 1px solid #85c585;
            }

            #cert-asistencia button {
                padding: 0;
                border: none;
                color: #4b924b;
                font-size: 14px;
                cursor: pointer;
                background-color: transparent;
            }

            @media (min-width: 600px) {
                paper-fab {
                    right: 260px;
                }
            }
        `;

        return [BasePacientePerfil.headerStyles, base];
    }

    render() {
        // eslint-disable-next-line object-curly-newline
        const { loading, data, updateQuery, estados, menuOpened, certificado } = this;
        const paciente = data.paciente || {};
        const tratamientos = data.tratamientos.results || [];
        const total = data.tratamientos.totalCount || 0;
        const variables = { paciente: paciente.id, offset: tratamientos.length };

        return html`
            <base-paciente-perfil selected-menu="tratamientos" .paciente="${paciente}">
                <header>
                    <h1>Tratamientos</h1>
                </header>

                <section>
                    <vaadin-combo-box label="Estado" .items="${estados}" @change="${this._filterByEstado}"></vaadin-combo-box>
                    <div>
                        <paper-icon-button icon="my-icons:more-vert" @click="${this._toggleOptionsMenu}"></paper-icon-button>
                        ${optionsMenu(menuOpened, this._enableTreatmentSelectForCerticate.bind(this))}
                    </div>
                </section>

                <p id="cert-asistencia" ?hidden="${!certificado}">Escoge los tratamientos para generar el certificado. <button @click="${this._disableTreatmentSelectForCerticate}">(Cancelar)</button></p>

                <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                <ul>
                    ${certificado ? tratamientos.map(tratamientoItemWithCheck) : tratamientos.map(tratamientoItem)}
                </ul>
                <div id="more">
                    <paper-button ?hidden="${tratamientos.length === 0 || tratamientos.length === total}"
                        @click="${() => this.fetchMore({ updateQuery, variables })}">
                        ver mas
                    </paper-button>
                </div>
                <paper-fab ?hidden="${!certificado}" icon="my-icons:print" @click="${this._generarCertificado}"></paper-fab>
            </base-paciente-perfil>
        `;
    }

    constructor() {
        super();
        this.estados = [
            { label: 'No Iniciado', value: 'NI' },
            { label: 'Iniciado', value: 'IN' },
            { label: 'Terminado', value: 'TE' },
            { label: 'Facturado', value: 'FAC' },
            { label: 'Cancelado', value: 'CA' },
        ];
        this.menuOpened = false;
        this.certificado = false;
        this.notifyOnNetworkStatusChange = true;
        this.query = gql`
            query TratamientosPaciente($paciente: ID!, $estado: String, $offset: Int) {
                paciente(id: $paciente) {
                    ...BasePacientePerfil
                }
                tratamientos(paciente: $paciente, estado: $estado) {
                    totalCount
                    results(ordering: "-id", limit: 10, offset: $offset) {
                        id
                        ordenUrl
                        ...TratamientoInfo
                    }
                }
            }
            ${TratamientoInfo.fragment}
            ${BasePacientePerfil.fragment}
        `;
    }

    get pacienteId() {
        return this._pacienteId;
    }

    set pacienteId(value) {
        this._pacienteId = value;
        this._fetchData(value);
    }

    // lifecycles
    firstUpdated() {
        this._optionsMenu = this.shadowRoot.getElementById('options-menu');
    }

    _filterByEstado(e) {
        const { pacienteId: paciente } = this;
        const { value } = e.target;
        this.variables = value ? { paciente, estado: value } : { paciente };
        this.subscribe();
    }

    _toggleOptionsMenu(e) {
        this._optionsMenu.positionTarget = e.target;
        this.menuOpened = !this.menuOpened;
    }

    _enableTreatmentSelectForCerticate() {
        this.menuOpened = false;
        this.certificado = true;
    }

    _disableTreatmentSelectForCerticate() {
        console.log('disabled');
        this.certificado = false;
    }

    _generarCertificado() {
        const selectedCheckboxes = [...this.shadowRoot.querySelectorAll('vaadin-checkbox')].filter(c => c.checked);
        if (selectedCheckboxes.length === 0) {
            notifyErrorMessage(this, 'Debes escoger algun tratamiento.');
            return;
        }

        const selectedTreatments = selectedCheckboxes.map(c => c.value);
        const queryString = createUrlQueryStringFromObject({ tratamientos: selectedTreatments, paciente: this.pacienteId });
        window.location = `${this.certificadoAsistenciaUrl}?${queryString}`;
    }

    /** Fetch los datos */
    _fetchData(id) {
        this.variables = { paciente: id };
        this.subscribe();
    }

    /** Pagination */
    updateQuery(prev, { fetchMoreResult }) {
        if (!fetchMoreResult) return prev;
        return Object.assign({}, prev, {
            tratamientos: {
                totalCount: fetchMoreResult.tratamientos.totalCount,
                results: [...prev.tratamientos.results, ...fetchMoreResult.tratamientos.results],
                __typename: prev.tratamientos.__typename,
            },
        });
    }
}

customElements.define('mh-tratamientos', MedhisTratamientos);
