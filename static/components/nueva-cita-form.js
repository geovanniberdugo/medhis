import { ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element/lit-element';
import { DateTime } from 'luxon';
import gql from 'graphql-tag';
import { formatDateToISO, formatJSDate } from '../date';
import { getAge, formatDateTimeToISO } from '../utils';

import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-button';
import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-group';
import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@polymer/paper-spinner/paper-spinner-lite';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-input/paper-input';
import ModalMixin from './modal-mixin';
import '@polymer/iron-form/iron-form';
import './tipos-documento-combo';
import './instituciones-combo';
import './convenios-combo';
import './servicios-combo';
import './es-date-picker';
import './duracion-combo';
import './generos-combo';

const AGENDAR_CITA_MUTATION = gql`
    mutation AgendarCita($cita: AgendarCitaInput!) {
        agendarCita(input: $cita) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `nueva-cita-form` Formulario para crear una cita.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class NuevaCitaForm extends ModalMixin(ApolloMutation) {
    static get properties() {
        return {
            /** Info del paciente. */
            paciente: { type: Object },

            /** Is loading paciente data. */
            loadingPaciente: { type: Boolean },

            /** Id de la institucion. */
            institucion: { type: String },

            /** Horario de la cita. */
            horario: {
                type: Date,
                attribute: false,
            },
            fechaNacimiento: { type: String },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            form {
                display: grid;
            }

            fieldset {
                border: none;
                display: contents;
            }

            legend {
                font-size: medium;
                font-weight: bold;
            }

            paper-dialog {
                width: 75%;
            }

            vaadin-date-picker {
                width: 100%;
            }

            paper-spinner-lite {
                --paper-spinner-stroke-width: 2px;
            }

            /* Large devices (desktops, 992px and up) */
            @media (min-width: 992px) {
                form {
                    grid-gap: 10px;
                    grid-template-columns: repeat(6, 1fr);
                }

                legend, .full {
                    grid-column: 1 / -1;
                }

                .half {
                    grid-column: span 3;
                }

                .third {
                    grid-column: span 2;
                }
            }
        `;
    }

    render() {
        // eslint-disable-next-line object-curly-newline
        const { pacienteQuery, paciente, loadingPaciente, opened, horario, institucion, loading, fechaNacimiento } = this;
        return html`
            <apollo-query .noAutoSubscribe="${true}" .query="${pacienteQuery}" @data-changed="${this._setPacienteData}"
                @loading-changed="${(e) => { this.loadingPaciente = e.detail.value; }}">
            </apollo-query>
            <paper-dialog modal ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                <h2>AGENDAR CITA</h2>
                <paper-dialog-scrollable>
                    <iron-form>
                        <form>
                            <fieldset>
                                <legend>Datos del paciente</legend>
                                <tipos-documento-combo name="tipoDocumento" class="half" required autofocus value="${paciente.tipoDocumento || ''}"></tipos-documento-combo>
                                <paper-input name="numeroDocumento" class="half" label="Número de documento*" required auto-validate 
                                    @blur="${this._fetchPacienteInfo}">
                                    <paper-spinner-lite slot="suffix" alt="Cargando datos paciente" ?active="${loadingPaciente}"></paper-spinner-lite>
                                </paper-input>
                                <paper-input name="primerNombre" class="half" label="Primer nombre*" required auto-validate value="${paciente.primerNombre || ''}"></paper-input>
                                <paper-input name="segundoNombre" class="half" label="Segundo nombre" auto-validate value="${paciente.segundoNombre || ''}"></paper-input>
                                <paper-input name="primerApellido" class="half" label="Primer apellido*" required auto-validate value="${paciente.primerApellido || ''}"></paper-input>
                                <paper-input name="segundoApellido" class="half" label="Segundo apellido" auto-validate value="${paciente.segundoApellido || ''}"></paper-input>
                                <generos-combo name="genero" required class="third" value="${paciente.genero || ''}"></generos-combo>
                                <es-date-picker class="third">
                                    <vaadin-date-picker name="fechaNacimiento" label="Fecha de nacimiento" required
                                        auto-validate value="${paciente.fechaNacimiento || ''}" @change="${e => this.fechaNacimiento = e.target.value}">
                                    </vaadin-date-picker>
                                </es-date-picker>
                                <p class="third">Edad <br> ${getAge(fechaNacimiento)}</p>
                                <paper-input name="telefono" class="half" label="Teléfono del domicilio" maxlength="8" auto-validate value="${paciente.telefono || ''}"></paper-input>
                                <paper-input name="celular" class="half" label="Celular" maxlength="10" auto-validate value="${paciente.celular || ''}"></paper-input>
                                <paper-input name="telefono2" class="half" label="Telefono 2" auto-validate value="${paciente.telefono2 || ''}"></paper-input>
                                <paper-input name="direccion" class="half" label="Dirección" auto-validate value="${paciente.direccion || ''}"></paper-input>
                            </fieldset>
                            <fieldset>
                                <legend>Datos de la cita</legend>
                                <div class="half">
                                    Fecha asignada: <b>${formatJSDate(horario, { ...DateTime.DATE_SHORT })}</b> <br>
                                    Hora de la cita: <b>${formatJSDate(horario, { ...DateTime.TIME_SIMPLE, hour12: true })}</b> <br>
                                </div>
                                <duracion-combo required class="half" name="duracion"></duracion-combo>
                                <es-date-picker class="half">
                                    <vaadin-date-picker name="fechaDeseada" label="Fecha deseada" required 
                                        auto-validate value="${formatDateToISO(horario)}">
                                    </vaadin-date-picker>
                                </es-date-picker>
                                <instituciones-combo name="institucion" required class="half" @change="${(e) => { this.institucion = e.target.value; }}"></instituciones-combo>
                                <convenios-combo name="convenio" required class="half" nombre-completo institucion="${institucion}"
                                    @change="${(e) => { this.shadowRoot.querySelector('servicios-combo').convenio = e.target.value; }}">
                                </convenios-combo>
                                <servicios-combo name="servicio" required class="half" institucion="${institucion}"></servicios-combo>
                                <vaadin-radio-group required class="full" error-message="Escoge un estado">
                                    <vaadin-radio-button name="estado" value="NC">No confirmada</vaadin-radio-button>
                                    <vaadin-radio-button name="estado" value="CO">Confirmada</vaadin-radio-button>
                                </vaadin-radio-group>
                            </fieldset>
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss>Cancelar</paper-button>
                    <paper-button @click="${this.agendarCita}" ?disabled="${loading}">Agendar</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.medico = '';
        this.sucursal = '';
        this.paciente = {};
        this.loadingPaciente = false;
        this.mutation = AGENDAR_CITA_MUTATION;
        this.openModalEvent = 'show-nueva-cita-form';
        this.pacienteQuery = gql`
            query PacienteByDocumento($documento: String!) {
                pacientes(numeroDocumento: $documento) {
                    totalCount 
                    results { 
                        id 
                        genero
                        celular
                        telefono
                        telefono2
                        direccion
                        primerNombre
                        segundoNombre
                        tipoDocumento
                        primerApellido 
                        segundoApellido 
                        fechaNacimiento
                    } 
                }
            }
        `;
    }

    _handleOpenEvent({ detail: { medico, horario, sucursal } }) {
        this.reset();
        this.medico = medico;
        this.horario = horario;
        this.sucursal = sucursal;
    }

    /** Gets la información del paciente. */
    _fetchPacienteInfo(e) {
        const { value: documento } = e.target;
        if (!documento) return;

        const queryEl = this.shadowRoot.querySelector('apollo-query');
        queryEl.variables = { documento };
        queryEl.subscribe();
    }

    /** Sets paciente data. */
    _setPacienteData(e) {
        const { pacientes } = e.detail.value;
        const tipoDocumento = this.shadowRoot.querySelector('tipos-documento-combo').value;
        this.paciente = pacientes.totalCount > 0 ? { ...pacientes.results[0] } : { tipoDocumento };
        this.fechaNacimiento = this.paciente.fechaNacimiento;
    }

    /** Clears el formulario. */
    reset() {
        this.shadowRoot.querySelector('iron-form').reset();
        this.paciente = {};
    }

    /** Agenda una nueva cita. */
    agendarCita() {
        const form = this.shadowRoot.querySelector('iron-form');
        if (form.validate()) {
            const { fechaDeseada, convenio, institucion, servicio, estado, duracion, ...paciente } = form.serializeForm();
            const variables = {
                cita: {
                    estado,
                    paciente,
                    convenio,
                    servicio,
                    duracion,
                    institucion,
                    fechaDeseada,
                    medico: this.medico,
                    sucursal: this.sucursal,
                    inicio: formatDateTimeToISO(this.horario),
                },
            }

            return this.mutate({
                variables,
                mutation: this.mutation,
                refetchQueries: ['AgendaCitas'],
            });
        }
    }

    onCompleted(data) {
        const { agendarCita: { ok } } = data;
        if (ok) this.opened = false;
    }
}

customElements.define('nueva-cita-form', NuevaCitaForm);
