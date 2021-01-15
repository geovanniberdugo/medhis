import {PolymerElement, html} from '@polymer/polymer/polymer-element.js';
import '@polymer/iron-a11y-keys/iron-a11y-keys.js';
import '@polymer/iron-icon/iron-icon.js';
import '../my-icons.js';

/**
 * `search-box` Componente para buscar pacientes
 *
 * @customElement
 * @polymer
 * @demo
 * 
 */
class SearchBox extends PolymerElement {
    static get properties() {
        return {
            /**
             * Termino a buscar
             */
            term: {
                type: String,
                notify: true,
                value: '',
            },

            /** Texto que aparece en input */
            placeholder: {
                type: String,
                value: 'Buscar',
            },

            target: {
                type: Object,
            },

            _icon: {
                type: String,
                value: 'my-icons:search',
            },
        }
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                    --search-box-text-color: #FFF;
                    --search-box-focus-color: black;
                }

                #container {
                    position: relative;
                }

                input {
                    background-color: rgba(255, 255, 255, .2);
                    border: 0;
                    border-radius: 2px;
                    color: var(--search-box-text-color);
                    padding-left: 4em;
                    width: 100%;
                    height: 3em;
                    transition: background-color .5s, color .5s;
                    -webkit-appearance: textfield;
                }

                ::-webkit-input-placeholder { /* WebKit, Blink, Edge */
                    color: inherit;
                }
                :-moz-placeholder { /* Mozilla Firefox 4 to 18 */
                    color: inherit;
                }
                ::-moz-placeholder { /* Mozilla Firefox 19+ */
                    color: inherit;
                }
                :-ms-input-placeholder { /* Internet Explorer 10-11 */
                    color: inherit;
                }
                ::-ms-input-placeholder { /* Microsoft Edge */
                    color: inherit;
                }

                iron-icon {
                    --iron-icon-width: 1em;
                    --iron-icon-height: 100%;
                    position: absolute;
                    top: 0;
                    left: .5em;
                    transition: color .3s, transform .4s, -webkit-transform .4s;
                }

                /* Focus state */
                #container.active iron-icon{
                    color: var(--search-box-focus-color);
                    transform: rotate(180deg);
                }

                input:focus {
                    background-color: #f3f3f3;
                    color: var(--search-box-focus-color);
                }

                :focus {
                    outline: 0;
                }
            </style>

            <iron-a11y-keys target="[[target]]" keys="enter" on-keys-pressed="onEnter"></iron-a11y-keys>

            <div id="container">
                <input id="search" type="search" name="search" value="{{term::input}}" placeholder$="[[placeholder]]" on-focus="_onFocus" on-blur="_onBlur">
                <iron-icon icon="[[_icon]]"></iron-icon>
            </div>
        `;
    }

    /**
     * Instance of the element is created/upgraded. Use: initializing state,
     * set up event listeners, create shadow dom.
     * @constructor
     */
    constructor() {
        super();
    }

    /**
     * Use for one-time configuration of your component after local
     * DOM is initialized.
     */
    ready() {
        super.ready();
        this.target = this.$.search;
    }

    _onFocus() {
        this.$.container.classList.add('active');
        this._icon = 'my-icons:arrow-forward';
    }

    _onBlur() {
        this.$.container.classList.remove('active');
        this._icon = 'my-icons:search';
    }

    /**
     * Emite un evento con el termino a buscar
     * @event enter
     */
    onEnter() {
        if (this.term !== '') {
            this.dispatchEvent(new CustomEvent('enter', {
                bubbles: true,
                composed: true,
                detail: this.term,
            }));
        }
    }
}

customElements.define('search-box', SearchBox);