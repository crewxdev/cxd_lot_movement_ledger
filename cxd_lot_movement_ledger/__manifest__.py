{
    "name": "Lot Inventory Ledger",
    "version": "19.0.0.1",
    "summary": "Lot wise inventory cost and movement tracker",
    "description": """
        Shows actual purchased qty, remaining qty and cost per lot
        based on stock move lines.
        """,
    "author": "crewxdev",
    'images': ['images/banner.jpg'],
    "website": "https://crewxdev.com",
    'license': "OPL-1",
    "category": "Inventory",
    "depends": ["stock"],
    "data": [
        "security/ir.model.access.csv",
        "views/lot_ledger_summary_views.xml",
    ],
    "installable": True,
    "application": False,
}
