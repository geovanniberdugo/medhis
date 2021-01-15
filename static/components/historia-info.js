import { DATE_READABLE_FORMAT, formatISODate, formatISOTime, notifySuccessMessage, TIME_FORMAT } from '../utils';
import { ApolloMutation } from '@apollo-elements/lit-apollo';
import { css, html, LitElement } from 'lit-element';
import gql from 'graphql-tag';

import '@polymer/iron-selector/iron-selector';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/iron-pages/iron-pages';
import { cardCss } from './common-css';
import '@polymer/iron-icon/iron-icon';


const ELIMINAR_HISTORIA_MUTATION = gql`
    mutation BorrarEncuentro($encuentro: ID!) {
        borrarEncuentro(id: $encuentro) {
            ok
            historia { id }
        }
    }
`;

/**
 * `eliminar-historia` Componente para eliminar hiistoria.
 */
class EliminarHistoria extends ApolloMutation {
    static get properties() {
        return {
            id: { type: String },
            opened: { type: Boolean },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }
        `;
    }

    render() {
        const { opened, loading } = this;

        return html`
            <paper-dialog ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                <p><b>¿Esta seguro que deseas eliminar la historia?</b></p>
                <div class="buttons">
                    <paper-button dialog-dismiss>CANCELAR</paper-button>
                    <paper-button ?disabled="${loading}" @click="${this._eliminar}">ELIMINAR</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.opened = false;
    }

    _eliminar(e) {
        e.stopPropagation();
        this.mutate({
            variables: { encuentro: this.id },
            mutation: ELIMINAR_HISTORIA_MUTATION,
            refetchQueries: ['HistoriasPaciente'],
        });
    }

    open() {
        this.opened = true;
    }

    onCompleted({ borrarEncuentro }) {
        const { ok } = borrarEncuentro;
        if (ok) {
            this.opened = false;
            notifySuccessMessage(this, 'Historia eliminada satifastoriamente');
        }
    }
}

customElements.define('eliminar-historia', EliminarHistoria);

const ABRIR_HISTORIA_MUTATION = gql`
    mutation AbrirHistoria($historia: ID!) {
        abrirHistoria(id: $historia) {
            historia { 
                id
                canAbrir
                printUrl
                detailUrl
            }
        }
    }
`;

/**
 * `abrir-historia` Componente para abrir hiistoria.
 */
class AbrirHistoria extends ApolloMutation {
    static get properties() {
        return {
            id: { type: String },
            opened: { type: Boolean },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }
        `;
    }

    render() {
        const { opened, loading } = this;

        return html`
            <paper-dialog ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                <p><b>¿Esta seguro que deseas abrir la historia?</b></p>
                <div class="buttons">
                    <paper-button dialog-dismiss>CANCELAR</paper-button>
                    <paper-button ?disabled="${loading}" @click="${this._abrir}">ABRIR</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.opened = false;
    }

    _abrir(e) {
        e.stopPropagation();
        this.mutate({
            variables: { historia: this.id },
            mutation: ABRIR_HISTORIA_MUTATION,
        });
    }

    open() {
        this.opened = true;
    }

    onCompleted({ abrirHistoria }) {
        const { historia } = abrirHistoria;
        if (historia) {
            this.opened = false;
            notifySuccessMessage(this, 'Historia abierta satifastoriamente');
        }
    }
}

customElements.define('abrir-historia', AbrirHistoria);

/**
 * `historia-info` Informacion de una historia de un paciente.
 */
class HistoriaInfo extends LitElement {
    static get properties() {
        return {
            opened: { 
                type: Boolean,
                reflect: true,
            },

            disabled: {
                type: Boolean,
                reflect: true,
            },

            historia: { type: Object },
            selectedContent: { type: String },
        };
    }

    static get styles() {
        const base = css`
            :host {
                display: block;
            }

            ul {
                margin: 0;
                padding: 0;
            }

            li {
                cursor: pointer;
                list-style: none;
                margin-bottom: 5px;
            }

            div.collapse {
                display: grid;
                grid-gap: 5px;
                align-items: center;
                grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
            }

            div.collapse p {
                margin: 5px 0;
            }

            div.collapse p:nth-child(2) span {
                font-size: 14px;
                color: var(--app-primary-color);
            }

            iron-icon, paper-icon-button {
                padding: 5px;
                color: initial;
                border: 1px solid;
                border-radius: 20px;
            }

            .card {
                background-color: var(--historia-info-background-color, white);
            }

            .label {
                color: grey;
            }

            .center {
                text-align: center;
            }

            .chip {
                color: #5f6368;
                padding: 2px 12px;
                border-radius: 15px;
                display: inline-block;
                box-sizing: border-box;
                box-shadow: inset 0 0 0 1px rgba(100,121,143,0.302);
            }

            /* Expanded */
            header {
                margin-bottom: 15px;
            }

            header > * {
                margin: 0;
            }

            header h2 {
                margin-bottom: 10px;
                color: var(--app-primary-color);
            }

            header p {
                font-size: 14px;
            }

            #tabs {
                font-size: 14px;
            }

            #tabs paper-button[active] {
                color: white;
                background-color: var(--app-primary-color);
            }

            #content {
                margin-top: 10px;
            }

            #content div:first-child {
                columns: 2 20em;
            }

            #content .record-title {
                padding: 3px;
                font-size: 10pt;
                margin-bottom: 0px;
                text-transform: capitalize;
                background-color: #d3d3d396;
                /* color: var(--app-primary-color); */
            }

            #content p {
                margin: 5px;
                font-size: 11pt;
            }

            #content .chip a {
                color: inherit;
                text-decoration: none;
            }

            #creation-date {
                margin: 6px 0;
                font-size: 13px;
            }

            #actions {
                padding: 5px;
                display: flex;
                justify-content: center;
                border-top: 1px solid lightgray;
            }

            #actions a {
                color: inherit;
                text-decoration: inherit;
            }
        `;

        return [cardCss, base];
    }

    render() {
        const { historia, opened, selectedContent } = this;

        return opened ? this.fullRecord(historia, selectedContent) : this.reduceRecord(historia);
    }

    reduceRecord(historia) {
        return html`
            <div class="card collapse">
                <p>
                    ${formatISODate(historia.cita.inicio, { weekday: 'long' })} <br>
                    ${formatISODate(historia.cita.inicio, DATE_READABLE_FORMAT)} <br>
                    ${formatISOTime(historia.cita.inicio)}
                </p>
                <p>
                    ${historia.formato.nombre} <br>
                    <span>Por ${historia.medico.nombreCompleto}</span>
                </p>
                <p>
                    <span class="label">Servicio</span> <br>
                    ${historia.cita.servicio.nombre}
                </p>
            </div>
        `;
    }

    fullRecord(historia, selectedContent) {
        return html`
            <div class="card expanded">
                <header>
                    <h2>${historia.formato.nombre}</h2>
                    <div>
                        <p>
                            <span class="label">Por</span> ${historia.medico.nombreCompleto} <br>
                            ${formatISODate(historia.cita.inicio, { ...DATE_READABLE_FORMAT, ...TIME_FORMAT })} <br>
                            <span class="label">Servicio:</span> ${historia.cita.servicio.nombre}
                        </p>

                    </div>
                </header>

                <section id="tabs" @click="${e => e.stopPropagation()}">
                    <iron-selector selected="${selectedContent}" selected-attribute="active" @selected-changed="${e => this.selectedContent = e.detail.value}">
                        <paper-button>CONTENIDO</paper-button>
                        <paper-button>ADJUNTOS</paper-button>
                    </iron-selector>
                </section>

                <section id="content">
                    <iron-pages selected="${selectedContent}">
                        <div>${this.recordContent(historia.printContent)}</div>
                        <div>${this.recordAttachments(historia.adjuntos)}</div>
                    </iron-pages>
                </section>
                <p id="creation-date" class="label">creado el ${historia.fecha}</p>
                <section id="actions" @click="${e => e.stopPropagation()}">
                    ${historia.detailUrl && html`<a href="${historia.detailUrl}"><paper-button>Editar</paper-button></a>`}
                    ${historia.printUrl && html`<a href="${historia.printUrl}"><paper-button>Imprimir</paper-button></a>`}
                    ${historia.canAbrir ? html`<paper-button @click="${this._abrir}">Abrir</paper-button>` : ''}
                    ${historia.canDelete && html`<paper-button @click="${this._eliminar}">Eliminar</paper-button>`}
                    <eliminar-historia id="${historia.id}"></eliminar-historia>
                    <abrir-historia id="${historia.id}"></abrir-historia>
                </section>
            </div>
        `;
    }

    recordContent(content) {
        const _content = JSON.parse(content);
        return _content.map(field => {
            switch(field.type) {
                case 'title':
                    return html`<h2 class="record-title center">${field.label}</h2>`;
                case 'subtitle':
                    return html`<h3>${field.label}</h3>`;
                case 'subtitle2':
                    return html`<h4>${field.label}</h4>`;
                case 'space':
                    return html`<br>`;
                case 'text':
                    return html`<p>${field.label ? html`<strong>${field.label}:</strong>` : ''} ${field.value}</p>`;
                case 'table':
                    return html`
                        <h4>${field.label}</h4>
                        <table>
                        ${field.value.map(row => html`
                            <tr>
                                ${row.items.map((e, d) => html`<td>${d}</td>`)}
                            </tr>
                        `)}
                        </table>
                    `;
                case 'canvas':
                    return html`
                        <h4>${field.label}</h4>
                        <div class="canvas" data-image="${field.image}" data-data="${field.value}"></div>
                    `;
            };
        });
    }

    recordAttachments(adjuntos) {
        return html`
        <ul @click="${e => e.stopPropagation()}">
            ${adjuntos.map(adjunto => html`
                <li class="chip"><a target="_blank" href="${adjunto.archivo.url}">${adjunto.archivo.nombre}</a></li>
            `)}
        </ul>
        `;
    }

    constructor() {
        super();
        this.opened = false;
        this.disabled = false;
        this.selectedContent = '0';
    }

    _eliminar() {
        this.shadowRoot.querySelector('eliminar-historia').open();
    }

    _abrir() {
        this.shadowRoot.querySelector('abrir-historia').open();
    }
}

customElements.define('historia-info', HistoriaInfo);

HistoriaInfo.fragment = gql`
    fragment HistoriaInfo on Historia {
        id
        canAbrir
        printUrl
        detailUrl
        canDelete
        printContent
        fecha @date(format: "DD/MM/YYYY")
        formato { id, nombre @title_case }
        adjuntos { id, archivo { nombre, url } }
        medico: proveedor { id, nombreCompleto @title_case }
        cita {
            id
            inicio
            servicio { id, nombre @title_case }
        }
    }
`;

export default HistoriaInfo;