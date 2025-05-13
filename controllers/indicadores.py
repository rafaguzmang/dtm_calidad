from calendar import month
from datetime import datetime
from  odoo import  http
from odoo.http import request,Response
import json

class IndicadoresCalidad(http.Controller):

    @http.route('/calidad_indicadores', type='json', auth='public')
    def indicadores_calidad(self, **kwargs):

        get_calidad = request.env['dtm.calidad.rechazo'].search([]).mapped('job_no')
        indicadores = []
        for month in range(1,13):
            if month <= int(datetime.today().strftime("%m")):
                request.env.cr.execute(
                    " SELECT ot_number,create_date FROM dtm_facturado_odt WHERE EXTRACT(MONTH FROM create_date) = " + str(month) +
                    " AND EXTRACT(YEAR FROM create_date) = " + datetime.today().strftime("%Y") + ";")
                get_totales = request.env.cr.fetchall()
                ordenes = len([item[0] for item in get_totales])
                defectos = len(list(filter(lambda x: str(x) in get_calidad, [item[0] for item in get_totales])))
                porciento = round(((defectos * 100)/ordenes),2)
                mes = str(get_totales[0][1].strftime("%B")).capitalize()
                indicadores.append({'totales':ordenes,'defectos':defectos,'porciento':porciento,'mes':mes})

        result = indicadores

        return result
