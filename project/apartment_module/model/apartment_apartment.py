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


class ApartmentApartment(models.Model):
    _name = 'apartment.apartment'
    _description = """ Apartment Management"""
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    @api.depends('contract_ids', 'contract_ids.state',
                 'contract_ids.apartment_id')
    @api.multi
    def _compute_status(self):
        for record in self:
            if record.contract_ids:
                if any(contract.state == 'inprogress' for
                       contract in record.contract_ids):
                    record.status = 'inprogress'
            else:
                record.status = 'free'

    name = fields.Char(string="Apartment", required=True,
                       track_visibility='onchange')
    user_id = fields.Many2one(
        'res.users', 'User', track_visibility='onchange',
        default=lambda self: self.env.user, readonly=True)
    manager_team_id = fields.Many2one('manager.team', 'Manager Team',
                                      related='user_id.manager_team_id',
                                      readonly=True)
    description = fields.Text('Description', track_visibility='onchange')
    address = fields.Text('Address', track_visibility='onchange')
    area = fields.Integer('Area')
    contract_ids = fields.One2many('apartment.contract', 'apartment_id',
                                   'Contracts')
    status = fields.Selection([('free', 'Free'), ('inprogress', 'Inprogress')],
                              default='free')
