import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import { notifyErrorMessage, notifySuccessMessage } from '../utils';

import '@polymer/paper-toggle-button/paper-toggle-button';
import '@polymer/polymer/lib/elements/dom-repeat';
import '@apollo-elements/polymer/apollo-mutation';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '@polymer/paper-fab/paper-fab';
import '@polymer/iron-form/iron-form';
import '../components/sucursales-combo';
import '../components/medicos-combo';
import '../elements';


const fieldNames = {
    f: 'fin',
    i: 'inicio',
    d: 'conDescanso',
    fd: 'finDescanso',
    id: 'inicioDescanso',
};

const groupByDia = (obj, horario) => {
    const [key, value] = horario;
    const [name, dia] = key.split('_');
    if ((name === 'fd' || name === 'id') && !value) return obj;

    if (!obj[dia]) {
        obj[dia] = { dia, [fieldNames[name]]: value };
    } else {
        obj[dia] = { ...obj[dia], [fieldNames[name]]: value };
    }

    return obj;
};

const GUARDAR_HORARIO_MUTATION = gql`
    mutation GuardarHorarioAtencion($medico: MedicoInput!, $sucursal: ID!) {
        guardarHorarioAtencion(input: $medico) {
            ok
            errors { field, messages }
            empleado {
                id
                horariosAtencion(sucursal: $sucursal) {
                    id
                    dia
                    fin
                    inicio
                    conDescanso
                    finDescanso
                    inicioDescanso
                }
            }
        }
    }
`;

/**
 * `mh-horario-atencion` Página para cambias los horarios de atencion de los medicos.
 *
 * @customElement
 * @polymer
 * @demo
 */
class MedhisHorarioAtencion extends PolymerElement {
    static get properties() {
        return {
            /**
             * Dias de la semana
             * @todo Traer de servidor.
             */
            dias: {
                type: Array,
                value: () => [
                    { nombre: 'Lunes', value: '1' },
                    { nombre: 'Martes', value: '2' },
                    { nombre: 'Miercoles', value: '3' },
                    { nombre: 'Jueves', value: '4' },
                    { nombre: 'Viernes', value: '5' },
                    { nombre: 'Sabado', value: '6' },
                    { nombre: 'Domingo', value: '7' },
                ],
            },

            /**
             * Id medico escogido
             */
            medicoId: {
                type: String,
                value: '',
            },

            /**
             * Id sucursal escogida
             */
            sucursalId: {
                type: String,
                value: '',
            },
        };
    }

    static get template() {
        return html`
<style>
    :host {
        display: block;
    }

    paper-card {
        width: 100%;
        margin-bottom: 10px;
    }

    paper-fab {
        right: 10px;
        bottom: 10px;
        position: fixed;
    }

    @media(min-width: 40em) {

        .filtros,
        .dates {
            display: flex;
            align-items: center;
            justify-content: space-around;
        }
    }
</style>

<apollo-mutation mutation="[[mutation]]" on-data-changed="_horarioGuardado">
</apollo-mutation>
<apollo-query query="[[query]]" data="{{data}}"></apollo-query>
<iron-form>
    <form>
        <paper-card>
            <div class="card-content filtros">
                <medicos-combo autofocus required value="{{medicoId}}"></medicos-combo>
                <sucursales-combo required value="{{sucursalId}}"></sucursales-combo>
            </div>
        </paper-card>
        <br>
        <template is="dom-repeat" items="[[dias]]" as="dia">
            <paper-card>
                <div class="card-content dates">
                    <h2>[[dia.nombre]]</h2>
                    <div>
                        <paper-toggle-button name="dispo_[[dia.value]]"
                            on-checked-changed="_disponibleChanged"
                            checked="[[_getValor(dia.value, 'noDisponible', data.medico.horariosAtencion)]]">
                            No atiende</paper-toggle-button>
                    </div>
                    <div class$="fe_[[index]]"
                        hidden$="[[_getValor(dia.value, 'noDisponible', data.medico.horariosAtencion)]]">
                        <paper-input name="i_[[dia.value]]" label="Inicio" type="time"
                            value="[[_getValor(dia.value, 'inicio', data.medico.horariosAtencion)]]">
                        </paper-input>
                        <paper-input name="f_[[dia.value]]" label="Fin" type="time"
                            value="[[_getValor(dia.value, 'fin', data.medico.horariosAtencion)]]">
                        </paper-input>
                    </div>
                    <div class$="desto_[[index]]"
                        hidden$="[[_getValor(dia.value, 'noDisponible', data.medico.horariosAtencion)]]">
                        <paper-toggle-button name="d_[[dia.value]]"
                            on-checked-changed="_descansoChanged"
                            checked="[[_getValor(dia.value, 'conDescanso', data.medico.horariosAtencion)]]">
                            ¿Descanso?</paper-toggle-button>
                    </div>
                    <div class$="des_[[index]]"
                        hidden$="[[_getValor(dia.value, 'noDisponible', data.medico.horariosAtencion)]]">
                        <paper-input name="id_[[dia.value]]" label="Inicio descanso"
                            type="time"
                            value="[[_getValor(dia.value, 'inicioDescanso', data.medico.horariosAtencion)]]">
                        </paper-input>
                        <paper-input name="fd_[[dia.value]]" label="Fin descanso"
                            type="time"
                            value="[[_getValor(dia.value, 'finDescanso', data.medico.horariosAtencion)]]">
                        </paper-input>
                    </div>
                </div>
            </paper-card>
        </template>
    </form>
</iron-form>
<paper-fab icon="my-icons:save" on-click="save">Guardar</paper-fab>`;
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_fetchHorarios(medicoId, sucursalId)'
        ];
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        this.mutation = GUARDAR_HORARIO_MUTATION;
        this.query = gql`
            query HorarioAtencionMedico($medico: ID!, $sucursal: ID!) {
                medico: empleado(id: $medico) {
                    id
                    horariosAtencion(sucursal: $sucursal) {
                        id
                        dia
                        fin
                        inicio
                        conDescanso
                        finDescanso
                        inicioDescanso
                    }
                }
            }
        `;
    }

    /**
     * Fetches los horarios.
     * @param {string} medico Medico id.
     * @param {string} sucursal Sucursal id.
     */
    _fetchHorarios(medico, sucursal) {
        if (!medico || !sucursal) return;

        const query = this.shadowRoot.querySelector('apollo-query');
        const variables = { medico, sucursal };
        if (!query.refetch(variables)) {
            query.variables = variables;
        }
    }

    /**
     * Obtiene el valor del campo indicado para el dia
     * @param {string} dia 
     * @param {string} campo 
     * @param {array} horarios 
     */
    _getValor(dia, campo, horarios = []) {
        const horario = horarios.filter(v => v.dia === dia);
        if (horario.length > 0) {
            return horario[0][campo];
        }

        if (campo === 'conDescanso') return false;
        return '';
    }

    /** Limpia los input del descanso si el check es false */
    _descansoChanged(e) {
        if (!e.detail.value) {
            const { index } = e.model;
            const inputs = [...this.shadowRoot.querySelectorAll(`.des_${index} > paper-input`)];
            inputs.forEach(input => {
                input.value = '';
            });
        }
    }

    /** Limpia los input si el check es true */
    _disponibleChanged(e) {
        const { index } = e.model;
        const divs = [...this.shadowRoot.querySelectorAll(`.des_${index}, .fe_${index}, .desto_${index}`)];
        if (e.detail.value) {
            const inputs = [...this.shadowRoot.querySelectorAll(`.des_${index} > paper-input, .fe_${index} > paper-input`)];
            inputs.forEach(input => {
                input.value = '';
            });
            divs.forEach(div => {
                div.setAttribute('hidden', true);
            })
        }
        else {
            divs.forEach(div => {
                div.removeAttribute('hidden');
            })
        }
    }

    /** Horario guardado */
    _horarioGuardado(e) {
        if (!e.detail.value) return;

        const { guardarHorarioAtencion: { ok } } = e.detail.value;
        if (ok) notifySuccessMessage(this, 'Horario guardado satisfactoriamente');
    }

    /** Valida los horarios. @todo */
    valid(horarios) {
        return true;
    }

    /** Guarda los horarios. */
    save() {
        const form = this.shadowRoot.querySelector('iron-form');
        const medico = this.shadowRoot.querySelector('medicos-combo').value;
        const sucursal = this.shadowRoot.querySelector('sucursales-combo').value;
        const { prefix, suffix, ...formData } = form.serializeForm();
        const data = Object.entries(formData).reduce(groupByDia, {});
        const horarios = Object.values(data).filter(v => !!v.inicio && !!v.fin);

        if (form.validate() && this.valid(horarios)) {
            this.shadowRoot.querySelector('apollo-mutation').mutate({
                variables: {
                    sucursal,
                    medico: {
                        horarios,
                        sucursal,
                        id: medico,
                    }
                }
            });
        } else {
            notifyErrorMessage(this, 'Hubo un error por favor verifica');
        }
    }
}

customElements.define('mh-horario-atencion', MedhisHorarioAtencion);
