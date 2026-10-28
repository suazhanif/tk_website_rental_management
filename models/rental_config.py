# -*- coding: utf-8 -*-
# Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PropertyRentalConfig(models.Model):
    """Theme Config"""
    _name = 'property.theme.config'
    _description = __doc__
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Title", default="Property Website Home Configuration", tracking=True)
    no_latest_list = fields.Integer(string="No. of Latest Listing", default=10, required=True, tracking=True)
    no_popular_list = fields.Integer(string="No. of Popular Listing", default=10, required=True, tracking=True)
    google_map_api = fields.Char(string="Google Map API Key")
    map_center_address = fields.Char(string="Map Center Address", default="USA", tracking=True)
    latitude = fields.Char(string="Latitude", tracking=True)
    longitude = fields.Char(string="Longitude", tracking=True)
    zoom_level = fields.Integer(string="Zoom Level", default="6", tracking=True)
    review_ids = fields.Many2many('property.website.reviews', string="Website Reviews", tracking=True)
    video_link = fields.Char(string="Video Link", tracking=True)
    partner_ids = fields.Many2many('property.website.partner', string="Partners", tracking=True)
    city_ids = fields.One2many('property.by.city', 'config_id', string="Cities", tracking=True)
    mailling_list_id = fields.Many2one('mailing.list', string="Newsletter", tracking=True)
    list_property_per_page = fields.Integer(string='Listing Properties per Page', default=12, tracking=True,
                                            required=True)

    hs_one = fields.Integer(string="Home stats 1", default=1254, tracking=True)
    hs_two = fields.Integer(string="Home stats 2", default=12168, tracking=True)
    hs_three = fields.Integer(string="Home stats 3", default=2172, tracking=True)
    hs_four = fields.Integer(string="Home stats 4", default=732, tracking=True)

    # price filters
    price_start = fields.Integer(string="Price Start Range", default=0, tracking=True)
    price_end = fields.Integer(string="Price End Range", default=50000, tracking=True)
    # area filters
    area_start = fields.Integer(string="Area Start Range", default=0, tracking=True)
    area_end = fields.Integer(string="Area End Range", default=5000, tracking=True)
    # show landlord
    display_landlord = fields.Boolean(string="Display Landlord on Property ?", default=True, tracking=True)
    # Section Search Images
    hero_choice = fields.Selection([('img', "Image Background"), ('vid', "Video Background"),
                                    ('youtube', "Youtube Video")], default='img',
                                   string="Search Section Background Type", tracking=True)
    video_bg_url = fields.Char(string="Video URL", tracking=True)
    youtube_bg_video = fields.Char(string="Youtube Video ID", tracking=True)
    mob_background = fields.Binary(string="Mobile BG Image for video")
    image_1920_0 = fields.Binary(string="Main BG Image")
    image_1920_1 = fields.Binary(string="Any Status BG Image")
    image_1920_2 = fields.Binary(string="For Rent BG Image")
    image_1920_3 = fields.Binary(string="For Sale BG Image")
    # Section 2 & # BG Images
    sec_img_2 = fields.Binary(string="Stats BG Image")
    sec_img_3 = fields.Binary(string="Promo Video BG Image")

    is_rtl = fields.Boolean(string="Is RTL Enable ?", tracking=True)

    visible_accommodation = fields.Boolean('Visible Accommodation ?', default=True, tracking=True)
    visible_three_sixty_view = fields.Boolean(string="Visible 360° Virtual Tour", default=True, tracking=True)
    visible_floor_plans = fields.Boolean(string="Visible Floor Plans", default=True, tracking=True)

    enquiry_submitted_on_logged_out = fields.Boolean(string="Enquiry without login?", tracking=True)

    is_user_send_whatsapp_messages = fields.Boolean(string="User Send Whatsapp Messages ?", tracking=True)
    whatsapp_number = fields.Char(string="Whatsapp Number", tracking=True)

    filter_currency_id = fields.Many2one('res.currency', string="Currency For Pricing Filter",
                                         default=lambda self: self.env.company.currency_id, tracking=True)
    pricing_display_type = fields.Selection(
        [('normal_pricing', 'Normal Pricing'), ('indian_pricing', 'Indian Pricing'),
         ('english_pricing', 'English Pricing')], string="Pricing Display Type",
        default="normal_pricing", tracking=True)

    is_latest_listing_visible = fields.Boolean(string="Is Latest Listing Visible", default=True, tracking=True)
    is_popular_properties_visible = fields.Boolean(string="Is Popular Properties Visible",
                                                   default=True, tracking=True)

    # Color Configuration
    primary_background = fields.Char(string="Primary Background", default="#2e3f6e", tracking=True)
    secondary_background = fields.Char(string="Secondary Background", default="#3d528b", tracking=True)
    emphasis_background = fields.Char(string="Secondary Background ", default="#4DB7FE", tracking=True)
    btn_primary = fields.Char(string="Primary Background ", default="#3d528b", tracking=True)
    btn_primary_text = fields.Char(string="Primary Text ", default="#f9fafe", tracking=True)
    btn_secondary_text = fields.Char(string="Secondary Text ", default="#f9fafe", tracking=True)
    text_color = fields.Char(string="Text Color", default="#7d93b2", tracking=True)
    link_color = fields.Char(string="Link Color", default="#4DB7FE", tracking=True)
    header_color = fields.Char(string="Header Color", default="#566985", tracking=True)
    header_text = fields.Char(string="Header / Footer Text", default="#FFFFFF", tracking=True)

    pricing_type = fields.Selection([('decimal', 'Decimal'), ('round', 'Round')], default="decimal", tracking=True)

    is_mail_send_to_landlord = fields.Boolean("Send mail to landlord while enquiry ?", tracking=True)

    listing_section_background = fields.Binary(string="Listing Section Background")

    @api.onchange('list_property_per_page', 'price_start', 'price_end', 'area_start', 'area_end',
                  'no_latest_list', 'no_popular_list', 'hs_one', 'hs_two', 'hs_three', 'hs_four')
    def _onchange_integer_field_validation(self):
        """Add Validation on all integer value"""
        if self.list_property_per_page <= 0:
            raise ValidationError(_("Listing properties per page should be greater than 0"))
        if self.price_start < 0:
            raise ValidationError(_("Price start range is not negative"))
        if self.price_end < 0:
            raise ValidationError(_("Price end range is not negative"))
        if self.area_start < 0:
            raise ValidationError(_("Area start range is not negative"))
        if self.area_end < 0:
            raise ValidationError(_("Area end range is not negative"))
        if self.no_latest_list <= 0:
            raise ValidationError(_("No. of Latest Listing should be greater than 0"))
        if self.no_popular_list <= 0:
            raise ValidationError(_("No. of Popular Listing should be greater than 0"))
        if self.hs_one < 0:
            raise ValidationError(_("Home stats 1 is not negative"))
        if self.hs_two < 0:
            raise ValidationError(_("Home stats 2 is not negative"))
        if self.hs_three < 0:
            raise ValidationError(_("Home stats 3 is not negative"))
        if self.hs_four < 0:
            raise ValidationError(_("Home stats 4 is not negative"))

    def action_reset_theme_colors(self):
        """Reset Theme Color To Default Colors"""
        for rec in self:
            rec.primary_background = "#2e3f6e"
            rec.secondary_background = "#3d528b"
            rec.emphasis_background = "#4DB7FE"
            rec.btn_primary = "#3d528b"
            rec.btn_primary_text = "#f9fafe"
            rec.btn_secondary_text = "#f9fafe"
            rec.text_color = "#7d93b2"
            rec.link_color = "#4DB7FE"
            rec.header_color = "#566985"
            rec.header_text = "#FFFFFF"


class PropertyWebsiteReview(models.Model):
    """Property Rental Website Reviews"""
    _name = 'property.website.reviews'
    _description = __doc__

    name = fields.Char(string="Name", required=True)
    image_1920 = fields.Binary(string="Profile Image")
    role = fields.Char(string="Role", required=True)
    rate = fields.Selection(
        [('1', '1 Star'), ('2', '2 Stars'), ('3', "3 Stars"), ('4', '4 Stars'), ('5', '5 Stars')],
        string="Rating", default='5', required=True)
    reviews = fields.Text(string="Reviews")


class PropertyWebsitePartners(models.Model):
    """Property Website Partners"""
    _name = 'property.website.partner'
    _description = __doc__

    name = fields.Char(string="Name", required=True)
    partner_logo = fields.Binary(string="Image", required=True)


class PropertiesByCity(models.Model):
    """Properties by city"""
    _name = 'property.by.city'
    _rec_name = 'city_id'
    _description = __doc__

    sequence = fields.Integer()
    property_count = fields.Integer(compute='_compute_property_total_counts',
                                    string="No. of Properties")
    city_id = fields.Many2one('property.res.city', required=True, string="City")
    cover_image = fields.Binary(string="Image", required=True)
    size = fields.Selection([('4', "4"), ('6', "6"), ('8', "8"), ('10', "10"), ('12', "12")],
                            default='4',
                            required=True)
    tag_line = fields.Text(string="Tag Line",
                           default="Constant care and attention to the patients makes good record")
    config_id = fields.Many2one('property.theme.config')

    @api.depends('city_id')
    def _compute_property_total_counts(self):
        """Total number of properties by city"""
        for rec in self:
            count = 0
            if rec.city_id:
                count = self.env['property.details'].sudo().search_count(
                    [('stage', '=', 'available'), ('city_id', '=', rec.city_id.id)])
            rec.property_count = count
