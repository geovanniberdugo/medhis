import { ApolloMutation } from '@apollo-elements/lit-apollo';
import { LitElement, html, css } from 'lit-element';
import { formatISODate, formatMoney, notifySuccessMessage } from '../utils';
import gql from 'graphql-tag';

import '@polymer/paper-icon-button/paper-icon-button';
import '@polymer/paper-tooltip/paper-tooltip';
import '@polymer/paper-input/paper-textarea';
import '@polymer/paper-dialog/paper-dialog';
import '@polymer/paper-button/paper-button';
import { cardCss } from './common-css';
import '@polymer/iron-icon/iron-icon';

const ELIMINAR_FACTURA_MUTATION = gql`
    mutation EliminarFactura($input: ID!) {
        eliminarFactura(id: $input) {
            ok
        }
    }
`;

/**
 * `eliminar-factura` Componente para eliminar factura.
 */
class EliminarFactura extends ApolloMutation {
    static get properties() {
        return {
            id: { type: String },
            opened: { type: Boolean },
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
        const { opened, loading } = this;

        return html`
            <paper-dialog ?opened="${opened}" @opened-changed="${(e) => { this.opened = e.detail.value; }}">
                <p><b>¿Esta seguro que deseas eliminar la factura?</b></p>
                <div class="buttons">
                    <paper-button dialog-dismiss>CANCELAR</paper-button>
                    <paper-button ?disabled="${loading}" @click="${this._eliminar}">ELIMINAR</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.opened = false;
    }

    _eliminar(e) {
        e.stopPropagation();
        this.mutate({
            refetchQueries: ['Facturas'],
            variables: { input: this.id },
            mutation: ELIMINAR_FACTURA_MUTATION,
        });
    }

    open({ facturaId }) {
        this.id = facturaId;
        this.opened = true;
    }

    onCompleted({ eliminarFactura }) {
        const { ok } = eliminarFactura;
        if (ok) {
            this.opened = false;
            notifySuccessMessage(this, 'Factura eliminada satifastoriamente');
        }
    }
}

customElements.define('eliminar-factura', EliminarFactura);

const ANULAR_FACTURA_MUTATION = gql`
    mutation AnularFactura($input: AnularFacturaInput!) {
        anularFactura(input: $input) {
            ok
            factura {
                id
                razonAnulacion
                anuladoEl @date(format: "DD/MM/YYYY")
                anuladoPor { id, nombreCompleto @title_case }
            }
        }
    }
`;

/**
 * `anular-factura` Anular factura.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class AnularFactura extends ApolloMutation {
    static get properties() {
        return {

        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            paper-dialog {
                margin: 5px;
                width: 250px;
            }
        `;
    }

    render() {
        const { loading } = this;

        return html`
            <paper-dialog no-overlap horizontal-align="center" vertical-align="auto" scroll-action="lock">
                <paper-textarea autofocus required label="Razón"></paper-textarea>
                <div class="buttons">
                    <paper-button ?disabled="${loading}" @click="${this._anular}">anular</paper-button>
                </div>
            </paper-dialog>
        `;
    }

    constructor() {
        super();
        this.mutation = ANULAR_FACTURA_MUTATION;
    }

    firstUpdated() {
        this.textElem = this.shadowRoot.querySelector('paper-textarea');
        this.dialogElem = this.shadowRoot.querySelector('paper-dialog');
    }

    _anular() {
        if (!this.textElem.validate()) return;

        this.variables = { input: { id: this.facturaId, razonAnulacion: this.textElem.value } };
        this.mutate();
    }

    onCompleted({ anularFactura: { ok } }) {
        if (ok) {
            this.textElem.value = '';
            this.dialogElem.close();
        }
    }

    open({ element, facturaId }) {
        this.dialogElem.positionTarget = element;
        this.facturaId = facturaId;
        this.dialogElem.open();
    }
}

customElements.define('anular-factura', AnularFactura);

/**
 * `factura-item` Item de factura.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class FacturaItem extends LitElement {
    static get properties() {
        return {
            factura: { type: Object },
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

            li {
                display: grid;
                grid-gap: 10px;
                list-style: none;
                margin-bottom: 10px;
                align-items: center;
                justify-items: center;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            }

            li h3 {
                text-align: center;
            }

            li span {
                color: slategrey;
            }

            li p {
                margin: 0px;
            }

            .anulado span:first-child {
                color: red;
            }
        `;

        return [cardCss, base];
    }

    render() {
        const { factura } = this;

        return html`
            <li class="card">
                <h3>Factura<br>#${factura.numero}</h3>
                <p><span>Fecha creación:</span><br>${formatISODate(factura.fechaExpedicion)}</p>
                <p><span>Total:</span><br>${formatMoney(factura.total)}</p>
                ${factura.anuladoPor && html`
                    <p class="anulado">
                        <span>ANULADO</span><br>
                        <span>${factura.anuladoEl}</span><br>
                        <span>${factura.anuladoPor.nombreCompleto}</span><br>
                        <paper-tooltip>${factura.razonAnulacion}</paper-tooltip>
                    </p>
                `}
                <div ?hidden="${factura.anuladoPor}">
                    <a href="${factura.detalleUrl}"><iron-icon icon="my-icons:remove-red-eye"></iron-icon></a>
                    ${factura.canAnular ? html`<paper-icon-button icon="my-icons:close" @click="${this.showAnularDialog}"></paper-icon-button>` : ''}
                    ${factura.canEliminar ? html`<paper-icon-button icon="my-icons:delete" @click="${this._eliminar}"></paper-icon-button>` : ''}
                </div>
            </li>
            <anular-factura></anular-factura>
            <eliminar-factura></eliminar-factura>
        `;
    }

    showAnularDialog({ target }) {
        this.shadowRoot.querySelector('anular-factura').open({ element: target, facturaId: this.factura.id });
    }

    _eliminar() {
        this.shadowRoot.querySelector('eliminar-factura').open({ facturaId: this.factura.id });
    }
}

customElements.define('factura-item', FacturaItem);

FacturaItem.fragment = gql`
    fragment FacturaItem on Factura {
        id
        total
        numero
        fechaFin
        canAnular
        detalleUrl
        canEliminar
        fechaInicio
        razonAnulacion
        fechaExpedicion
        anuladoEl @date(format: "DD/MM/YYYY")
        anuladoPor { id, nombreCompleto @title_case }
    }
`;

export default FacturaItem;