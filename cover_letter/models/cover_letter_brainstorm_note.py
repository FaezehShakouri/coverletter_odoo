from odoo import api, fields, models, _


class CoverLetterBrainstormNote(models.Model):
    """Represents a movable sticky-note style idea on the brainstorming board."""

    _name = "cover.letter.brainstorm.note"
    _description = "Brainstorming Note"
    _order = "sequence, id"

    name = fields.Char(
        string="Headline",
        required=True,
        default=lambda self: _("New Idea"),
        help="Give the note a short title so it is easy to scan on the board.",
    )
    summary = fields.Text(
        string="Details",
        help="Expand on the point: metrics, story beats, or reminders.",
    )
    document_id = fields.Many2one(
        "cover.letter.document",
        string="Cover Letter",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10, help="Controls ordering in list/kanban views.")
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
        help="Pick a color to visually separate ideas on the board.",
    )
    anchor_x = fields.Integer(
        string="Horizontal Position",
        help="Reserved for future drag-and-drop capabilities.",
    )
    anchor_y = fields.Integer(
        string="Vertical Position",
        help="Reserved for future drag-and-drop capabilities.",
    )

    def action_open_edit_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Edit Sticky Note"),
            "res_model": "cover.letter.sticky.note.wizard",
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "new",
            "context": {
                "default_document_id": self.document_id.id,
                "default_note_id": self.id,
                "default_name": self.name,
                "default_summary": self.summary,
                "default_color": self.color,
            },
        }

    @api.model
    def action_reorder_notes(self, note_ids):
        """Reorder notes based on the provided list of IDs.

        Args:
            note_ids: List of note IDs in the desired order.
        """
        for idx, note_id in enumerate(note_ids):
            note = self.browse(note_id)
            if note.exists():
                note.write({"sequence": idx * 10})
