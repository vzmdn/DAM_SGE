# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Editorial(models.Model):
    _inherit = 'modulo1.libro'

    editorial_id = fields.Many2one('modulo2.editorial', string='Editorial')
