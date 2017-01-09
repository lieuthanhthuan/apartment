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


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_create_id = fields.Many2one(
        'res.users', 'User', track_visibility='onchange',
        default=lambda self: self.env.user, readonly=True)
    manager_team_id = fields.Many2one(
        'manager.team', 'Manager Team',
        default=lambda self: self.env.user.manager_team_id)
    related_user = fields.Many2one(
        'res.users', 'Login Account',
        track_visibility='onchange')
