# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2009-2017
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

from odoo import http
from odoo.http import request
from datetime import datetime


class Maintenance(http.Controller):

    @http.route('/maintenance/', website=True)
    def index(self, **kw):
        """
            TO DO: load all information customer claims
        """
        customer_claim_obj = http.request.env['customer.claim']
        claims = customer_claim_obj.search([], limit=80, order="id desc")
        return request.render('apartment_module.maintenance', {
            'claims': claims,
            'error': False
        })

    @http.route('/claim/', type='http', website=True)
    def claim_receipt(self, **kw):
        """
            TO DO: Create new Claim from a Customer
        """
        uid = http.request.uid
        res_user_obj = http.request.env['res.users']
        user = res_user_obj.browse(uid)
        partner_id = user.partner_id.id
        manager_team_id = user.partner_id.manager_team_id.id
        content = kw['content']
        claims = []
        error = False
        customer_claim_obj = http.request.env['customer.claim']
        last_claim = customer_claim_obj.search([], limit=1, order="id desc")
        last_sent = 0
        if last_claim:
            last_time = datetime.strptime(
                last_claim.date, '%Y-%m-%d %H:%M:%S')
            now = datetime.now()
            delta = now - last_time
            last_sent = delta.total_seconds()
        if not last_claim or last_sent > (2*3600):
            claims = customer_claim_obj.create({
                'name': content,
                'partner_id': partner_id,
                'manager_team_id': manager_team_id, })
        else:
            error = True
        return request.render('apartment_module.maintenance', {
            'claims': claims,
            'error': error
        })

    @http.route('/claim/<model("customer.claim"):claim>/', website=True)
    def claim_view_detail(self, claim, **kwargs):
        """
            TO DO: Load Claim Detail Information
        """
        return request.render('apartment_module.claim_detail', {
            'claim': claim
        })
