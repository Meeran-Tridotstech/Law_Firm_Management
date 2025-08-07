# /your_app/www/chat_room.py
import frappe

def get_context(context):
    context.room_id = frappe.form_dict.room_id
    context.messages = frappe.get_all("Chat Message", filters={"room": context.room_id}, fields=["sender", "message", "creation"])
