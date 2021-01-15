import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { formatMoney } from '../utils';

import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-button';
import '@vaadin/vaadin-radio-button/theme/material/vaadin-radio-group';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@polymer/paper-input/paper-textarea';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import '@polymer/iron-form/iron-form';
import './modal-spinner';

const AUDITAR_CAJA = gql`
    mutation AuditarCaja($caja: VerificarCajaInput!) {
        verificarCaja(input: $caja) {
            caja {
                id
                verificacionCorrecta
                observacionesVerificacion
                verificadoPor { id, nombreCompleto @title_case }
            }
        }
    }
`;

/** Flattens los datos de un recibo. */
const flattenRecibo = (recibo) => {
    const {
        valor,
        numero,
        formaPago,
        formaPagoLabel,
        tratamiento: {
            servicio,
            entidad,
            orden: { institucion, paciente },
        },
    } = recibo;
    return {
        valor,
        numero,
        entidad,
        paciente,
        servicio,
        formaPago,
        institucion,
        formaPagoLabel,
    };
};

/** Agrupa los recibos de caja por institucion. */
const groupByInstitucion = (obj, recibo) => {
    const { institucion, valor } = recibo;
    const key = `${institucion.id}`;
    if (!obj[key]) {
        obj[key] = { nombre: institucion.nombre, recibos: [recibo], total: valor };
    } else {
        obj[key].total += valor;
        obj[key].recibos = [...obj[key].recibos, recibo];
    }

    return obj;
};

/** Totaliza los recibos de caja por forma de pago. */
const totalByFormaPago = (obj, recibo) => {
    const { formaPago, valor } = recibo;
    if (!obj[formaPago]) {
        obj[formaPago] = valor;
    } else {
        obj[formaPago] += valor;
    }

    return obj;
};

// Templates
const auditoriaInfo = caja => html`
    <p><span class="label">Verificado por:</span><br> ${caja.verificadoPor.nombreCompleto}</p>
    <p>${caja.verificacionCorrecta ? 'correcto' : 'no correcto'}</p>
    <p ?hidden="${caja.verificacionCorrecta}"><span class="label">Observaciones</span> <br>${caja.observacionesVerificacion}</p>
`;

const auditoriaForm = (conObservaciones, estadoChanged) => html`
    <iron-form>
        <form>
            <vaadin-radio-group required @value-changed="${estadoChanged}" error-message="Escoge una opción">
                <vaadin-radio-button name="estado" value="1">Correcto</vaadin-radio-button>
                <vaadin-radio-button name="estado" value="0">No Correcto</vaadin-radio-button>
            </vaadin-radio-group>
            <paper-textarea label="Observaciones" name="observaciones" ?required="${conObservaciones}"></paper-textarea>
        </form>
    </iron-form>
`;

/**
 * `auditar-caja` Mutacion para auditar la caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class AuditarCaja extends ApolloMutation {
    render() {
        const { loading } = this;

        return html`
            <paper-button ?disabled="${loading}">Verificar</paper-button>
        `;
    }

    /** Auditar la caja */
    auditar(variables) {
        this.mutate({
            variables,
            mutation: AUDITAR_CAJA,
            refetchQueries: ['Cajas'],
        });
    }
}

customElements.define('auditar-caja', AuditarCaja);

/**
 * `transacciones-caja` Lista las transacciones de una caja.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class TransaccionesCaja extends ApolloQuery {
    static get properties() {
        return {
            /** Indica si el modal se esta mostrando. */
            opened: {
                type: Boolean,
                reflect: true,
            },

            /** Datos de la caja. */
            caja: { type: Object },

            /** Transacciones de la caja. */
            transacciones: { type: Array },

            /** Total de recibos por forma de pago. */
            totalesByFormaPago: { type: Object },

            /** Indica si las observaciones son requeridas para la auditoria. */
            conObservaciones: { type: Boolean },
        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            h4 {
                margin: 0;
            }

            table {
                width: 100%;
                border-collapse: collapse;
            }

            table.border, .border th, .border td {
                border: 1px solid lightgray;
            }

            paper-dialog {
                width: 90%;
            }

            #user {
                margin: 0;
            }

            .darker {
                background-color: lightgray;
            }

            .center {
                text-align: center;
            }

            .ips {
                text-transform: uppercase;
                background-color: #b9b3b3;
            }
        `;
    }

    render() {
        // eslint-disable-next-line object-curly-newline
        const { opened, loading, conObservaciones, caja = {}, transacciones = [], totalesByFormaPago = {} } = this;
        const totalRecibos = Object.values(totalesByFormaPago).reduce((sum, act) => sum + act, 0);

        return html`
            <paper-dialog modal ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                ${loading ? html`<modal-spinner ?active="${loading}"></modal-spinner>` : ''}
                <h2>Caja # ${caja.id}</h2>
                <paper-dialog-scrollable>
                    <section>
                        <h3 id="user">${caja.empleado.nombreCompleto}</h3>
                        <h4>${caja.fecha} - ${caja.sucursal.nombre}</h4>
                    </section>
                    <section>
                        <table>
                            <thead>
                                <tr>
                                    <th colspan="2">Cierre caja</th>
                                    <th colspan="2">Recibos de caja</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${caja.detalles.map(detalle => html`
                                    <tr class="center">
                                        <td>${detalle.formaPagoLabel}</td>
                                        <td>${formatMoney(detalle.valor)}</td>
                                        <td>${detalle.formaPagoLabel}</td>
                                        <td>${formatMoney(totalesByFormaPago[detalle.formaPago] || 0)}</td>
                                    </tr>
                                `)}
                                <tr class="center">
                                    <td>Pagos hechos</td>
                                    <td style="color: #ff2600;">${formatMoney(caja.pagos)}</td>
                                    <td></td>
                                    <td></td>
                                </tr>
                            </tbody>
                            <tfoot>
                                <tr>
                                    <th>Total</th>
                                    <th class="center">${formatMoney(caja.total)}</th>
                                    <th>Total</th>
                                    <th class="center">${formatMoney(totalRecibos)}</th>
                                </tr>
                            </tfoot>
                        </table>
                    </section>
                    <section class="center darker">DIFERENCIA: ${formatMoney(Math.abs(caja.total - totalRecibos))}</section>
                    <section>
                        <h3>Transacciones</h3>
                        <table class="border">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Paciente</th>
                                    <th>Entidad</th>
                                    <th>Servicio</th>
                                    <th>Forma de pago</th>
                                    <th>Valor</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${transacciones.map(transaccion => html`
                                    <tr>
                                        <th class="ips" colspan="6">${transaccion.nombre}</th>
                                    </tr>
                                    ${transaccion.recibos.map(recibo => html`
                                        <tr>
                                            <td class="center">${recibo.numero}</td>
                                            <td>${recibo.paciente.nombreCompleto}</td>
                                            <td>${recibo.entidad.nombre}</td>
                                            <td>${recibo.servicio.nombre}</td>
                                            <td>${recibo.formaPagoLabel}</td>
                                            <td class="center">${formatMoney(recibo.valor)}</td>
                                        </tr>
                                    `)}
                                    <tr class="darker">
                                        <th colspan="5">Total</th>
                                        <th class="center">${formatMoney(transaccion.total)}</th>
                                    </tr>
                                `)}
                            </tbody>
                        </table>
                    </section>
                    <section>
                        <h3>Auditoria</h3>
                        ${caja.verificadoPor ? auditoriaInfo(caja) : auditoriaForm(conObservaciones, (e) => { this.conObservaciones = e.detail.value === '0'; })}
                    </section>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <auditar-caja ?hidden="${caja.verificadoPor}" @click="${this._auditar}"></auditar-caja>
                    <paper-button dialog-dismiss>cerrar</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.opened = false;
        this.conObservaciones = false;
        this._boundOpenListener = this._open.bind(this);
        this.query = gql`
            query TransaccionesCaja($caja: ID!) {
                caja(id: $caja) {
                    id
                    total
                    pagos
                    verificacionCorrecta
                    observacionesVerificacion
                    fecha @date(format: "DD/MM/YYYY")
                    sucursal { id, nombre @capitalize }
                    empleado { id, nombreCompleto @title_case }
                    verificadoPor { id, nombreCompleto @title_case }
                    detalles { id, formaPago, formaPagoLabel, valor }
                }
                recibosCaja(caja: $caja, anulados: false) {
                    results {
                        id
                        valor
                        numero
                        formaPago
                        formaPagoLabel
                        tratamiento: servicioPrestado {
                            id
                            entidad { id, nombre @capitalize }
                            servicio { id, nombre @capitalize }
                            orden {
                                id
                                institucion { id, nombre }
                                paciente { id, nombreCompleto @title_case }
                            }
                        }
                    }
                }
            }
        `;
    }

    get id() {
        return this._id;
    }

    set id(value) {
        this._id = value;
        this._fetchData(value);
    }

    get data() {
        return this._data;
    }

    set data(value) {
        this._data = value;
        this._setData(value);
    }

    // lifecycles

    connectedCallback() {
        super.connectedCallback();
        window.addEventListener('show-transacciones-caja', this._boundOpenListener);
    }

    disconnectedCallback() {
        window.removeEventListener('show-transacciones-caja', this._boundOpenListener);
        super.disconnectedCallback();
    }

    /** Show modal */
    _open({ detail: { caja } }) {
        this.id = caja;
        this.opened = true;
    }

    /**
     * Fetches las transacciones.
     * @param {String} id Id de la caja.
     */
    _fetchData(id) {
        if (!id) return;

        this.variables = { caja: id };
        this.subscribe();
    }

    /** Sets los datos de la caja y las transacciones. */
    _setData({ caja, recibosCaja: { results: recibos } }) {
        this.caja = { ...caja };
        this.totalesByFormaPago = recibos.reduce(totalByFormaPago, {});
        this.transacciones = Object.values(recibos.map(flattenRecibo).reduce(groupByInstitucion, {}));
    }

    /** Audita la caja. */
    _auditar(e) {
        const form = this.shadowRoot.querySelector('iron-form');
        if (!form.validate()) return;

        const { estado, observaciones } = form.serializeForm();
        const _observaciones = observaciones ? { observacionesVerificacion: observaciones } : {};
        e.target.auditar({ caja: { id: this.id, verificacionCorrecta: estado === '1', ..._observaciones } });
    }
}

customElements.define('transacciones-caja', TransaccionesCaja);
