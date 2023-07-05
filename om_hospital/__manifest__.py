# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'author': 'marion',
    'sequence':-100,
    'summary': 'Hospital Management system',
    'description': """ Hospital Management system""",
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/patient_view.xml'

    ],
    'demo': [],
    'installable': True,
    'application' : True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {}
}
