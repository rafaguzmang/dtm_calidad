from odoo import fields,api,models
from datetime import datetime


class Calidad(models.Model):
    _name = 'dtm.calidad.rechazo'
    _description = 'Registro de calidad'

    consecutivo = fields.Integer(string='ID')
    job_no = fields.Char(string='JOB NO')
    po_number = fields.Char(string='P. O. NO.')
    part_no = fields.Char(string='PART NO')
    no_of_pieces_rejected = fields.Integer(string='NO. OF PIECES REJECTED')
    reason = fields.Char(string='REASON')
    inspector = fields.Char(string='INSPECTOR')
    date = fields.Date(string='DATE')

