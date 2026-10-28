# -*- coding: utf-8 -*-
# Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
import uuid
from io import BytesIO
import base64
import qrcode

from odoo.http import request
from odoo import fields, models, api, _
from odoo.tools.translate import html_translate


class PropertyRentalConfig(models.Model):
    """Inherit property details modal"""
    _inherit = 'property.details'

    # website listing features
    web_gym = fields.Boolean('Gym')
    web_wifi = fields.Boolean('WiFi')
    web_parking = fields.Boolean('Parking ')
    web_pool = fields.Boolean('Pool')
    web_security = fields.Boolean('Security')
    web_laundry = fields.Boolean('Laundry Room')
    web_equip_kitchen = fields.Boolean('Equipped Kitchen')
    web_air_condition = fields.Boolean('Air Conditioned')
    web_semi_furnish = fields.Boolean('Semi Furnished')
    web_full_furnish = fields.Boolean('Full Furnished')
    web_alarm = fields.Boolean('Safety Alarm')
    web_window_cover = fields.Boolean('Window Covering')
    accommodation = fields.Integer('Accommodation')

    similar_properties = fields.Many2many('property.details', 'similar_property_rel', 'sp_id',
                                          'property_id',
                                          string="Similar Properties")

    website_description = fields.Html(string="Website Description", translate=html_translate,
                                      sanitize_attributes=False, )
    short_description = fields.Char(string="Short Description", size=150, translate=True)

    access_token = fields.Char()
    is_popular_list = fields.Boolean(string="Is Popular Listing ?")
    is_verify = fields.Boolean(string="Is Verified ?")

    lead_count = fields.Integer(string="Leads", compute='_compute_get_lead_count')

    website_amenity_ids = fields.Many2many('property.amenities', 'property_website_amenity_rel',
                                           'property_id',
                                           'amenity_id', string="Website Extra Amenities")

    video_url = fields.Char(string="Video Link")
    video_background_image = fields.Image(string="Video Background Image")
    three_sixty_view_link = fields.Char(
        string="360° Virtual Tour Link",
        default="https://my.matterport.com/show/?m=wWcGxjuUuSb&amp;utm_source=hit-content-embed")

    broker_id = fields.Many2one('res.partner', string="Property Broker",
                                domain="[('user_type','=','broker')]")
    visible_broker_on_property = fields.Boolean(string="Visible Broker on Property")

    # SEO Section
    seo_title = fields.Char(string="Title")
    seo_description = fields.Text(string="Description")
    seo_keyword = fields.Char(string="Keywords")
    seo_author = fields.Char(string="Author")
    seo_generator = fields.Char(string="Generator")
    seo_type = fields.Char(string="Type", default="Website")

    property_brochure_qr = fields.Binary()
    is_latest_listing = fields.Boolean(string="Is Latest Listing ?")

    @api.model_create_multi
    def create(self, vals):
        """overwrite create method of property details"""
        for value in vals:
            value['access_token'] = str(uuid.uuid4())
            base_url = request.httprequest.url_root
            brochure_url = f"{base_url}property/brochure-qr/{value.get('access_token')}"
            value['property_brochure_qr'] = self._generate_qr_code(brochure_url)
        res = super().create(vals)
        return res

    def _generate_qr_code(self, url):
        """Generate qr code"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp, format="PNG")
        qr_code = base64.b64encode(temp.getvalue())
        return qr_code

    def action_generate_property_brochure_qr(self):
        """Generate QR for property brochure"""
        for rec in self:
            if not rec.property_brochure_qr:
                if not rec.access_token:
                    rec.assign_access_token()
                base_url = request.httprequest.url_root
                brochure_url = f"{base_url}property/brochure-qr/{rec.access_token}"
                rec.property_brochure_qr = self._generate_qr_code(brochure_url)

    def three_sixty_view_tour(self):
        """Redirect to 360 virtual tour website"""
        return {
            "type": "ir.actions.act_url",
            "url": "https://matterport.com/discover",
            "target": "new",
        }

    def _compute_get_lead_count(self):
        """Compute lead count"""
        for rec in self:
            leads = 0
            if rec.id:
                leads = self.env['crm.lead'].sudo().search_count([('property_id', '=', rec.id)])
            rec.lead_count = leads

    def assign_access_token(self):
        """Assign access token"""
        self.access_token = str(uuid.uuid4())

    def action_get_leads(self):
        """action of redirect to leads tree view"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Property Leads',
            'res_model': 'crm.lead',
            'domain': [('property_id', '=', self.id)],
            'context': {'default_property_id': self.id},
            'view_mode': 'tree,form',
            'target': 'current'
        }

    def get_all_cities(self):
        """Get all city which is added in available property"""
        cities = self.env['property.details'].sudo().search([('stage', '=', 'available')]).mapped(
            'city_id')
        city_list = []
        if cities:
            city_list = sorted(cities.mapped('name'))
        return city_list

    def action_show_property(self):
        """Redirect to property details website page"""
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': f'/property-details/{request.env["ir.http"]._slug(self)}',
        }

    def share_on_facebook(self):
        """Create link for share property on facebook"""
        slug = request.env["ir.http"]._slug(self)
        article_url = f'{request.httprequest.url_root}/property-details/{slug}'
        url = f'https://www.facebook.com/sharer/sharer.php?u={article_url}'

        client_action = {
            'type': 'ir.actions.act_url',
            'name': "Share on facebook",
            'target': 'new',
            'url': url,
        }
        return client_action

    def share_on_x(self):
        """Create link for share property on x"""
        slug = request.env["ir.http"]._slug(self)
        article_url = f'{request.httprequest.url_root}/property-details/{slug}'
        tweet_text = _("Amazing property: %(name)s! Check it live: %(url)s", name=self.name,
                       url=article_url)
        url = f'https://twitter.com/intent/tweet?tw_p=tweetbutton&text={tweet_text}'

        client_action = {
            'type': 'ir.actions.act_url',
            'name': "Share on facebook",
            'target': 'new',
            'url': url,
        }
        return client_action

    def share_on_linkedin(self):
        """Create link for share property on linkedin"""
        slug = request.env["ir.http"]._slug(self)
        article_url = f'{request.httprequest.url_root}/property-details/{slug}'
        url = f'https://www.linkedin.com/sharing/share-offsite/?url={article_url}'

        client_action = {
            'type': 'ir.actions.act_url',
            'name': "Share on facebook",
            'target': 'new',
            'url': url,
        }
        return client_action

    def format_price(self, price):
        """
        Converts a price into a human-readable format.

        Parameters:
            price (str or int): The price value to format (e.g., "3,00,000" or 30000000).

        Returns:
            str: The formatted price.
        """
        # Remove commas and convert to integer
        if isinstance(price, str):
            price = float(price.replace(",", ""))
        elif not isinstance(price, float):
            return price

        home_config = self.env.ref('tk_website_rental_management.property_theme_config_rec')
        format_type = home_config.pricing_display_type
        pricing_type = home_config.pricing_type
        formated_price = ""

        if format_type == "indian_pricing":
            if price >= 1_00_00_000:  # Cr
                formated_price = (f"{price / 1_00_00_000:.2f} Cr" if pricing_type == "decimal"
                                  else f"{price / 1_00_00_000:.0f} Cr")
            elif price >= 1_00_000:  # Lac
                formated_price = (f"{price / 1_00_000:.2f} Lac" if pricing_type == "decimal"
                                  else f"{price / 1_00_000:.0f} Lac")
            else:
                formated_price = f"{price:,.2f}" if pricing_type == "decimal" else f"{price:,.0f}"
                # Return with commas for thousands

        elif format_type == "english_pricing":
            if price >= 1_00_00_00_000:  # Billions
                formated_price = (f"{price / 1_00_00_00_000:.2f}B" if pricing_type == "decimal"
                                  else f"{price / 1_00_00_00_000:.0f}B")
            elif price >= 1_00_00_000:  # Millions
                formated_price = (f"{price / 1_00_00_000:.2f}M" if pricing_type == "decimal"
                                  else f"{price / 1_00_00_000:.0f}M")
            elif price >= 1_000:  # Thousands
                formated_price = (f"{price / 1_000:.2f}K" if pricing_type == "decimal"
                                  else f"{price / 1_000:.0f}K")
            else:
                formated_price = f"{price:,.2f}" if pricing_type == "decimal" else f"{price:,.0f}"
                # Return with commas for thousands

        else:
            formated_price = f"{price:.2f}" if pricing_type == "decimal" else f"{price:.0f}"
        return formated_price


class PropertyBookmark(models.Model):
    """Property Bookmark"""
    _name = 'property.bookmark'
    _description = __doc__

    partner_id = fields.Many2one('res.partner', string="User")
    property_id = fields.Many2one('property.details', string="Property")


class PropertyWebsiteAmenities(models.Model):
    """Property Website Amenities"""
    _inherit = 'property.amenities'

    fa_class = fields.Char(string="Fa Class")
    is_on_website = fields.Boolean(string="Is Published on Website?")

    def get_fa_icon(self):
        """Return to fontawesome website"""
        return {
            "type": "ir.actions.act_url",
            "url": "https://fontawesome.com/v4/icons/",
            "target": "new",
        }


class PropertySubTypes(models.Model):
    """Property Sub Types"""
    _inherit = 'property.sub.type'

    display_on_home = fields.Boolean(string="Display On Home Page?")
    image = fields.Image(string="Image")
