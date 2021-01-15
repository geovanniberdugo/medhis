import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';
import { urlQueryToDict, updateFiltersOnUrl } from '../utils';

import '@polymer/polymer/lib/elements/dom-repeat';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/iron-selector/iron-selector';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-card/paper-card';
import '../components/sucursales-combo';
import '../components/citas-scheduler';
import '../components/medicos-combo';
import '../elements';

/**
 * `mh-agenda-citas` Página para ver las distintas agendas de citas.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisAgendaCitas extends PolymerElement {
    static get properties() {
        return {
            /**
             * Tipos de agenda.
             */
            tiposAgenda: {
                type: Array,
                value: () => [],
            },

            /**
             * Tipo de la agenda.
             */
            agenda: {
                type: String,
                value: 'm',
            },

            /**
             * Id de la sucursal.
             */
            sucursal: {
                type: String,
                value: '',
            },

            /**
             * Id del medico.
             */
            medico: {
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

                h2 {
                    text-align: center;
                }

                paper-card {
                    width: 100%;
                }

                paper-button[active] {
                    color: white;
                    background-color: var(--app-primary-color);
                }

                sucursales-combo {
                    margin-right: 5px;
                }

                @media (min-width: 56em) {
                    section {
                        display: flex;
                        align-items: center;
                    }

                    section sucursales-combo {
                        margin-left: auto;
                    }
                }
            </style>

            <apollo-query query="[[query]]" on-data-changed="_tiposAgendaFetched"></apollo-query>
            <paper-card>
                <div class="card-content">
                    <section>
                        <iron-selector selected="{{agenda}}" selectable="paper-button" selected-attribute="active" attr-for-selected="name">
                            <paper-button name="m" raised>Por medico</paper-button>
                            <template is="dom-repeat" items="[[tiposAgenda]]" as="tipoAgenda">
                                <paper-button name="[[tipoAgenda.id]]" raised>[[tipoAgenda.nombre]]</paper-button>
                            </template>
                        </iron-selector>
                        <sucursales-combo auto required selected-item="{{sucursalItem}}" value="{{sucursal}}"></sucursales-combo>
                        <medicos-combo auto hidden$="[[_hideMedicos(agenda)]]" required="[[!_hideMedicos(agenda)]]" sucursal="[[sucursal]]"
                            individuales activos value="{{medico}}" selected-item="{{medicoItem}}">
                        </medicos-combo>
                    </section>
                    <h2>[[sucursalItem.nombre]] - [[_titulo(agenda, medicoItem.nombreCompleto)]]</h2>
                    <citas-scheduler agenda="[[agenda]]" sucursal="[[sucursal]]" medico="[[medico]]"></citas-scheduler>
                </div>
            </paper-card>
        `;
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_setQueryParams(agenda, sucursal, medico)',
            '_setDuracionSlots(agenda, medicoItem.duracionCita)',
        ];
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
        this.query = gql`
            query TiposAgenda {
                tiposAgenda {
                    results {
                        id
                        duracion
                        nombre @title_case
                    }
                }
            }
        `;
    }

    /**
     * Use for one-time configuration of your component after local
     * DOM is initialized.
     */
    ready() {
        super.ready();
        this.allSet = true;
        this._setFiltersFromUrl();
    }

    _setDuracionSlots(agenda, duracionMedico) {
        const duracion = agenda === 'm' ? (duracionMedico || '00:10:00') : '00:20:00';
        this.shadowRoot.querySelector('citas-scheduler').slotDuration = duracion;
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        const { tipo, medico, sucursal } = urlQueryToDict();
        this.agenda = tipo || this.agenda;
        this.medico = medico || this.medico;
        this.sucursal = sucursal || this.sucursal;
    }

    /**
     * Actualiza la url.
     * @param {string} fecha
     * @param {string} medico
     * @param {string} sucursal
     */
    _setQueryParams(agenda, sucursal, medico) {
        if (!this.allSet) return;

        const filtros = Object.assign(
            {},
            agenda ? { tipo: agenda } : {},
            medico && agenda === 'm' ? { medico } : {},
            sucursal ? { sucursal } : {},
        );
        updateFiltersOnUrl(filtros, true);
    }

    /** Sets tipos de agenda. */
    _tiposAgendaFetched(e) {
        const { tiposAgenda } = e.detail.value;
        this.tiposAgenda = tiposAgenda.results;
    }

    /** Muestra o Oculta el combo de medicos. */
    _hideMedicos(agenda) {
        return agenda !== 'm';
    }

    /**
     * Si el tipo de agenda es 'm' se usa el nombre del medico, sino se usa el tipo de agenda.
     * @param {string} agenda Tipo de agenda
     * @param {string} medico Nombre del medico
     */
    _titulo(agenda, medico) {
        if (agenda === 'm') return medico;

        return this.tiposAgenda.length > 0 ? this.tiposAgenda.filter(t => t.id === agenda)[0].nombre : '';
    }
}

customElements.define('mh-agenda-citas', MedhisAgendaCitas);
