# Copyright 2024 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Mail Main Attachment",
    "summary": """This addon allows select main attachment in a record to set as default for other actions.""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/social",
    "depends": [
        "mail",
    ],
    "data": [],
    "demo": [],
    "assets": {
        "web.assets_backend": [
            "mail_main_attachment/static/src/components/*/*.js",
            "mail_main_attachment/static/src/components/*/*.scss",
            "mail_main_attachment/static/src/components/*/*.xml",
        ],
    },
}
