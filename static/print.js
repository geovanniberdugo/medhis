const printFab = document.querySelector('#print-button');
printFab.addEventListener('click', () => window.print());

const mediaQueryList = window.matchMedia('print');
mediaQueryList.addListener((mql) => {
    if (mql.matches) {
        document.querySelector('app-header-layout')._updateLayoutStates();
    }
});
