import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import '@polymer/paper-button/paper-button';

/**
 * `paper-step-action-buttons` Step buttons.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class PaperStepActionButtons extends PolymerElement {
    /**
    * Fired when the continue button is clicked.
    *
    * @event continue-clicked
    * @param {Object} detail empty
    */
    /**
     * Fired when the skip button is clicked.
     *
     * @event skip-clicked
     * @param {Object} detail empty
     */
    /**
     * Fired when the update button is clicked.
     *
     * @event update-clicked
     * @param {Object} detail empty
     */
    /**
     * Fired when the finish button is clicked.
     *
     * @event finish-clicked
     * @param {Object} detail empty
     */
    /**
     * Fired when the back button is clicked.
     *
     * @event back-clicked
     * @param {Object} detail empty
     */

    static get properties() {
        return {
            skipButton: {
                type: Boolean,
                value: false,
            },
            backButton: {
                type: Boolean,
                value: false,
            },
            isUpdate: {
                type: Boolean,
                value: false,
                observer: 'setContinueHidden',
            },
            __isContinueHidden: {
                type: Boolean,
                value: false,
            },
            isFinish: {
                type: Boolean,
                value: false,
                observer: 'setContinueHidden',
            },
            /**
             * The back button text value
             */
            backLabel: String,
            /**
             * The continue button text value
             */
            continueLabel: String,
            /**
             * The skip button text value
             */
            skipLabel: String,
            /**
             * The skip button text value
             */
            finishLabel: String,
            /**
             * The skip button text value
             */
            updateLabel: String,
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                }

                paper-button#continueBtn, paper-button#finishBtn {
                    color: var(--app-primary-color);
                }
            </style>

            <paper-button id="updateBtn" data-event="update" hidden$="[[!isUpdate]]" on-tap="_fireEvent">{{updateLabel}}</paper-button>
            <paper-button id="continueBtn" data-event="continue" hidden$="[[__isContinueHidden]]" on-tap="_fireEvent">{{continueLabel}}</paper-button>
            <paper-button id="skipBtn" data-event="skip" hidden$="[[!skipButton]]" on-tap="_fireEvent">{{skipLabel}}</paper-button>
            <paper-button id="backBtn" data-event="back" hidden$="[[!backButton]]" on-tap="_fireEvent">{{backLabel}}</paper-button>
            <paper-button id="finishBtn" data-event="finish" hidden$="[[!isFinish]]" on-tap="_fireEvent">{{finishLabel}}</paper-button>
        `;
    }

    /**
     * This function is used to set the 'isFinish' property.
     * @param {Boolean} value true or false
     */
    setFinish(value) {
        this.isFinish = value;
    }

    /**
     * This function is used to set the 'isUpdate' property.
     * @param {Boolean} value true or false
     */
    setUpdate(value) {
        this.isUpdate = value;
    }

    /**
     * This is a callback function called when one of the different button is clicked.
     * @param {Object} e The event object
     */
    _fireEvent(e) {
        const eventName = e.currentTarget.dataset.event;
        this.dispatchEvent(new CustomEvent(`${eventName}-clicked`, {
            bubbles: true,
            composed: true,
        }));
    }

    /**
     * This function is used to set the  '__isContinueHidden' property.
     * @param {Boolean} value true to hide the continue button, false otherwise.
     */
    setContinueHidden(value) {
        if (value) {
            this.__isContinueHidden = true;
        } else {
            this.__isContinueHidden = false;
        }
    }

    /**
     * This function is used to reinitialize all the parameter of this element.
     */
    reset() {
        this.setContinueHidden(false);
        this.setFinish(false);
        this.setUpdate(false);
    }
}

customElements.define('paper-step-action-buttons', PaperStepActionButtons);

/**
 * @namespace IGStepper
 */
window.IGStepper = window.IGStepper || {};
window.IGStepper.PaperStepActionButtons = PaperStepActionButtons;
