from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = "mail.thread", 'mail.activity.mixin'
    _description = "Hospital Appointment"
    _rec_name = 'ref'
    # convention for a many to one field
    patient_id = fields.Many2one(comodel_name='hospital.patient', string="Patient", required=True , ondelete="restrict")
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_time = fields.Date(string='Booking Time', default=fields.Date.context_today)
    # readonly false make the parent patient reflected by a change
    gender = fields.Selection(translate=True, related='patient_id.gender', readonly=False)
    ref = fields.Char(string="Reference")
    prescription = fields.Html(string='Prescription')
    appointment_count = fields.Integer(string="Appointment_count")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
    ], string="Priority")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string="Status", default='draft', required=True)
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string='Pharmacy Lines')
    hide_sales_price = fields.Boolean(string="Hide Sales PRice")
    operation = fields.Many2one('hospital.operation', string="Operation")
    company_id = fields.Many2one('res.company' , required=False )
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment, self).create(vals)

    def unlink(self):
        print("Test .............................SS")
        if self.state == 'done':
            raise ValidationError(_("Error you cannot delete record in done state"))
        return super(HospitalAppointment ,  self).unlink()
    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("Button Clicked  !!!!!!!!!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Clicked successful',
                'type': "rainbow_amin"
            }
        }

    def action_send_email(self):
        template = self.env.ref('om_hospital.appointment_mail_template')
        print(template)
        for rec in self:
            if rec.patient_id.email:
                email_values = {'subject': 'Test OM'}
                # force_send parameter to send it immediatly
                #template.send_mail(rec.id , force_send=True, email_values=email_values )
                template.send_mail(rec.id , force_send=True )
    def action_in_consultation(self):
        for rec in self:
            if rec.state == "draft":
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        print("action 0" , action)
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    class AppointmentPharmacyLines(models.Model):
        _name = "appointment.pharmacy.lines"
        _description = "Appointment Pharmacy lines"

        product_id = fields.Many2one("product.product", required=True)
        price_unit = fields.Float(related="product_id.list_price")
        qty = fields.Integer(string="Quantity", default=1)
        appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
