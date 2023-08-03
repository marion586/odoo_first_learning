# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'helpdesk.support'

    marker_color = fields.Char(
        string='Marker Color', default='red', required=True)
