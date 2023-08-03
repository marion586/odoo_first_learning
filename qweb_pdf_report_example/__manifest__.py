# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name':'Qweb Report Demo',
    'version': '1.1',
    'author': 'Weblearns',
    'summary': "Qweb Report Demo",
    'sequence': 1,
    'description':"Qweb Report Demo",
    'category':'School',
    'website':'https://freeweblearns.blogspot.com',
    'depends':['school', 'school_student'],
    'data':[
        "report/student_report_template.xml",
        "report/inherit-qweb_template.xml"
    ]
}
