import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import BasePacientePerfil from '../components/base-paciente-perfil';
import NuevoServicioOrden from '../components/nuevo-servicio-orden';
import ServiciosOrden from '../components/servicios-orden';
import OrdenInfo from '../components/orden-info';
import '@apollo-elements/polymer/apollo-query';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-card/paper-card';
import '@polymer/iron-icon/iron-icon';
import '../elements';

/**
 * `mh-detalle-orden` Detalle de una orden.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisDetalleOrden extends PolymerElement {
    static get properties() {
        return {
            /** Id de la orden */
            ordenId: String,
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                header {
                    margin-bottom: 1rem;
                    padding: 1rem 1rem 0;
                    position: relative;
                }

                header > h1 {
                    margin: 0;
                    color: #676767;
                    line-height: 100%;
                    font-weight: 400;
                    font-size: 1.15rem;
                    text-transform: uppercase;
                }

                header > small {
                    font-size: 1rem;
                    display: block;
                    margin-top: .8rem;
                    color: #959595;
                }

                h2 {
                    color: #676767;
                    line-height: 100%;
                    font-weight: 400;
                    font-size: 1rem;
                    text-transform: uppercase;
                }

                paper-card {
                    width: 100%;
                }

                paper-button {
                    color: var(--app-primary-color);
                }

                #add-servicio {
                    float: right;
                }
            </style>

            <apollo-query query="[[query]]" data="{{data}}"></apollo-query>
            <base-paciente-perfil paciente="[[data.orden.paciente]]">
                <header>
                    <h1>Orden #[[data.orden.id]]</h1>
                </header>

                <paper-card>
                    <div class="card-content">
                        <orden-info orden="[[data.orden]]"></orden-info>
                    </div>
                </paper-card>

                <h2>Servicios</h2>
                <paper-button id="add-servicio" hidden$="[[!data.orden.canEdit]]"
                    on-click="_showNuevoServicioForm">agregar servicio
                </paper-button>
                <servicios-orden tratamientos="[[data.orden.tratamientos]]" convenio="[[data.orden.convenio.id]]"
                    institucion="[[data.orden.institucion.id]]">
                </servicios-orden>
            </base-paciente-perfil>
        `;
    }

    /**
      * Array of strings describing multi-property observer methods and their
      * dependant properties
      */
    static get observers() {
        return [
            '_fetchOrdenData(ordenId)',
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
            query OrdenDetalle($orden: ID!) {
                orden(id: $orden) {
                    id
                    ...OrdenInfo
                    convenio: plan {
                        ...NuevoServicioOrden
                    }
                    paciente {
                        ...BasePacientePerfil
                    }
                    tratamientos: serviciosRealizar {
                        ...ServiciosOrden
                    }
                }
            }
            ${OrdenInfo.fragment}
            ${ServiciosOrden.fragment}
            ${BasePacientePerfil.fragment}
            ${NuevoServicioOrden.fragment}
        `;
    }

    /**
     * Use for one-time configuration of your component after local
     * DOM is initialized.
     */
    ready() {
        super.ready();
    }

    /**
     * Fetches los datos de la orden.
     * @param {String} orden Id dela orden.
     */
    _fetchOrdenData(orden) {
        if (!orden) return;

        const queryElem = this.shadowRoot.querySelector('apollo-query');
        const variables = { orden };
        if (!queryElem.refetch(variables)) {
            queryElem.variables = variables;
        }
    }

    /** Muestra formulario para agregar nuevo servicio. */
    _showNuevoServicioForm() {
        const servicioForm = NuevoServicioOrden.instance;
        servicioForm.orden = this.data.orden;
        servicioForm.opened = true;
    }
}

customElements.define('mh-detalle-orden', MedhisDetalleOrden);
