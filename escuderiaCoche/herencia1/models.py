# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Coche(models.Model):
    _name = 'herencia1.coche'
    _description = 'herencia1.coche'

    nombre = fields.Char(string='Nombre')

    escuderia_id = fields.Many2one('herencia1.escuderia', string='Escuderia')

class Escuderia(models.Model):
    _name = 'herencia1.escuderia'
    _description = 'herencia1.escuderia'

    nombre = fields.Char(string='Escuderia')

    coches_ids = fields.One2many('herencia1.coche', 'escuderia_id', string='Coches')