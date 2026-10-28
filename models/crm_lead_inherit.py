# -*- coding: utf-8 -*-
# Copyright (C) 2023-TODAY TechKhedut (<https://www.techkhedut.com>)
# Part of TechKhedut. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class PropertyCrmLeadInherit(models.Model):
    """Inherit lead for public submitted lead"""
    _inherit = 'crm.lead'

    is_public_lead = fields.Boolean(string="Is public lead")
