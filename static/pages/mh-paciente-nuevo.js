import { ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { notifyErrorMessage, notifySuccessMessage } from '../utils';

import '@polymer/paper-button/paper-button';
import '@polymer/paper-card/paper-card';
import '../components/paciente-form';
import '../elements';

const CREAR_PACIENTE_MUTATION = gql`
    mutation CrearPaciente($paciente: NuevoPacienteInput!) {
        crearPaciente(input: $paciente) {
            ok
            errors { field, messages }
        }
    }
`;

/**
 * `mh-paciente-nuevo` Crear nuevo paciente.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisPacienteNuevo extends ApolloMutation {
    static get properties() {
        return {

        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            paper-card {
                width: 100%;
            }
        `;
    }

    render() {
        const { loading } = this;

        return html`
            <paper-card>
                <div class="card-content">
                    <paciente-form filloption="partial"></paciente-form>
                </div>
                <div class="card-actions">
                    <paper-button ?disabled="${loading}" @click="${this.save}">crear</paper-button>
                </div>
            </paper-card>
        `;
    }

    constructor() {
        super();
        this.mutation = CREAR_PACIENTE_MUTATION;
    }

    save() {
        const form = this.shadowRoot.querySelector('paciente-form');
        if (!form.validate()) {
            notifyErrorMessage(this, 'Hubo un error en el formulario por favor revisa');
            return;
        }

        this.variables = { paciente: { ...form.value } };
        this.mutate();
    }

    onCompleted({ crearPaciente: { ok, errors } }) {
        const form = this.shadowRoot.querySelector('paciente-form');
        if (ok) {
            form.reset();
            notifySuccessMessage(this, 'Paciente creado correctamente.');
        } else {
            form.setFormErrors(errors);
            notifyErrorMessage(this, 'Hubo un error en el formulario por favor revisa');
        }
    }
}

customElements.define('mh-paciente-nuevo', MedhisPacienteNuevo);
