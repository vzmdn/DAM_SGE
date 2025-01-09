from odoo import models, fields, api
from datetime import date


class jugador(models.Model):
    _name = 'partido2.jugador'
    _description = 'partido2.jugador'

    name = fields.Char(string="Nombre", required=True)
    posicion = fields.Char(string="Posicion")
    apellido = fields.Char(string="Apellido")
    fecha_nacimiento = fields.Date(string='Fecha de nacimiento')
    edad = fields.Integer(string='Edad', compute='_compute_age')

    equipojugadores_id = fields.One2many('partido2.equipojugador', 'jugador_id', string='Jugador')

    @api.depends('fecha_nacimiento')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.fecha_nacimiento:
                record.edad = today.year - record.fecha_nacimiento.year - (
                            (today.month, today.day) < (record.fecha_nacimiento.month, record.fecha_nacimiento.day))
            else:
                record.edad = 0


class equipo(models.Model):
    _name = 'partido2.equipo'
    _description = 'partido2.equipo'

    name = fields.Char(string="Nombre", required=True)

    equipojugadores_id = fields.One2many('partido2.equipojugador', 'equipo_id', string='Equipo')


class equipojugador(models.Model):
    _name = 'partido2.equipojugador'
    _description = 'partido2.equipojugador'

    name = fields.Char(string="Nombre", required=True)
    fecha_contrato = fields.Date(string="Fecha de inicio del contrato")

    jugador_id = fields.Many2one('partido2.jugador', string='Jugador')
    equipo_id = fields.Many2one('partido2.equipo', string='Equipo')

    def name_get(self):
        result = []
        for record in self:
            name = '(' + record.jugador_id.name + ') ' + record.equipo_id.name
            result.append((record.id, name))
        return result

class partido(models.Model):
    _name = 'partido2.partido'
    _description = 'partido2.partido'

    equipo_local_id = fields.Many2one('partido2.equipo', string='Equipo local')
    equipo_visitante_id = fields.Many2one('partido2.equipo', string='Equipo visitante')
    goles_local = fields.Integer(string='Goles local')
    goles_visitante = fields.Integer(string='Goles visitante')
    ganador = fields.Char(string="Ganador", compute='_compute_ganador')

    @api.depends('goles_local','goles_visitante')
    def _compute_ganador(self):
        for record in self:
            if record.goles_visitante < record.goles_local:
                record.ganador = "Equipo local"
            elif record.goles_visitante > record.goles_local:
                record.ganador = "Equipo visitante"
            else:
                record.ganador = "Empate"

