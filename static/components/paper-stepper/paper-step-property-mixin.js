/**
 * PaperStepPropertyMixin - Step Mixin.
 * @polymerMixin
 * @mixinFunction
 */
const PaperStepPropertyMixin = superClass => class extends superClass {
    static get properties() {
        return {
            /**
             * Property used to indicate if the step is saved.
             * True if it's saved, false otherwise.
             */
            save: {
                type: Boolean,
                value: false,
            },
            /**
             * Property used to indicate if the step is editable.
             * True if it's editable, false otherwise.
             */
            editable: {
                type: Boolean,
                value: false,
            },
            /**
             * Property used to indicate if the step is optional.
             * True if it's optional, false otherwise.
             */
            optional: {
                type: Boolean,
                value: false,
            },
            /**
             * Property used to indicate if the step is active.
             * If the step is active that means it will be open, and it's the current step we are focused on.
             * True if it's active, false otherwise.
             */
            active: {
                type: Boolean,
                value: false,
                reflectToAttribute: true,
                observer: 'changeActiveStep',
            },
            /**
             * The continue button text value
             * 'Continue' by default
             */
            continueLabel: {
                type: String,
                value: 'Continue',
            },
            /**
             * The finish button text value
             * 'Finish' by default
             */
            finishLabel: {
                type: String,
                value: 'Finish',
            },
            /**
             * The update button text value
             * 'Update' by default
             */
            updateLabel: {
                type: String,
                value: 'Update',
            },
            /**
             * The skip button text value
             * 'Skip' by default
             */
            skipLabel: {
                type: String,
                value: 'Skip',
            },
            /**
             * True to display the skip button, false otherwise.
             * If the step is linear, the skip button will do nothing, except if the property Optional is true.
             */
            skipButton: {
                type: Boolean,
                value: false,
                reflectToAttribute: true,
            },
            /**
             * The back button text value
             * 'Back' by default
             */
            backLabel: {
                type: String,
                value: 'Back',
            },
            /**
             * True to display the back button, false otherwise.
             */
            backButton: {
                type: Boolean,
                value: false,
            },
            /**
             * If true this will skip the validation of the input.
             * If false all the checkbox will have a native validation check on the input.
             *
             */
            noInputNativeValidity: {
                type: Boolean,
                value: false,
            },
        };
    }

    /**
     * This function is used to set the property save to true.
     */
    saveStep() {
        this.setAttribute('save', true);
    }

    /**
     * Getter used to know if the step is active or not.
     * @return {Boolean} True if it is, false otherwise.
     */
    isActive() {
        return this.active;
    }

    /**
     * This function is used to register an element to the parent.
     * @private
     */
    _register() {
        this.parentElement._registerStep(this);
    }

    /**
     * This function is used to check the validity of the required input.
     * This will check the native validation for classic input and call the validate() function for the polymer element.
     * @private
     */
    _nestedValidate() {
        // We check if the validity is required.
        if (this.noInputNativeValidity) return true;

        let result = true;
        this.querySelectorAll('[required]').forEach((el) => {
            let r;
            try {
                // Use classic input validation
                r = el.checkValidity();
            } catch (err) {
                // used to try on input that may be polymer input with a validate() function.
                try {
                    r = el.validate();
                } catch (err) {
                    console.log('caribou-step', "Can't validate required input");
                }
            }
            if (!r) result = false;
        });
        return result;
    }

    validate() {
        return true;
    }

    /**
     * This function is used to know if the property 'openFirstStepOnStartup' is set to true.
     * @private
     */
    _getOpenFirstStepOnStartup() {
        return this.parentElement.openFirstStepOnStartup;
    }

    changeActiveStep(active) {
        if (active) this.parentElement.setActiveStep(this);
    }
};

export default PaperStepPropertyMixin;
