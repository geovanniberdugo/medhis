import { ApolloQuery, ApolloMutation } from '@apollo-elements/lit-apollo';
import { html, css } from 'lit-element';
import gql from 'graphql-tag';
import { DateTime } from 'luxon';
import { formatMoney, formatDateToISO, notifyErrorMessage, setErrorsOnForm, groupBy, mapObject } from '../utils';

import '@vaadin/vaadin-grid/theme/material/vaadin-grid-selection-column';
import '@vaadin/vaadin-grid/theme/material/vaadin-grid-filter-column';
import '@vaadin/vaadin-date-picker/theme/material/vaadin-date-picker';
import '@polymer/paper-dialog-scrollable/paper-dialog-scrollable';
import '@vaadin/vaadin-grid/theme/material/vaadin-grid';
import '@polymer/paper-icon-button/paper-icon-button';
import '@polymer/paper-input/paper-textarea';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import '@polymer/paper-input/paper-input';
import ModalMixin from './modal-mixin';
import '@polymer/iron-form/iron-form';
import '../components/es-date-picker';
import '../components/modal-spinner';

/**
 * `crear-factura` Mutacion para crear factura.
 *
 * @customElement
 * @demo
 * 
 */
class CrearFactura extends ApolloMutation {
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
            <paper-button ?disabled="${loading}">crear</paper-button>
        `;
    }

    constructor() {
        super();
        this.mutation = gql`
            mutation CrearFactura($factura: FacturaInput!) {
                generarFactura(input: $factura) {
                    ok
                    errors { field, messages }
                    factura { id, detalleUrl }
                }
            }
        `;
    }

    execute(factura) {
        this.variables = { factura };
        this.mutate();
    }

    onCompleted({ generarFactura }) {
        const { ok, errors, factura } = generarFactura;
        if (ok) {
            this.dispatchEvent(new CustomEvent('mutation-done', { detail: { factura } }));
        } else {
            this.dispatchEvent(new CustomEvent('mutation-error', { detail: { errors } }));
        }
    }
}

customElements.define('crear-factura', CrearFactura);


/**
 * `nueva-factura` Formulario para crear nueva factura.
 *
 * @customElement
 * @demo
 * 
 */
class NuevaFactura extends ModalMixin(ApolloQuery) {
    static get properties() {
        return {
            citas: { type: Array },
            fecha: { type: String },
            cliente: { type: Object },
            paciente: { type: Object },
            institucion: { type: Object },
            consecutivo: { type: Number },
        }
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            paper-dialog {
                width: 95%;
            }

            paper-icon-button {
                justify-self: center;
            }

            vaadin-date-picker {
                width: 100%;
            }

            #header {
                display: grid;
                align-items: center;
                grid-template-columns: 2fr 1fr;
            }

            #inputs {
                display: grid;
                grid-gap: 10px;
                align-items: end;
                grid-template-columns: 1fr 1fr;
            }

            #inputs paper-textarea {
                grid-column: 1 / -1;
            }
        `;
    }

    render() {
        const { opened, cliente, paciente, institucion, fecha, citas, consecutivo, loading } = this;

        return html`
            <paper-dialog modal ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                ${loading ? html`<modal-spinner ?active="${loading}"></modal-spinner>` : ''}
                <h2>Nueva Factura</h2>
                <paper-dialog-scrollable>
                    <div id="header">
                        <p>
                            Institución: ${institucion.nombre} <br>
                            Cliente: ${cliente.nombre} <br>
                            ${cliente.facturaPaciente ? html`Paciente: ${paciente.nombreCompleto}` : ''}
                        </p>
                        <paper-icon-button icon="my-icons:refresh" @click="${this._refetchData}"></paper-icon-button>
                    </div>
                    <iron-form>
                        <form>
                            <div id="inputs">
                                <paper-input name="numero" required label="Número factura *" type="number" value="${consecutivo}"></paper-input>
                                <es-date-picker><vaadin-date-picker name="fechaExpedicion" required label="Fecha" value="${fecha}"></vaadin-date-picker></es-date-picker>
                                <es-date-picker><vaadin-date-picker name="fechaInicio" label="Fecha inicio"></vaadin-date-picker></es-date-picker>
                                <es-date-picker><vaadin-date-picker name="fechaFin" label="Fecha fin"></vaadin-date-picker></es-date-picker>
                                <paper-textarea name="observaciones" label="Observaciones"></paper-textarea>
                            </div>
                        </form>
                    </iron-form>
                    <br>
                    <vaadin-grid .items="${citas}" @selected-items-changed="${this._selectedCitasHandler}">
                        <vaadin-grid-selection-column frozen auto-select></vaadin-grid-selection-column>
                        <vaadin-grid-filter-column width="220px" frozen header="Paciente" path="paciente.nombre">
                            <template>[[item.paciente.nombre]]<br>[[item.paciente.id]]</template>
                        </vaadin-grid-filter-column>
                        <vaadin-grid-column frozen width="210px" header="Servicio" path="servicio"></vaadin-grid-column>
                        <vaadin-grid-column header="Autorización"></vaadin-grid-column>
                        <vaadin-grid-column header="Fecha" path="fecha"></vaadin-grid-column>
                        <vaadin-grid-column header="Cantidad" flex-grow="0" text-align="center">
                            <template>[[item.cantidad]]</template>
                            <template class="footer">TOTALES</template>
                        </vaadin-grid-column>
                        <vaadin-grid-column header="Valor Unitario" width="160px">
                            <template class="footer"><div id="totalValorUnitario"></div></template>
                        </vaadin-grid-column>
                        <vaadin-grid-column header="Coopago Bruto" width="160px" ?hidden="${!cliente.discriminarIva}">
                            <template class="footer"><div id="totalCoopagoBruto"></div></template>
                        </vaadin-grid-column>
                        <vaadin-grid-column header="Iva Coopago" width="160px" ?hidden="${!cliente.discriminarIva}">
                            <template class="footer"><div id="totalIvaCoopago"></div></template>
                        </vaadin-grid-column>
                        <vaadin-grid-column header="Coopago" width="160px">
                            <template class="footer"><div id="totalCoopago"></div></template>
                        </vaadin-grid-column>
                        <vaadin-grid-column header="Subtotal" width="160px">
                            <template class="footer"><div id="total"></div></template>
                        </vaadin-grid-column>
                    </vaadin-grid>
                </paper-dialog-scrollable>
                <div class="buttons">
                    <paper-button dialog-dismiss>cancelar</paper-button>
                    <crear-factura @click="${this._crear}" @mutation-done="${this._facturaCreada}"
                        @mutation-error="${this._showErrors}">
                        crear
                    </crear-factura>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.citas = [];
        this.cliente = {};
        this.paciente = {};
        this.institucion = {};
        this.selectedCitas = [];
        this.notifyOnNetworkStatusChange = true;
        this.fecha = formatDateToISO(new Date());
        this.openModalEvent = 'show-nueva-factura';
        this.query = gql`
            query CitasFacturar($institucion: ID!, $cliente: ID!) {
                consecutivoFactura(ips: $institucion)
                citas(disponibleFacturar: true, empresa: $cliente, institucion: $institucion) {
                    results {
                        id
                        autorizacion
                        inicio @date(format: "DD/MM/YYYY")
                        servicio { id, nombre @capitalize }
                        paciente { id, numeroDocumento, nombreCompleto @title_case }
                        servicioPrestado { 
                            id
                            valor
                            coopago
                            ordenUrl
                            cantidad
                            isUnaCita
                            ivaCoopago
                            coopagoBruto
                            isCoopagoTotal
                            numSesionesCoopago
                        }
                    }
                }
            }
        `;
    }

    get data() {
        return this._data;
    }

    set data(value) {
        this._data = value;
        this._setData(value);
    }

    // Lifecycles
    shouldUpdate() {
        return true;
    }

    updated(changedProps) {
        const shouldFetch = changedProps.has('cliente') || changedProps.has('institucion');
        if (shouldFetch) this._fetchData();
    }

    firstUpdated() {
        const columns = this.shadowRoot.querySelectorAll('vaadin-grid-column');

        columns[1].renderer = (root, column, rowData) => {
            root.innerHTML = `<a href="${rowData.item.ordenUrl}" target="_blank">${rowData.item.autorizacion || 'No ingresado'}</a>`; 
        };
        columns[4].renderer = (root, column, rowData) => {
            root.textContent = formatMoney(rowData.item.valor || 0);
        };
        columns[5].renderer = (root, column, rowData) => {
            root.textContent = formatMoney(rowData.item.coopagoBruto || 0);
        };
        columns[6].renderer = (root, column, rowData) => {
            root.textContent = formatMoney(rowData.item.ivaCoopago || 0);
        };
        columns[7].renderer = (root, column, rowData) => {
            root.textContent = formatMoney(rowData.item.coopago || 0);
        };
        columns[8].renderer = (root, column, rowData) => {
            root.textContent = formatMoney(rowData.item.subtotal || 0);
        };
    }

    _handleOpenEvent({ detail: { cliente, paciente, institucion } }) {
        this.cliente = cliente;
        this.paciente = paciente;
        this.institucion = institucion;
    }

    _fetchData() {
        const { cliente: { id: clienteId }, institucion: { id: institucionId } } = this;
        if (!clienteId || !institucionId) return;
        this.selectedCitas = [];
        this.variables = {
            cliente: clienteId,
            institucion: institucionId,
        };
        this.subscribe();
    }

    _setData({ citas: { results: citas }, consecutivoFactura }) {
        this.consecutivo = consecutivoFactura;
        this.citas = Object.values(this._summarize(this._groupCitasByAuthServicio2(citas)));
        this.shadowRoot.querySelector('vaadin-grid').selectedItems = this.citas.filter(cita => this.selectedCitas.includes(cita.key));
    }

    _groupCitasByAuthServicio2(citas) {
        return groupBy(citas, cita => `${cita.autorizacion}-${cita.servicioPrestado.id}`)
    }

    _summarize(grouppedCitas) {
        return mapObject(grouppedCitas, (key, value) => {
            const totalizarValor = (func) => {
                return value.reduce((total, val) => total + func(val), 0);
            };

            const { servicioPrestado: tratamiento, autorizacion, inicio, servicio, paciente } = value[0];
            const valorUnitario = tratamiento.valor;
            const cantidad = tratamiento.isUnaCita ? tratamiento.cantidad : value.length;
            const coopago = (
                tratamiento.isCoopagoTotal || !!tratamiento.numSesionesCoopago
                    ? tratamiento.coopago 
                    : totalizarValor(item => item.servicioPrestado.coopago)
            );
            const subtotal = cantidad * valorUnitario - coopago;

            return {
                key,
                coopago,
                cantidad,
                autorizacion,
                fecha: inicio,
                valor: valorUnitario,
                servicio: servicio.nombre,
                citas: value.map(v => v.id),
                ordenUrl: tratamiento.ordenUrl,
                subtotal: Math.max(subtotal, 0),
                ivaCoopago: totalizarValor(item => item.servicioPrestado.ivaCoopago),
                coopagoBruto: totalizarValor(item => item.servicioPrestado.coopagoBruto),
                paciente: { id: paciente.numeroDocumento, nombre: paciente.nombreCompleto },
            };
        });
    }

    _selectedCitasHandler({ target }) {
        const totalizarValor = (func) => {
            return formatMoney(target.selectedItems.reduce((total, cita) => total + func(cita), 0));
        };

        const setTotalOnElem = (elemId, func) => {
            const elem = target.querySelector(`#${elemId}`);
            if (elem) elem.textContent = totalizarValor(func);
        };

        setTotalOnElem('totalValorUnitario', item => item.valor * item.cantidad);
        setTotalOnElem('totalCoopagoBruto', item => item.coopagoBruto);
        setTotalOnElem('totalIvaCoopago', item => item.ivaCoopago);
        setTotalOnElem('totalCoopago', item => item.coopago);
        setTotalOnElem('total', item => item.subtotal);
    }

    _refetchData() {
        this.selectedCitas = this.shadowRoot.querySelector('vaadin-grid').selectedItems.map(sel => sel.key);
        this.refetch();
    }

    _crear({ target }) {
        const form = this.shadowRoot.querySelector('iron-form');
        const grid = this.shadowRoot.querySelector('vaadin-grid');
        
        if (grid.selectedItems.length == 0 || !form.validate()) {
            if (grid.selectedItems.length == 0) notifyErrorMessage(this, 'Debes seleccionar alguna cita para poder facturar.')
            return;
        }

        const { fechaExpedicion: fecha, fechaInicio, fechaFin, ...formData } = form.serializeForm();
        const { id: clienteId, discriminarIva, facturaPaciente } = this.cliente;

        target.execute({
            ...formData,
            cliente: clienteId,
            ...(fechaFin && { fechaFin }),
            institucion: this.institucion.id,
            ...(fechaInicio && { fechaInicio }),
            ...(facturaPaciente && { paciente: this.paciente.id }),
            fechaExpedicion: `${fecha}T${DateTime.local().toISOTime()}`,
            detalle: this._buildDetalleFactura(grid.selectedItems, discriminarIva),
        });
    }

    _buildDetalleFactura(citas, conIva) {
        return citas.map(cita => {
            const { valor, coopago, citas: aFacturar, ivaCoopago, coopagoBruto, cantidad } = cita;
            return {
                valor,
                coopago,
                cantidad,
                citas: aFacturar,
                ivaCoopago: conIva ? ivaCoopago : 0,
                coopagoBruto: conIva ? coopagoBruto : 0,
            };
        })
    }

    _facturaCreada({ detail }) {
        this.selectedCitas = [];
        location.href = detail.factura.detalleUrl;
    }

    _showErrors({ detail }) {
        const form = this.shadowRoot.querySelector('iron-form');
        setErrorsOnForm(form, detail.errors);
    }
}

customElements.define('nueva-factura', NuevaFactura);