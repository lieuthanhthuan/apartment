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
from odoo import fields, models


class ManagerTeam(models.Model):
    _name = 'manager.team'
    _description = """ Manager Team"""
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Char(string="Name", required=True,
                       track_visibility='onchange')
    type = fields.Selection([('manager', 'Manager'),
                             ('super_manager', 'Super Manager')], 'Type',
                            default='manager')
    user_id = fields.Many2one(
        'res.users', 'User', track_visibility='onchange',
        default=lambda self: self.env.user, readonly=True)
    company_id = company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get())
    manager_id = fields.Many2one('res.users', 'Manager')
    member_ids = fields.One2many('res.users', 'manager_team_id', 'Members')
    member2_ids = fields.One2many('res.users', 'manager_id', 'Members')
