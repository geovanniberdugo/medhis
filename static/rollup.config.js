import resolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import replace from 'rollup-plugin-replace';
import { terser } from 'rollup-plugin-terser';
import rimraf from 'rimraf';

rimraf.sync('build');

const ENV = process.env.BUILD || 'development';
const production = process.env.BUILD === 'production';
const assets = [
    'pages/mh-rips.js',
    'pages/mh-cajas.js',
    'pages/mh-tarifas.js',
    'pages/mh-medicos.js',
    'pages/mh-facturas.js',
    'pages/mh-dashboard.js',
    'pages/mh-tratamientos.js',
    'pages/mh-agenda-citas.js',
    'pages/mh-print-factura.js',
    'pages/mh-agenda-diaria.js',
    'pages/mh-detalle-orden.js',
    'pages/mh-control-citas.js',
    'pages/mh-pagos-paciente.js',
    'pages/mh-print-historia.js',
    'pages/mh-paciente-nuevo.js',
    'pages/mh-resolucion-256.js',
    'pages/mh-asignacion-citas.js',
    'pages/mh-detalle-paciente.js',
    'pages/mh-horario-atencion.js',
    'pages/mh-facturacion-siigo.js',
    'pages/mh-relacion-facturas.js',
    'pages/mh-oportunidad-citas.js',
    'pages/mh-citas-no-cumplidas.js',
    'pages/mh-print-detalle-caja.js',
    'pages/mh-historias-paciente.js',
    'pages/mh-print-agenda-diaria.js',
    'pages/mh-relacion-recibos-caja.js',
    'pages/mh-citas-servicio-entidad.js',
    'pages/mh-print-oportunidad-cita.js',
    'pages/mh-certificado-asistencia.js',
    'pages/mh-relacion-citas-paciente.js',
    'pages/mh-ind-mortalidad-morbilidad.js',
    'pages/mh-tratamientos-pago-medicos.js',
    'pages/mh-medicos-ordenan-tratamiento.js',
    'pages/mh-print-citas-servicio-entidad.js',
    'pages/mh-tratamientos-pago-terapeutas.js',
    'pages/mh-contabilizacion-recibos-caja.js',
    'pages/mh-tratamientos-facturados-entidad.js',
    'pages/mh-print-ind-mortalidad-morbilidad.js',
    'pages/mh-pacientes-terminaron-tratamiento.js',
    'pages/mh-tratamientos-no-facturados-entidad.js',
    'pages/mh-tratamientos-iniciados-profesional.js',
    'pages/mh-tratamientos-terminados-profesional.js',
    'pages/mh-tratamientos-no-terminados-profesional.js',
];

export default {
    input: assets,
    output: [
        {
            dir: 'build/pages',
            format: 'es',
            sourcemap: true,
        },
    ],
    plugins: [
        replace({
            'process.env.NODE_ENV': JSON.stringify(ENV),
        }),
        resolve(),
        commonjs({
            namedExports: {
                '@fullcalendar/core': ['Calendar'],
            },
        }),
        production && terser(),
    ],
    watch: {
        include: 'pages/**',
    },
};
