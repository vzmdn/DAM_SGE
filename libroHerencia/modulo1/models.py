# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Autor(models.Model):
    _name = 'modulo1.autor'
    _description = 'Autor'

    name = fields.Char(string='Nombre')
    surnameOne = fields.Char(string='Apellido 1')
    surnameTwo = fields.Char(string='Apellido 2')
    fechaNac = fields.Date(string='Fecha de nacimiento')
    libro_ids = fields.One2many('modulo1.libro', 'autor_id', string='Libros')
    ciudad = fields.Char(string='Ciudad')


class Libro(models.Model):
    _name = 'modulo1.libro'
    _description = 'Libro'

    name = fields.Char(string='Título')
    description = fields.Text(string='Sinopsis')
    pages = fields.Integer(string='Páginas')
    isbn = fields.Integer(string='ISBN')
    autor_id = fields.Many2one('modulo1.autor', string='Autor')
    purchase = fields.Boolean(string='Comprar')
