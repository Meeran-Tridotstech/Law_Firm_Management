import frappe
from frappe.utils import now

@frappe.whitelist()
def send_message(room, message):
    user = frappe.session.user

    doc = frappe.new_doc("Chat Message")
    doc.room = room
    doc.sender = user
    doc.message = message
    doc.sent_at = now()
    doc.insert(ignore_permissions=True)

    frappe.publish_realtime(f"chat_room_{room}", {
        'sender': user,
        'message': message,
        'sent_at': doc.sent_at
    })

    return "sent"