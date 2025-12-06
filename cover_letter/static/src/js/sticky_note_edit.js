/** @odoo-module **/

import { registry } from "@web/core/registry";

const stickyNoteEditService = {
    dependencies: ["action", "orm"],
    start(env) {
        const { action, orm } = env.services;

        let draggedCard = null;
        let draggedOverCard = null;

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

        const handleDragStart = (event) => {
            const card = event.target.closest(".o_cover_letter_sticky_card");
            if (!card) return;

            draggedCard = card;
            card.style.opacity = "0.5";
            card.style.cursor = "grabbing";
            event.dataTransfer.effectAllowed = "move";
            event.dataTransfer.setData("text/plain", card.dataset.noteId);
        };

        const handleDragEnd = (event) => {
            const card = event.target.closest(".o_cover_letter_sticky_card");
            if (card) {
                card.style.opacity = "1";
                card.style.cursor = "grab";
            }
            draggedCard = null;
            draggedOverCard = null;

            // Remove all drag-over styling
            document.querySelectorAll(".o_cover_letter_sticky_card").forEach((c) => {
                c.style.outline = "";
                c.style.outlineOffset = "";
            });
        };

        const handleDragOver = (event) => {
            event.preventDefault();
            event.dataTransfer.dropEffect = "move";

            const card = event.target.closest(".o_cover_letter_sticky_card");
            if (!card || card === draggedCard) return;

            // Visual feedback for drop target
            if (draggedOverCard && draggedOverCard !== card) {
                draggedOverCard.style.outline = "";
                draggedOverCard.style.outlineOffset = "";
            }
            draggedOverCard = card;
            card.style.outline = "3px dashed #3b82f6";
            card.style.outlineOffset = "4px";
        };

        const handleDragLeave = (event) => {
            const card = event.target.closest(".o_cover_letter_sticky_card");
            if (card && card !== draggedCard) {
                card.style.outline = "";
                card.style.outlineOffset = "";
            }
        };

        const handleDrop = async (event) => {
            event.preventDefault();

            const targetCard = event.target.closest(".o_cover_letter_sticky_card");
            if (!targetCard || !draggedCard || targetCard === draggedCard) {
                return;
            }

            // Get the wrapper and all cards
            const wrapper = targetCard.closest(".o_cover_letter_sticky_wrapper");
            if (!wrapper) return;

            const cards = Array.from(wrapper.querySelectorAll(".o_cover_letter_sticky_card"));
            const draggedIdx = cards.indexOf(draggedCard);
            const targetIdx = cards.indexOf(targetCard);

            if (draggedIdx === -1 || targetIdx === -1) return;

            // Reorder cards in DOM for immediate visual feedback
            if (draggedIdx < targetIdx) {
                targetCard.after(draggedCard);
            } else {
                targetCard.before(draggedCard);
            }

            // Collect new order of note IDs
            const reorderedCards = Array.from(wrapper.querySelectorAll(".o_cover_letter_sticky_card"));
            const noteIds = reorderedCards.map((c) => parseInt(c.dataset.noteId, 10));

            // Clear styling
            targetCard.style.outline = "";
            targetCard.style.outlineOffset = "";

            // Persist to backend
            try {
                await orm.call(
                    "cover.letter.brainstorm.note",
                    "action_reorder_notes",
                    [noteIds]
                );
            } catch (error) {
                console.error("Failed to reorder sticky notes", error);
            }
        };

        document.addEventListener("click", handleClick);
        document.addEventListener("dragstart", handleDragStart);
        document.addEventListener("dragend", handleDragEnd);
        document.addEventListener("dragover", handleDragOver);
        document.addEventListener("dragleave", handleDragLeave);
        document.addEventListener("drop", handleDrop);

        return {
            stop() {
                document.removeEventListener("click", handleClick);
                document.removeEventListener("dragstart", handleDragStart);
                document.removeEventListener("dragend", handleDragEnd);
                document.removeEventListener("dragover", handleDragOver);
                document.removeEventListener("dragleave", handleDragLeave);
                document.removeEventListener("drop", handleDrop);
            },
        };
    },
};

registry.category("services").add(
    "cover_letter_sticky_note_service",
    stickyNoteEditService
);
