import { LitElement, html, css } from 'lit-element';

import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-button/paper-button';
import '../components/instituciones-combo';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '@polymer/iron-form/iron-form';
import '../components/clientes-combo';
import '../elements';

/**
 * `mh-rips` Página para generar los rips.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisRips extends LitElement {
    static get properties() {
        return {
            /** Url de descarga de rips */
            url: { type: String },
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
        const { url } = this;
        return html`
            <paper-card>
                <div class="card-content">
                    <iron-form allow-redirect>
                        <form method="POST" action="${url}">
                            <range-datepicker-input>
                                <template>
                                    <div style="display: grid; grid-gap: 10px; grid-template-columns: 1fr 1fr;">
                                        <paper-input required label="Desde *" value="[[dateFrom]]" name="desde"></paper-input>
                                        <paper-input required label="Hasta *" value="[[dateTo]]" name="hasta"></paper-input>
                                    </div>
                                </template>
                            </range-datepicker-input>
                            <instituciones-combo required name="institucion"></instituciones-combo>
                            <clientes-combo required name="cliente"></clientes-combo>
                            <slot></slot>
                            <paper-button @click="${this.submit}">GENERAR</paper-button>
                        </form>
                    </iron-form>
                </div>
            </paper-card>
        `;
    }

    /** Generar rips. */
    submit() {
        const form = this.shadowRoot.querySelector('iron-form');
        if (form.validate()) {
            form.submit();
        }
    }
}

customElements.define('mh-rips', MedhisRips);
