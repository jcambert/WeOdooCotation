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
    'depends': ['base','product','uom', 'mail'],

    # always loaded
    'data': [
        'security/quotation_security.xml',
        'security/ir.model.access.csv',
        'views/menu_views.xml',
        'views/stage_views.xml',
        'views/cotation_views.xml',
        'views/workcenter_views.xml',
        'views/bom_views.xml',
        'views/product_views.xml',
        'views/product_template_views.xml',
        
        # 'data/ir_cron.xml',

        # 'data/workcenters.xml',
        # 'data/stages.xml',
        # 'data/product_template.xml',
        

    ],
    'qweb': ['static/src/xml/*.xml'],
    # only loaded in demonstration mode
    # 'demo': ['data/mrp_plm_demo.xml'],
    
    #Module Installation
    'installable': True,
    'application': True,
    'auto_install': False
}
