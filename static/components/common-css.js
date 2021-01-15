import { css } from 'lit-element';

const cardCss = css`
    .card {
        padding: 10px;
        border-radius: 2px;
        background-color: white;
        box-shadow: var(--shadow-elevation-2dp_-_box-shadow);
    }
`;

const progressCss = css`
    paper-progress {
        width: 100%;
        --paper-progress-active-color: var(--app-primary-color);
    }
`;

export { cardCss, progressCss };