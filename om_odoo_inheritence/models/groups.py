from odoo import api, fields, models


class ResGroups(models.Model):
    _inherit = "res.groups"

    def get_application_groups(self,domain):
        print('Domain' , domain)
        group_id = self.env.ref('project.group_project_recurring_tasks').id
        tax_group_id = self.env.ref('project.group_project_rating').id
        #return super(ResGroups,self).get_application_groups(domain + [('id' , '!=' , group_id)])
        return super(ResGroups,self).get_application_groups(domain + [('id' , 'not in' , (group_id,tax_group_id))])
