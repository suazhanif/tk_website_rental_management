# -*- coding: utf-8 -*-
# Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from urllib.parse import unquote
from werkzeug.urls import url_join

from odoo import http
from odoo.http import request, content_disposition
from odoo.addons.website.controllers.main import Website
from odoo.tools.image import image_data_uri
from odoo.addons.portal.controllers.portal import CustomerPortal


def category_wise_domain_filter(list_type):
    """Category wise domain filter for property"""
    list_domain = []
    if list_type and list_type == 'lands':
        list_domain.append(('type', '=', 'land'))
    if list_type and list_type == 'residential':
        list_domain.append(('type', '=', 'residential'))
    if list_type and list_type == 'commercial':
        list_domain.append(('type', '=', 'commercial'))
    if list_type and list_type == 'industrial':
        list_domain.append(('type', '=', 'industrial'))
    return list_domain


# DYNAMIC CATEGORY FILTER
def dynamic_category_filter(vals):
    """Dynamic Amenities"""
    dc_catg = None
    if vals.get('dc'):
        dc_catg = vals.get('dc')
    return dc_catg


def convert_str_to_dict(input_string):
    """Converting string into dictionary"""
    # Split the string into key-value pairs
    pairs = input_string.split("&")

    # Create a dictionary to store the key-value pairs
    result_dict = {}

    # Iterate over each pair and add it to the dictionary
    for pair in pairs:
        # Split the pair into key and value
        key, value = pair.split("=")

        # Add key-value pair to the dictionary
        result_dict[key] = value

    # Display the resulting dictionary
    return result_dict


def get_amenities_filters(param):
    """Amenities wise domain filter of property"""
    url_args, list_domain = {}, []
    # Amenities filter - gym
    args = None
    if param.get('facility'):
        args = param.get('facility').split(',')
    if args and 'gym' in args:
        url_args['facility'] = 'gym'
        list_domain.append(('web_gym', '=', True))
    # wifi
    if args and 'wifi' in args:
        url_args['facility'] = 'wifi'
        list_domain.append(('web_wifi', '=', True))
    # parking
    if args and 'parking' in args:
        url_args['facility'] = 'parking'
        list_domain.append(('web_parking', '=', True))
    # pool
    if args and 'pool' in args:
        url_args['facility'] = 'pool'
        list_domain.append(('web_pool', '=', True))
    # security
    if args and 'security' in args:
        url_args['facility'] = 'security'
        list_domain.append(('web_security', '=', True))
    # laundry
    if args and 'laundry' in args:
        url_args['facility'] = 'laundry'
        list_domain.append(('web_laundry', '=', True))
    # Equipped Kitchen
    if args and 'kitchen' in args:
        url_args['facility'] = 'kitchen'
        list_domain.append(('web_equip_kitchen', '=', True))
    # AC
    if args and 'air' in args:
        url_args['facility'] = 'air'
        list_domain.append(('web_air_condition', '=', True))
    # semi furnish
    if args and 'sfur' in args:
        url_args['facility'] = 'sfur'
        list_domain.append(('web_semi_furnish', '=', True))
    # full furnish
    if args and 'fuf' in args:
        url_args['facility'] = 'fuf'
        list_domain.append(('web_full_furnish', '=', True))
    # Alarm
    if args and 'alarm' in args:
        url_args['facility'] = 'alarm'
        list_domain.append(('web_alarm', '=', True))
    # window cover
    if args and 'window' in args:
        url_args['facility'] = 'window'
        list_domain.append(('web_window_cover', '=', True))

    return url_args, list_domain


def property_filters(param):
    """Get all filters together"""
    url_args, list_domain = {}, []
    # status filters
    status = param.get('st')
    if status and status in ['sale', 'rent']:
        url_args['st'] = status
        if status == 'sale':
            list_domain.append(('sale_lease', '=', 'for_sale'))
        else:
            list_domain.append(('sale_lease', '=', 'for_tenancy'))

    # price range filters - starting price
    price_start = param.get('price-start')
    if price_start and price_start.isdigit():
        if status == 'sale':
            url_args['price-start'] = price_start
            list_domain.append(('price', '>=', int(price_start)))
        else:
            list_domain.append(('price', '>=', int(price_start)))
    # price range filters - ending price
    price_end = param.get('price-end')
    if price_end and price_end.isdigit():
        url_args['price-end'] = price_end
        if status == 'sale':
            list_domain.append(('price', '<=', int(price_end)))
        else:
            list_domain.append(('price', '<=', int(price_end)))

    # city filters
    city = param.get('cn')
    if city and 'All' not in city:
        decoded_string = unquote(city)
        cities = request.env['property.res.city'].sudo().search(
            [('name', '=', str(decoded_string))]).ids
        if cities:
            url_args['cn'] = city
            list_domain.append(('city_id', 'in', cities))

    # Dynamic Category Filters
    dc_categ = param.get('dc')
    if dc_categ and dc_categ.isdigit():
        url_args['dc'] = dc_categ
        list_domain.append(('property_subtype_id', '=', int(dc_categ)))

    # category filters
    categ = param.get('categ')
    if categ and len(categ) > 0 and 'All' not in categ:
        url_args['categ'] = categ
        list_domain = list_domain + category_wise_domain_filter(categ)

        # area filters
        area_start = param.get('area-start')
        area_end = param.get('area-end')
        if area_start and area_start.isdigit() and area_end and area_end.isdigit():
            url_args['area-start'] = area_start
            url_args['area-end'] = area_end
            if categ in ('residential', 'commercial', 'industrials', 'lands'):
                list_domain.append(('total_area', '>=', int(area_start)))
                list_domain.append(('total_area', '<=', int(area_end)))

    # max price filters
    max_price = param.get('max_prc')
    if max_price and max_price.isdigit():
        url_args['max_prc'] = max_price
        if status and status in ['sale', 'rent']:
            list_domain.append(('price', '<=', int(max_price)))
            if status == 'sale':
                list_domain.append(('sale_lease', '=', 'for_sale'))
            else:
                list_domain.append(('sale_lease', '=', 'for_tenancy'))
        else:
            list_domain.append(('price', '<=', int(max_price)))

    # search term filters
    search_term = param.get('search_term')
    if search_term:
        url_args['search_term'] = search_term
        list_domain.append(('name', 'ilike', search_term))

    # bedrooms filters
    bedrooms = param.get('rooms')
    if bedrooms and bedrooms.isdigit():
        url_args['rooms'] = bedrooms
        if int(bedrooms) >= 10:
            list_domain.append(('bed', '>=', bedrooms))
        else:
            list_domain.append(('bed', '=', bedrooms))

    # bathrooms filters
    bathrooms = param.get('bathrooms')
    if bathrooms and bathrooms.isdigit():
        url_args['bathrooms'] = bathrooms
        if int(bathrooms) >= 10:
            list_domain.append(('bathroom', '>=', bathrooms))
        else:
            list_domain.append(('bathroom', '=', bathrooms))

    # floor filters
    floor = param.get('floor')
    if floor and floor.isdigit():
        url_args['floor'] = floor
        if int(floor) >= 10:
            list_domain.append(('total_floor', '>=', floor))
        else:
            list_domain.append(('total_floor', '=', floor))

    return url_args, list_domain


def property_sorting_orders(param):
    """Sorting order of property records"""
    url_args, default_order = {}, ""
    # Property type sort filter
    property_type = param.get('property_type')
    if property_type and property_type in ['sale', 'rent']:
        url_args['property_type'] = property_type
        if property_type == 'sale':
            default_order = 'sale_lease ASC'
        else:
            default_order = 'sale_lease DESC'
    else:
        default_order = 'id DESC'
    # Price order sort filter
    price_order = param.get('price_order')
    if price_order and property_type and property_type in ('sale', 'rent') and price_order in (
            'lh', 'hl'):
        url_args['price_order'] = price_order
        if price_order == 'lh':
            default_order += ',' + 'price ASC' if property_type == 'rent' else ',' + 'price ASC'
        else:
            default_order += ',' + 'price DESC' if property_type == 'rent' else ',' + 'price DESC'
    return url_args, default_order


def get_all_filters(param):
    """Combine filters & Sorting orders"""
    # query param args
    url_args, list_domain = {}, []

    # sorting orders
    sort_args, default_order = property_sorting_orders(param)
    url_args.update(sort_args)

    # property filters
    filter_args, prop_list_domain = property_filters(param)
    url_args.update(filter_args)
    list_domain = list_domain + prop_list_domain

    # amenities filters
    ame_args, ame_filters = get_amenities_filters(param)
    url_args.update(ame_args)
    list_domain = list_domain + ame_filters

    return url_args, list_domain, default_order


def dynamic_amenities_list(vals):
    """Dynamic Amenities"""
    da_list = None
    if vals.get('da'):
        da_str = unquote(vals.get('da'))[:-1]
        if len(da_str) > 0:
            da_str_lst = da_str.split(',')
            da_list = [int(i) for i in da_str_lst]
    return da_list


class PropertyController(Website):
    """Property website"""

    @http.route('/colors/style.css', type='http', auth="public", website=True)
    def dynamic_theme_colors(self):
        """Adding Theme Dynamic Colors"""
        home_config = request.env.ref('tk_website_rental_management.property_theme_config_rec')
        css_content = f"""
            :root {{
                --dynamic_primary_background: {home_config.primary_background};
                --dynamic_secondary_background: {home_config.secondary_background};
                --dynamic_btn_primary_background: {home_config.btn_primary};
                --dynamic_btn_secondary_background: {home_config.emphasis_background};
                --dynamic_btn_primary_text: {home_config.btn_primary_text};
                --dynamic_btn_secondary_text: {home_config.btn_secondary_text};
                --dynamic_text_color: {home_config.text_color};
                --dynamic_link_color: {home_config.link_color};
                --dynamic_header_color: {home_config.header_color};
                --dynamic_header_text: {home_config.header_text};
            }}
        """
        return http.Response(
            css_content,
            headers=[('Content-Type', 'text/css')],
        )

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        """Home page of property management"""
        # theme config rec
        home_config = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        # property details env
        property_param = request.env['property.details'].sudo()
        # latest listing
        latest_listing = property_param.search(
            [('stage', '=', 'available'),
             ('company_id', 'in', [request.website.company_id.id, False]),
             ('is_latest_listing', '=', True)],
            order='id desc',
            limit=home_config.no_latest_list)
        # popular listing
        popular_listing = property_param.search(
            [('stage', '=', 'available'), ('is_popular_list', '=', True),
             ('company_id', 'in', [request.website.company_id.id, False]), ],
            order='id desc', limit=home_config.no_popular_list)

        # Hero Categories
        hero_categories = request.env['property.sub.type'].sudo().search(
            [('display_on_home', '=', True)], limit=8,
            order='sequence asc')

        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids
        ctx = {
            'latest_listing': latest_listing,
            'popular_listing': popular_listing,
            'hero_categories': hero_categories,
            'home_config': home_config,
            'book_properties': book_prop,
            'book_property_count': len(book_prop),
            'cities': property_param.get_all_cities(),
        }
        return request.render("tk_website_rental_management.homes", ctx)

    @http.route('/property/advance-filters', type='jsonrpc', auth="public")
    def property_advance_filters(self, **kw):
        """Property advance filters"""
        category_domain, category_name, category_id = [], [], []
        if kw.get('category_value'):
            category_domain = category_domain + [('type', '=', kw.get('category_value'))]
        categories = request.env['property.sub.type'].sudo().search(
            category_domain, order='sequence asc')
        if categories:
            category_name = [data.name for data in categories]
            category_id = [data.id for data in categories]
        ctx = {
            'categories_name': category_name,
            'categories_id': category_id
        }
        return ctx

    def get_dynamic_amenity_filter(self, da_list):
        """Get dynamic amenity filters"""
        # Get leads values
        query = """
            SELECT
            property_id
            FROM
            property_website_amenity_rel
            WHERE amenity_id IN %s
        """
        request._cr.execute(query, [tuple(da_list)])
        properties = [i[0] for i in request._cr.fetchall()]
        return [('id', 'in', properties)]

    @http.route(['/properties-list',
                 '/properties-list/page/<int:page>',
                 '/properties-list/<string:list_type>',
                 '/properties-list/<string:list_type>/page/<int:page>'], type='http', auth="public",
                website=True)
    def properties_list(self, list_type=None, page=0, **kw):
        """List of properties"""
        property_param = request.env['property.details'].sudo()
        # theme config rec
        config_rec = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        # domain list
        list_domain = [('stage', '=', 'available')]
        # category wise filter domain
        if list_type:
            list_domain = list_domain + category_wise_domain_filter(list_type)

        # Property filters
        url_args, prop_filters, default_order = get_all_filters(request.params)
        list_domain = list_domain + prop_filters
        # multi company
        #list_domain = list_domain + [('company_id', 'in', [request.website.company_id.id, False])]
        # Dynamic Amenities
        da_list = dynamic_amenities_list(request.params)
        if da_list:
            properties = self.get_dynamic_amenity_filter(da_list)
            list_domain = list_domain + properties

        # property list limit
        property_per_page = config_rec.list_property_per_page
        list_count = property_param.search_count(list_domain)

        # pagination
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=list_count,
            page=page,
            step=property_per_page,
            url_args=url_args,
        )
        # listings
        listing = property_param.search(list_domain, order=default_order, offset=pager['offset'],
                                        limit=property_per_page)

        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids

        dynamic_amenity_ids = request.env['property.amenities'].sudo().search(
            [('is_on_website', '=', True)])

        # Categories
        category_domain = []
        if kw.get('categ'):
            category_domain = category_domain + [('type', '=', kw.get('categ'))]
        categories = request.env['property.sub.type'].sudo().search(
            category_domain, order='sequence asc')
        ctx = {
            'listing': listing,
            'list_type': list_type,
            'pager': pager,
            'cities': property_param.get_all_cities(),
            'theme_config': config_rec,
            'book_properties': book_prop,
            'book_property_count': len(book_prop),
            'da_ids': dynamic_amenity_ids,
            'da_list': da_list,
            'categories': categories,
        }
        return request.render("tk_website_rental_management.property_list", ctx)

    @http.route(['/properties/city/<model("property.res.city"):city>/',
                 '/properties/city/<model("property.res.city"):city>/page/<int:page>'], type='http',
                auth="public",
                website=True)
    def properties_list_by_city(self, city, page=0):
        """City wise property list"""
        # theme config rec
        config_rec = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        property_param = request.env['property.details'].sudo()
        # domain list city wise
        list_domain = [('stage', '=', 'available')]

        # Property filters
        url_args, prop_filters, default_order = get_all_filters(request.params)

        # If in URL search parameter 'cn' is not present then add default url city
        # otherwise 'city_id' domain come from 'get_all_filters' function
        if request.params and 'cn' not in request.params:
            list_domain = list_domain + [('city_id', '=', city.id)]

        list_domain = list_domain + prop_filters
        # multi company
        list_domain = list_domain + [('company_id', 'in', [request.website.company_id.id, False])]
        # limit per page
        property_per_page = config_rec.list_property_per_page
        list_count = property_param.search_count(list_domain)

        # Dynamic Amenities
        da_list = dynamic_amenities_list(request.params)
        if da_list:
            properties = self.get_dynamic_amenity_filter(da_list)
            list_domain = list_domain + properties

        # Pagination
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=list_count,
            page=page,
            step=property_per_page,
            url_args=url_args,
        )
        listing = property_param.search(list_domain, order=default_order, offset=pager['offset'],
                                        limit=property_per_page)

        # Change city according to filter ->
        # For Getting In Filter Section and Header Section Right Name
        if len(listing.mapped('city_id').ids) == 1:
            city = listing.mapped('city_id')
        else:
            city = None

        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids
        dynamic_amenity_ids = request.env['property.amenities'].sudo().search(
            [('is_on_website', '=', True)])
        ctx = {
            'listing': listing,
            'pager': pager,
            'city': city,
            'cities': property_param.get_all_cities(),
            'theme_config': config_rec,
            'book_properties': book_prop,
            'book_property_count': len(book_prop),
            'da_ids': dynamic_amenity_ids,
            'da_list': da_list,
        }
        return request.render("tk_website_rental_management.property_list", ctx)

    @http.route('/property-details/<string:prop_slug>', type='http', auth="public",
                website=True)
    def property_details(self, prop_slug, **kw):
        """Get single property details"""
        try:
            prop_id = int(prop_slug.split('-')[-1])
        except (ValueError, IndexError):
            return request.redirect('/')
        prop = request.env['property.details'].sudo().browse(prop_id)
        if not prop.exists() or prop.stage != 'available':
            return request.redirect('/')
        error_msg, enquiry_made = False, False
        if request.httprequest.method == 'POST':
            # Enquiry form validation
            if not kw.get('name'):
                error_msg = 'Name is required'
            if not kw.get('email'):
                error_msg = 'Email is required'
            if not kw.get('phone'):
                error_msg = 'Mobile is required'
            # Create lead
            logged_user = request.env.user.id != request.env.ref('base.public_user').id
            if not error_msg:
                lead_data = {
                    'name': prop.name + " " + kw.get('name', ''),
                    'contact_name': kw.get('name', ''),
                    'email_from': kw.get('email', ''),
                    'phone': kw.get('phone', ''),
                    'description': kw.get('additional_details', ''),
                    'partner_id': request.env.user.partner_id.id if logged_user else False,
                    'property_id': prop.id,
                    'type': 'lead',
                    'user_id': request.env.user.id if logged_user else False,
                    'is_public_lead': False if logged_user else True,
                    'company_id': prop.company_id.id,
                }
                lead_id = request.env['crm.lead'].sudo().create(lead_data)
                if lead_id:
                    # send mail to landlord if boolean true from theme_config
                    # and landlord present in property
                    config_rec = request.env.ref(
                        'tk_website_rental_management.property_theme_config_rec')
                    template_id = (
                        'tk_website_rental_management.landlord_enquiry_notification_mail_template')
                    if config_rec.is_mail_send_to_landlord and prop.landlord_id:
                        # Mail Template
                        mail_template = request.env.ref(template_id)
                        if mail_template:
                            mail_template.sudo().send_mail(lead_id.id, force_send=True)
                    return request.redirect(
                        f"/property-details/{request.env['ir.http']._slug(prop)}")
        # Find booked properties
        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids
        # Check already enquiry is submitted or not
        if request.env.user.id != request.env.ref('base.public_user').id:
            lead = request.env['crm.lead'].sudo().search(
                [('partner_id', '=', request.env.user.partner_id.id),
                 ('property_id', '=', prop.id)])
            if lead:
                enquiry_made = True
        # No of bookmarks
        bookmark_count = request.env['property.bookmark'].sudo(
        ).search_count([('property_id', '=', prop.id)])
        # context
        config_rec = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')

        meta_data = {
            'twitter:card': prop.seo_description or prop.short_description,
            'twitter:title': prop.seo_title or prop.name,
        }
        opengraph_data = {
            'og:type': prop.seo_type or 'website',
            'og:title': prop.seo_title or prop.name,
            'og:site_name': prop.seo_description or prop.short_description,
            'og:url': url_join(request.website.domain or request.httprequest.url_root,
                               request.env['ir.http']._url_for(request.httprequest.path)),
        }
        if not prop.image:
            image_path = 'tk_website_rental_management/static/src/images/property-placeholder.jpg'
            opengraph_data['og:image'] = f'{request.httprequest.url_root}' + image_path
            meta_data['twitter:image'] = f'{request.httprequest.url_root}' + image_path
        else:
            opengraph_data[
                'og:image'] = (
                f'{request.httprequest.url_root}web/image/property.details/{prop.id}/image')
            meta_data[
                'twitter:image'] = (
                f'{request.httprequest.url_root}web/image/property.details/{prop.id}/image')

        seo_data = {
            'meta_data': meta_data,
            'opengraph_data': opengraph_data,
            'title': prop.seo_title,
            'description': prop.seo_description if prop.seo_description else prop.short_description,
            'keywords': prop.seo_keyword,
            'author': prop.seo_author,
            'generator': prop.seo_generator,
        }

        ctx = {
            'prop': prop,
            'book_properties': book_prop,
            'theme_config': config_rec,
            'error_msg': error_msg,
            'enquiry_made': enquiry_made,
            'book_count': bookmark_count,
            'seo_data': seo_data,
        }
        return request.render("tk_website_rental_management.property_details", ctx)

    @http.route('/property/wishlist', type='jsonrpc', auth="user")
    def property_wishlist(self, **kw):
        """User wise wishlist of different property"""
        bookmark_param = request.env['property.bookmark'].sudo()
        property_id = request.env['property.details'].sudo().search(
            [('access_token', '=', kw.get('access'))],
            limit=1)
        property_data = False
        if property_id:
            toggle = kw.get('toggle')
            bookmark_property = bookmark_param.search([('property_id', '=', property_id.id),
                                                       ('partner_id', '=',
                                                        request.env.user.partner_id.id)],
                                                      limit=1)
            if toggle and bookmark_property:
                bookmark_property.unlink()
            else:
                bookmark_param.create(
                    {'property_id': property_id.id, 'partner_id': request.env.user.partner_id.id})
            property_data = {
                'name': property_id.name,
                'image': image_data_uri(property_id.image) if property_id.image else '/tk_website_rental_management/static/src/images/property-placeholder.jpg',
                'redirect_url': f"/property-details/{request.env['ir.http']._slug(property_id)}",
                'access_token': property_id.access_token,
                'map_url': f'https://maps.google.com/maps?q=loc:{property_id.latitude},{property_id.longitude}',
            }

            if property_id.street or property_id.city_id or property_id.state_id or property_id.country_id:
                address = ""
                if property_id.street:
                    address += property_id.street
                if property_id.street and (
                        property_id.city_id or property_id.state_id or property_id.country_id):
                    address += ", "
                if property_id.city_id:
                    address += property_id.city_id.name
                if property_id.city_id and (property_id.state_id or property_id.country_id):
                    address += ", "
                if property_id.state_id:
                    address += property_id.state_id.code
                if property_id.state_id and property_id.country_id:
                    address += ", "
                if property_id.country_id:
                    address += property_id.country_id.code
                property_data['address'] = address

        book_prop = bookmark_param.search_count(
            [('partner_id', '=', request.env.user.partner_id.id)])
        return {'count': book_prop, 'property_data': property_data}

    @http.route('/property/wishlist/clear', type='jsonrpc', auth="user")
    def property_wishlist_clear(self, **kw):
        """Clear wishlist of property"""
        bookmark_param = request.env['property.bookmark'].sudo()
        property_id = request.env['property.details'].sudo().search(
            [('access_token', '=', kw.get('access'))],
            limit=1).id
        if property_id:
            bookmark_property = bookmark_param.search([('property_id', '=', property_id),
                                                       ('partner_id', '=',
                                                        request.env.user.partner_id.id)],
                                                      limit=1)
            if bookmark_property:
                bookmark_property.unlink()
        book_prop = bookmark_param.search_count(
            [('partner_id', '=', request.env.user.partner_id.id)])
        return {'count': book_prop}

    @http.route(['/map-view',
                 '/map-view/page/<int:page>',
                 '/map-view/<string:list_type>',
                 '/map-view/<string:list_type>/page/<int:page>'], type='http', auth="public",
                website=True)
    def map_view(self, list_type=None, page=0, **kw):
        """List of properties"""
        property_param = request.env['property.details'].sudo()
        # theme config rec
        config_rec = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        # domain list
        list_domain = [('stage', '=', 'available')]
        # category wise filter domain
        if list_type:
            list_domain = list_domain + category_wise_domain_filter(list_type)

        # Property filters
        url_args, prop_filters, default_order = get_all_filters(request.params)
        list_domain = list_domain + prop_filters
        # multi company
        list_domain = list_domain + [('company_id', 'in', [request.website.company_id.id, False])]
        # Dynamic Amenities
        da_list = dynamic_amenities_list(request.params)
        if da_list:
            properties = self.get_dynamic_amenity_filter(da_list)
            list_domain = list_domain + properties

        # property list limit
        property_per_page = config_rec.list_property_per_page
        list_count = property_param.search_count(list_domain)

        # pagination
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=list_count,
            page=page,
            step=property_per_page,
            url_args=url_args,
        )
        # listings
        listing = property_param.search(list_domain, order=default_order, offset=pager['offset'],
                                        limit=property_per_page)

        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids

        dynamic_amenity_ids = request.env['property.amenities'].sudo().search(
            [('is_on_website', '=', True)])

        # Categories
        category_domain = []
        if kw.get('categ'):
            category_domain = category_domain + [('type', '=', kw.get('categ'))]
        categories = request.env['property.sub.type'].sudo().search(
            category_domain, order='sequence asc')

        ctx = {
            'listing': listing,
            'list_type': list_type,
            'pager': pager,
            'cities': property_param.get_all_cities(),
            'theme_config': config_rec,
            'book_properties': book_prop,
            'book_property_count': len(book_prop),
            'da_ids': dynamic_amenity_ids,
            'da_list': da_list,
            'categories': categories,
        }
        return request.render('tk_website_rental_management.map_view', ctx)

    @http.route(['/map/map-view',
                 '/map/map-view/page/<int:page>',
                 '/map/map-view/<string:list_type>',
                 '/map/map-view/<string:list_type>/page/<int:page>',
                 '/map/<string:lang>/map-view',
                 '/map/<string:lang>/map-view/page/<int:page>',
                 '/map/<string:lang>/map-view/<string:list_type>',
                 '/map/<string:lang>/map-view/<string:list_type>/page/<int:page>'], type='jsonrpc',
                auth="public",
                website=True, csrf=False)
    def get_properties_by_json(self, list_type=None, lang=None, page=0, **kw):
        """Get property data for showing in map"""
        property_param = request.env['property.details'].sudo()
        # theme config rec
        config_rec = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        # domain list
        list_domain = [('stage', '=', 'available')]
        # category wise filter domain
        if list_type:
            list_domain = list_domain + category_wise_domain_filter(list_type)

        req_params = {}
        # Property filters
        if kw.get('param', False):
            req_params = convert_str_to_dict(kw.get('param'))
        url_args, prop_filters, default_order = get_all_filters(req_params)
        list_domain = list_domain + prop_filters
        # multi company
        list_domain = list_domain + [('company_id', 'in', [request.website.company_id.id, False])]
        # Dynamic Amenities
        da_list = dynamic_amenities_list(req_params)
        if da_list:
            properties = self.get_dynamic_amenity_filter(da_list)
            list_domain = list_domain + properties

        # property list limit
        property_per_page = config_rec.list_property_per_page
        list_count = property_param.search_count(list_domain)

        # pagination
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=list_count,
            page=page,
            step=property_per_page,
            url_args=url_args,
        )
        # listings
        list_domain += [('longitude', '!=', False), ('latitude', '!=', False)]
        listing = property_param.search(list_domain, order=default_order, offset=pager['offset'],
                                        limit=property_per_page)
        property_data = []

        for prop in listing:
            address = self.get_property_address(prop)
            property_class = self.get_property_type(prop)
            if prop.image:
                property_image = image_data_uri(prop.image)
            else:
                property_image = (
                    '/tk_website_rental_management/static/src/images/property-placeholder.jpg')
            property_url = '/property-details/' + request.env['ir.http']._slug(prop)

            if prop.sale_lease == 'for_sale':
                property_type = 'Sale'
                property_amount = prop.currency_id.symbol + " " + str(
                    prop.format_price(prop.price))
            else:
                property_type = 'Rent'
                property_amount = prop.currency_id.symbol + " " + str(
                    prop.format_price(prop.price)) + " / " + prop.rent_unit

            property_data.append((property_url, property_image, prop.name, address,
                                  property_class, property_amount,
                                  '', property_type,
                                  prop.latitude, prop.longitude, 0, property_image))

        ctx = {
            'properties': property_data,
            'center': config_rec.map_center_address,
            'latitude': config_rec.latitude,
            'longitude': config_rec.longitude,
            'zoom_level': config_rec.zoom_level,
        }

        return ctx

    @http.route('/get-filter-currency-symbol', type='jsonrpc', auth="public", website=True)
    def get_currency_for_filter(self):
        """Getting currency and pricing display type"""
        # theme config rec
        home_config = request.env.ref('tk_website_rental_management.property_theme_config_rec')
        filter_currency = home_config.filter_currency_id.symbol
        return {
            'filter_currency': filter_currency,
            'pricing_display_type': home_config.pricing_display_type,
        }

    @http.route('/property/brochure-qr/<string:access_token>', type='http', auth="public",
                website=True)
    def download_property_brochure(self, access_token):
        """Download property brochure from website"""
        if not access_token:
            return request.redirect('/')

        property_id = request.env["property.details"].sudo().search(
            [('access_token', '=', access_token)], limit=1)

        if not property_id:
            return request.redirect('/')

        pdf_data = "rental_management.property_details_report_id"
        file_name = "Property Details.pdf"

        pdf_content = request.env['ir.actions.report'].sudo()._render_qweb_pdf(pdf_data,
                                                                               property_id.id)
        response = request.make_response(pdf_content, headers=[('Content-Type', 'application/pdf')])

        response.headers.add('Content-Disposition', content_disposition(file_name))
        return response

    def get_property_address(self, prop):
        """Return property address"""
        address = ""
        if prop.street:
            address += prop.street + ", "
        if prop.street2:
            address += prop.street2 + ", "
        if prop.city_id:
            address += prop.city_id.name + ", "
        if prop.state_id:
            address += prop.state_id.code + ", "
        if prop.country_id:
            address += prop.country_id.code
        return address

    def get_property_type(self, prop):
        """Return property type"""
        property_class = ""
        if prop.type == 'residential':
            property_class = 'fa-home'
        if prop.type == 'land':
            property_class = 'fa-map'
        if prop.type == 'commercial':
            property_class = 'fa-dumpster'
        if prop.type == 'industrial':
            property_class = 'fa-industry'
        return property_class


class PropertyCustomerPortal(CustomerPortal):
    """Customer portal entry for property enquiry"""

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'enquiry_count' in counters and 'broker_commission_count' in counters:
            enquiries = request.env['crm.lead']
            domain = [('partner_id', '=', request.env.user.partner_id.id),
                      ('property_id', '!=', False)]
            values['enquiry_count'] = enquiries.search_count(domain)

            if request.env.user.partner_id.user_type == 'broker':
                broker_rent_contracts = request.env.user.partner_id.tenancy_ids
                broker_sale_contracts = request.env.user.partner_id.property_sold_ids
                values['broker_commission_count'] = len(broker_rent_contracts) + len(
                    broker_sale_contracts)
        return values

    @http.route(['/property/enquiries'], type='http', auth="user", website=True)
    def property_enquiry_details(self):
        """Get list of property enquiries"""
        enquiries = request.env['crm.lead'].sudo()
        domain = [('partner_id', '=', request.env.user.partner_id.id),
                  ('property_id', '!=', False)]
        recs = enquiries.search(domain)
        ctx = {
            'enqs': recs,
            'page_name': 'enquiry',
        }
        return request.render("tk_website_rental_management.enquiry_list", ctx)

    @http.route(['/property/enquiry/details/<model("crm.lead"):enquiry>'], type='http', auth="user",
                website=True)
    def portal_my_enquiry_detail(self, enquiry):
        """Return enquiry by property"""
        ctx = {
            'enquiry': enquiry,
            'page_name': 'enquiry',
        }
        return request.render("tk_website_rental_management.enquiry_details", ctx)

    @http.route(['/broker/contracts/commission',
                 '/broker/contracts/commission/page/<int:page>'], type='http', auth="user",
                website=True)
    def broker_contracts_commission(self):
        """Get brokers all contract"""
        if request.env.user.partner_id.user_type != 'broker':
            return request.redirect("/my/home")
        broker_rent_contracts = request.env.user.partner_id.tenancy_ids
        broker_sale_contracts = request.env.user.partner_id.property_sold_ids
        is_contract_available = False
        if len(broker_sale_contracts) > 0 or len(broker_rent_contracts) > 0:
            is_contract_available = True

        ctx = {
            'broker_rent_contracts': broker_rent_contracts,
            'broker_sale_contracts': broker_sale_contracts,
            'is_any_contract_available': is_contract_available,
            'page_name': 'broker_commission_list_view',
        }
        return request.render("tk_website_rental_management.broker_contracts_commission", ctx)

    @http.route(
        ['/broker/contracts/commission/details/rent/<model("tenancy.details"):rent_contract>',
         '/broker/contracts/commission/details/sale/<model("property.vendor"):sale_contract>'],
        type='http', auth="user", website=True)
    def broker_contracts_commission_details(self, rent_contract=None, sale_contract=None):
        """Contract Commission Details"""
        if request.env.user.partner_id.user_type != 'broker':
            return request.redirect("/my/home")
        if not rent_contract and not sale_contract:
            return request.redirect("/my/home")

        if sale_contract:
            if (
                    not sale_contract.is_any_broker
                    or not sale_contract.broker_id
                    or sale_contract.broker_id.id != request.env.user.partner_id.id
                    or not sale_contract.broker_bill_id
                    or sale_contract.broker_bill_id.sudo().state == 'draft'
            ):
                return request.redirect('/my/home')
            contract_details = sale_contract
            contract_type = 'sale'
        else:
            if (not rent_contract.broker_id
                    or rent_contract.broker_id.id != request.env.user.partner_id.id
            ):
                return request.redirect('/my/home')
            contract_details = rent_contract
            contract_type = 'rent'

        ctx = {
            'contract_details': contract_details,
            'contract_type': contract_type,
            'page_name': 'broker_commission_form_view',
        }
        return request.render("tk_website_rental_management.broker_contracts_commission_details",
                              ctx)
