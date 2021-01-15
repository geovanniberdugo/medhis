import { LitElement, html, css } from 'lit-element';
import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-button/paper-button';
import '../components/instituciones-combo';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '@polymer/iron-form/iron-form';
import '../elements';

/**
 * `mh-citas-servicio-entidad` Reporte del total de citas por servicio y entidad.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisCitasServicioEntidad extends LitElement {
    static get properties() {
        return {
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
                        <form method="GET" action="${url}">
                            <range-datepicker-input>
                                <template>
                                    <div style="display: grid; grid-gap: 10px; grid-template-columns: 1fr 1fr;">
                                        <paper-input required label="Desde *" value="[[dateFrom]]" name="desde"></paper-input>
                                        <paper-input required label="Hasta *" value="[[dateTo]]" name="hasta"></paper-input>
                                    </div>
                                </template>
                            </range-datepicker-input>
                            <instituciones-combo required name="institucion"></instituciones-combo>
                            <slot></slot>
                            <paper-button @click="${this.generar}">GENERAR</paper-button>
                        </form>
                    </iron-form>
                </div>
            </paper-card>
        `;
    }

    generar() {
        const form = this.shadowRoot.querySelector('iron-form');
        if (form.validate()) {
            form.submit();
        }
    }
}

customElements.define('mh-citas-servicio-entidad', MedhisCitasServicioEntidad);
