import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import PaperStepPropertyMixin from './paper-step-property-mixin';
import '@polymer/iron-collapse/iron-collapse';
import '@polymer/paper-button/paper-button';
import '@polymer/iron-icon/iron-icon';
import './paper-step-action-buttons';

window.IGStepper.Stepper = window.IGStepper.Stepper || {};
window.IGStepper.Stepper.Context = window.IGStepper.Stepper.Context || {};

/**
 * `paper-step` Step.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class PaperStep extends PaperStepPropertyMixin(PolymerElement) {
    static get properties() {
        return {
            /**
             * This is the label of the step
             */
            label: {
                type: String,
            },
            /**
             * This is the number of the step.
             * This property is used on the badge.
             */
            _badgeNumber: {
                type: Number,
                readOnly: true,
            },
            /**
             * True if the paper-stepper is set horizontal, false otherwise
             */
            stepperHorizontal: {
                type: Boolean,
                value: false,
                readOnly: true,
                reflectToAttribute: true,
            },
        };
    }

    static get template() {
        return html`
            <style>
                /* General */
                :host {
                    height: inherit;
                }

                :host([stepper-horizontal]) {
                    width: auto;
                    @apply --layout-flex;
                }

                :host([stepper-horizontal][active]) {
                    height: 400px;
                    width: auto;
                    @apply --layout-flex;
                }

                div.layout {
                    border-left: 1px solid var(--step-connector-line-color, #BDBDBD);
                    margin-left: 24px;
                }

                :host([stepper-horizontal]) div.layout {
                    border-left: none;
                    position: absolute;
                    left: 0;
                    right: 0;
                    overflow: hidden;
                    @apply --layout-flex;
                }

                paper-button {
                    display: flex;
                    margin: 0;
                    justify-content: flex-start;
                }

                paper-button {
                    text-align: center;
                    display: flex;
                    position: relative;
                    justify-content: flex-start;
                }

                :host([stepper-horizontal]) paper-button::after {
                    content: '';
                    border-top: 1px solid var(--step-connector-line-color, #BDBDBD);
                    width: 100%;
                    @apply --layout-flex;
                }

                :host(:last-child) paper-button::after {
                    border-top: none;
                }

                :host([optional]) span#subtitle {
                    display: block;
                    font-size: 0.8em;
                    margin-top: 2px;
                    max-width: 150px;
                    text-transform: capitalize;
                }

                :host span#subtitle {
                    display: none;
                }

                /* label button */
                :host([save]) div#labelBtn {
                    color: var(--step-saved-label-color, #424242);
                    font-weight: inherit;
                }

                :host([save][active]) div#labelBtn,
                :host([active]) div#labelBtn {
                    color: var(--step-active-label-color, #424242);
                    font-weight: 600;
                }

                div#labelBtn {
                    align-self: center;
                    padding: 0 16px;
                    font-size: 14sp;
                    color: var(--step-label-color, #E0E0E0);
                }

                /* icon button */
                :host iron-icon#iconBtn {
                    display: none;
                    --iron-icon-fill-color: var(--step-badge-content-color, #FFFFFF);
                    --iron-icon-stroke-color: var(--step-badge-content-color, #FFFFFF);
                }

                :host([save]) iron-icon#iconBtn {
                    display: block;
                    border-color: var(--step-save-badge-color, var(--primary-color));
                    background-color: var(--step-save-badge-color, var(--primary-color));
                }

                /* Badge */
                :host([save]) span.badgeNumber {
                    display: none;
                }

                span.badgeNumber {
                    @apply --layout-horizontal;
                    @apply --layout-center-justified;
                    @apply --layout-center;
                    width: var(--step-badge-width, 18px);
                    height: var(--step-badge-height, 18px);
                }

                /* Badge and iron-icon */
                iron-icon#iconBtn,
                span.badgeNumber {
                    --iron-icon-height: 18px;
                    --iron-icon-width: 18px;
                    min-width: 18px;
                    border-radius: 25px;
                    border: 6px solid var(--step-badge-color, #9E9E9E);
                    background-color: var(--step-badge-color, #9E9E9E);
                    color: var(--step-badge-content-color, #FFFFFF);
                }

                paper-step-action-buttons paper-button {
                    @apply --button-style;
                }

                #stepContent {
                    width: 100%;
                }
            </style>

            <paper-button on-tap="_toggle">
                <iron-icon id="iconBtn" icon="my-icons:[[_getIcon(editable)]]"></iron-icon>
                <span class="badgeNumber">{{_badgeNumber}}</span>
                <div id="labelBtn">{{label}}
                    <span id="subtitle">Optional</span>
                </div>
            </paper-button>
            <div class="layout">
                <iron-collapse id="stepContent" opened="{{active}}" horizontal$="{{stepperHorizontal}}">
                    <slot></slot>
                    <paper-step-action-buttons id="stepButtons" continue-label="[[continueLabel]]" finish-label="[[finishLabel]]"
                        update-label="[[updateLabel]]" skip-label="[[skipLabel]]" skip-button="[[skipButton]]" back-label="[[backLabel]]"
                        back-button="[[backButton]]">
                    </paper-step-action-buttons>
                </iron-collapse>
            </div>
        `;
    }

    /**
     * Into this constructor we will initialize the badge value.
     * The badge value is determine according a property set and increment into the window.IGStepper.Stepper.Context
     */
    constructor() {
        super();
        // init the badge value
        window.IGStepper.Stepper.Context.numberOfStep = window.IGStepper.Stepper.Context.numberOfStep === undefined ? 1 : window.IGStepper.Stepper.Context.numberOfStep + 1;
        this._set_badgeNumber(window.IGStepper.Stepper.Context.numberOfStep);
        this._setStepperHorizontal(this.parentElement.horizontal);
        // if there is no step behind, we clear the number of step context temp we used.
        if (this.nextElementSibling === null) {
            this.parentElement.numberOfStep = window.IGStepper.Stepper.Context.numberOfStep;
            window.IGStepper.Stepper.Context.numberOfStep = undefined;
        }
    }

    /**
     * In this ready function, we will take care of oppening the step if it's the first one
     * And if the parameter is set for.
     * Then we will call the register function, which is used to register a step into the stepper.
     */
    ready() {
        super.ready();
        const openFirst = this._getOpenFirstStepOnStartup();
        // we open the first step according the value set on the stepper element.
        if (this._badgeNumber === 1) {
            this.active = openFirst;
        } else if (this._badgeNumber === 2 && openFirst) {
            this.parentElement.setNextStep(this);
        }
        // register the element
        this._register();
    }

    /**
     * Used in the horizontal mode to set the float property.
     * This is used to give the effect of the transition coming from left or right.
     *
     * @param {Boolean} active is the active step or not.
     * @private
     */
    _setFloatForTransition() {
        const toStep = this.parentElement.__toStep;
        const fromStep = this.parentElement.__fromStep;
        const { activeStep } = this.parentElement;

        if (toStep !== undefined && toStep !== null) {
            if (toStep._badgeNumber === this.parentElement.numberOfStep && !this.parentElement.horizontal) {
                this.$.stepContent.style.float = '';
            } else if (toStep._badgeNumber < this._badgeNumber) {
                this.$.stepContent.style.float = 'right';
            } else if (toStep._badgeNumber > this._badgeNumber) {
                this.$.stepContent.style.float = '';
            } else if (activeStep === undefined) {
                this.$.stepContent.style.float = '';
            } else if (toStep._badgeNumber === this._badgeNumber && fromStep !== undefined && toStep._badgeNumber < fromStep._badgeNumber) {
                this.$.stepContent.style.float = '';
            } else if (toStep._badgeNumber === this._badgeNumber && fromStep !== undefined && toStep._badgeNumber > fromStep._badgeNumber) {
                this.$.stepContent.style.float = 'right';
            } else if (toStep._badgeNumber === this._badgeNumber && activeStep === null) {
                this.$.stepContent.style.float = 'right';
            } else if (toStep._badgeNumber === this._badgeNumber && activeStep._badgeNumber < this._badgeNumber) {
                this.$.stepContent.style.float = 'right';
            } else if (toStep._badgeNumber === this._badgeNumber && activeStep._badgeNumber > this._badgeNumber) {
                this.$.stepContent.style.float = '';
            }
            // else if (toStep._badgeNumber === this._badgeNumber && !active)
            //     this.$.stepContent.style.float = "";
        }
    }

    /**
     * This is a callback function called whent the step title is clicked.
     * This will close all the open steps before opening the one selected, if the criteria are respected.
     * Moreover, if we are in a case of a modification, we will display the update button.
     * @private
     */
    _toggle() {
        if (!this.parentElement.finish && ((!this.parentElement.linear && (!this.save || this.editable)) || (this.parentElement.linear && this.save && this.editable || this.parentElement.activeStep.save && (this.parentElement.previousStep !== null && this.parentElement.previousStep.save)))) {
            this.parentElement.__closeAllStep(this);
            this.toggleStep();
            if (this.save && this.editable) this.$.stepButtons.setUpdate(true);
        }
    }

    /**
     * This function is used to toggle the step. That means, it will open the current step.
     * When a step is open the 'active' property is true.
     * @param {Boolean} isLast This property is used to indicate if this step is the last step of the stepper.
     *                         If it is, we will call the function setFinish() to set the good button.
     */
    toggleStep(isLast) {
        this._setFloatForTransition();
        if (isLast !== undefined && isLast) {
            this.$.stepButtons.setFinish(true);
        }
        this.$.stepContent.toggle();
    }

    /**
     * This function is used to set the finish action button state to true.
     * For this step the button will display the finish button. 
     */
    setFinishActionButtonsState() {
        this.$.stepButtons.setFinish(true);
    }

    /**
     * This function is used to get the good icon to display into the badge,
     * accordign to the 'editable' property.
     * @param {Boolean} editable true if it's an editable step, false otherwise.
     * @private
     */
    _getIcon(editable) {
        if (editable) return 'create';

        return 'check';
    }

    /**
     * This function is used to reinitialize all the parameter of this element
     * and the action buttons
     */
    reset(openFirstStep) {
        this.removeAttribute('save');
        this.active = false;
        this.$.stepButtons.reset();
        this.updateStyles();
        if (openFirstStep) {
            if (this._badgeNumber === 1) {
                this.active = true;
            } else if (this._badgeNumber === 2) {
                this.parentElement.setNextStep(this);
            }
        }
    }

    fireInvalidStep() {
        this.dispatchEvent(new CustomEvent('step-invalid', {
            bubbles: true,
            composed: true,
        }));
    }
}

customElements.define('paper-step', PaperStep);

/**
 * @namespace IGStepper
 */
window.IGStepper = window.IGStepper || {};
window.IGStepper.PaperStep = PaperStep;
