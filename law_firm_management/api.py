import frappe
from frappe.utils import now

@frappe.whitelist()
def send_message(room_id, message):
    """
    Save message to Chat Message and publish realtime event.
    room_id must be the name (ID) of Chat Room doc, eg "CHAT-0001"
    """
    user = frappe.session.user or "Guest"

    # Basic validation
    if not room_id or not message:
        frappe.throw("Room and message are required")

    # Insert Chat Message
    doc = frappe.get_doc({
        "doctype": "Chat Message",
        "room": room_id,
        "sender": user,
        "message": message,
        "sent_at": now()
    }).insert(ignore_permissions=True)

    # Publish realtime event
    try:
        frappe.publish_realtime(f"chat_room_{room_id}", {
            "sender": user,
            "message": message,
            "sent_at": doc.sent_at
        })
    except Exception as e:
        frappe.log_error(f"Realtime publish failed: {e}", "chat.publish_realtime")

    return {"status": "ok", "message": "sent"}
