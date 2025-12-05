from odoo import api, fields, models, _
from odoo.tools import html_escape


class CoverLetterDocument(models.Model):
    """A workspace that keeps brainstorming ideas and the final letter together."""

    _name = "cover.letter.document"
    _description = "Cover Letter Draft"
    _order = "name, id"

    name = fields.Char(
        string="Title",
        required=True,
        default=lambda self: _("New Cover Letter"),
        help="Give this draft a short, recognizable title (e.g. Role + Company).",
    )
    target_company = fields.Char(string="Company")
    target_role = fields.Char(string="Role")
    final_letter_body = fields.Html(
        string="Letter",
        help="Write or paste the final version of your cover letter here.",
    )
    brainstorming_note_ids = fields.One2many(
        "cover.letter.brainstorm.note",
        "document_id",
        string="Brainstorming Notes",
    )
    note_count = fields.Integer(
        compute="_compute_note_count",
        store=True,
        string="Brainstorm Notes",
    )
    sticky_note_html_preview = fields.Html(
        string="Sticky Note Preview",
        compute="_compute_sticky_note_html",
        sanitize=False,
    )

    @api.depends("brainstorming_note_ids")
    def _compute_note_count(self):
        for record in self:
            record.note_count = len(record.brainstorming_note_ids)

    @api.depends(
        "brainstorming_note_ids",
        "brainstorming_note_ids.name",
        "brainstorming_note_ids.summary",
        "brainstorming_note_ids.color",
    )
    def _compute_sticky_note_html(self):
        for record in self:
            notes = record.brainstorming_note_ids.sorted(
                key=lambda n: (n.sequence, n.id)
            )

            if not notes:
                record.sticky_note_html_preview = f"""
                    <div class="o_cover_letter_sticky_wrapper" style="
                        margin-bottom: 16px;
                        padding: 18px 22px;
                        border: 1px dashed #D0D5DD;
                        border-radius: 16px;
                        color: #475467;
                        background: #F8FAFC;
                        font-size: 15px;
                        text-align: center;
                    ">
                        {_('No sticky notes yet. Tap “New Sticky” to add your first idea.')}
                    </div>
                """
                continue

            def build_card(note, idx):
                safe_title = html_escape(note.name or _("Untitled idea"))
                safe_body = html_escape(note.summary or "").replace("\n", "<br/>")
                color = note.color or "#fef3c7"
                font_color = "#0f172a"
                rotation = -2.5 if idx % 2 == 0 else 2.2
                tape_rotation = rotation * -0.4
                return f"""
                    <div class="o_cover_letter_sticky_card" style="
                        position: relative;
                        flex: 1 1 260px;
                        max-width: 360px;
                        background: {color};
                        color: {font_color};
                        border-radius: 22px;
                        padding: 26px 28px 24px;
                        box-shadow: 0 25px 45px rgba(16, 24, 40, 0.25);
                        transform: rotate({rotation}deg);
                        transition: transform 0.1s ease;
                        min-height: 170px;
                        overflow: hidden;
                    ">
                        <div style="
                            position:absolute;
                            top:-14px;
                            left:50%;
                            width:78px;
                            height:22px;
                            background:rgba(255,255,255,0.85);
                            box-shadow:0 8px 22px rgba(15,23,42,0.15);
                            border-radius:6px;
                            transform: translateX(-50%) rotate({tape_rotation}deg);
                        "></div>
                        <button class="o_cover_letter_delete_btn" style="
                            position:absolute;
                            top:12px;
                            right:12px;
                            border:none;
                            background:none;
                            font-size:15px;
                            cursor:pointer;
                            color:#991b1b;
                            padding:4px;
                        " data-note-id="{note.id}" type="button" title="{_('Delete note')}" aria-label="{_('Delete note')}">
                            <i class="fa fa-times"></i>
                        </button>
                        <button class="o_cover_letter_edit_btn" style="
                            position:absolute;
                            top:12px;
                            right:42px;
                            border:none;
                            background:none;
                            font-size:15px;
                            cursor:pointer;
                            color:{font_color};
                            padding:4px;
                        " data-note-id="{note.id}" type="button" title="{_('Edit note')}" aria-label="{_('Edit note')}">
                            <i class="fa fa-pencil"></i>
                        </button>
                        <div style="font-size:22px; font-weight:600; margin-bottom:12px;">
                            {safe_title}
                        </div>
                        <div style="font-size:15px; line-height:1.6;">
                            {safe_body}
                        </div>
                    </div>
                """

            cards = [build_card(note, idx) for idx, note in enumerate(notes)]
            record.sticky_note_html_preview = f"""
                <div class="o_cover_letter_sticky_wrapper" style="
                    display:flex;
                    flex-wrap:wrap;
                    gap:24px;
                    align-items:stretch;
                    margin-bottom:24px;
                ">
                    {''.join(cards)}
                </div>
            """

    def action_open_sticky_note_wizard(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("New Sticky Note"),
            "res_model": "cover.letter.sticky.note.wizard",
            "view_mode": "form",
            "views": [(False, "form")],
            "target": "new",
            "context": {
                "default_document_id": self.id,
                "default_name": _("Untitled Idea"),
                "default_color": "#fef3c7",
            },
        }
