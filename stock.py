from openerp.osv import osv, fields


# Nieuwe velden op header niveau om location & destination te gebruiken
# ---------------------------------------------------------------------
class stock_picking(osv.osv):
    _name = "stock.picking"
    _inherit = "stock.picking"
    _columns = {
        'location_id': fields.many2one('stock.location', 'Source Location', select=True,states={'done': [('readonly', True)]}, help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations."),
        'location_dest_id': fields.many2one('stock.location', 'Destination Location', states={'done': [('readonly', True)]}, select=True, help="Location where the system will stock the finished products."),
    }

stock_picking()

class stock_move(osv.osv):
    _name = "stock.move"
    _inherit = "stock.move"


    # on_change methods om de waarden vanuit header niveau over te nemen
    # de waarde wordt alleen overschreven indien leeg
    # ------------------------------------------------------------------
    def on_change_location_id(self, cr, uid, location_id, parent_location_id, context):
        if not parent_location_id:
            return {'value': {'location_id': context}}
        else:
            return {'value': {}}

    def on_change_location_dest_id(self, cr, uid, location_dest_id, parent_location_dest_id, context):
        if not parent_location_dest_id:
            return {'value': {'location_dest_id': context}}
        else:
            return {'value': {}}




    # deze methode is overschreven vanuit de superclass om ervoor
    # te zorgen dat de location & destination id niet TERUG overschreven worden
    # -------------------------------------------------------------------------
    def onchange_move_type(self, cr, uid, ids, type, context=None):
        """ On change of move type gives sorce and destination location.
        @param type: Move Type
        @return: Dictionary of values
        """
        if type == 'internal':
            return {'value':{}}
        else:
            return super(stock_move, self).onchange_move_type(cr, uid, ids, type, context)



    # de on_default methodes worden overschreven dat de oude functionaliteit nog
    # werkt voor non-internal move objecten
    # --------------------------------------------------------------------------
    def _default_location_destination(self, cr, uid, context=None):
        """ Gets default address of partner for destination location
        @return: Address id or False
        """

        if context.get('picking_type') != 'internal':
            return super(stock_move, self)._default_location_destination(cr, uid, context)

        return False


    def _default_location_source(self, cr, uid, context=None):
        """ Gets default address of partner for source location
        @return: Address id or False
        """

        if context.get('picking_type') != 'internal':
            return super(stock_move, self)._default_location_source(cr, uid, context)

        return False


    _defaults = {
        'location_id': _default_location_source,
        'location_dest_id': _default_location_destination,
    }

stock_move()











