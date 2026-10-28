# -*- coding: utf-8 -*-
#############################################################################
#
#    TechKhedut Inc.
#
#    Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
#    Author: TechKhedut(<https://www.techkhedut.com>)
#    Part of TechKhedut. See LICENSE file for full copyright and licensing details.
#
#############################################################################
{
    'name': 'Property Management Website | Property Rental Website | Theme Rental Management | Real Estate Website | Property Sale Website',
    'description': 'Property Sale & Rental Website',
    'summary': 'Property Sale & Rental Website',
    'category': 'Website',
    'version': '3.2.1',
    'author': 'TechKhedut Inc.',
    'company': 'TechKhedut Inc.',
    'maintainer': 'TechKhedut Inc.',
    'website': "https://techkhedut.com",
    'depends': [
        'web',
        'crm',
        'rental_management',
        'portal',
        'website',
        'website_blog',
        'website_mass_mailing'
    ],
    'data': [
        # data
        'data/data.xml',
        'data/property_book_mail_template.xml',
        # security
        'security/ir.model.access.csv',
        # backend
        'views/backend/property_theme_config.xml',
        'views/backend/property_details.xml',
        'views/backend/crm_lead_inherit.xml',
        # templates
        'views/assets.xml',
        'views/footer.xml',
        'views/header.xml',
        'views/home.xml',
        'views/listing.xml',
        'views/property_details.xml',
        'views/my_portal.xml',
        'views/map_view.xml',
        'views/website_layout_inherit.xml',
        # Snippets
        'views/snippets/static_snippets.xml',
        'views/snippets/popular_properties.xml',
        'views/snippets/latest_listing.xml',
        'views/snippets/home_banner.xml',
        'views/snippets/dynamic_snippets.xml',
        'views/snippets/snippet_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'tk_website_rental_management/static/src/css/backend/style.css',
        ],
        'web.assets_frontend': [
            'tk_website_rental_management/static/src/css/reset.css',
            'tk_website_rental_management/static/src/css/plugins.css',
            'tk_website_rental_management/static/src/css/style.css',
            'tk_website_rental_management/static/src/css/color.css',
            'tk_website_rental_management/static/src/css/skeleton.css',
            'tk_website_rental_management/static/src/css/extra.css',
            'tk_website_rental_management/static/src/js/plugin_loader.js',
            'tk_website_rental_management/static/src/js/map-listing.js',
            'tk_website_rental_management/static/src/js/scripts.js',
            'tk_website_rental_management/static/src/js/website_rental.js',
            'tk_website_rental_management/static/src/js/property_share.js',
            # Snippets
            'tk_website_rental_management/static/src/xml/popular_properties.xml',
            'tk_website_rental_management/static/src/xml/latest_listing.xml',
            'tk_website_rental_management/static/src/xml/home_banner.xml',
            'tk_website_rental_management/static/src/xml/counter.xml',
            'tk_website_rental_management/static/src/xml/testimonials.xml',
            'tk_website_rental_management/static/src/xml/partners.xml',
            'tk_website_rental_management/static/src/xml/popular_places.xml',
            'tk_website_rental_management/static/src/js/dynamic_snippets/common_utlities.js',
            'tk_website_rental_management/static/src/js/dynamic_snippets/dynamic_popular_places.js',
            'tk_website_rental_management/static/src/js/dynamic_snippets/dynamic_partners.js',
            'tk_website_rental_management/static/src/js/dynamic_snippets/dynamic_testimonials.js',
            'tk_website_rental_management/static/src/js/dynamic_snippets/dynamic_counter.js',
            'tk_website_rental_management/static/src/js/dynamic_snippets/dynamic_home_banner.js',
            'tk_website_rental_management/static/src/js/dynamic_snippets/dynamic_popular_properties.js',
            'tk_website_rental_management/static/src/js/dynamic_snippets/dynamic_latest_listing.js',
        ],
        'web._assets_primary_variables': [
        ],
        'website.website_builder_assets': [
            'tk_website_rental_management/static/src/xml/website_builders/header_builder.xml',
            'tk_website_rental_management/static/src/xml/website_builders/footer_builder.xml',
        ],
    },
    'images': [
        'static/description/property-rental.gif',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 274,
    'currency': 'USD',
}
