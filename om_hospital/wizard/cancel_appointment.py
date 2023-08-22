
from    odoo.exceptions import ValidationError
from odoo import api, fields, models
from datetime import date
from dateutil import relativedelta
import datetime


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        print("Default get executed", res)
        res['date_cancel'] = datetime.date.today()
        print('...... context', self.env.context)
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    # we can do it from the view
    # appointment_id = fields.Many2one('hospital.appointment', string="Appointment" ,  domain=['|', ('state', '=', 'draft'),
    #                                                                                          ('priority', 'in', ('0', '1' , False) )])

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", domain=['|', ('state', '=', ''
                                                                                                               ''
                                                                                                               ''),
                                    ('priority', 'in', ('0', '1' , False) )])
    reason = fields.Text(string="Reason", default="Test Reason")
    date_cancel = fields.Date(string="Cancellation Date")

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_days')
        print('cancel_day',cancel_day)

        today = date.today()
        allowed_date = self.appointment_id.booking_time - relativedelta.relativedelta(days=int(cancel_day))
        print("allowed-date" , allowed_date , date.today() , allowed_date < date.today() )
        if allowed_date < date.today():
            raise ValidationError("Invalid appointment cancellation request. Please provide a valid reason.")
        self.appointment_id.state = 'cancel'
        print('appointment_state', self.appointment_id.state)
        # return
