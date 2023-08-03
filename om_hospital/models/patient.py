
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = "mail.thread", 'mail.activity.mixin'
    _description = "Hospital Patient"
    _rec_name = 'name'
    # need to have chatter for a tracking
    name = fields.Char(string='Name', tracking=True, translate=True)
    date_of_birth = fields.Date(string="Date of Birth", default=fields.Date.context_today)
    # computed field will not going going to be stored in the database , that wy we iterate it of each day of birth change
    age = fields.Integer(string="Age", compute='_compute_age', tracking=True)
    ref = fields.Char(string="Reference", translate=True, default="odoo Mates", help="Reference of the patient record")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True,
                              default='female', translate=True)
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment')
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            print('rec', rec , rec.date_of_birth)
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError("The entered date of birth is no acceptable")

    @api.model
    def create(self, vals):
        print("self crreate", self)
        print("marion", vals)
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        print(type(vals))
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        print("write method getting called", vals)
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        print("today", today)
        print("typee", type(self))
        # we use loop to avoid singleton error in odoo
        for rec in self:
            # self.age = today.year - self.date_of_birth.year - ((today.month,today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            if rec.date_of_birth:
                rec.age = today.year - rec.date_of_birth.year
            else:
                rec.age = 1


    def action_done(self):
        print("done by marion")
    def name_get(self):
        #print("name get",self.env['ir.sequence'].next_by_code('hospital.patient'))
        #print(self.env.user.name)
        #print(self.env.is_superuser)
        #print(self.env.company)
        #print(self.env.company.name)
        #print(self.env.companies)
        #print(self.env.lang)
        #print(self.env.cr.execute("select * from hospital_patient"))
        #print(self.env.context)
        #print(self.env.context.get('uid'))
        #print(self.env['hospital.patient'])
        #print(self.env['hospital.patient'].browse(1))
        #print(print(self.env['hospital.patient'].browse(1).ref))
        #print(print(self.env['hospital.patient'].browse(1).action_done()))
        print(self.env.ref("om_hospital.view_patient_tag_tree").id)
        #print("env" , self.env)
        # patient_list = []
        # for record in self:
        #     name = record.ref + ' ' + record.name
        #     patient_list.append((record.id, name))
        # return patient_list
        return [(record.id, "%s  %s" % (record.ref, record.name)) for record in self]
