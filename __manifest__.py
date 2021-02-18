# -*- coding: utf-8 -*-
{
    'name': "We Addon Cotation",

    'summary': """
        Extenssion Addon that manage Cotation""",

    'description': """
        Addon ERP to manage cotation
    """,

    'author': "We",
    'website': "http://jc.ambert.free.fr",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity',
    'version': '1.0',
    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/plm_security.xml',
        'security/ir.model.access.csv',
        'views/stage_views.xml',
        'views/cotation_views.xml',
        'views/workcenter_views.xml',
        'views/menu_views.xml'
        # 'data/ir_cron.xml',
        # 'data/ir_module_category.xml',
        # 'data/mrp_plm_data.xml',
        # 'views/user.xml',

    ],
    'qweb': ['static/src/xml/*.xml'],
    # only loaded in demonstration mode
    # 'demo': ['data/mrp_plm_demo.xml'],
    
    #Module Installation
    'installable': True,
    'application': True,
    'auto_install': False
}
