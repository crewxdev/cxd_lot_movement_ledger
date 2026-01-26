from odoo import models, fields, tools

class LotMovementLedger(models.Model):
    _name = "lot.movement.ledger"
    _description = "Lot Movement Ledger"
    _auto = False
    _order = "date desc"

    lot_id = fields.Many2one("stock.lot", readonly=True)
    product_id = fields.Many2one("product.product", readonly=True)

    date = fields.Datetime(readonly=True)
    reference = fields.Char(readonly=True)

    source_location_id = fields.Many2one("stock.location", readonly=True)
    dest_location_id = fields.Many2one("stock.location", readonly=True)

    qty = fields.Float(readonly=True)
    move_type = fields.Selection([
        ("in", "Incoming"),
        ("out", "Outgoing"),
        ("internal", "Internal"),
        ("adjustment", "Adjustment"),
    ], readonly=True)

    unit_cost = fields.Float(readonly=True)
    total_cost = fields.Float(readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    sml.id AS id,
                    sml.lot_id,
                    sml.product_id,
                    sml.date,
                    COALESCE(sp.name, sm.reference) AS reference,
                    sml.location_id AS source_location_id,
                    sml.location_dest_id AS dest_location_id,

                    CASE
                        WHEN src.usage != 'internal' AND dest.usage = 'internal' THEN 'in'
                        WHEN src.usage = 'internal' AND dest.usage != 'internal' THEN 'out'
                        WHEN src.usage = 'internal' AND dest.usage = 'internal' THEN 'internal'
                        ELSE 'adjustment'
                    END AS move_type,

                    sml.quantity AS qty,
                    sm.price_unit AS unit_cost,
                    sml.quantity * sm.price_unit AS total_cost

                FROM stock_move_line sml
                JOIN stock_move sm ON sml.move_id = sm.id
                LEFT JOIN stock_picking sp ON sm.picking_id = sp.id
                JOIN stock_location src ON sml.location_id = src.id
                JOIN stock_location dest ON sml.location_dest_id = dest.id
                WHERE sml.lot_id IS NOT NULL
                AND sm.state = 'done'
            )
        """)

