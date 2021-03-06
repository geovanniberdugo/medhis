import { PolymerElement, html } from '@polymer/polymer/polymer-element';
import StepperPropertyMixin from './paper-stepper-property-mixin';
import './paper-step';

/**
 * `paper-stepper` Stepper.
 *
 * @customElement
 * @polymer
 * @demo
 *
 */
class PaperStepper extends StepperPropertyMixin(PolymerElement) {
    static get properties() {
        return {
            /**
             * Contain all the steps registered.
             */
            _steps: {
                type: Array,
                value: () => [],
            },
            /**
             * This property is toggled when the reset function is called.
             * When we are currently resetting the value, the property is true, false otherwise.
             * @readonly
             */
            isResetting: {
                type: Boolean,
                value: false,
                readOnly: true,
            },
        };
    }

    static get template() {
        return html`
            <style>
                :host {
                    display: block;
                    --primary-color: #2196F3;
                    position: relative;
                }
                :host([horizontal]) {
                    @apply --layout-horizontal;
                }
            </style>
            <slot></slot>
        `;
    }

    /**
     * This function is used by the `caribou-step` to register into the `caribou-stepper`.
     * Then multiple event fired from the stepper can be handled :
     *  - last-step-closed
     *  - continue-clicked : call the __nextStep() function.
     *  - finish-clicked : call the __nextStep() function.
     *  - skip-clicked : call the __skipStep() function.
     *  - update-clicked : call the __nextStep() function.
     *
     *  All elements registered are added into the _steps property.
     */
    _registerStep(element) {
        this.push('_steps', element);
        // element.addEventListener("last-step-closed", this._validStepper.bind(this));
        element.addEventListener('continue-clicked', this.__nextStep.bind(this));
        element.addEventListener('finish-clicked', this.__finishStep.bind(this));
        element.addEventListener('skip-clicked', this.__skipStep.bind(this));
        element.addEventListener('back-clicked', this.__previousStep.bind(this));
        element.addEventListener('update-clicked', this.__nextStep.bind(this));
    }

    /**
     * This is a private callback function used to go to the next step when a button is clicked.
     * This will save and close the active step, then open the next one.
     * @private
     */
    __nextStep() {
        this.openNextStep();
    }
    /**
     * This is a private callback function used to skip the current state and open the next one.
     * This can be done only if we are in linear mode.
     * @private
     */

    __skipStep() {
        this.skipStep();
    }

    /**
     * This is a private callback function used to skip the current state and open the next one.
     * This can be done only if we are in linear mode.
     * @private
     */
    __previousStep() {
        this.openPreviousStep();
    }

    /**
     * This is a private callback function used to skip the current state and open the next one.
     * This can be done only if we are in linear mode.
     * @private
     */
    __finishStep() {
        if (this.activeStep._nestedValidate() && this.activeStep.validate()) {
            this.openNextStep();
            this._setFinish(true);
            this.dispatchEvent(new CustomEvent('stepper-finished', {
                bubbles: true,
                composed: true,
            }));
            // console.log("caribou-stepper finished.");
        } else {
            this.activeStep.fireInvalidStep();
        }
    }

    /**
     * This function is used to open the next step.
     * It will save and close the current active step.
     * Then it will open the next step if there is one.
     */
    openNextStep() {
        if (this.activeStep._nestedValidate() && this.activeStep.validate()) {
            this.activeStep.saveStep();
            // set the value to and from the the transition effect.
            this.__fromStep = this.activeStep;
            this.__toStep = this.nextStep;
            // toggle the step
            this.activeStep.toggleStep();
            this.removeActiveStep();
            if (this.nextStep !== null) this.nextStep.toggleStep();
        } else {
            this.activeStep.fireInvalidStep();
        }
    }

    /**
     * This function is used to open the next step.
     * It will save and close the current active step.
     * Then it will open the next step if there is one.
     */
    openPreviousStep() {
        this.activeStep.toggleStep();
        this.removeActiveStep();
        if (this.previousStep !== null) this.previousStep.toggleStep();
    }

    /**
     * This function is used to skip the current active step.
     * This function can work only if we are not in linear mode.
     * TODO : allow the
     */
    skipStep() {
        if ((this.linear && this.activeStep.optional) || !this.linear) {
            if (this.linear) this.activeStep.saveStep();
            this.activeStep.toggleStep();
            if (this.nextStep !== null) this.nextStep.toggleStep();
        } else {
            console.log("can't skip you are in linear mode.");
        }
    }

    /**
     * This function is used to close all the steps and save the target step
     * that is the initiative of the close.
     * @param {Object} stepInitiator The step inititor and targeted.
     */
    __closeAllStep(stepInitiator) {
        // we set the to step used for the transition from the step button.
        this.__toStep = stepInitiator;
        this.closeAllStep();
    }

    /**
     * This function is used to close all the steps.
     */
    closeAllStep() {
        for (let i = 0; i < this._steps.length; i++) {
            const step = this.getStepById(i);
            if (step.isActive()) {
                step.toggleStep();
            }
        }
    }

    /**
     * This function is used to check if all steps are saved, 
     * if not, it will open the first step in linear order that is not saved.
     *
     * @return {Object} The stepper to open if there is or null.
     * @private
     */
    _getUnsavedStep() {
        for (let i = 0; i < this._steps.length; i++) {
            const step = this.getStepById(i);
            if (!step.save) {
                if (step !== this.activeStep) return step;
            }
        }
        return null;
    }

    /**
     * This function is used to check all the previous step the the active one.
     * If there is a step that is not saved or editabled, we returned it.
     *
     * @return {Object} The stepper to open if there is or null.
     * @private
     */
    _getPreviousStep() {
        for (let i = this.activeStep._badgeNumber - 1; i === 0; i--) {
            const step = this.getStepById(i);
            if (!step.save || step.editable) {
                if (step !== this.activeStep) return step;
            }
        }
        return null;
    }

    /**
     * This function is used to return the step element
     * situated at the specific ID.
     * @param {Number} id The id of the step to retrieve
     * @return {Object} The stepper object.
     */
    getStepById(id) {
        return this.get(['_steps', id]);
    }

    /**
     * This function is used to set the active step.
     * @param {Object} step The step object.
     */
    setActiveStep(step) {
        this.activeStep = step;
        // When we are resetting the values, the activeStep and next step depends of the 'openFirstStepOnStartup' property.
        if (!this.isResetting) {
            this.setNextStep(this.findNextStep(step));
            this.setPreviousStep(this.findPreviousStep(step));
            if (this.nextStep === null) this.activeStep.setFinishActionButtonsState(true);
        }
    }

    /**
     * This function is used clear the active step property.
     */
    removeActiveStep() {
        this.activeStep = null;
    }

    /**
     * This function is used to set the nextStep property.
     * @param {Object} step The step object
     */
    setNextStep(step) {
        this.nextStep = step;
    }

    /**
     * This function is used to set the previousStep property.
     * @param {Object} step The step object
     */
    setPreviousStep(step) {
        this.previousStep = step;
    }

    /**
     * This function is used to find the next next following step of a specific one.
     * @param {Object} activeStep The step from which we are looking the next possible step.
     */
    findNextStep(activeStep) {
        if (activeStep.nextElementSibling !== undefined && activeStep.nextElementSibling !== null && !activeStep.nextElementSibling.save) {
            return activeStep.nextElementSibling;
        }
        
        if (activeStep.nextElementSibling !== undefined && activeStep.nextElementSibling !== null) {
            return this.findNextStep(activeStep.nextElementSibling);
        }
        
        return this._getUnsavedStep();
    }

    /**
     * This function is used to find the next next following step of a specific one.
     * @param {Object} activeStep The step from which we are looking the next possible step.
     */
    findPreviousStep(activeStep) {
        if (activeStep.previousElementSibling !== undefined && activeStep.previousElementSibling === null) {
            return activeStep.previousElementSibling;
        }

        if (activeStep.previousElementSibling !== undefined && activeStep.previousElementSibling !== null && (!activeStep.previousElementSibling.save || activeStep.previousElementSibling.editable)) {
            return activeStep.previousElementSibling;
        }
        
        if (activeStep.previousElementSibling !== undefined && activeStep.previousElementSibling !== null) {
            return this.findPreviousStep(activeStep.previousElementSibling);
        }

        return this._getPreviousStep();
    }

    /**
     * This function is used to reinitialize all the parameter of this element
     * and from all the steppers.
     */
    reset() {
        this._setIsResetting(true);
        this._setFinish(false);
        this.activeStep = undefined;
        this.nextStep = undefined;
        for (let i = 0; i < this._steps.length; i++) {
            const step = this.getStepById(i);
            step.reset(this.openFirstStepOnStartup);
        }
        this._setIsResetting(false);
    }
}

customElements.define('paper-stepper', PaperStepper);

/**
 * @namespace IGStepper
 */
window.IGStepper = window.IGStepper || {};
window.IGStepper.PaperStepper = PaperStepper;
