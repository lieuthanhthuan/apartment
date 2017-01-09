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


class CustomerClaimLine(models.Model):
    _name = 'customer.claim.line'
    _description = """ Customer Claims Lines"""
    _inherit = ['mail.thread', 'ir.needaction_mixin']

    name = fields.Text(string="Content", required=True,
                       track_visibility='onchange')
    user_id = fields.Many2one(
        'res.users', 'User', track_visibility='onchange',
        default=lambda self: self.env.user, readonly=True)
    manager_team_id = fields.Many2one('manager.team', 'Manager Team',
                                      related='user_id.manager_team_id')
    company_id = company_id = fields.Many2one(
        'res.company', 'Company',
        default=lambda self: self.env['res.company']._company_default_get())
    active = fields.Boolean('Active', default=True)
    date = fields.Datetime('Date', readonly=True, default=fields.Datetime.now)
    customer_claim_id = fields.Many2one(
        'customer.claim', 'Customer Claim',
        ondelete='cascade')
    manager_task_id = fields.Many2one('manager.task', 'Manager Task')
    manager_team_task_id = fields.Many2one('manager.team.task',
                                           'Manager Team Task')
