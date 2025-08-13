// Copyright (c) 2025, Meeran and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Client Consultation", {
// 	refresh(frm) {

// 	},
// });


frappe.ui.form.on("Client Consultation", {
    onload(frm) {
        // Hide status section by default on new form
        if (frm.is_new()) {
            frm.toggle_display("in_person_section", false);
            frm.toggle_display("phone_section", false);

        }
    },

    refresh(frm) {
        // Apply server-side decision if available
        if (frm.doc.__onload && !frm.doc.__onload.show_status_section) {
            frm.toggle_display("in_person_section", false);
            frm.toggle_display("phone_section", false);

        } else if (frm.doc.__onload && frm.doc.__onload.show_status_section) {
            frm.toggle_display("in_person_section", true);
            frm.toggle_display("phone_section", true);

        }
    },

    consultation_type(frm) {
        // Toggle based on selection
        if (frm.doc.consultation_type === "In-person") {
            frm.toggle_display("in_person_section", true);
            frm.toggle_display("phone_section", false);

        } else {
            frm.toggle_display("phone_section", true);
            frm.toggle_display("in_person_section", false);

        }
    }
});