from odoo import api, fields, models, _


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string='Name', required=True)
    #copy=False means , the value will not copied in duplicate functionnal)
    active = fields.Boolean(string="Active", default=True , copy=False)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence" , default=1)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        print("default", default)
        if default is None:
            default = {}
        if not default.get('name'):
            print("not name")
            default['name'] = _("%s (copy)", self.name)
            # default['name'] = self.name + "(copy)"
            print("default name", default)
            default['sequence'] = 1
        return super(PatientTag, self).copy(default)

    _sql_constraints = [
        ('unique_tag_name',  'unique (name,active)', 'Name must be unique.'),
        ('check_sequence', 'check(sequence > 0)', 'Sequence must be non zero positive number.')
    ]




