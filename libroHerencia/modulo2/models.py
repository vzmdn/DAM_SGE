# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Editorial(models.Model):
    _name = 'modulo2.editorial'
    _description = 'Editorial'

    name = fields.Char(string='Empresa')
    fechaCreacion = fields.Date(string='Fecha de creación')
    libro_ids = fields.One2many('modulo1.libro', 'editorial_id', string='Libros')
    ciudad = fields.Char(string='Ciudad')
