# -*- coding: utf-8 -*-
# DCR INFORMATIC SERVICES SAS DE CV
# https://www.dcrsoluciones.com

from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    purchase_price = fields.Float(
        string='Purchase price',
        digits='Product Price',
        store=True
    )

    margin = fields.Float(
        string='Margin',
        compute='_compute_margin',
        store=True
    )

    @api.depends('price_unit', 'product_uom_qty', 'discount', 'purchase_price')
    def _compute_margin(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.margin = (price - (line.purchase_price or 0.0)) * line.product_uom_qty

    @api.onchange('product_id')
    def _onchange_product_id_set_purchase_price(self):
        for line in self:
            if line.product_id:
                line.purchase_price = line.product_id.standard_price

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    margin = fields.Monetary(
        string='Margin',
        compute='_compute_margin',
        store=True
    )

    @api.depends('order_line.margin')
    def _compute_margin(self):
        for order in self:
            order.margin = sum(line.margin for line in order.order_line)