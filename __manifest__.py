{
    'name': 'Calidad',
    'version': '1.0',
    'description': 'Modulo para llevar las actividades de calidad',
    'author': 'Rafael Guzmán Granados',
    'depends': ["base"],
    'data': [
        'views/dtm_calidad_rechazo_view.xml',
        'views/seguimiento_view.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'dtm_calidad/static/src/css/styles.css',
            'dtm_calidad/static/src/js/indicadores.js',
            'dtm_calidad/static/src/xml/indicadores.xml',
            'dtm_calidad/static/lib/chart.js',  # Ruta local que usarás para Chart.js
            'dtm_calidad/static/lib/chartjs-plugin-annotation.js',
            ],
    },
    'installable': True,
    'auto_install': False
}
