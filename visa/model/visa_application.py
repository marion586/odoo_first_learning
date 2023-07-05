from odoo import models, fields
class VisaApplication(models.Model):
    _name = ("visa.application")
    nam = fields.Char("Name")