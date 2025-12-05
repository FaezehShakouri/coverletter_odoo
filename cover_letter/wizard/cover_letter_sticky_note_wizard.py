from odoo import api, fields, models, _


class CoverLetterStickyNoteWizard(models.TransientModel):
    _name = "cover.letter.sticky.note.wizard"
    _description = "Quick Sticky Note Wizard"

    document_id = fields.Many2one(
        "cover.letter.document",
        string="Cover Letter",
        required=True,
        readonly=True,
    )
    note_id = fields.Many2one(
        "cover.letter.brainstorm.note",
        string="Sticky Note",
        readonly=True,
    )
    name = fields.Char(
        string="Title",
        required=True,
        default=lambda self: _("Untitled Idea"),
    )
    summary = fields.Text(
        string="Note",
        help="Describe the idea, metric, or reminder you want to capture.",
    )
    color = fields.Selection(
        selection=[
            ("#fef3c7", "Warm Yellow"),
            ("#bfdbfe", "Soft Blue"),
            ("#fbcfe8", "Blush Pink"),
            ("#bbf7d0", "Mint Green"),
            ("#fecdd3", "Rose Mist"),
        ],
        default="#fef3c7",
        string="Color",
    )

    def action_create_sticky_note(self):
        self.ensure_one()
        vals = {
            "name": self.name,
            "summary": self.summary,
            "color": self.color,
            "document_id": self.document_id.id,
        }
        if self.note_id:
            self.note_id.write(vals)
        else:
            self.env["cover.letter.brainstorm.note"].create(vals)

        return {
            "type": "ir.actions.act_window",
            "name": _("Brainstorm Note"),
            "res_model": "cover.letter.document",
            "view_mode": "form",
            "res_id": self.document_id.id,
        }
