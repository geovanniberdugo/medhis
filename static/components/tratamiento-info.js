import { LitElement, html, css } from 'lit-element';
import gql from 'graphql-tag';
import { formatMoney } from '../utils';

import '@polymer/paper-card/paper-card';

/**
 * `tratamiento-info` Info de un tratamiento.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class TratamientoInfo extends LitElement {
    static get properties() {
        return {
            tratamiento: { type: Object },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            h2, p {
                margin: 0;
            }

            section {
                display: grid;
                grid-gap: 5px;
                grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr));
            }

            ul {
                margin: 0;
                padding: 0;
            }

            li {
                list-style: none;
                margin-bottom: 5px;
            }

            paper-card {
                width: 100%;
                background-color: var(--tratamiento-card-color, white);
            }

            .label {
                color: #616161;
            }

            .estado {
                align-self: center;
                justify-self: center;
                text-transform: uppercase;
            }

            .estado.IN {
                color: darkorange;
            }

            .estado.TE {
                color: green;
            }

            .estado.CA {
                color: red;
            }

            .estado.FAC {
                color: blue;
            }

            .info {
                margin: 16px 0;
            }

            .info ul li {
                margin: 0;
            }

            .saldo {
                align-self: center;
                justify-self: center;
            }

            .saldo > div {
                color: white;
                padding: 1em;
                font-weight: bold;
                text-align: center;
                text-transform: uppercase;
                background-color: var(--tratamiento-estado-saldo, #ffc107);
            }

            .saldo > div.debt {
                --tratamiento-estado-saldo: #dd2c00;
            }

            .saldo > div.favor {
                --tratamiento-estado-saldo: #0f9d58;
            }
        `;
    }

    render() {
        const { tratamiento = {} } = this;

        return html`
            <paper-card>
                <div class="card-content">
                    <section>
                        <div>
                            <h2>#${tratamiento.id} ${tratamiento.servicio.nombre}</h2>
                            <p class="fechas">
                                <span class="label">Inicio: ${tratamiento.fechaInicioTratamiento}</span><br>
                                <span class="label">Fin: ${tratamiento.fechaFinTratamiento}</span>
                            </p>
                        </div>
                        <div class="estado ${tratamiento.estado}">${tratamiento.estadoLabel}</div>
                        <div class="estado FAC" ?hidden="${tratamiento.facturas.length === 0}">facturado</div>
                    </section>
                    <section class="info">
                        <p>
                            <b class="label">Entidad:</b> <br>
                            ${tratamiento.entidad.nombre}
                        </p>
                        <ul>
                            <li><b class="label">Medicos</b></li>
                            ${tratamiento.medicos.map(medico => html`<li>${medico.nombreCompleto}</li>`)}
                        </ul>
                        <p>
                            <b class="label">Cantidad:</b> ${tratamiento.cantidad} <br>
                            <b class="label">Atendidas:</b> ${tratamiento.sesionesAtendidas} <br>
                            <b class="label">Faltantes:</b> ${tratamiento.sesionesFaltantes} <br>
                        </p>
                        <p>
                            <b class="label">Valor sesión:</b> ${formatMoney(tratamiento.valor)} <br>
                            <b class="label">Valor total:</b> ${formatMoney(tratamiento.valorTotal)} <br>
                            <b class="label">Coopago:</b> ${formatMoney(tratamiento.coopago)} <br>
                        </p>
                        <p>
                            <b class="label">Valor a pagar:</b> ${formatMoney(tratamiento.coopagoTotal)} <br>
                            <b class="label">Valor pagado:</b> ${formatMoney(tratamiento.totalPagado)} <br>
                            <b class="label">Saldo actual:</b> ${formatMoney(tratamiento.saldoPaciente)} <br>
                        </p>
                        <div class="saldo" ?hidden="${tratamiento.saldoSesiones === 0}">
                            <div class="${this._estadoSaldoSesiones(tratamiento.saldoSesiones).clase}">
                                ${this._estadoSaldoSesiones(tratamiento.saldoSesiones).estado} <br>
                                ${formatMoney(tratamiento.saldoSesiones)}
                            </div>
                        </div>
                        <div ?hidden="${tratamiento.facturas.length === 0}">
                            <b class="label">Factura</b><br> ${tratamiento.facturas.map(factura => html`${factura.numero}`)}
                        </div>
                    </section>
                </div>
            </paper-card>
        `;
    }

    /** Indica si el paciente esta en deuda, al día o con saldo a favor. */
    _estadoSaldoSesiones(valor) {
        let clase = '';
        let estado = 'al día';

        if (valor < 0) {
            clase = 'debt';
            estado = 'deuda';
        } else if (valor > 0) {
            clase = 'favor';
            estado = 'saldo a favor';
        }

        return { estado, clase };
    }
}

customElements.define('tratamiento-info', TratamientoInfo);

TratamientoInfo.fragment = gql`
    fragment TratamientoInfo on ServicioRealizar {
        id
        valor
        estado
        coopago
        cantidad
        valorTotal
        estadoLabel
        totalPagado
        coopagoTotal
        saldoPaciente
        saldoSesiones
        sesionesAtendidas
        sesionesFaltantes
        facturas { id, numero }
        entidad { id, nombre @title_case }
        servicio { id, nombre @title_case }
        medicos { id, nombreCompleto @title_case }
        fechaFinTratamiento @date(format: "DD/MM/YYYY")
        fechaInicioTratamiento @date(format: "DD/MM/YYYY")
    }
`;

export default TratamientoInfo;
