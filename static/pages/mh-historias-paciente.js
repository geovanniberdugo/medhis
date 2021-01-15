import { ApolloQuery } from '@apollo-elements/lit-apollo';
import { repeat } from 'lit-html/directives/repeat';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';

import BasePacientePerfil from '../components/base-paciente-perfil';
import HistoriaInfo from '../components/historia-info';
import { progressCss } from '../components/common-css';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-button/paper-button';
import '../components/formatos-combo';
import '../components/medicos-combo';
import '../elements';

/**
 * `mh-historias-paciente` Historias de un paciente.
 */
class MedhisHistoriasPaciente extends ApolloQuery {
    static get properties() {
        return {
            pacienteId: { type: String },
        };
    }

    static get styles() {
        const base = css`
            :host {
                display: block;
            }

            a {
                color: inherit;
            }

            ul {
                margin: 0;
                padding: 0;
            }

            li {
                list-style: none;
                margin-bottom: 5px;
            }

            historia-info:not([opened]):hover {
                cursor: pointer;
                --historia-info-background-color: #f5f2f2;
            }

            historia-info[opened] {
                cursor: pointer;
            }

            historia-info[disabled] {
                opacity: 0.5;
                cursor: default;
                pointer-events: none;
            }

            #more {
                text-align: center;
            }

            @media (min-width: 40em) {
                section {
                    display: flex;
                }

                section * + * {
                    margin-left: 5px;
                }
            }
        `;

        return [BasePacientePerfil.headerStyles, progressCss, base];
    }

    render() {
        const { loading, data, updateQuery, medicoId, formatoId } = this;
        const paciente = data.paciente || {};
        const historias = data.historias.results || [];
        const total = data.historias.totalCount || 0;
        const variables = { offset: historias.length, ...this._qlVariables(paciente.id, medicoId, formatoId) };

        return html`
            <base-paciente-perfil selected-menu="historias" .paciente="${paciente}">
                <header>
                    <h1>Historias</h1>
                </header>

                <section>
                    <medicos-combo @change="${e => this.medicoId = e.target.value}"></medicos-combo>
                    <formatos-combo @change="${e => this.formatoId = e.target.value}"></formatos-combo>
                </section>
                <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                <ul>
                    ${repeat(historias, historia => historia.id, (historia, index) => html`
                        <li><historia-info .historia="${historia}" @click="${this._historiaClicked}"></historia-info></li>
                    `)}
                </ul>
                <div id="more">
                    <paper-button ?hidden="${historias.length === 0 || historias.length === total}"
                        @click="${() => this.fetchMore({ updateQuery, variables })}">
                        ver mas
                    </paper-button>
                </div>
            </base-paciente-perfil>
        `;
    }

    constructor() {
        super();
        this.query = gql`
            query HistoriasPaciente($paciente: ID!, $medico: ID, $formato: ID, $offset: Int) {
                paciente(id: $paciente) {
                    ...BasePacientePerfil
                }
                historias(paciente: $paciente, proveedor: $medico, formato: $formato) {
                    totalCount
                    results(ordering: "-cita__inicio", limit: 10, offset: $offset) {
                        ...HistoriaInfo
                    }
                }
            }
            ${HistoriaInfo.fragment}
            ${BasePacientePerfil.fragment}
        `;
    }

    get pacienteId() {
        return this._pacienteId;
    }

    set pacienteId(value) {
        this._pacienteId = value;
        this._fetchData();
    }

    get medicoId() {
        return this._medicoId;
    }

    set medicoId(value) {
        this._medicoId = value;
        this._fetchData();
    }

    get formatoId() {
        return this._formatoId;
    }

    set formatoId(value) {
        this._formatoId = value;
        this._fetchData();
    }

    _fetchData() {
        const { pacienteId, medicoId, formatoId } = this;
        this.variables = this._qlVariables(pacienteId, medicoId, formatoId);
        this.subscribe();
    }

    _qlVariables(paciente, medico, formato) {
        return {
            paciente,
            ...(medico && { medico }),
            ...(formato && { formato }),
        };
    }

    _historiaClicked({ target }) {
        if (target.disabled) return;

        const historiasElem = [...this.shadowRoot.querySelectorAll('historia-info')];
        if (!target.opened) {
            historiasElem.forEach((elem) => {
                if (elem !== target) {
                    elem.opened = false;
                    elem.disabled = true;
                }
            })
        } else {
            historiasElem.forEach((elem) => {
                elem.disabled = false;
            })
        }

        target.opened = !target.opened;
    }

    updateQuery(prev, { fetchMoreResult }) {
        if (!fetchMoreResult) return prev;
        return Object.assign({}, prev, {
            historias: {
                totalCount: fetchMoreResult.historias.totalCount,
                results: [...prev.historias.results, ...fetchMoreResult.historias.results],
                __typename: prev.historias.__typename,
            },
        });
    }
}

customElements.define('mh-historias-paciente', MedhisHistoriasPaciente);