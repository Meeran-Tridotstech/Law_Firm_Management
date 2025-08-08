import frappe

def get_context(context):
    # room_id from URL: /chat-room/<room_id>
    room_id = frappe.form_dict.get("room_id")
    if not room_id:
        frappe.throw("Room ID missing in URL")

    # Load chat room doc (to check participants and meta)
    room = frappe.get_doc("Chat Room", room_id)

    # Optional: restrict access to advocate or client or system managers
    user = frappe.session.user
    allowed = (user == room.advocate) or (user == room.client) or frappe.has_permission("Chat Room", "read", user="Administrator")
    # if you want strict:
    # if user not in [room.advocate, room.client] and not frappe.has_role(user, "System Manager"):
    #     frappe.throw("Not allowed to access this chat")

    # Load past messages
    messages = frappe.get_all("Chat Message",
                              filters={"room": room_id},
                              fields=["sender", "message", "sent_at"],
                              order_by="creation asc")

    context.room_id = room_id
    context.room = room
    context.messages = messages
    return context
