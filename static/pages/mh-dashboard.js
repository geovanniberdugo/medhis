import { LitElement, html, css } from 'lit-element';

import '@polymer/iron-icon/iron-icon';
import '../elements';

/**
 * `mh-dashboard`
 */
class MedhisDashboard extends LitElement {
    static get properties() {
        return {

        };
    }

    static get styles() {
        return css`
            :host {
                display: block;
            }

            section {
                display: grid;
                grid-gap: 15px;
            }
        `;
    }

    render() {
        return html`
            <section>
                <slot></slot>
            </section>
        `;
    }
}

customElements.define('mh-dashboard', MedhisDashboard);