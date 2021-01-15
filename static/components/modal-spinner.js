import { LitElement, html, css } from 'lit-element';

import '@polymer/paper-spinner/paper-spinner-lite';

/**
 * `modal-spinner` Loading spinner for modals.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class ModalSpinner extends LitElement {
    static get properties() {
        return {
            /** Indica si esta activo. */
            active: { type: Boolean },
        };
    }

    static get styles() {
        return css`
            :host {
                width: 100%;
                height: 100%;
                display: block;
            }

            paper-spinner-lite {
                opacity: 1;
                z-index: 2;
            }

            .outer {
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                display: flex;
                position: absolute;
                align-items: center;
                justify-content: center;
            }

            .overlay {
                z-index: 1;
                width: 100%;
                height: 100%;
                opacity: 0.5;
                position: absolute;
                background-color: white;
            }
        `;
    }

    render() {
        const { active } = this;
        return html`
            <div class="outer">
                <div class="overlay"></div>
                <paper-spinner-lite ?active="${active}"></paper-spinner-lite>
            </div>
        `;
    }

    constructor() {
        super();
        this.active = false;
    }
}

customElements.define('modal-spinner', ModalSpinner);
