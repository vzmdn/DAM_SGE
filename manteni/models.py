# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date, timedelta


class Machine(models.Model):
    # Machines
    _name = 'manteni.machine'

    name = fields.Char(size=32, string='Machine name', index=True)
    serial = fields.Char(size=32, string='Serial no', index=True)
    suplier_id = fields.Many2one('res.partner', string='Suplier',
                                 domain=[('parent_id', '=', False), ('machinery_seller', '=', True)])
    date_begin = fields.Date(string='Date begin', default=fields.Date.today)
    date_first_maintenance = fields.Date(compute='_maintenance_date')
    state = fields.Selection([('on_use', 'On use'), ('repairing', 'Repairing'), ('out_order', 'Out of order')],
                             string='State', default='on_use')
    city = fields.Char(related='suplier_id.city', store=False)
    hours_maint = fields.Integer(string='Hours till maintenances')
    active = fields.Boolean('Active', default=True)

    _sql_constraints = [('name_uniq', 'unique (name)', "Title name already exists !"),
                        ('serial_uniq', 'unique (serial)', "Serial code already exists !")]

    def _maintenance_date(self):
        for record in self:
            fecha = record.date_begin
            record.date_first_maintenance = fecha + timedelta(hours=record.hours_maint)


class Program(models.Model):
    # Maintenance programs, conjunt of rules.
    _name = 'manteni.program'

    name = fields.Char(string='Name', size=64, required=True)
    instruction_ids = fields.One2many('manteni.program.instruction', 'program_id', string='Instructions')


class ProgramInstruction(models.Model):
    # Rules being part of a program
    _name = 'manteni.program.instruction'

    name = fields.Char(string='Name', size=64, required=True, translate=True)
    description = fields.Text(string='Description', required=True, translate=True)
    program_id = fields.Many2one('manteni.program', string='Program')


class Workorder(models.Model):
    # Workorder to mantain/repair one of more machines
    _name = 'manteni.workorder'

    name = fields.Char('Title', size=64, required=True, translate=True)
    description = fields.Text('Description', translate=True)
    date_begin = fields.Date(string='Opening date', default=fields.Date.today)
    date_end = fields.Date(string='Closing date')
    employee_id = fields.Many2one('hr.employee', string='Employee', domain="[('department_id','=','Maintenance')]")
    employee_user_id = fields.Integer('hr.employee')
    employee_phone = fields.Char(string='Employee phone', compute='_compute_phone')
    machine_ids = fields.Many2many('manteni.machine', string='Machines')
    program_id = fields.Many2one('manteni.program', string='Program')
    state = fields.Selection(
        [('not_started', 'Not started'), ('opened', 'Opened'), ('closed', 'Closed'), ('cancelled', 'Cancelled')],
        string='State', default='opened')
    type = fields.Selection([('corrective', 'Corrective'), ('preventive', 'Preventive')], string='Type of maintenance',
                            default='corrective')
    closing_info = fields.Text('Closing information')

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'closed':
            self.date_end = date.today()

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        self.employee_user_id = self.employee_id.resource_id.user_id

    @api.depends('employee_id')
    def _compute_phone(self):
        self.employee_phone = self.employee_id.work_phone
