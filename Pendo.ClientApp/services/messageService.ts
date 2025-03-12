// Full Message Service Client in TypeScript

import { MESSAGE_API_BASE_URL } from "@/constants";

const WS_URL = MESSAGE_API_BASE_URL;
const DEFAULT_USER_ID = "12345";
const DEFAULT_CONVERSATION_ID = "12345";

export interface ChatMessage {
  isEcho: any;
  id?: string;
  type: string;
  from?: string;
  conversation_id?: string;
  content?: string;
  message?: string;
  timestamp: string;
  sender?: string;
  status?: "sending" | "sent" | "delivered";
}

// Event handling for message service
// https://stackoverflow.com/questions/65819527/require-handling-of-event-in-typescript-interface
interface MessageServiceEvents {
  message: (message: ChatMessage) => void;
  connected: () => void;
  disconnected: (reason?: string) => void;
  error: (error: any) => void;
  historyLoaded: (messages: ChatMessage[]) => void;
}

class MessageService {
  private ws: WebSocket | null = null;
  private isConnected = false;
  private userId: string = DEFAULT_USER_ID;
  private conversationId: string = DEFAULT_CONVERSATION_ID;
  private listeners: Partial<MessageServiceEvents> = {};
  private historyRequested: boolean = false;

  constructor() {
    this.connect = this.connect.bind(this);
    this.disconnect = this.disconnect.bind(this);
    this.sendMessage = this.sendMessage.bind(this);
    this.requestMessageHistory = this.requestMessageHistory.bind(this);
  }

  // WS Connection handling
  // Utilising: https://github.com/websockets/ws documentation & examples
  connect() {
    if (this.ws) {
      this.disconnect();
    }

    try {
      console.log("Connecting to WebSocket:", WS_URL);
      this.ws = new WebSocket(WS_URL);

      this.ws.onopen = () => {
        console.log("WebSocket connection established");
        this.isConnected = true;

        // Send registration message to register client with userId
        const registration = {
          type: "register",
          register: true,
          user_id: this.userId,
        };
        this.ws!.send(JSON.stringify(registration));

        // Join the conversation once registered
        this.joinConversation();

        if (this.listeners.connected) {
          console.log("Connected listener invoked");
          this.listeners.connected();
        }

        // Reset history requested flag on new connection
        this.historyRequested = false;
      };

      this.ws.onmessage = (event) => {
        let dataStr = event.data;
        let isEcho = false;
        if (typeof dataStr === "string" && dataStr.includes("ECHO:")) {
          isEcho = true;
          dataStr = dataStr.substring(5).trim();
        }
        let message: ChatMessage | any;
        try {
          message = JSON.parse(dataStr);
          // Attach echo flag if detected
          if (isEcho) {
            message.isEcho = true;
          }

          // Handle history response
          if (
            message.type === "history_response" &&
            Array.isArray(message.messages)
          ) {
            console.log("Received message history:", message.messages);
            const normalisedMessages = message.messages.map((msg: any) => ({
              ...msg,
              sender: msg.from === this.userId ? "user" : "other",
              status: msg.from === this.userId ? "delivered" : undefined,
            }));
            if (this.listeners.historyLoaded) {
              this.listeners.historyLoaded(normalisedMessages);
            }
            return;
          }

          if (!message.id && message.message_id) {
            message.id = message.message_id;
          }
        } catch (error) {
          console.error("Error parsing JSON message, using fallback:", error);
          message = {
            type: "unknown",
            content: event.data,
            timestamp: new Date().toISOString(),
            sender: "system",
          };
        }
        console.log("Received message:", message);

        // Transform welcome messages for display consistency
        if (message.type === "welcome" && message.message) {
          const formattedMessage: ChatMessage = {
            type: message.type,
            content: message.message,
            timestamp: message.timestamp,
            sender: "system",
          };
          if (this.listeners.message) {
            this.listeners.message(formattedMessage);
          }
        } else {
          if (this.listeners.message) {
            this.listeners.message(message);
          }
        }
      };

      // Handle WebSocket errors
      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        if (this.listeners.error) {
          this.listeners.error(error);
        }
      };

      // Handle WebSocket close event
      this.ws.onclose = (event) => {
        console.log("WebSocket connection closed:", event.code, event.reason);
        this.isConnected = false;
        if (this.listeners.disconnected) {
          this.listeners.disconnected(event.reason);
        }
      };
    } catch (error) {
      console.error("Error connecting to WebSocket:", error);
      if (this.listeners.error) {
        this.listeners.error(error);
      }
    }
  }

  // Join the conversation
  private joinConversation() {
    if (!this.isConnected || !this.ws) {
      console.error("Cannot join conversation: WebSocket not connected");
      return false;
    }
    const message = {
      type: "join_conversation",
      user_id: this.userId,
      conversation_id: this.conversationId,
    };
    console.log("Joining conversation:", message);
    try {
      this.ws.send(JSON.stringify(message));
      console.log("Join conversation message sent");
      return true;
    } catch (error) {
      console.error("Error sending join message:", error);
      return false;
    }
  }

  requestMessageHistory(sinceTimestamp?: string): boolean {
    if (!this.isConnected || !this.ws) {
      console.error("Cannot request history: WebSocket not connected");
      return false;
    }
    if (this.historyRequested) {
      console.log("Message history already requested for this session");
      return true;
    }
    const historyRequest = {
      type: "history_request",
      user_id: this.userId,
      conversation_id: this.conversationId,
      since_timestamp: sinceTimestamp,
    };
    try {
      this.ws.send(JSON.stringify(historyRequest));
      console.log("Message history request sent");
      this.historyRequested = true;
      return true;
    } catch (error) {
      console.error("Error requesting message history:", error);
      return false;
    }
  }

  // Send a message to the conversation
  sendMessage(content: string): boolean {
    if (!this.isConnected || !this.ws) {
      console.error("Cannot send message: WebSocket not connected");
      return false;
    }

    const message = {
      type: "chat",
      from: this.userId,
      conversation_id: this.conversationId,
      content: content,
      timestamp: new Date().toISOString(),
    };

    // Send the message
    try {
      this.ws.send(JSON.stringify(message));
      console.log("Message sent:", content);
      return true;
    } catch (error) {
      console.error("Error sending message:", error);
      return false;
    }
  }

  // Add event listener
  // Derived from: https://stackoverflow.com/questions/65819527/require-handling-of-event-in-typescript-interface
  on<K extends keyof MessageServiceEvents>(
    event: K,
    callback: MessageServiceEvents[K],
  ) {
    this.listeners[event] = callback;
  }

  // Remove event listener
  off<K extends keyof MessageServiceEvents>(event: K) {
    delete this.listeners[event];
  }

  // Set the conversation ID for the current session
  setConversationId(id: string) {
    this.conversationId = id;
    this.historyRequested = false;
  }
  
  // Set the user ID for the current session
  setUserId(id: string) {
    this.userId = id;
  }

  // Disconnect from the WebSocket
  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.isConnected = false;
    }
  }

}

export const messageService = new MessageService();
