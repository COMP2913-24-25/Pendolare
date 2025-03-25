document.addEventListener('DOMContentLoaded', function() {
    const chatMessageInput = document.getElementById('chatMessage');
    const sendButton = document.getElementById('sendMessageBtn');
    const consoleElem = document.getElementById('console');
    
    const conversationId = chatMessageInput.getAttribute('data-conversation-id');
    if (!conversationId) {
        console.error("Missing conversation id attribute.");
        return;
    }
    const sender = chatMessageInput.getAttribute('data-sender') || "00000000-0000-0000-0000-000000000000";
    
    const wsUrl = "wss://pendo-message.clsolutions.dev/ws/";
    let socket = new WebSocket(wsUrl);
    let typingTimeout = null;

    function logToConsole(message, type) {
        if (type !== 'sent' && type !== 'received') return;
        const msgElem = document.createElement('div');
        msgElem.className = `message ${type}`;
        msgElem.textContent = message;
        consoleElem.appendChild(msgElem);
        consoleElem.scrollTop = consoleElem.scrollHeight;
    }

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

    socket.onopen = () => {
        logToConsole('Connected to WebSocket!', 'system');
        const registrationPayload = {
            type: "register",
            register: true,
            user_id: sender
        };
        socket.send(JSON.stringify(registrationPayload));
        logToConsole(`Sent registration for admin user: ${sender}`, 'sent');
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

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            if (data.type === 'chat') {
                logChatMessage(data, 'received');
            }
            if (data.type === 'chat' && data.message_id && data.from !== sender) {
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
            logToConsole(`Received: ${event.data}`, 'received');
        }
    };

    socket.onerror = (error) => {
        logToConsole('WebSocket error: ' + error.message, 'error');
    };

    socket.onclose = (event) => {
        const reason = event.reason ? ` (${event.reason})` : '';
        logToConsole(`Connection closed with code ${event.code}${reason}`, 'system');
    };

    sendButton.addEventListener('click', () => {
        const content = chatMessageInput.value.trim();
        if(!content) {
            logToConsole('Please enter a message', 'error');
            return;
        }
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

    chatMessageInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter' && !sendButton.disabled) {
            sendButton.click();
        }
    });

    chatMessageInput.addEventListener('input', () => {
        if(typingTimeout) clearTimeout(typingTimeout);
        const typingMsg = {
            type: 'typing_notification',
            from: sender,
            conversation_id: conversationId,
            is_typing: true,
            timestamp: new Date().toISOString()
        };
        socket.send(JSON.stringify(typingMsg));
        typingTimeout = setTimeout(() => {
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
