/**
 * ModalMixin - Mixin to open modal from window event.
 * @mixinFunction
 */
const ModalMixin = (superClass) => class extends superClass {
    static get properties() {
        return {
            /** Indica si el modal se esta mostrando. */
            opened: {
                type: Boolean,
                reflect: true,
            },
        };
    }

    constructor() {
        super();
        this.opened = false;
        this.openModalEvent = '';
        this._boundOpenListener = this._open.bind(this);
    }

    // lifecycles

    connectedCallback() {
        super.connectedCallback();
        window.addEventListener(this.openModalEvent, this._boundOpenListener);
    }

    disconnectedCallback() {
        window.removeEventListener(this.openModalEvent, this._boundOpenListener);
        super.disconnectedCallback();
    }

    _open(e) {
        this._handleOpenEvent(e);
        this.opened = true;
    }

    _handleOpenEvent(e) {
        throw new Error('Implement me!!!!');
    }
};

export default ModalMixin;