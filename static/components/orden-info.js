import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import ConveniosCombo from './convenios-combo';
import '@polymer/paper-toggle-button/paper-toggle-button';
import '@polymer/paper-icon-button/paper-icon-button';
import '@apollo-elements/polymer/apollo-mutation';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-input/paper-input';
import '@polymer/iron-form/iron-form';
import './instituciones-combo';
import './tipos-usuario-combo';
import './afiliaciones-combo';
import './parentescos-combo';

/**
 * `orden-info` Datos de la orden.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class OrdenInfo extends PolymerElement {
    static get properties() {
        return {
            /**
             * Datos de la orden.
             */
            orden: {
                type: Object,
                value: () => ({}),
                observer: '_updateFormData',
            },

            /**
             * Datos del formulario.
             */
            formData: {
                type: Object,
                value: () => ({}),
            },

            /** Mostrar formulario */
            showForm: {
                type: Boolean,
                value: false,
            }
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                form {
                    display: grid;
                    grid-template-columns: 1fr;
                }

                iron-form[hidden] {
                    display: none;
                }

                paper-icon-button {
                    float: right;
                    color: var(--app-primary-color);
                }

                section {
                    display: grid;
                    grid-gap: 10px;
                    grid-template-columns: repeat(auto-fill, minmax(16em, 1fr))
                }

                section[hidden] {
                    display: none;
                }

                section p {
                    margin-bottom: 0;
                }

                section span {
                    color: gray;
                }

                paper-button {
                    color: var(--app-primary-color);
                }

                @media (min-width: 961px) {
                    form {
                        display: grid;
                        grid-gap: 10px;
                        align-items: start;
                        grid-template-columns: repeat(4, 1fr);
                    }

                    form .full {
                        grid-column: span 4;
                    }
                }
            </style>
            <apollo-mutation mutation="[[mutation]]" on-data-changed="_ordenEditada"></apollo-mutation>
            <paper-icon-button hidden$="[[!_showEditIcon(showForm, orden.canEdit)]]" icon="my-icons:edit" on-click="_showForm"></paper-icon-button>
            <section hidden$="[[showForm]]">
                <p>
                    <span>Institución:</span> [[orden.institucion.nombre]] <br>
                    <span>Convenio:</span> [[orden.convenio.nombreCompleto]] <br>
                    <span>Afiliación:</span> [[orden.afiliacionLabel]] <br>
                    <span>Tipo de usuario:</span> [[orden.tipoUsuarioLabel]] <br>
                    <span>Medico que ordena:</span> [[orden.medicoOrdena]] <br>
                </p>
                <p hidden$="[[!orden.asistioAcompanante]]">
                    <span>Acompañante</span> <br>
                    [[orden.acompanante.nombre]] <br>
                    [[orden.acompanante.parentescoLabel]] <br>
                    [[orden.acompanante.telefono]] <br>
                    [[orden.acompanante.direccion]] <br>
                </p>
            </section>
            <iron-form hidden$="[[!showForm]]">
                <form>
                    <instituciones-combo name$="institucion" required value="{{formData.institucion}}"></instituciones-combo>
                    <convenios-combo name$="convenio" nombre-completo required query="[[conveniosQuery]]" 
                        variables="[[_convenioVariables(formData.institucion)]]" value="{{formData.convenio}}">
                    </convenios-combo>
                    <afiliaciones-combo name$="afiliacion" required value="{{formData.afiliacion}}"></afiliaciones-combo>
                    <tipos-usuario-combo name$="tipoUsuario" required value="{{formData.tipoUsuario}}"></tipos-usuario-combo>
                    <paper-input required name$="medicoOrdena" label="Medico que ordena" value="{{formData.medicoOrdena}}"></paper-input>
                    <paper-toggle-button name$="asistio" class="full" checked="{{formData.asistioAcompanante}}">Asistio con acompañante</paper-toggle-button>
                    <parentescos-combo name$="parentesco" hidden$="[[!formData.asistioAcompanante]]" required="[[formData.asistioAcompanante]]"
                        value="{{formData.parentesco}}">
                    </parentescos-combo>
                    <paper-input label="Nombre completo" name$="nombre" hidden$="[[!formData.asistioAcompanante]]"
                        required="[[formData.asistioAcompanante]]" value="{{formData.nombre}}">
                    </paper-input>
                    <paper-input label="Telefono" name$="telefono" hidden$="[[!formData.asistioAcompanante]]" 
                        required="[[formData.asistioAcompanante]]" value="{{formData.telefono}}">
                    </paper-input>
                    <paper-input label="Dirección" name$="direccion" hidden$="[[!formData.asistioAcompanante]]"
                        required="[[formData.asistioAcompanante]]" value="{{formData.direccion}}">
                    </paper-input>
                </form>
                <paper-button on-click="save">Guardar</paper-button>
                <paper-button on-click="cancel">cancelar</paper-button>
            </iron-form>
        `;
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        this.conveniosQuery = gql`
            query ConveniosInstitucion($institucion: ID!) {
                convenios: planes(institucion: $institucion) {
                    results {
                        ...ConveniosCombo
                        cliente { id, sesionesAutorizacion }
                    }
                }
            }
            ${ConveniosCombo.fragment}
        `;

        this.mutation = gql`
            mutation EditarOrdenInfo($orden: OrdenInfoInput!) {
                editarOrdenInfo(input: $orden) {
                    ok
                    errors { field, messages }
                    orden {
                        ...OrdenInfo
                    }
                }
            }
            ${OrdenInfo.fragment}
        `;
    }

    /**
     * Gets las variables para el query del convenio.
     * @param {String} institucion Id de la institucion.
     */
    _convenioVariables(institucion) {
        return institucion ? { institucion } : null;
    }

    /** Llena los datos en el formulario */
    _updateFormData(newValue) {
        if (!newValue) return;

        const {
            convenio,
            afiliacion,
            tipoUsuario,
            institucion,
            acompanante,
            medicoOrdena,
            asistioAcompanante,
        } = newValue;

        this.formData = {
            afiliacion,
            tipoUsuario,
            medicoOrdena,
            asistioAcompanante,
            convenio: convenio && convenio.id,
            institucion: institucion && institucion.id,
            nombre: (acompanante && acompanante.nombre) || '',
            telefono: (acompanante && acompanante.telefono) || '',
            direccion: (acompanante && acompanante.direccion) || '',
            parentesco: (acompanante && acompanante.parentesco) || '',
        };
    }

    /**
     * Indica si se debe mostrar boton de editar orden.
     * @param {Boolean} showForm Indica si se esta mostrando el formulario.
     * @param {Boolean} canEdit Indica si tiene permiso de edición.
     */
    _showEditIcon(showForm, canEdit) {
        return canEdit && !showForm ;
    }

    /** Muestra el formulario */
    _showForm() {
        this.showForm = true;
    }

    /** Oculta el formulario */
    _hideForm() {
        this.showForm = false;
    }

    /** Orden editada */
    _ordenEditada(e) {
        if (!e.detail.value) return;

        const { editarOrdenInfo: { ok } } = e.detail.value;
        if (ok) this.showForm = false;
    }

    /**
     * Builds el input para la mutación.
     * @param {String} id Id de la orden.
     * @param {Object} data Datos del formulario.
     */
    _buildOrden(id, data) {
        const { convenio: plan, afiliacion, tipoUsuario, asistioAcompanante, institucion, medicoOrdena, ...acompanante } = data;
        const _acompanante = asistioAcompanante ? { acompanante } : {};
        return {
            id,
            plan,
            afiliacion,
            tipoUsuario,
            institucion,
            medicoOrdena,
            ..._acompanante,
            asistioAcompanante,
        };
    }

    /** Guarda la orden */
    save() {
        const form = this.shadowRoot.querySelector('iron-form');
        if (form.validate()) {
            const orden = this._buildOrden(this.orden.id, this.formData);
            this.shadowRoot.querySelector('apollo-mutation').mutate({ variables: { orden } });
        }
    }

    /** Oculta el formulario. */
    cancel() {
        this.showForm = false;
    }
}

customElements.define('orden-info', OrdenInfo);

OrdenInfo.fragment = gql`
    fragment OrdenInfo on Orden {
        id
        canEdit
        afiliacion
        tipoUsuario
        afiliacionLabel
        tipoUsuarioLabel
        asistioAcompanante
        medicoOrdena @title_case
        institucion { id, nombre @title_case }
        convenio: plan { id, nombreCompleto @title_case }
        acompanante {
            id
            nombre
            telefono
            direccion
            parentesco
            parentescoLabel
        }
    }
`;

export default OrdenInfo;
