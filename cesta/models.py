from odoo import models, fields, api


class cliente(models.Model):
    _name = 'cesta.cliente'
    _description = 'cesta.cliente'

    nombre = fields.Char(string='Nombre', required=True)
    numero_socio = fields.Integer(string='Número de socio', required=True)

    carritos_ids = fields.One2many('cesta.carrito', 'cliente_id', string='Carritos')


class carrito(models.Model):
    _name = 'cesta.carrito'
    _description = 'cesta.carrito'

    coste = fields.Float(string='Coste de la cesta', required=True)
    fecha = fields.Date(string='Fecha de compra')

    cliente_id = fields.Many2one('cesta.cliente', string='Cliente')
    cajero_id = fields.Many2one('cesta.cajero', string='Cajero')

    productos_ids = fields.One2many('cesta.producto_carrito', 'carrito_id', string='Productos')


class cajero(models.Model):
    _name = 'cesta.cajero'
    _description = 'cesta.cajero'

    nombre = fields.Char(string='Nombre')
    fecha_inicio = fields.Date(string='Fecha de inicio del contrato')

    carritos_ids = fields.One2many('cesta.carrito', 'cajero_id', string='Carritos')
    encargado_id = fields.Many2one('cesta.encargado', string='Encargado')


class encargado(models.Model):
    _name = 'cesta.encargado'
    _description = 'cesta.encargado'

    nombre = fields.Char(string='Nombre')
    fecha_inicio = fields.Date(string='Fecha de inicio del contrato')

    cajeros_ids = fields.One2many('cesta.cajero', 'encargado_id', string='Cajeros')


class producto(models.Model):
    _name = 'cesta.producto'
    _description = 'cesta.producto'

    nombre = fields.Char(string='Nombre del producto')
    precio_unidad = fields.Float(string='Precio unitario')
    stock = fields.Integer(string='Stock del producto')
    tipo = fields.Selection(string='Tipo de producto',
                            selection=[('alimentacion', 'Alimentación'), ('higiene', 'Higiene')])

    carritos_ids = fields.One2many('cesta.producto_carrito', 'producto_id', string='Carritos')


class producto_carrito(models.Model):
    _name = 'cesta.producto_carrito'
    _description = 'cesta.producto_carrito'

    producto_id = fields.Many2one('cesta.producto', string='Producto')
    carrito_id = fields.Many2one('cesta.carrito', string='Carrito')
