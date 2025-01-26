# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, timedelta, time

from odoo.exceptions import UserError


class Cliente(models.Model):
    _name = 'garajes.cliente'
    _description = 'garajes.cliente'

    nombre = fields.Char(string='Nombre')
    apellido1 = fields.Char(string='Primer apellido')
    apellido2 = fields.Char(string='Segundo apellido')
    reservas = fields.Integer(string='Reservas', compute='_compute_reservas')
    dinero_inicial = fields.Float(string='Dinero inicial')
    dinero = fields.Float(string='Dinero', compute='_compute_dinero', store=True)

    reservas_ids = fields.One2many('garajes.reserva', 'cliente_id', string='Reservas')

    def name_get(self):
        result = []
        for record in self:
            name = record.nombre + ' ' + record.apellido1
            result.append((record.id, name))
        return result

    @api.depends('reservas_ids')
    def _compute_reservas(self):
        for record in self:
            record.reservas = len(record.reservas_ids)

    @api.depends('reservas_ids','dinero_inicial')
    def _compute_dinero(self):
        for record in self:
            gastado = 0
            record.dinero = record.dinero_inicial
            for reserva in record.reservas_ids:
                gastado += reserva.precio
            record.dinero -= gastado


class Coche(models.Model):
    _name = 'garajes.coche'
    _description = 'garajes.coche'

    matricula = fields.Char(string='Matrícula')
    marca = fields.Char(string='Marca')
    modelo = fields.Char(string='Modelo')
    coste_dia = fields.Float(string='€/dia')
    reservado = fields.Boolean(string='Reservado', compute='_compute_reservado', store=True)

    reserva_id = fields.One2many('garajes.reserva', 'coche_id', string='Reservas')

    garaje_id = fields.Many2one('garajes.garaje', string='Garaje')

    def name_get(self):
        result = []
        for record in self:
            name = record.marca + ' ' + record.modelo + ' - ' + record.matricula
            result.append((record.id, name))
        return result

    @api.depends('reserva_id')
    def _compute_reservado(self):
        for record in self:
            record.reservado = bool(record.reserva_id)


class Reserva(models.Model):
    _name = 'garajes.reserva'
    _description = 'garajes.reserva'

    fecha_inicio = fields.Date(string='Fecha inicio', compute='_compute_fecha_inicio', store=True)
    fecha_fin = fields.Date(string='Fecha fin', compute='_compute_fecha_fin', store=True)
    hora = fields.Char(string='Hora', compute='_compute_hora', store=True)
    dias = fields.Integer(string='Días')
    precio = fields.Float(string='Precio', compute='_compute_precio', store=True)

    cliente_id = fields.Many2one('garajes.cliente', string='Cliente')

    coche_id = fields.Many2one('garajes.coche', string='Coche', domain=[('reservado', '=', False)])

    def name_get(self):
        result = []
        for record in self:
            name = record.cliente_id.nombre + ' ' + record.cliente_id.apellido1 + ' - ' + record.coche_id.matricula
            result.append((record.id, name))
        return result

    @api.depends('cliente_id')
    def _compute_fecha_inicio(self):
        for record in self:
            record.fecha_inicio = date.today()

    @api.depends('dias')
    def _compute_fecha_fin(self):
        for record in self:
            record.fecha_fin = record.fecha_inicio + timedelta(days=record.dias)

    @api.depends('cliente_id')
    def _compute_hora(self):
        for record in self:
            record.hora = datetime.now().time().strftime('%H:%M')

    @api.depends('dias')
    def _compute_precio(self):
        for record in self:
            record.precio = record.coche_id.coste_dia * record.dias

    @api.constrains('cliente_id', 'precio')
    def _check_cliente_dinero(self):
        for record in self:
            # Get the current money available for the client
            dinero_inicial = record.cliente_id.dinero_inicial
            print("dinero_inicial: " + str(dinero_inicial))
            gastado = 0
            for reserva in record.cliente_id.reservas_ids:
                if reserva.id != record.id:  # Ensure the current reservation is not included
                    gastado += reserva.precio
                    print("gastado: " + str(gastado))

            print("gastado + record.precio " + str(gastado + record.precio))
            # Check if the client has enough money for the current reservation
            if dinero_inicial < gastado + record.precio:
                raise UserError("El cliente no tiene suficiente dinero para realizar esta reserva.")


class Garaje(models.Model):
    _name = 'garajes.garaje'
    _description = 'garajes.garaje'

    calle = fields.Char(string='Calle')
    numero = fields.Integer(string='Número')
    plazas_totales = fields.Integer(string='Plazas')
    plazas_ocupadas = fields.Integer(string='Ocupadas', compute='_compute_plazas_ocupadas', store=True)
    plazas_libres = fields.Integer(string='Libres', compute='_compute_plazas_libres', store=True)

    coches_ids = fields.One2many('garajes.coche', 'garaje_id', string='Coche')

    def name_get(self):
        result = []
        for record in self:
            name = record.calle + ' - ' + str(record.numero)
            result.append((record.id, name))
        return result

    @api.depends('plazas_totales', 'coches_ids')
    def _compute_plazas_ocupadas(self):
        for record in self:
            record.plazas_ocupadas = len(record.coches_ids)

    @api.depends('plazas_ocupadas')
    def _compute_plazas_libres(self):
        for record in self:
            record.plazas_libres = record.plazas_totales - record.plazas_ocupadas
