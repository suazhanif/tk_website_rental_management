# -*- coding: utf-8 -*-
# Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.tools.image import image_data_uri


class SnippetsController(Website):
    """Routes For Dynamic Snippets"""

    def get_price_string(self, price, currency_id):
        """Return formated price with currency symbol"""
        if not currency_id:
            currency_id = request.env.company.currency_id
        if currency_id.position == 'before':
            formated_price = f"{currency_id.symbol} {price}"
        else:
            formated_price = f"{price} {currency_id.symbol}"
        return formated_price

    @http.route('/get-popular-property-data', type='jsonrpc', auth="public", website=True)
    def popular_properties_snippets(self):
        """Collect Data For Popular Properties"""
        property_param = request.env['property.details'].sudo()
        home_config = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        property_domain = [('stage', '=', 'available'),
                           ('is_popular_list', '=', True)]
        popular_listing = property_param.search(property_domain, order='id desc',
                                                limit=home_config.no_popular_list)

        popular_listing_list = []

        for data in popular_listing:
            popular_listing_data = {
                "id": data.id,
                "type": data.type,
                "access_token": data.access_token,
                "slug_data": request.env['ir.http']._slug(data),
                "image": (
                    image_data_uri(data.image) if data.image else
                    '/tk_website_rental_management/static/src/images/property-placeholder.jpg'),
                "name": data.name,
                "landlord_id": {
                    "name": data.landlord_id.name,
                    "image": (
                        image_data_uri(data.landlord_id.image_1920)
                        if data.landlord_id.image_1920 else
                        '/tk_website_rental_management/static/src/images/user.png'),
                },
                "sale_lease": data.sale_lease,
                "is_verify": data.is_verify,
                "latitude": data.latitude,
                "longitude": data.longitude,
                "street": data.street,
                "city": data.city_id.name if data.city_id else '',
                "state": data.state_id.code if data.state_id and data.state_id.code else '',
                "country": data.country_id.code,
                "short_description": data.short_description,
                "price": self.get_price_string(data['price'], request.env.company.currency_id),
                "rent_unit": data.rent_unit,
                "web_gym": data.web_gym,
                "web_wifi": data.web_wifi,
                "web_parking": data.web_parking,
                "web_air_condition": data.web_air_condition,
                "web_semi_furnish": data.web_semi_furnish,
                "web_full_furnish": data.web_full_furnish,
                "web_security": data.web_security,
                "web_laundry": data.web_laundry,
                "web_equip_kitchen": data.web_equip_kitchen,
                "website_amenity_ids": [{
                    "id": amenity.id,
                    "title": amenity.title if amenity.title else '',
                    "fa_class": amenity.fa_class if amenity.fa_class else '',
                } for amenity in data.website_amenity_ids if data.website_amenity_ids],
                "property_subtype_name": data.property_subtype_id.name,
                "property_images_ids": data.property_images_ids.ids,
                "property_images": [{
                    "src": image_data_uri(image.image),
                } for image in data.property_images_ids if data.property_images_ids],
            }
            popular_listing_list.append(popular_listing_data)

        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids

        logged_user = request.env.user.id != request.env.ref(
            'base.public_user').id

        return {
            'popular_listing': popular_listing_list,
            'logged_user': logged_user,
            'book_properties': book_prop,
            'display_landlord': home_config.display_landlord,
            'is_popular_properties_visible': home_config.is_popular_properties_visible,
        }

    @http.route('/get-latest-listing-data', type='jsonrpc', auth="public", website=True)
    def latest_listing_snippets(self):
        """Collect Data For Latest Listing"""
        property_param = request.env['property.details'].sudo()
        home_config = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        latest_listing = property_param.search(
            [('stage', '=', 'available'), ('is_latest_listing', '=', True)], order='id desc',
            limit=home_config.no_latest_list)
        logged_user = request.env.user.id != request.env.ref(
            'base.public_user').id
        book_prop = request.env['property.bookmark'].sudo().search(
            [('partner_id', '=', request.env.user.partner_id.id)]).mapped('property_id').ids

        latest_listing_list = []

        for data in latest_listing:
            latest_listing_data = {
                'id': data.id,
                'access_token': data.access_token,
                'name': data.name,
                'slug_data': request.env['ir.http']._slug(data),
                'image': (
                    image_data_uri(data.image) if data.image else
                    '/tk_website_rental_management/static/src/images/property-placeholder.jpg'),
                'is_verify': data.is_verify,
                'latitude': data.latitude,
                'longitude': data.longitude,
                'street': data.street,
                'city': data.city_id.name if data.city_id else '',
                'state': data.state_id.code if data.state_id and data.state_id.code else '',
                'country': data.country_id.code if data.country_id else '',
                'sale_lease': data.sale_lease,
                'type': data.type,
                'rent_unit': data.rent_unit,
                'landlord_id': {
                    'name': data.landlord_id.name,
                    'image': (
                        image_data_uri(data.landlord_id.image_1920)
                        if data.landlord_id.image_1920
                        else 'tk_website_rental_management/static/src/images/user.png'),
                },
                'property_subtype_name': data.property_subtype_id.name,
                'price': self.get_price_string(data.price, data.currency_id)
            }

            latest_listing_list.append(latest_listing_data)

        return {
            'latest_listing': latest_listing_list,
            'logged_user': logged_user,
            'display_landlord': home_config.display_landlord,
            'book_properties': book_prop,
            'is_latest_listing_visible': home_config.is_latest_listing_visible,
        }

    @http.route('/get-home-config-data', type='jsonrpc', auth="public", website=True)
    def home_banner_snippets(self):
        """Collect Data For Home Banner"""
        home_config = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        property_param = request.env['property.details'].sudo()

        config_data = {
            'hero_choice': home_config.hero_choice,
            'video_bg_url': home_config.video_bg_url,
            'youtube_bg_video': home_config.youtube_bg_video,
            'price_start': home_config.price_start,
            'price_end': home_config.price_end,
            'area_start': home_config.area_start,
            'area_end': home_config.area_end,
            'cities': property_param.get_all_cities(),
            'hero_categories': None,
            'da_ids': None,
            'param_da': request.params.get('da'),
        }
        if home_config.mob_background:
            config_data['mob_background'] = image_data_uri(
                home_config.mob_background)
        if home_config.image_1920_0:
            config_data['image_1920_0'] = image_data_uri(
                home_config.image_1920_0)
        if home_config.image_1920_1:
            config_data['image_1920_1'] = image_data_uri(
                home_config.image_1920_1)
        if home_config.image_1920_2:
            config_data['image_1920_2'] = image_data_uri(
                home_config.image_1920_2)
        if home_config.image_1920_3:
            config_data['image_1920_3'] = image_data_uri(
                home_config.image_1920_3)

        # Collect Hero Category Data
        hero_categories = request.env['property.sub.type'].sudo().search(
            [('display_on_home', '=', True)], limit=8, order='sequence asc')
        hero_category_list = []
        if hero_categories:
            for category in hero_categories:
                hero_category_data = {
                    'id': category.id,
                    'name': category.name,
                    'display_on_home': category.display_on_home,
                    'type': category.type,
                    'image': (
                        image_data_uri(category.image) if category.image else
                        '/tk_website_rental_management/static/src/images/category-placeholder.png')
                }
                hero_category_list.append(hero_category_data)
            config_data['hero_categories'] = hero_category_list

        # Collect Dynamic Amenities Data
        dynamic_amenity_ids = request.env['property.amenities'].sudo().search(
            [('is_on_website', '=', True)])
        amenity_list = []
        if dynamic_amenity_ids:
            for amenity in dynamic_amenity_ids:
                amenity_data = {
                    'id': amenity.id,
                    'title': amenity.title,
                }
                amenity_list.append(amenity_data)
            config_data['da_ids'] = amenity_list

        return {
            'home_config': config_data
        }

    @http.route('/get-counter-data', type='jsonrpc', auth="public", website=True)
    def couonter_snippets(self):
        """Collect Data For Counter"""
        home_config = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        counter_data = {
            "sec_img_2": False,
            "hs_one": home_config.hs_one,
            "hs_two": home_config.hs_two,
            "hs_three": home_config.hs_three,
            "hs_four": home_config.hs_four,
        }

        if home_config.sec_img_2:
            counter_data['sec_img_2'] = image_data_uri(home_config.sec_img_2)

        return counter_data

    @http.route('/get-testimonials-data', type='jsonrpc', auth="public", website=True)
    def testimonials_snippets(self):
        """Collect Data For Testimonials"""
        home_config = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        testimonials_list = []
        if home_config.review_ids:
            for review in home_config.review_ids:
                testimonials_data = {
                    "name": review.name,
                    "rate": review.rate,
                    "role": review.role,
                    "reviews": review.reviews,
                    "image_1920": (
                        image_data_uri(review.image_1920) if review.image_1920 else
                        '/tk_website_rental_management/static/src/images/user.png'),
                }
                testimonials_list.append(testimonials_data)
        return testimonials_list

    @http.route('/get-partners-data', type='jsonrpc', auth="public", website=True)
    def partners_snippets(self):
        """Collect Data For Partners"""
        home_config = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        partners_list = []
        if home_config.partner_ids:
            for partner in home_config.partner_ids:
                partners_data = {
                    "name": partner.name,
                    "partner_logo": (
                        image_data_uri(partner.partner_logo) if partner.partner_logo else
                        '/tk_website_rental_management/static/src/images/client.png'),
                }
                partners_list.append(partners_data)
        return partners_list

    @http.route('/get-popular-places-data', type='jsonrpc', auth="public", website=True)
    def popular_places_snippets(self):
        """Collect Data For Popular Places"""
        home_config = request.env.ref(
            'tk_website_rental_management.property_theme_config_rec')
        city_list = []
        if home_config.city_ids:
            for city in home_config.city_ids:
                city_data = {
                    "size": city.size,
                    "cover_image": image_data_uri(city.cover_image),
                    "property_count": city.property_count,
                    "city_name": city.city_id.name,
                    "tag_line": city.tag_line,
                    "city_slug": request.env['ir.http']._slug(city.city_id),
                }
                city_list.append(city_data)
        return city_list
