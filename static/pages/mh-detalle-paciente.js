import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { notifyErrorMessage, notifySuccessMessage } from '../utils';

import BasePacientePerfil from '../components/base-paciente-perfil';
import PacienteForm from '../components/paciente-form';
import '@polymer/paper-progress/paper-progress';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-card/paper-card';
import '../elements';

const EDITAR_PACIENTE_MUTATION = gql`
    mutation EditarPaciente($paciente: EditarPacienteInput!) {
        editarPaciente(input: $paciente) {
            ok
            errors { field, messages }
            paciente {
                id
                ...PacienteForm
                ...BasePacientePerfil
            }
        }
    }
    ${PacienteForm.fragment}
    ${BasePacientePerfil.fragment}
`;

/**
 * `editar-paciente` Boton para editar paciente
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class EditarPaciente extends ApolloMutation {
    static get properties() {
        return {

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
        const { loading } = this;

        return html`
            <div class="buttons">
                <paper-button ?disabled="${loading}">editar</paper-button>
            </div>
        `;
    }

    constructor() {
        super();
        this.mutation = EDITAR_PACIENTE_MUTATION;
    }

    save(paciente) {
        this.variables = { paciente };
        this.mutate();
    }

    onCompleted({ editarPaciente: { ok, errors } }) {
        this.dispatchEvent(new CustomEvent('mutation-done', {
            detail: {
                ok,
                errors,
            },
        }));
    }
}

customElements.define('editar-paciente', EditarPaciente);


/**
 * `mh-detalle-paciente` Detalle de un paciente.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisDetallePaciente extends ApolloQuery {
    static get properties() {
        return {
            /** Url a redireccionar si el paciente es editado correctamente. */
            ordenUrl: { type: String },
            pacienteId: { type: String },
        };
    }

    static get styles() {
        const base = css`
            :host {
                display: block;
            }

            paper-progress {
                width: 100%;
                --paper-progress-active-color: var(--app-primary-color);
            }

            paper-card {
                width: 100%;
            }
        `;

        return [BasePacientePerfil.headerStyles, base];
    }

    render() {
        const { loading, data, ordenUrl } = this;
        const paciente = data.paciente || {};

        return html`
            <base-paciente-perfil selected-menu="detalle" .paciente="${paciente}">
                <header>
                    <h1>Detalle paciente</h1>
                </header>

                <paper-card>
                    <paper-progress indeterminate ?disabled="${!loading}"></paper-progress>
                    <div class="card-content">
                        <paciente-form .fillOption=${this._fillOption(paciente.canEdit, ordenUrl)} .paciente="${paciente}" @file-abort="${this.removeFile}"></paciente-form>
                    </div>
                    ${paciente.canEdit ? html`<editar-paciente @click="${this.save}" @mutation-done="${this.onCompleted}"></editar-paciente>` : ''}
                </paper-card>
            </base-paciente-perfil>
        `;
    }

    removeFile(e) {
        // remove file from patient
        // console.log('remove', e);
        // console.log(e.target);
        // console.log(e.composedPath());
    }

    constructor() {
        super();
        this.ordenUrl = '';
        this.query = gql`
            query DetallePaciente($paciente: ID!) {
                paciente(id: $paciente) {
                    id
                    canEdit
                    ...PacienteForm
                    ...BasePacientePerfil
                }
            }
            ${PacienteForm.fragment}
            ${BasePacientePerfil.fragment}
        `;
    }

    get pacienteId() {
        return this._pacienteId;
    }

    set pacienteId(value) {
        this._pacienteId = value;
        this._fetchData(value);
    }

    _fetchData(id) {
        this.variables = { paciente: id };
        this.subscribe();
    }


    _fillOption(canEdit, ordenUrl) {
        if (!canEdit) return 'noedit';

        return ordenUrl ? 'full' : 'partial';
    }

    save({ target }) {
        const form = this.shadowRoot.querySelector('paciente-form');
        if (!form.validate()) {
            notifyErrorMessage(this, 'Hubo un error en el formulario por favor revisa');
            return;
        }

        target.save({ id: this.pacienteId, ...form.value });
    }

    onCompleted({ detail }) {
        const { ok, errors } = detail;

        if (ok) {
            notifySuccessMessage(this, 'Paciente editado correctamente.');
            if (this.ordenUrl) window.location = this.ordenUrl;
            return;
        }

        const form = this.shadowRoot.querySelector('paciente-form');
        form.setFormErrors(errors);
        notifyErrorMessage(this, 'Hubo un error en el formulario por favor revisa');
    }
}

customElements.define('mh-detalle-paciente', MedhisDetallePaciente);
