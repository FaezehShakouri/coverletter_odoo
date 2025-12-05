{
    'name': "Cover Letter Workspace",
    'summary': "Brainstorm ideas and craft the final cover letter in one place.",
    'description': """
        Bring structure to cover letter writing. Capture ideas on sticky-note style
        cards, reorganize them freely, and turn the best points into a polished letter
        without leaving Odoo.
    """,
    'author': "thefazi",
    'website': "https://www.yourcompany.com",
    'license': 'LGPL-3',
    'category': 'Productivity',
    'version': '0.1',
    'depends': ['base', 'web'],
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'wizard/cover_letter_sticky_note_wizard_views.xml',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'cover_letter/static/src/js/sticky_note_edit.js',
        ],
    },
}

