import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import { DateTime } from 'luxon';
import gql from 'graphql-tag';
// eslint-disable-next-line object-curly-newline
import { ESTADOS, urlQueryToDict, updateFiltersOnUrl, formatISOTime } from '../utils';

import '@vaadin/vaadin-grid/theme/material/vaadin-grid-filter-column';
import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker';
import '@vaadin/vaadin-grid/theme/material/vaadin-grid-sort-column';
import '@vaadin/vaadin-grid/theme/material/vaadin-grid';
import '@polymer/paper-icon-button/paper-icon-button';
import '@polymer/paper-progress/paper-progress';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-card/paper-card';
import '../components/sucursales-combo';
import '../components/es-date-picker';
import '../components/medicos-combo';
import '../elements';

/**
 * `mh-agenda-diaria` Página para mostrar la agenda diaria.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisAgendaDiaria extends PolymerElement {
    static get properties() {
        return {
            /**
             * Url base para la impresión.
             */
            baseUrl: {
                type: String,
                value: '',
            },

            /**
             * Url para imprimir
             */
            printUrl: {
                type: String,
                computed: '_printUrl(baseUrl, date, medico, sucursal)',
            },

            /**
             * Citas del dia;
             */
            citas: {
                type: Array,
                value: () => [],
            },

            /**
             * Citas filtradas del dia;
             */
            citasFiltradas: {
                type: Array,
                value: () => [],
            },

            /**
             * Fecha para ver las sesiones.
             */
            date: {
                type: String,
                observer: '_fetchCitas',
                value: DateTime.local().toISODate(),
            },

            /**
             * Medico seleccionado en filtro
             */
            medico: {
                type: String,
                value: '',
            },

            /**
             * Sucursal seleccionada en filtro
             */
            sucursal: {
                type: String,
                value: '',
            },

            /**
             * Indica si el usuario puede ver todas las citas
             */
            todasCitas: {
                type: Boolean,
                value: false,
            },
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                a {
                    color: var(--material-body-text-color);
                    text-decoration: none;
                }

                paper-card {
                    width: 100%;
                }

                paper-progress {
                    width: 100%;
                    --paper-progress-active-color: var(--app-primary-color);
                }

                .card-content {
                    display: grid;
                    grid-gap: 5px;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                }

                .card-content > a {
                    align-self: center;
                    justify-self: start;
                }

                .circle {
                    height: 0.8em;
                    width: 0.8em;
                    border-radius: 50%;
                    display: inline-block;
                }
            </style>
            
            <apollo-query query="[[query]]" loading="{{loading}}" on-data-changed="_citasFetched"></apollo-query>

            <paper-card>
                <div class="card-content">
                    <es-date-picker>
                        <vaadin-date-picker value="{{date}}" label="Fecha" required error-message="Debes escoger una fecha">
                        </vaadin-date-picker>
                    </es-date-picker>
                    <medicos-combo hidden$="[[!todasCitas]]" value="{{medico}}"></medicos-combo>
                    <sucursales-combo hidden$="[[!todasCitas]]" value="{{sucursal}}"></sucursales-combo>
                    <a href="[[printUrl]]" target="_blank" tabindex="-1" hidden$="[[!todasCitas]]">
                        <paper-button disabled="[[!printUrl]]">imprimir</paper-button>
                    </a>
                </div>
                <paper-progress indeterminate disabled="[[!loading]]"></paper-progress>
            </paper-card>
            <br><br>
            <vaadin-grid items="[[citasFiltradas]]">
                <vaadin-grid-sort-column header="Hora" flex-grow="0">
                    <template>[[_formatHora(item.inicio)]]</template>
                </vaadin-grid-sort-column>
                <vaadin-grid-filter-column header="Paciente" path="paciente.nombreCompleto">
                    <template>[[item.paciente.nombreCompleto]] <br> [[item.paciente.numeroDocumento]]</template>
                </vaadin-grid-filter-column>
                <vaadin-grid-column hidden$="[[!todasCitas]]" header="Profesional" path="medico.nombreCompleto"></vaadin-grid-column>
                <vaadin-grid-column header="Servicio" path="servicio.nombre"></vaadin-grid-column>
                <vaadin-grid-column header="IPS" path="institucion.nombre"></vaadin-grid-column>
                <vaadin-grid-column header="Empresa" path="convenio.cliente.nombre"></vaadin-grid-column>
                <vaadin-grid-sort-column header="Estado">
                    <template>
                        <span class="circle" style="background-color: [[_getEstadoColor(item.estadoActual.estado)]];"></span>
                        [[item.estadoActual.estadoLabel]]
                    </template>
                </vaadin-grid-sort-column>
                <vaadin-grid-column flex-grow="0" width="150px">
                    <template class="header"></template>
                    <template>
                        <a href="[[item.ordenUrl]]" tabindex="-1" title="Ver orden" hidden$="[[!item.ordenUrl]]">
                            <paper-icon-button icon="my-icons:remove-red-eye"></paper-icon-button>
                        </a>
                        <a href="[[item.visitaUrl]]" tabindex="-1" title="Ver visita" hidden$="[[!item.visitaUrl]]">
                            <paper-icon-button icon="my-icons:assignment"></paper-icon-button>
                        </a>
                    </template>
                </vaadin-grid-column>
            </vaadin-grid>
        `;
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_filterCitas(citas, medico, sucursal)',
            '_setQueryParams(date, medico, sucursal)',
        ];
    }

    /**
      * Instance of the element is created/upgraded. Useful for initializing
      * state, set up event listeners, create shadow dom.
      * @constructor
      */
    constructor() {
        super();
        this.query = gql`
            query AgendaDiaria($fecha: Date!) {
                citas(start: $fecha) {
                    results {
                        id
                        inicio
                        ordenUrl
                        visitaUrl
                        sucursal { id }
                        servicioPrestado { id }
                        servicio { id, nombre @title_case }
                        institucion { id, nombre @title_case }
                        medico { id, nombreCompleto @title_case }
                        convenio { id, cliente { id, nombre @title_case }}
                        estadoActual: historialActual { estado, estadoLabel }
                        paciente {
                            id
                            numeroDocumento
                            nombreCompleto @title_case
                        }
                    }
                }
            }
        `;
        this._setFiltersFromUrl();
    }

    /** Set los filtros con los params en la URL. */
    _setFiltersFromUrl() {
        const { fecha, medico, sucursal } = urlQueryToDict();
        this.date = fecha || this.date;
        this.medico = medico || this.medico;
        this.sucursal = sucursal || this.sucursal;
    }

    /**
     * Actualiza la url.
     * @param {string} fecha
     * @param {string} medico
     * @param {string} sucursal
     */
    _setQueryParams(fecha, medico, sucursal) {
        const filtros = Object.assign(
            {},
            fecha ? { fecha } : {},
            medico ? { medico } : {},
            sucursal ? { sucursal } : {},
        );
        updateFiltersOnUrl(filtros, true);
    }

    /**
     * Fetches las citas.
     * @param {string} newVal Fecha.
     */
    _fetchCitas(newVal) {
        if (!newVal) return;

        const query = this.shadowRoot.querySelector('apollo-query');
        const variables = { fecha: newVal };
        if (!query.refetch(variables)) {
            query.variables = variables;
        }
    }

    /**
     * Formatea la hora.
     *
     * @param {string} date Fecha a formatear.
     * @return {string}
     */
    _formatHora(date) {
        return formatISOTime(date);
    }

    /**
     * Indica el estado del color.
     * @param {string} estado Valor del estado
     */
    _getEstadoColor(estado) {
        return ESTADOS[estado].color;
    }

    /** Sets citas */
    _citasFetched(e) {
        const { citas } = e.detail.value;
        this.citas = citas.results;
    }

    /**
     * Filtra las citas por medico. Si no se escoge medico se muestran todas las citas.
     * @param {Array} citas Citas a filtrar.
     * @param {String} medico Id del medico.
     * @param {String} sucursal Id de la sucursal.
     */
    _filterCitas(citas, medico, sucursal) {
        const filtradasMedico = medico
            ? citas.filter(cita => cita.medico.id === medico)
            : [...citas];

        this.citasFiltradas = sucursal
            ? filtradasMedico.filter(cita => cita.sucursal.id === sucursal)
            : [...filtradasMedico];
    }

    /**
     * Construye la url para imprimir las citas del dia.
     * @param {string} url Url base de la impresión.
     * @param {string} fecha Dia de las citas a mostrar.
     * @param {string} medico Medico para filtrar las citas.
     * @param {string} sucursal Sucursal para filtrar las citas.
     */
    _printUrl(url, fecha, medico, sucursal) {
        if (!url || !fecha) return '';

        const addMedico = medico ? `&medico=${medico}` : '';
        const addSucursal = sucursal ? `&sucursal=${sucursal}` : '';
        return `${url}?fecha=${fecha}${addMedico}${addSucursal}`;
    }
}

customElements.define('mh-agenda-diaria', MedhisAgendaDiaria);
