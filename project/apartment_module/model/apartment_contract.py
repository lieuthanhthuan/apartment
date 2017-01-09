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


class ApartmentContract(models.Model):
    _name = 'apartment.contract'
    _description = """ Apartment Contract"""
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string="Contract Name", required=True,
                       readonly=True,
                       track_visibility='onchange',
                       states={'draft': [('readonly', False)]})
    user_id = fields.Many2one(
        'res.users', 'User',
        track_visibility='onchange',
        default=lambda self: self.env.user,
        readonly=True)
    manager_team_id = fields.Many2one(
        'manager.team', 'Manager Team',
        default=lambda self: self.env.user.manager_team_id)
    partner_id = fields.Many2one(
        'res.partner', 'Customer',
        domain=[('company_type', '=', 'company')],
        readonly=True, required=True,
        track_visibility='onchange',
        states={'draft': [('readonly', False)]})
    date_from = fields.Date(
        'Date From', readonly=True, required=True,
        track_visibility='onchange',
        states={'draft': [('readonly', False)]})
    date_to = fields.Date(
        'Date To', readonly=True, track_visibility='onchange',
        states={'draft': [('readonly', False)]})
    description = fields.Text(
        'Description', readonly=True, track_visibility='onchange',
        states={'draft': [('readonly', False)]})
    apartment_id = fields.Many2one(
        'apartment.apartment', string="Apartment",
        readonly=True, required=True, track_visibility='onchange',
        states={'draft': [('readonly', False)]},
        domain=[('status', '=', 'free')])
    unit_price = fields.Integer(
        'Unit price', readonly=True, required=True,
        track_visibility='onchange',
        states={'draft': [('readonly', False)]})
    uom_unit = fields.Selection(
        [('month', 'Month'), ('year', 'Year')],
        string="Uom", readonly=True, required=True,
        track_visibility='onchange',
        states={'draft': [('readonly', False)]},
        default='month')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inprogress', 'Inprogress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, required=True,
        track_visibility='onchange',
        states={'draft': [('readonly', False)]},
        default="draft")

    @api.multi
    def action_confirm(self):
        self.write({'state': 'inprogress'})
        for record in self:
            if record.apartment_id:
                record.apartment_id.write({'status': 'inprogress'})

    @api.multi
    def action_done(self):
        self.write({'state': 'done'})
        for record in self:
            if record.apartment_id:
                record.apartment_id.write({'status': 'free'})

    @api.multi
    def action_cancel(self):
        self.write({'state': 'cancel'})
        for record in self:
            if record.apartment_id:
                record.apartment_id.write({'status': 'free'})

    @api.multi
    def action_set_draft(self):
        self.write({'state': 'draft'})
        for record in self:
            if record.apartment_id:
                record.apartment_id.write({'status': 'free'})
