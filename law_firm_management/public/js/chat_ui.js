// your_app/public/js/chat.js
frappe.realtime.on("chat_room_RM-01", function(data) {
    console.log("New message:", data);

    // Example: append to chat container
    const container = document.getElementById("chat-container");
    const msg = document.createElement("div");
    msg.innerHTML = `<b>${data.sender}</b>: ${data.message} <small>${data.sent_at}</small>`;
    container.appendChild(msg);

    // Optional: Scroll to bottom
    container.scrollTop = container.scrollHeight;
});
