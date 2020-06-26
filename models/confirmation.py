from odoo import models, fields, api


class confirmation(models.Model):
    
    _name = 'commande.confirmation'

    name = fields.Char(string='Commande Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: ('/'))
    partner_id = fields.Many2one('res.partner', string='Prestataire')
    write_date = fields.Date(string='Date de la commande')
    offer_number = fields.Char(string="Numéro offre prestataire")
    offer_reception_date = fields.Date(string="Date réception offre")
    comande_line = fields.One2many('commande.lines', 'commande_id', string="Commandes lines")
    delai = fields.Date('Délai')
    payment_term_id = fields.Many2one('account.payment.term', 'Détail Paiement')
    delivery = fields.Char('Livraison')
    user_id = fields.Many2one(
    'res.partner', string='Acheteur', index=True, tracking=True,
    default=lambda self: self.env.user)
    
    def _get_default_city(self):
        return self.env['res.partner'].search([('name', '=', 'city')], limit=1).city

    ville = fields.Char(string="Ville", default=_get_default_city, domain=[])

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        self.ville = self.partner_id.city

    def _get_default_poste(self):
        return self.env['res.partner'].search([('name', '=', 'function')], limit=1).id

    poste = fields.Char(string="Poste occupé", default=_get_default_poste, domain=[])
    
    @api.onchange('user_id')
    def onchange_user_id(self):
        self.poste = self.user_id.function

    @api.model 
    def create(self, vals):
        if vals.get('name', ('/')) == ('/'):
            vals['name'] = self.env['ir.sequence'].next_by_code('commande.order') or ('/')
        result = super(confirmation, self).create(vals)
        return result 

    class commandelines(models.Model):
        _name = 'commande.lines'
        
        product_id = fields.Many2one('product.product', string="Article")
        product_unit = fields.Integer(string='Unité')
        product_qut = fields.Integer(string='Quantité')
        price_unit = fields.Integer(string="Prix unitaire")
        taxes_id = fields.Many2many('account.tax', string='TVA')
        commande_id = fields.Many2one('commande.confirmation', string="commande ID")
        untaxed_total = fields.Integer(string='Total HT')
        taxed_total = fields.Integer(string='Total TTC')
        #price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)
        #amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=True)
        #amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
        #amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')

        #@api.depends('product_qut', 'product_unit', 'taxes_id')
        #def _compute_amount(self):
            #for line in self:
                #vals = line._prepare_compute_all_values()
                #taxes = line.taxes_id.compute_all(
                    #vals['product_unit'],
                    #vals['product_qut'],
                    #vals['product_id'],
                    #vals['partner_id'])
                #line.update({
                    #'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    #'price_total': taxes['total_included'],
                    #'price_subtotal': taxes['total_excluded'],
                #})
        
        #@api.depends('price_total')
        #def _amount_all(self):
            #for order in self:
                #amount_untaxed = amount_tax = 0.0
                #for line in order.commande_line:
                    #amount_untaxed += line.price_subtotal
                    #amount_tax += line.price_tax
                #order.update({
                    #'amount_untaxed': order.currency_id.round(amount_untaxed),
                    #'amount_tax': order.currency_id.round(amount_tax),
                    #'amount_total': amount_untaxed + amount_tax,
                #})
    
        #def _prepare_compute_all_values(self):
            # Hook method to returns the different argument values for the
            # compute_all method, due to the fact that discounts mechanism
            # is not implemented yet on the purchase orders.
            # This method should disappear as soon as this feature is
            # also introduced like in the sales module.
            #self.ensure_one()
            #return {
                #'product_unit': self.product_unit,
                #'product_qut': self.product_qut,
                #'product_id': self.product_id,
        #}
