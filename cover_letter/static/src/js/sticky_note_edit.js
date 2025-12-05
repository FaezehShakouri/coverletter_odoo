/** @odoo-module **/

import { registry } from "@web/core/registry";

const stickyNoteEditService = {
    dependencies: ["action", "orm"],
    start(env) {
        const { action, orm } = env.services;

        const handleClick = async (event) => {
            const button = event.target.closest(".o_cover_letter_edit_btn");
            if (!button || button.dataset.actionLocked === "1") {
                return;
            }

            const noteId = parseInt(button.dataset.noteId, 10);
            if (!noteId) {
                return;
            }

            event.preventDefault();
            button.dataset.actionLocked = "1";
            button.classList.add("o_cover_letter_edit_btn_loading");

            try {
                const wizardAction = await orm.call(
                    "cover.letter.brainstorm.note",
                    "action_open_edit_wizard",
                    [[noteId]]
                );
                if (wizardAction) {
                    action.doAction(wizardAction);
                }
            } catch (error) {
                console.error("Unable to open sticky note wizard", error);
            } finally {
                delete button.dataset.actionLocked;
                button.classList.remove("o_cover_letter_edit_btn_loading");
            }
        };

        document.addEventListener("click", handleClick);

        return {
            stop() {
                document.removeEventListener("click", handleClick);
            },
        };
    },
};

registry.category("services").add(
    "cover_letter_sticky_note_service",
    stickyNoteEditService
);
