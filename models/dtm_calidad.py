from odoo import models,fields,api
from odoo.exceptions import ValidationError, AccessError, MissingError,Warning


class Calidad(models.Model):
    _name = "dtm.calidad"
    _inherit = ['mail.thread']
    _description = "Modelo para llevar el control de calidad"
    _order = "ot_number desc"

    status = fields.Selection(string="Estatus", selection=[("aprobacion","Pendiente a aprobación"),
                                         ("corte","Corte"),("corterevision","Corte - Revisión FAI"),
                                         ("revision","Revisión FAI"),("corterevision","Corte - Revisión FAI"),
                                         ("cortedoblado","Corte - Doblado"),("doblado","Doblado"),
                                         ("soldadura","Soldadura"),("lavado","Lavado"),("pintura","Pintura"),
                                         ("ensamble","Ensamble"),("calidad","Calidad"),("instalacion","Instalación"),
                                         ("terminado","Terminado")])


    sequence = fields.Integer()
    ot_number = fields.Char(string="NÚMERO",readonly=True)
    tipe_order = fields.Char(string="TIPO",readonly=True)
    name_client = fields.Char(string="CLIENTE",readonly=True)
    product_name = fields.Char(string="NOMBRE DEL PRODUCTO",readonly=True)
    date_in = fields.Date(string="FECHA DE ENTRADA", readonly=True)
    po_number = fields.Char(string="PO",readonly=True)
    date_rel = fields.Date(string="FECHA DE ENTREGA",readonly=True)
    version_ot = fields.Integer(string="VERSIÓN OT",readonly=True)
    color = fields.Char(string="COLOR",readonly=True)
    cuantity = fields.Integer(string="CANTIDAD",readonly=True)
    materials_ids = fields.Many2many("dtm.materials.line",readonly=True)
    planos = fields.Boolean(string="Planos",default=False,readonly=True)
    nesteos = fields.Boolean(string="Nesteos",default=False,readonly=True)

    rechazo_id = fields.Many2many("dtm.odt.rechazo",readonly=False)
    anexos_id = fields.Many2many("dtm.proceso.anexos",readonly=True)
    cortadora_id = fields.Many2many("dtm.proceso.cortadora",readonly=True)
    primera_pieza_id = fields.Many2many("dtm.proceso.primer",readonly=True)
    tubos_id = fields.Many2many("dtm.proceso.tubos",readonly=True)

    material_cortado = fields.Boolean(default=False)

    firma = fields.Char(string="Firma", readonly = True)
    firma_compras = fields.Char(string = "Compras", readonly = True)
    firma_diseno = fields.Char(string = "Diseñador", readonly = True)
    firma_almacen = fields.Char(string = "", readonly = True)
    firma_ventas = fields.Char(string = "Ventas", readonly = True)
    firma_proceso = fields.Char(string = "", readonly = True)

    #---------------------Resumen de descripción------------

    description = fields.Text(string= "DESCRIPCIÓN",placeholder="RESUMEN DE DESCRIPCIÓN")

    notes = fields.Text()
    #------------------Datos exclusivos de este modelo----------------------------
    pausa = fields.Boolean()
    pausa_motivo = fields.Text()
    #-----------------------------------
    pausado = fields.Char(string="Detenido por: ", readonly=True)
    status_pausado = fields.Char()
    pausa_motivo = fields.Text()

    materials = fields.Integer(string="Material")
    firma_parcial = fields.Boolean()
    firma_ventas_kanba = fields.Char(string = "Ventas", readonly = True)
    firma_compras_kanba = fields.Char(string = "Compras", readonly = True)
    firma_almacen_kanba = fields.Char(string = "", readonly = True)
    firma_calidad_kanba = fields.Char(string = "", readonly = True)

    def action_detener(self):
        get_pro = self.env['dtm.proceso'].search([("ot_number","=",self.ot_number),("tipe_order","=",self.tipe_order)])
        get_pro.write({
            "pausado":"Pausado por Calidad",
            "status_pausado": get_pro.status,
            "pausa_motivo": self.pausa_motivo
        })
        self.pausa = True

    def action_continuar(self):
        get_pro = self.env['dtm.proceso'].search([("ot_number","=",self.ot_number),("tipe_order","=",self.tipe_order)])
        get_pro.write({
                "pausado":"",
                "status_pausado": ""
            })
        self.pausa = False

    def action_firma(self):
        self.firma = self.env.user.partner_id.name
        get_ot = self.env['dtm.odt'].search([("ot_number","=",self.ot_number)])
        get_ot.write({"firma_produccion": self.firma})
        get_proc = self.env['dtm.proceso'].search([("ot_number","=",self.ot_number),("tipe_order","=",self.tipe_order)])
        if get_proc.status == 'calidad' and get_proc.firma_compras_kanba and get_proc.firma_almacen_kanba and get_proc.firma_ventas_kanba:
            print(get_proc.status,get_proc.firma_compras_kanba,get_proc.firma_almacen_kanba,get_proc.firma_ventas_kanba)
            get_proc.write({
                "firma_calidad": self.firma,
                "firma_calidad_kanba":"Calidad"
            })

        else:
            raise ValidationError("OT/NPI debe de estar en status Calidad o faltan firmas")

    def get_view(self, view_id=None, view_type='form', **options):
        res = super(Calidad,self).get_view(view_id, view_type,**options)

        get_process = self.env['dtm.proceso'].search([])
        for proceso in get_process:
            vals = {
                "status": proceso.status,
                "sequence": proceso.sequence,
                "ot_number": proceso.ot_number,
                "tipe_order": proceso.tipe_order,
                "name_client": proceso.name_client,
                "product_name": proceso.product_name,
                "date_in": proceso.date_in,
                "po_number": proceso.po_number,
                "date_rel": proceso.date_rel,
                "version_ot": proceso.version_ot,
                "color": proceso.color,
                "cuantity": proceso.cuantity,
                "materials_ids": proceso.materials_ids,
                "planos": proceso.planos,
                "nesteos": proceso.nesteos,
                "rechazo_id":proceso.rechazo_id,
                "anexos_id":proceso.anexos_id,
                "cortadora_id":proceso.cortadora_id,
                "primera_pieza_id":proceso.primera_pieza_id,
                "tubos_id":proceso.tubos_id,
                "firma_proceso": proceso.firma,
                "firma_compras": proceso.firma_compras,
                "firma_diseno": proceso.firma_diseno,
                "firma_almacen": proceso.firma_almacen,
                "firma_ventas": proceso.firma_ventas,
                "description": proceso.description,
                "pausado": proceso.pausado,
                "status_pausado": proceso.status_pausado,
                "pausa_motivo": proceso.pausa_motivo,
                "materials": proceso.materials,
                "firma_parcial": proceso.firma_parcial,
                "firma_ventas_kanba": proceso.firma_ventas_kanba,
                "firma_compras_kanba": proceso.firma_compras_kanba,
                "firma_almacen_kanba": proceso.firma_almacen_kanba,
                "firma_calidad_kanba": proceso.firma_calidad_kanba,
            }


            get_self = self.env['dtm.calidad'].search([("ot_number","=", proceso.ot_number)])
            if get_self:
                get_self.write(vals)
            else:
                get_self.create(vals)

        return res


