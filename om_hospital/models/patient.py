from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import  relativedelta

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = "mail.thread", 'mail.activity.mixin'
    _description = "Hospital Patient"
    _rec_name = 'name'
    # need to have chatter for a tracking
    name = fields.Char(string='Name', tracking=True, translate=True)
    date_of_birth = fields.Date(string="Date of Birth", default=fields.Date.context_today)
    # computed field will not going going to be stored in the database , that wy we iterate it of each day of birth change
    #inverse to make it editable
    age = fields.Integer(string="Age", compute='_compute_age', inverse='_inverse_compute_age', search="_search_age", tracking=True)
    ref = fields.Char(string="Reference", translate=True, default="odoo Mates", help="Reference of the patient record")
    email = fields.Char(string="Email", translate=True,  help="Email of the patient record")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender", tracking=True,
                              default='female', translate=True)
    active = fields.Boolean(string="Active", default=True)
    appointment_id = fields.Many2one(comodel_name='hospital.appointment')
    image = fields.Image(string="Image")
    tag_ids = fields.Many2many('patient.tag', string="Tags")
    #if you store a field stored without depends it will not changed
    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count", store=True)
    #will get only the apointment related to the patient_id ,  whenever we create an appointments this computed value will be triggered
    appointment_ids = fields.One2many('hospital.appointment' , 'patient_id' ,string="Appointments")

    parent = fields.Char(string=" Parent")
    marital_status = fields.Selection([('married', 'Married'),
                                       ('single' , 'Single')] , string="Marital Status" , tracking=True)
    partner_name = fields.Char(string = "Partner name")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            print("recod id", rec.id , rec.appointment_ids )
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            print('rec', rec, rec.date_of_birth)
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError("The entered date of birth is no acceptable")

    # @api.ondelete(at_uninstall=False)
    # def check_appointments(self):
    #     for rec in self:
    #         if rec.appointment_ids:
    #             raise ValidationError("You cannot delte a patient with Appointments")
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
    @api.depends("age")
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)

    def _search_age(self, operator, value):
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        print('............date of birth',value , date.today() , date_of_birth)
        start_of_year = date_of_birth.replace(day=1 , month=1)
        end_of_year = date_of_birth.replace(day=31 , month=12)

        print("start ...." , start_of_year)
        print("end ......." ,end_of_year)
        return [ ('date_of_birth' , '>=' , start_of_year) , ('date_of_birth' , '<=' , end_of_year) ]
    def action_done(self):
        print("done by marion")

    def name_get(self):
        # print("name get",self.env['ir.sequence'].next_by_code('hospital.patient'))
        # print(self.env.user.name)
        # print(self.env.is_superuser)
        # print(self.env.company)
        # print(self.env.company.name)
        # print(self.env.companies)
        # print(self.env.lang)
        # print(self.env.cr.execute("select * from hospital_patient"))
        # print(self.env.context)
        # print(self.env.context.get('uid'))
        # print(self.env['hospital.patient'])
        # print(self.env['hospital.patient'].browse(1))
        # print(print(self.env['hospital.patient'].browse(1).ref))
        # print(print(self.env['hospital.patient'].browse(1).action_done()))
        print(self.env.ref("om_hospital.view_patient_tag_tree").id)
        # print("env" , self.env)
        # patient_list = []
        # for record in self:
        #     name = record.ref + ' ' + record.name
        #     patient_list.append((record.id, name))
        # return patient_list
        return [(record.id, "%s  %s" % (record.ref, record.name)) for record in self]

    def action_test(self):
        print("clicked")
        return
