import { LitElement, html, css } from 'lit-element';
import { DateTime } from 'luxon';
import gql from 'graphql-tag';
import { setErrorsOnForm, getAge } from '../utils';

import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker';
import '@vaadin/vaadin-text-field/theme/material/vaadin-number-field';
import '@vaadin/vaadin-text-field/theme/material/vaadin-email-field';
import '@vaadin/vaadin-text-field/theme/material/vaadin-text-field';
import '@vaadin/vaadin-upload/theme/material/vaadin-upload';
import '@polymer/paper-toggle-button/paper-toggle-button';
import '@polymer/iron-form/iron-form';
import './tipos-documento-combo';
import './grupo-sanguineo-combo';
import './grupos-etnicos-combo';
import './estados-civil-combo';
import './parentescos-combo';
import './profesiones-combo';
import './procedencia-combo';
import './es-date-picker';
import './poblados-combo';
import './generos-combo';
import './zona-combo';

const fillOptions = {
    FULL: 'full',
    NOEDIT: 'noedit',
    PARTIAL: 'partial',
};

/**
 * `paciente-form` Formulario de un paciente.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class PacienteForm extends LitElement {
    static get properties() {
        return {
            paciente: { type: Object },

            /** Opciones de llenado. 'full', 'partial', 'noedit' */
            fillOption: { type: String },
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
                display: contents;
            }

            fieldset[hidden] {
                display: none;
            }

            legend {
                padding: 10px 0px;
                font-size: medium;
                font-weight: bold;
                text-transform: uppercase;
            }

            vaadin-date-picker {
                width: 100%;
            }

            vaadin-number-field {
                width: 100%;
            }

            /* Large devices (desktops, 640px and up) */
            @media (min-width: 40em) {
                form {
                    grid-gap: 10px;
                    grid-template-columns: 1fr 1fr;
                }

                legend {
                    grid-column: 1 / -1;
                }
            }
        `;
    }

    render() {
        const { isMinorAge, paciente = {}, fillOption, fechaNacimiento } = this;
        const disableField = fillOption === fillOptions.NOEDIT;
        const isFullField = fillOption === fillOptions.FULL;

        return html`
            <iron-form>
                <form>
                    <input type="hidden" name="opcionLlenado" value="${fillOption}">
                    <fieldset>
                        <legend>Datos Personales</legend>
                        <vaadin-text-field name="primerNombre" label="Primer nombre" required autofocus
                            value="${paciente.primerNombre || ''}" ?disabled="${disableField}">
                        </vaadin-text-field>
                        <vaadin-text-field name="segundoNombre" label="Segundo nombre"
                            value="${paciente.segundoNombre || ''}" ?disabled="${disableField}">
                        </vaadin-text-field>
                        <vaadin-text-field name="primerApellido" label="Primer apellido" required
                            value="${paciente.primerApellido || ''}" ?disabled="${disableField}">
                        </vaadin-text-field>
                        <vaadin-text-field name="segundoApellido" label="Segundo apellido"
                            value="${paciente.segundoApellido || ''}" ?disabled="${disableField}">
                        </vaadin-text-field>
                        <tipos-documento-combo name="tipoDocumento" required value="${paciente.tipoDocumento || ''}"
                            ?disabled="${disableField}">
                        </tipos-documento-combo>
                        <vaadin-text-field name="numeroDocumento" label="Número de documento" required
                            value="${paciente.numeroDocumento || ''}" ?disabled="${disableField}">
                        </vaadin-text-field>
                        <generos-combo name="genero" required value="${paciente.genero || ''}" ?disabled="${disableField}"></generos-combo>
                        <estados-civil-combo name="estadoCivil" value="${paciente.estadoCivil || ''}" ?disabled="${disableField}" ?required="${isFullField}">
                        </estados-civil-combo>
                        <es-date-picker>
                            <vaadin-date-picker name="fechaNacimiento" label="Fecha de nacimiento" required value="${paciente.fechaNacimiento || ''}"
                                .max="${DateTime.local().toISODate()}" @value-changed="${this.handleFechaNacimientoChanged}" ?disabled="${disableField}">
                            </vaadin-date-picker>
                        </es-date-picker>
                        <p>Edad <br>${getAge(fechaNacimiento)}</p>
                        <vaadin-email-field name="email" label="Email" value="${paciente.email || ''}" ?disabled="${disableField}" ?required="${isFullField}">
                        </vaadin-email-field>
                        <vaadin-text-field name="direccion" label="Dirección" required value="${paciente.direccion || ''}"
                            ?disabled="${disableField}">
                        </vaadin-text-field>
                        <vaadin-number-field name="telefono" label="Teléfono del domicilio" value="${paciente.telefono || ''}"
                            ?disabled="${disableField}">
                        </vaadin-number-field>
                        <vaadin-number-field name="celular" label="Celular" value="${paciente.celular || ''}"
                            ?disabled="${disableField}">
                        </vaadin-number-field>
                        <vaadin-text-field name="telefono2" label="Telefono 2" value="${paciente.telefono2 || ''}"
                            ?disabled="${disableField}">
                        </vaadin-text-field>
                        <poblados-combo name="lugarResidencia" label="Lugar de residencia" ?disabled="${disableField}" ?required="${isFullField}"
                            value="${(paciente.lugarResidencia && paciente.lugarResidencia.id) || ''}">
                        </poblados-combo>
                        <poblados-combo name="lugarNacimiento" label="Donde nacio" ?disabled="${disableField}" ?required="${isFullField}"
                            value="${(paciente.lugarNacimiento && paciente.lugarNacimiento.id) || ''}">
                        </poblados-combo>
                    </fieldset>
                    <fieldset>
                        <legend>Datos Responsable</legend>
                        <parentescos-combo name="parentescoResponsable" value="${paciente.parentescoResponsable || ''}"
                            ?disabled="${disableField}" ?required="${isFullField}">
                        </parentescos-combo>
                        <vaadin-text-field name="nombreResponsable" label="Nombre completo" value="${paciente.nombreResponsable || ''}"
                            ?disabled="${disableField}" ?required="${isFullField}">
                        </vaadin-text-field>
                        <vaadin-text-field name="direccionResponsable" label="Dirección" value="${paciente.direccionResponsable || ''}"
                            ?disabled="${disableField}" ?required="${isFullField}">
                        </vaadin-text-field>
                        <vaadin-text-field name="telefonoResponsable" label="Telefono" value="${paciente.telefonoResponsable || ''}"
                            ?disabled="${disableField}" ?required="${isFullField}">
                        </vaadin-text-field>
                    </fieldset>
                    <fieldset id="minor" ?hidden="${!isMinorAge}">
                        <legend>Datos Menor de Edad</legend>
                        <vaadin-text-field name="identificacionPadre" label="Identificación padre" ?disabled="${!isMinorAge || disableField}"
                            value="${paciente.identificacionPadre || ''}">
                        </vaadin-text-field>
                        <vaadin-text-field name="nombrePadre" label="Nombre completo padre" ?disabled="${!isMinorAge || disableField}"
                            value="${paciente.nombrePadre || ''}">
                        </vaadin-text-field>
                        <vaadin-number-field name="telefonoPadre" label="Telefono padre" ?disabled="${!isMinorAge || disableField}"
                            value="${paciente.telefonoPadre || ''}">
                        </vaadin-number-field>
                        <vaadin-text-field name="identificacionMadre" label="Identificación madre" ?disabled="${!isMinorAge || disableField}"
                            value="${paciente.identificacionMadre || ''}">
                        </vaadin-text-field>
                        <vaadin-text-field name="nombreMadre" label="Nombre completo madre" ?disabled="${!isMinorAge || disableField}"
                            value="${paciente.nombreMadre || ''}">
                        </vaadin-text-field>
                        <vaadin-number-field name="telefonoMadre" label="Telefono madre" ?disabled="${!isMinorAge || disableField}"
                            value="${paciente.telefonoMadre || ''}">
                        </vaadin-number-field>
                    </fieldset>
                    <fieldset>
                        <legend>Datos de la empresa</legend>
                        <vaadin-text-field name="empresa" label="Empresa donde labora" value="${paciente.empresa || ''}"
                            ?disabled="${disableField}" ?required="${isFullField}">
                        </vaadin-text-field>
                        <vaadin-text-field name="direccionEmpresa" label="Dirección" value="${paciente.direccionEmpresa || ''}"
                            ?disabled="${disableField}" ?required="${isFullField}">
                        </vaadin-text-field>
                        <vaadin-text-field name="telefonoEmpresa" label="Telefono" value="${paciente.telefonoEmpresa || ''}"
                            ?disabled="${disableField}" ?required="${isFullField}">
                        </vaadin-text-field>
                    </fieldset>
                    <fieldset>
                        <legend>Datos Adicionales</legend>
                        <zonas-combo name="zona" value="${paciente.zona || ''}" ?disabled="${disableField}" ?required="${isFullField}"></zonas-combo>
                        <profesiones-combo name="profesion" value="${(paciente.profesion && paciente.profesion.id) || ''}"
                            ?disabled="${disableField}">
                        </profesiones-combo>
                        <grupos-sanguineos-combo name="grupoSanguineo" value="${paciente.grupoSanguineo || ''}"
                            ?disabled="${disableField}">
                        </grupos-sanguineos-combo>
                        <grupos-etnicos-combo name="grupoEtnico" value="${paciente.grupoEtnico || ''}" ?disabled="${disableField}">
                        </grupos-etnicos-combo>
                        <procedencias-combo name="procedencia" value="${paciente.procedencia || ''}" ?disabled="${disableField}">
                        </procedencias-combo>
                        <paper-toggle-button name="activo" ?checked="${paciente.activo}" ?disabled="${disableField}">Activo</paper-toggle-button>
                        <div>
                            <h4>Foto</h4>
                            <vaadin-upload name="foto" no-auto max-files="${disableField ? 0 : 1}" accept="image/*"
                                .files="${this.setUploadedFile(paciente.foto)}">
                            </vaadin-upload>
                        </div>
                        <div>
                            <h4>Firma</h4>
                            <vaadin-upload name="firma" no-auto max-files="${disableField ? 0 : 1}" accept="image/*"
                                .files="${this.setUploadedFile(paciente.firma)}">
                            </vaadin-upload>
                        </div>
                    </fieldset>
                </form>
            </iron-form>
        `;
    }

    constructor() {
        super();
        this.fillOption = fillOptions.FULL;
    }

    set isMinorAge(birthdate) {
        const oldVal = this._isMinorAge;

        const MAYORIA_EDAD = 18;
        const { years } = DateTime.fromISO(birthdate).diffNow('years').toObject();
        this._isMinorAge = years >= 0 || Math.abs(years) < MAYORIA_EDAD;
        this.requestUpdate('isMinorAge', oldVal);
    }

    get isMinorAge() {
        return this._isMinorAge;
    }

    get value() {
        const fotoElem = this.shadowRoot.querySelector('vaadin-upload[name="foto"]');
        const firmaElem = this.shadowRoot.querySelector('vaadin-upload[name="firma"]');
        const {
            zona,
            input,
            suffix,
            prefix,
            'file-list': a,
            'add-button': b,
            'drop-label': c,
            'drop-label-icon': d,
            estadoCivil,
            grupoEtnico,
            procedencia,
            grupoSanguineo,
            parentescoResponsable,
            ...data
        } = this._form.serializeForm();

        return {
            ...data,
            ...(zona && { zona }),
            ...(estadoCivil && { estadoCivil }),
            ...(grupoEtnico && { grupoEtnico }),
            ...(procedencia && { procedencia }),
            ...(grupoSanguineo && { grupoSanguineo }),
            ...(fotoElem.files.length > 0 && fotoElem.files[0] instanceof File && { foto: fotoElem.files[0] }),
            ...(parentescoResponsable && { parentescoResponsable }),
            ...(firmaElem.files.length > 0 && firmaElem.files[0] instanceof File && { firma: firmaElem.files[0] }),
        };
    }

    // Lifecycles
    firstUpdated() {
        this._form = this.shadowRoot.querySelector('iron-form');
        // Hack to display guardian data when edit/show patient data.
        if (this.isMinorAge) this.requestUpdate();
    }

    handleFechaNacimientoChanged({ target }) {
        this.isMinorAge = target.value;
        this.fechaNacimiento = target.value;
    }

    setUploadedFile(name) {
        return name ? [{ name, progress: 100, complete: true }] : [];
    }

    resetRequiredDisabledFields() {
        // eslint-disable-next-line no-param-reassign
        [...this.shadowRoot.querySelectorAll('form vaadin-upload')].forEach(elem => elem.maxFiles = 1);
        [...this.shadowRoot.querySelectorAll('form *[name]')].forEach((elem) => {
            // eslint-disable-next-line no-param-reassign
            elem.disabled = false;
            // eslint-disable-next-line no-param-reassign
            elem.required = false;
        });
    }

    disableAllFields() {
        // eslint-disable-next-line no-param-reassign
        [...this.shadowRoot.querySelectorAll('form *[name]')].forEach(elem => elem.disabled = true);
        // eslint-disable-next-line no-param-reassign
        [...this.shadowRoot.querySelectorAll('form vaadin-upload')].forEach(elem => elem.maxFiles = 0);
    }

    requireFields(fields) {
        const selector = fields.map(name => `*[name="${name}"]`).join(',');
        // eslint-disable-next-line no-param-reassign
        [...this.shadowRoot.querySelectorAll(selector)].forEach(elem => elem.required = true);
    }

    setFormErrors(errors) {
        setErrorsOnForm(this._form, errors);
        this._setErrorsOnUpload('foto', errors);
        this._setErrorsOnUpload('firma', errors);
    }

    _setErrorsOnUpload(name, errors) {
        const msg = errors.filter(error => error.field === 'foto').map(error => error.messages).flat().join('.');
        if (msg) {
            const elem = this.shadowRoot.querySelector(`vaadin-upload[name="${name}"]`);
            elem.files = elem.files.map(file => ({ ...file, complete: false, error: msg }));
        }
    }

    reset() {
        // eslint-disable-next-line no-param-reassign
        [...this.shadowRoot.querySelectorAll('vaadin-upload')].forEach(input => input.files = []);
        this._form.reset();
    }

    validate() {
        // Set rules before validation
        this._setValidationRulesOnPhone();
        this._setValidationRulesOnMinorGuardianFields();
        return this._form.validate();
    }

    _setValidationRulesOnPhone() {
        const celElem = this.shadowRoot.querySelector('*[name="celular"]');
        const telElem = this.shadowRoot.querySelector('*[name="telefono"]');
        const { value: celular } = celElem;
        const { value: telefono } = telElem;
        celElem.invalid = false;
        telElem.invalid = false;

        if (!celular && !telefono) {
            this._setRequiredOn([celElem, telElem], true);
        } else {
            this._setRequiredOn([celElem, telElem], false);
        }
    }

    _setValidationRulesOnMinorGuardianFields() {
        const fatherFields = this._guardianFieldsByName('Padre');
        const motherFields = this._guardianFieldsByName('Madre');
        const allFields = [...motherFields, ...fatherFields];
        // eslint-disable-next-line no-param-reassign
        allFields.forEach(field => field.invalid = false);

        if (this.fillOption !== fillOptions.FULL || !this.isMinorAge) {
            this._setRequiredOn(allFields, false);
            return;
        }

        const motherDataIsFilled = this._isAnyFieldFilled(motherFields);
        const fatherDataIsFilled = this._isAnyFieldFilled(fatherFields);
        if (!motherDataIsFilled && !fatherDataIsFilled) {
            // eslint-disable-next-line no-param-reassign
            allFields.forEach(field => field.required = true);
        } else {
            if (motherDataIsFilled) {
                this._setRequiredOn(motherFields, true);
            } else {
                this._setRequiredOn(motherFields, false);
            }
            if (fatherDataIsFilled) {
                this._setRequiredOn(fatherFields, true);
            } else {
                this._setRequiredOn(fatherFields, false);
            }
        }
    }

    /**
     * @param {Array} fields
     * @param {Boolean} value
     */
    _setRequiredOn(fields, value) {
        // eslint-disable-next-line no-param-reassign
        fields.forEach(field => field.required = value);
    }

    /**
     * Gets los inputs del guardian del menor de edad.
     * @param {String} parent 'Madre' o 'Padre'
     */
    _guardianFieldsByName(parent) {
        const fields = ['nombre', 'telefono', 'identificacion'];
        return fields.map(fieldName => this.shadowRoot.querySelector(`*[name="${fieldName}${parent}"]`));
    }

    /**
     * Indica si tiene algún campo lleno.
     * @param {Array} fields
     */
    _isAnyFieldFilled(fields) {
        return fields.some(field => !!field.value);
    }
}

customElements.define('paciente-form', PacienteForm);

PacienteForm.fragment = gql`
    fragment PacienteForm on Paciente {
        id
        zona
        foto
        firma
        email
        genero
        activo
        celular
        empresa
        telefono
        telefono2
        direccion
        estadoCivil
        grupoEtnico
        procedencia
        nombrePadre
        nombreMadre
        primerNombre
        telefonoMadre
        telefonoPadre
        segundoNombre
        tipoDocumento
        grupoSanguineo
        primerApellido
        segundoApellido
        numeroDocumento
        fechaNacimiento
        telefonoEmpresa
        profesion { id }
        direccionEmpresa
        nombreResponsable
        identificacionMadre
        identificacionPadre
        telefonoResponsable
        direccionResponsable
        parentescoResponsable
        lugarNacimiento { id }
        lugarResidencia { id }
    }
`;

export default PacienteForm;
