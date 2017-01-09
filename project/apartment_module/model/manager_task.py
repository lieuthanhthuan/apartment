# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2016
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import api, fields, models


class ManagerTask(models.Model):
    _name = 'manager.task'
    _description = """ Customer Claims"""
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.multi
    def _compute_new_status(self):
        for record in self:
            if not record.line_ids:
                record.new_status = ""
            else:
                last_line = self.env['customer.claim.line'].search([
                    ('manager_task_id', '=', record.id)], order="id desc",
                                                                   limit=1)
                if not last_line:
                    record.new_status = ""
                else:
                    record.new_status = last_line.name

    apartment_id = fields.Many2one('apartment.apartment', 'Apartment')
    name = fields.Text(string="Content", required=True,
                       track_visibility='onchange')
    user_id = fields.Many2one(
        'res.users', 'User', track_visibility='onchange',
        default=lambda self: self.env.user, readonly=True)
    manager_team_id = fields.Many2one(
        'manager.team', 'Manager Team',
        default=lambda self: self.env.user.manager_id)
    company_id = company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get())
    active = fields.Boolean('Active', default=True)
    date = fields.Datetime('Date', readonly=True, default=fields.Datetime.now)
    new_status = fields.Text('New Status', compute=_compute_new_status)
    state = fields.Selection([
        ('receipted', 'Receipted'),
        ('inprogress', 'Inprogress'),
        ('done', 'done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, required=True,
        track_visibility='onchange',
        states={'receipted': [('readonly', False)]},
        default="receipted")
    line_ids = fields.One2many('customer.claim.line', 'manager_task_id',
                               'Lines')

    @api.multi
    def action_confirm(self):
        self.write({'state': 'inprogress'})

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.multi
    def action_set_draft(self):
        self.write({'state': 'receipted'})
