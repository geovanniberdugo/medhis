import { PolymerElement, html } from '@polymer/polymer/polymer-element';

import 'range-datepicker/range-datepicker-input';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-input/paper-input';
import '@polymer/paper-card/paper-card';
import '@polymer/iron-form/iron-form';
import '../components/instituciones-combo';
import '../components/sucursales-combo';
import '../elements';

/**
 * `mh-contabilizacion-recibos-caja` Exporta a sistema contable recibos de caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class MedhisContabilizacionRecibosCaja extends PolymerElement {
    static get properties() {
        return {
            /** Url para obtener el archivo de los indicadores. */
            url: String,
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                paper-card {
                    width: 100%;
                }

                .card-content {
                    display: grid;
                }

                .card-content paper-button {
                    grid-column: 1 / -1;
                    align-self: center;
                }
            </style>

            <paper-card>
                <div class="card-content">
                    <iron-form id="form" allow-redirect>
                        <form action="[[url]]" method="POST">
                            <range-datepicker-input locale="es" date-from="{{desde}}" date-to="{{hasta}}">
                                <template>
                                    <div style="display: grid; grid-gap: 10px; grid-template-columns: 1fr 1fr;">
                                        <paper-input name="desde" required label="Desde *" value="[[dateFrom]]"></paper-input>
                                        <paper-input name="hasta" required label="Hasta *" value="[[dateTo]]"></paper-input>
                                    </div>
                                </template>
                            </range-datepicker-input>
                            <instituciones-combo required name="institucion"></instituciones-combo>
                            <sucursales-combo required name="sucursal"></sucursales-combo>
                            <slot></slot>
                            <paper-button on-click="contabilizar">contabilizar</paper-button>
                        </form>
                    </iron-form>
                </div>
            </paper-card>
        `;
    }

    contabilizar() {
        this.$.form.submit();
    }
}

customElements.define('mh-contabilizacion-recibos-caja', MedhisContabilizacionRecibosCaja);
