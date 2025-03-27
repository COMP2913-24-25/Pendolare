document.addEventListener('DOMContentLoaded', function() {
    const chatMessageInput = document.getElementById('chatMessage');
    const sendButton = document.getElementById('sendMessageBtn');
    const consoleElem = document.getElementById('console');
    
    // Retrieve conversation ID and sender information from DOM attributes.
    const conversationId = chatMessageInput.getAttribute('data-conversation-id');
    if (!conversationId) {
        console.error("Missing conversation id attribute.");
        return;
    }
    const sender = chatMessageInput.getAttribute('data-sender') || "00000000-0000-0000-0000-000000000000";
    
    // Establish WebSocket connection.
    const wsUrl = "wss://pendo-message.clsolutions.dev/ws/";
    let socket = new WebSocket(wsUrl);
    let typingTimeout = null;

    // logToConsole: Logs system, sent, and received messages to the console UI.
    function logToConsole(message, type) {
        if (type !== 'sent' && type !== 'received') return;
        const msgElem = document.createElement('div');
        msgElem.className = `message ${type}`;
        msgElem.textContent = message;
        consoleElem.appendChild(msgElem);
        consoleElem.scrollTop = consoleElem.scrollHeight;
    }

    // logChatMessage: Formats and displays chat messages with sender info and timestamps.
    function logChatMessage(msgObj, type) {
        const msgElem = document.createElement('div');
        msgElem.className = `message ${type}`;
        const sender = msgObj.from || "System";
        const content = msgObj.content || msgObj.message || '';
        const timestamp = msgObj.timestamp ? `<small>${msgObj.timestamp}</small>` : '';
        msgElem.innerHTML = `<strong>${sender}:</strong> ${content} ${timestamp}`;
        consoleElem.appendChild(msgElem);
        consoleElem.scrollTop = consoleElem.scrollHeight;
    }

    // Handle WebSocket connection opening.
    socket.onopen = () => {
        logToConsole('Connected to WebSocket!', 'system');
        // Send registration message.
        const registrationPayload = {
            type: "register",
            register: true,
            user_id: sender
        };
        socket.send(JSON.stringify(registrationPayload));
        logToConsole(`Sent registration for admin user: ${sender}`, 'system');
        setTimeout(() => {
            const joinPayload = {
                type: "join_conversation",
                user_id: sender,
                conversation_id: conversationId
            };
            socket.send(JSON.stringify(joinPayload));
            logChatMessage({from: sender, content: `Joined conversation: ${conversationId}`, timestamp: new Date().toISOString()}, 'sent');
        }, 500);
    };

    // Process incoming WebSocket messages.
    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.type === 'chat') {
                logChatMessage(data, 'received');
            }
            if (data.type === 'chat' && data.message_id && data.from !== sender) {
                // Send read receipt after a delay.
                const readReceipt = {
                    type: 'read_receipt',
                    from: sender,
                    conversation_id: conversationId,
                    message_id: data.message_id,
                    timestamp: new Date().toISOString()
                };
                setTimeout(() => {
                    socket.send(JSON.stringify(readReceipt));
                }, 1000);
            }
        } catch (e) {
            // Fallback logging for non-JSON messages.
            logToConsole(`Received: ${event.data}`, 'received');
        }
    };

    // Handle WebSocket errors.
    socket.onerror = (error) => {
        logToConsole('WebSocket error: ' + error.message, 'error');
    };

    // Handle WebSocket closure.
    socket.onclose = (event) => {
        const reason = event.reason ? ` (${event.reason})` : '';
        logToConsole(`Connection closed with code ${event.code}${reason}`, 'system');
    };

    // Listen for click events on the send message button.
    sendButton.addEventListener('click', () => {
        const content = chatMessageInput.value.trim();
        if(!content) {
            logToConsole('Please enter a message', 'error');
            return;
        }
        // Construct message payload.
        const messageId = `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        const message = {
            type: 'chat',
            from: sender,
            conversation_id: conversationId,
            content: content,
            message_id: messageId,
            timestamp: new Date().toISOString()
        };
        socket.send(JSON.stringify(message));
        logChatMessage(message, 'sent');
        chatMessageInput.value = '';
        if(typingTimeout) {
            clearTimeout(typingTimeout);
            // Notify that typing has stopped.
            const stoppedTypingMsg = {
                type: 'typing_notification',
                from: sender,
                conversation_id: conversationId,
                is_typing: false,
                timestamp: new Date().toISOString()
            };
            socket.send(JSON.stringify(stoppedTypingMsg));
        }
    });

    // Trigger send button click when pressing Enter.
    chatMessageInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter' && !sendButton.disabled) {
            sendButton.click();
        }
    });

    // Handle typing notifications.
    chatMessageInput.addEventListener('input', () => {
        if(typingTimeout) clearTimeout(typingTimeout);
        // Inform that the user is typing.
        const typingMsg = {
            type: 'typing_notification',
            from: sender,
            conversation_id: conversationId,
            is_typing: true,
            timestamp: new Date().toISOString()
        };
        socket.send(JSON.stringify(typingMsg));
        typingTimeout = setTimeout(() => {
            // Inform that the user stopped typing.
            const stoppedTypingMsg = {
                type: 'typing_notification',
                from: sender,
                conversation_id: conversationId,
                is_typing: false,
                timestamp: new Date().toISOString()
            };
            socket.send(JSON.stringify(stoppedTypingMsg));
        }, 2000);
    });

    logToConsole('WebSocket client initialized.', 'system');
});
