import { ApolloQuery, ApolloMutation }  from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { setErrorsOnForm } from '../utils';

import '@vaadin/vaadin-text-field/theme/material/vaadin-password-field';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@vaadin/vaadin-upload/theme/material/vaadin-upload';
import '@polymer/paper-toggle-button/paper-toggle-button';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-input/paper-input';
import './instituciones-multi-select';
import '@polymer/iron-form/iron-form';
import './tipos-agenda-combo';
import './modal-spinner';
import './roles-combo';

const CREAR_MEDICO_MUTATION = gql`
    mutation CrearMedico($medico: CrearMedicoInput!) {
        crearMedico(input: $medico) {
            ok
            errors { field, messages }
        }
    }
`;

const EDITAR_MEDICO_MUTATION = gql`
    mutation EditarMedico($medico: EditarMedicoInput!) {
        editarMedico(input: $medico) {
            ok
            errors { field, messages }
            medico: empleado {
                id
                firma
                activo
                cedula
                nombres
                apellidos
                duracionCita
                registroMedico
                porcentajePago
                agenda { id }
                instituciones { id }
                atencionesSimultaneas
                usuario { id, username, rol { id } }
            }
        }
    }
`;

/**
 * `guardar-medico` Crea o edita medico.
 *
 * @customElement
 * @demo
 * 
 */
class GuardarMedico extends ApolloMutation {
    static get properties() {
        return {
            edit: { type: Boolean },
        }
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }
        `;
    }

    render() {
        const { loading, edit } = this;

        return html`
            <paper-button ?disabled="${loading}">${edit ? 'editar' : 'crear'}</paper-button>
        `;
    }

    constructor() {
        super();
        this.edit = false;
    }

    onCompleted(data) {
        const mutation = this.edit ? data.editarMedico : data.crearMedico;
        const { ok, errors } = mutation;

        if (ok) {
            this.dispatchEvent(new CustomEvent('mutation-done', { detail: null }));
        } else {
            this.dispatchEvent(new CustomEvent('mutation-error', { detail: { errors } }));
        }
    }

    /** Ejecuta la mutación. */
    execute(medico) {
        const opts = this.edit ? { mutation: EDITAR_MEDICO_MUTATION } : { mutation: CREAR_MEDICO_MUTATION, refetchQueries: ['TodosMedicos'] };
        this.mutate({
            ...opts,
            variables: { medico },
        });
    }
}

customElements.define('guardar-medico', GuardarMedico);

/**
 * `medico-form` Formulario de edicion/creacion de medico.
 *
 * @customElement
 * @demo
 * 
 */
class MedicoForm extends ApolloQuery {
    static get properties() {
        return {
            opened: {
                type: Boolean,
                reflect: true,
            },
        }
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
                display: contents;
            }

            legend {
                padding: 10px 0px;
                font-size: medium;
                font-weight: bold;
                text-transform: uppercase;
            }

            span {
                font-size: var(--paper-font-caption_-_font-size);
                line-height: var(--paper-font-caption_-_line-height);
                letter-spacing: var(--paper-font-caption_-_letter-spacing);
            }

            paper-dialog {
                width: 80%;
            }

            @media(min-width: 40em) {
                form {
                    grid-gap: 10px;
                    align-items: end;
                    grid-template-columns: 1fr 1fr;
                }

                legend {
                    grid-column: 1 / -1;
                }

                paper-toggle-button {
                    align-self: center;
                }
            }

            @media(min-width: 60em) {
                paper-dialog {
                    width: 60%;
                }
            }
        `;
    }

    render() {
        const { opened, loading, data } = this;
        const medico = data.medico || { instituciones: [], usuario: {} };
        const instituciones = medico.instituciones.map(institucion => institucion.id);

        return html`
            <paper-dialog modal ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                ${loading ? html`<modal-spinner ?active="${loading}"></modal-spinner>` : ''}
                <h2>Medico</h2>
                <paper-dialog-scrollable>
                    <iron-form>
                        <form>
                            <fieldset>
                                <legend>Datos personales</legend>
                                <paper-input required label="Nombres *" name="nombres" .value="${medico.nombres}"></paper-input>
                                <paper-input required label="Apellidos *" name="apellidos" .value="${medico.apellidos}"></paper-input>
                                <paper-input required label="Cedula *" name="cedula" .value="${medico.cedula}" type="number"></paper-input>
                                <paper-input required label="Registro medico *" name="registroMedico" .value="${medico.registroMedico}"></paper-input>
                                <div>
                                    <h4>Firma</h4>
                                    <vaadin-upload name="firma" no-auto max-files="1" accept="image/*"
                                        .files="${this._setUploadedFile(medico.firma)}">
                                    </vaadin-upload>
                                </div>
                            </fieldset>
                            <fieldset>
                                <legend>Datos de atención</legend>
                                <instituciones-multi-select required name="instituciones" .value="${instituciones}"></instituciones-multi-select>
                                <tipos-agenda-combo name="agenda" .value="${medico.agenda && medico.agenda.id}"></tipos-agenda-combo>
                                <div>
                                    <paper-input label="Duracion cita" name="duracionCita" .value="${medico.duracionCita}"></paper-input>
                                    <span>Ingresar duración de la forma HH:MM:SS. Ej. para una duración de 15mins -> 00:15:00</span>
                                </div>
                                <paper-input label="Atenciones simultaneas" name="atencionesSimultaneas" .value="${medico.atencionesSimultaneas}" type="number" min="0"></paper-input>
                                <div>
                                    <paper-input label="Porcentaje de pago" name="porcentajePago" type="number"
                                        max="100" min="0" .value="${medico.porcentajePago}">
                                    </paper-input>
                                    <span>Porcentaje usado para calcular el pago al profesional.</span>
                                </div>
                                <paper-toggle-button name="activo" ?checked="${medico.activo}">Activo</paper-toggle-button>
                            </fieldset>
                            <fieldset>
                                <legend>Datos de usuario</legend>
                                <paper-input required label="Usuario *" name="username" .value="${medico.usuario.username}"></paper-input>
                                <roles-combo required name="rol" .value="${medico.usuario.rol && medico.usuario.rol.id}"></roles-combo>
                                <vaadin-password-field label="Contraseña" name="password1"></vaadin-password-field>
                                <vaadin-password-field label="Confirmar contraseña" name="password2"></vaadin-password-field>
                            </fieldset>
                        </form>
                    </iron-form>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss>Cancelar</paper-button>
                    <guardar-medico ?edit="${!!medico.id}" @click="${this._save}" @mutation-done="${() => { this.opened = false; }}"
                        @mutation-error="${this._showErrors}">
                    </guardar-medico>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.opened = false;
        this.notifyOnNetworkStatusChange = true;
        this._boundOpenListener = this._open.bind(this);
        this.query = gql`
            query InfoMedico($id: ID!) {
                medico: empleado(id: $id) {
                    id
                    firma
                    activo
                    cedula
                    nombres
                    apellidos
                    duracionCita
                    registroMedico
                    porcentajePago
                    agenda { id }
                    instituciones { id }
                    atencionesSimultaneas
                    usuario { id, username, rol { id } }
                }
            }
        `;
    }

    get id() {
        return this._id;
    }

    set id(value) {
        this._id = value;
        if (value) { 
            this._fetchData(value);
        } else {
            this.data = {};
        }
    }

    // lifecycles

    connectedCallback() {
        super.connectedCallback();
        window.addEventListener('show-medico-form', this._boundOpenListener);
    }

    disconnectedCallback() {
        window.removeEventListener('show-medico-form', this._boundOpenListener);
        super.disconnectedCallback();
    }

    _open({ detail }) {
        this.id = detail && detail.medicoId;
        this.opened = true;
    }

    _setUploadedFile(name) {
        return name ? [{ name, progress: 100, complete: true }] : [];
    }

    _fetchData(id) {
        this.variables = { id };
        this.subscribe();
    }

    _save({ target }) {
        const form = this.shadowRoot.querySelector('iron-form');
        const firmaElem = this.shadowRoot.querySelector('vaadin-upload');
        if (!this._validate()) return;

        const { password1, password2, duracionCita, activo, atencionesSimultaneas, ...formData } = form.serializeForm();
        target.execute({
            ...formData,
            activo: !!activo,
            ...(password1 && { password1 }),
            ...(password2 && { password2 }),
            ...(this.id && { id: this.id }),
            ...(duracionCita && { duracionCita }),
            atencionesSimultaneas: atencionesSimultaneas || null,
            ...(firmaElem.files.length > 0 && firmaElem.files[0] instanceof File && { firma: firmaElem.files[0] }),
        });
    }

    _validate() {
        const form = this.shadowRoot.querySelector('iron-form');
        this._resetInvalidElements(form);
        return form.validate();
    }

    _resetInvalidElements(form) {
        [...form.querySelectorAll('*[name]')].filter(elem => elem.invalid).forEach(elem => elem.invalid = false);
    }

    _showErrors({ detail }) {
        const form = this.shadowRoot.querySelector('iron-form');
        setErrorsOnForm(form, detail.errors);
    }
}

customElements.define('medico-form', MedicoForm);
