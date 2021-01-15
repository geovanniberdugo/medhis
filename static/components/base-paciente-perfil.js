import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import { css } from 'lit-element';
import gql from 'graphql-tag';

import PacienteInfo from './paciente-info';
import '@polymer/paper-icon-button/paper-icon-button';
import '@polymer/iron-media-query/iron-media-query';
import '@polymer/paper-listbox/paper-listbox';
import '@polymer/paper-item/paper-icon-item';
import '@polymer/iron-icon/iron-icon';

/**
 * `base-paciente-perfil` Layout base de la pagina de un paciente.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class BasePacientePerfil extends PolymerElement {
    static get properties() {
        return {
            /** Indica si el menu esta abierto. */
            openedMenu: {
                type: Boolean,
                value: false,
            },

            /** Menu seleccionado */
            selectedMenu: {
                type: String,
                value: '',
            },

            /** Datos del paciente */
            paciente: {
                type: Object,
                value: () => ({}),
            },
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                .container {
                    display: grid;
                    grid-gap: 10px;
                    grid-template-columns: 1fr;
                }

                section ::slotted(header) {
                    margin-bottom: 1rem;
                    padding: 1rem 1rem 0;
                    position: relative;
                }

                section {
                    position: var(--paciente-perfil-content-position, static);
                }

                nav {
                    top: 0;
                    bottom: 0;
                    z-index: 1;
                    width: 256px;
                    right: -300px;
                    position: absolute;
                    background-color: white;
                    transition: transform .3s ease-in-out;
                }

                nav[opened] {
                    transform: translateX(-300px);
                }

                a {
                    color: inherit;
                    text-decoration: none;
                }

                #menu {
                    right: 0;
                    top: 50%;
                    z-index: 1;
                    position: fixed;
                    background-color: white;
                }

                #scrim {
                    top: 0;
                    left: 0;
                    right: 0;
                    bottom: 0;
                    opacity: 0;
                    display: none;
                    position: absolute;
                    transition-property: opacity;
                    background: rgba(0, 0, 0, 0.5);
                }

                #scrim[opened] {
                    opacity: 1;
                    z-index: 1;
                    display: block;
                }

                @media (min-width: 600px) {
                    .container {
                        display: grid;
                        grid-gap: 10px;
                        grid-template-rows: auto 1fr;
                        grid-template-columns: 1fr fit-content(250px);

                        grid-template-areas:
                            "main paciente"
                            "main nav"
                    }

                    paciente-info {
                        grid-area: paciente;
                    }

                    nav {
                        width: auto;
                        grid-area: nav;
                        position: static;
                        background: transparent;
                    }
                    
                    section {
                        grid-area: main;
                    }

                    #menu {
                        display: none;
                    }

                    #menu-close {
                        display: none;
                    }
                }
            </style>

            <iron-media-query query="(min-width: 600px)" query-matches="{{large}}"></iron-media-query>
            <div id="scrim" opened$="[[openedMenu]]"></div>
            <paper-icon-button id="menu" on-click="_openMenu" icon="my-icons:arrow-back" hidden$="[[openedMenu]]"></paper-icon-button>
            <div class="container">
                <paciente-info mini$="[[!large]]" paciente="[[paciente]]"></paciente-info>
                <nav opened$="[[openedMenu]]">
                    <paper-icon-button id="menu-close" icon="my-icons:close" on-click="_closeMenu"></paper-icon-button>
                    <paper-listbox attr-for-selected="name" selected="{{selectedMenu}}">
                        <a hidden$="[[!paciente.detailUrl]]" href="[[paciente.detailUrl]]" tabindex="-1">
                            <paper-icon-item name="detalle">
                                <iron-icon icon="my-icons:person"></iron-icon> Datos
                            </paper-icon-item>
                        </a>
                        <a hidden$="[[!paciente.tratamientosUrl]]" href="[[paciente.tratamientosUrl]]" tabindex="-1">
                            <paper-icon-item name="tratamientos">
                                <iron-icon icon="my-icons:view-list"></iron-icon> Tratamientos
                            </paper-icon-item>
                        </a>
                        <a hidden$="[[!paciente.pagosUrl]]" href="[[paciente.pagosUrl]]" tabindex="-1">
                            <paper-icon-item name="pagos">
                                <iron-icon icon="my-icons:view-list"></iron-icon> Pagos
                            </paper-icon-item>
                        </a>
                        <a hidden$="[[!paciente.citasUrl]]" href="[[paciente.citasUrl]]" tabindex="-1">
                            <paper-icon-item name="citas">
                                <iron-icon icon="my-icons:view-list"></iron-icon> Citas
                            </paper-icon-item>
                        </a>
                        <a hidden$="[[!paciente.historiasUrl]]" href="[[paciente.historiasUrl]]" tabindex="-1">
                            <paper-icon-item name="historias">
                                <iron-icon icon="my-icons:view-list"></iron-icon> Historias
                            </paper-icon-item>
                        </a>
                    </paper-listbox>
                </nav>
                <section><slot></slot></section>
            </div>
        `;
    }

    /** Muestra el menu */
    _openMenu() {
        this.openedMenu = true;
    }

    /** Oculta el menu */
    _closeMenu() {
        this.openedMenu = false;
    }
}

customElements.define('base-paciente-perfil', BasePacientePerfil);

BasePacientePerfil.headerStyles = css`
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
`;

BasePacientePerfil.fragment = gql`
    fragment BasePacientePerfil on Paciente {
        id
        citasUrl
        pagosUrl
        detailUrl
        historiasUrl
        tratamientosUrl
        ...PacienteInfo
    }
    ${PacienteInfo.fragment}
`;

export default BasePacientePerfil;
