from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Cliente(models.Model):
    _name = 'supermercado.cliente'
    _description = 'supermercado.cliente'

    nombre = fields.Char(string='Nombre', required=True)
    numero_socio = fields.Integer(string='Número de socio', required=True)
    total_gastado = fields.Float(string='Total gastado', compute='_compute_gastado')

    cestas_ids = fields.One2many('supermercado.cesta', 'cliente_id', string='cestas')

    country_id = fields.Many2one('res.country', string='País')

    @api.depends('cestas_ids.coste')
    def _compute_gastado(self):
        for record in self:
            record.total_gastado = sum(cesta.coste for cesta in record.cestas_ids)

    def name_get(self):
        result = []
        for record in self:
            name = record.nombre
            result.append((record.id, name))
        return result


class Cesta(models.Model):
    _name = 'supermercado.cesta'
    _description = 'supermercado.cesta'

    coste = fields.Float(string='Coste de la cesta', required=True, compute='_compute_coste')
    fecha = fields.Date(string='Fecha de compra')

    cliente_id = fields.Many2one('supermercado.cliente', string='Cliente', required=True)
    cajero_id = fields.Many2one('supermercado.cajero', string='Cajero', required=True)

    productos_ids = fields.One2many('supermercado.producto_cesta', 'cesta_id', string='Productos')

    @api.depends('productos_ids.total')
    def _compute_coste(self):
        for record in self:
            record.coste = sum(producto.total for producto in record.productos_ids)

    @api.constrains('fecha')
    def _check_fecha(self):
        for record in self:
            if record.fecha and record.fecha > fields.Date.today():
                raise ValidationError("La fecha no puede ser posterior a hoy.")

    def name_get(self):
        result = []
        for record in self:
            name = f"Cesta de {record.cliente_id.nombre} - {record.fecha}"
            result.append((record.id, name))
        return result


class Cajero(models.Model):
    _name = 'supermercado.cajero'
    _description = 'supermercado.cajero'

    nombre = fields.Char(string='Nombre')
    fecha_inicio = fields.Date(string='Fecha de inicio del contrato')

    total_cobrado = fields.Float(string='Total Cobrado', compute='_compute_total_cobrado', store=True)

    cestas_ids = fields.One2many('supermercado.cesta', 'cajero_id', string='cestas')
    encargado_id = fields.Many2one('supermercado.encargado', string='Encargado')


    def name_get(self):
        result = []
        for record in self:
            name = record.nombre
            result.append((record.id, name))
        return result

    @api.depends('cestas_ids.coste')
    def _compute_total_cobrado(self):
        for record in self:
            record.total_cobrado = sum(cesta.coste for cesta in record.cestas_ids)


class Encargado(models.Model):
    _name = 'supermercado.encargado'
    _description = 'supermercado.encargado'

    nombre = fields.Char(string='Nombre')
    fecha_inicio = fields.Date(string='Fecha de inicio del contrato')

    cajeros_ids = fields.One2many('supermercado.cajero', 'encargado_id', string='Cajeros')

    def name_get(self):
        result = []
        for record in self:
            name = record.nombre
            result.append((record.id, name))
        return result


class Producto(models.Model):
    _name = 'supermercado.producto'
    _description = 'supermercado.producto'

    nombre = fields.Char(string='Nombre del producto')
    precio_unidad = fields.Float(string='Precio unitario')
    stock_inicial = fields.Integer(string='Stock inicial ', store=True)
    stock = fields.Integer(string='Stock del producto', compute='_compute_stock', store=True)
    tipo = fields.Selection(string='Tipo de producto',
                            selection=[('alimentacion', 'Alimentación'), ('higiene', 'Higiene')])

    cestas_ids = fields.One2many('supermercado.producto_cesta', 'producto_id', string='cestas')

    def name_get(self):
        result = []
        for record in self:
            name = record.nombre
            result.append((record.id, name))
        return result

    @api.depends('cestas_ids.cantidad', 'stock_inicial')
    def _compute_stock(self):
        for record in self:
            stock = record.stock_inicial
            total_cesta_quantity = sum(cesta.cantidad for cesta in record.cestas_ids)
            record.stock = stock - total_cesta_quantity


class ProductoCesta(models.Model):
    _name = 'supermercado.producto_cesta'
    _description = 'supermercado.producto_cesta'

    producto_id = fields.Many2one('supermercado.producto', string='Producto')
    cesta_id = fields.Many2one('supermercado.cesta', string='Cesta')

    cantidad = fields.Integer(string='Cantidad', default=1)
    precio = fields.Float(related='producto_id.precio_unidad', string='Precio', store=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('cantidad', 'precio')
    def _compute_total(self):
        for record in self:
            record.total = record.cantidad * record.precio
