frappe.ready(function () {
    // 1. Get room_id from URL (last segment)
    let pathParts = window.location.pathname.split("/").filter(Boolean);
    let roomId = pathParts[pathParts.length - 1];

    if (!roomId) {
        console.error("Room ID not found in URL");
        return;
    }

    const container = document.getElementById("chat-container");
    const input = document.getElementById("chat-input");
    const sendBtn = document.getElementById("send-btn");

    // Helper: Append message to chat box
    function appendMessage(data) {
        if (!container) return;

        // Remove "No messages yet" placeholder
        const noMsg = document.getElementById("no-msg");
        if (noMsg) noMsg.remove();

        const row = document.createElement("div");
        row.className = "chat-row";
        row.style.padding = "6px 0";
        row.innerHTML = `
            <b>${frappe.utils.escape_html(data.sender)}</b>: 
            ${frappe.utils.escape_html(data.message)} 
            <small style="color:#666; margin-left:8px;">
                ${data.sent_at || ''}
            </small>
        `;
        container.appendChild(row);
        container.scrollTop = container.scrollHeight;
    }

    // 2. Listen for new messages via Realtime
    frappe.realtime.on("chat_room_" + roomId, function (data) {
        console.log("Realtime message received:", data);
        appendMessage(data);
    });

    // 3. Send message function
    function sendMessage() {
        const message = (input.value || "").trim();
        if (!message) return;

        frappe.call({
            method: "law_firm_management.api.send_message",
            args: {
                room_id: roomId,
                message: message
            },
            callback: function (r) {
                if (r && r.message && r.message.status === "ok") {
                    input.value = ""; // Clear input on success
                } else {
                    console.error("Send failed:", r);
                }
            },
            error: function (err) {
                console.error("Error sending message:", err);
            }
        });
    }

    // 4. Event Listeners
    if (sendBtn) {
        sendBtn.addEventListener("click", sendMessage);
    }
    if (input) {
        input.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});
