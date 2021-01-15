import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import gql from 'graphql-tag';

import '@polymer/iron-image/iron-image';
import '@polymer/paper-card/paper-card';

/**
 * `paciente-info` Datos basicos de un paciente.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class PacienteInfo extends PolymerElement {
    static get properties() {
        return {
            /**
             * Datos del paciente.
             */
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
                    line-height: 1;
                    text-align: center;
                    display: inline-block;
                }

                :host([mini]) figure {
                    display: flex;
                    text-align: left;
                    align-items: center;
                }

                :host([mini]) figure iron-image {
                    width: 50px;
                    height: 50px;
                    margin-right: 10px;
                }

                :host([mini]) h4 {
                    margin-top: 0;
                }

                figure {
                    margin: inherit;
                }

                h4 {
                    margin-bottom: 0;
                }

                p {
                    margin: 0;
                }

                paper-card {
                    width: 100%;
                }

                iron-image {
                    width: 150px;
                    height: 150px;
                }
            </style>
            <paper-card>
                <div class="card-content">
                    <figure>
                        <iron-image src="[[paciente.foto]]" sizing="cover" preload fade placeholder="/static/img/profile-none.png"></iron-image>
                        <figcaption>
                            <h4>[[paciente.nombreCompleto]]</h4>
                            <p>
                                <small>[[paciente.tipoDocumento]] [[paciente.numeroDocumento]]</small> <br>
                                <small>[[paciente.edad]]</small>
                            </p>
                        </figcaption>
                    </figure>
                </div>
            </paper-card>
        `;
    }
}

customElements.define('paciente-info', PacienteInfo);

PacienteInfo.fragment = gql`
    fragment PacienteInfo on Paciente {
        id
        foto
        edad
        tipoDocumento
        nombreCompleto
        numeroDocumento
    }
`;

export default PacienteInfo;
