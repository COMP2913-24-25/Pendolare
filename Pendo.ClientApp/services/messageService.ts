import { MESSAGE_API_BASE_URL } from "@/constants";

const WS_URL = MESSAGE_API_BASE_URL;

// For this demo, we're hardcoding these values
const DEFAULT_USER_ID = '12345';
const DEFAULT_CONVERSATION_ID = '12345';

export interface ChatMessage {
  id?: string;
  type: string;
  from?: string;
  conversation_id?: string;
  content?: string;
  message?: string;  // Added for welcome message format
  timestamp: string;
  sender?: string; // Used for UI display ("user" or other)
}

interface MessageServiceEvents {
  message: (message: ChatMessage) => void;
  connected: () => void;
  disconnected: (reason?: string) => void;
  error: (error: any) => void;
}

class MessageService {
  private ws: WebSocket | null = null;
  private isConnected = false;
  private userId: string = DEFAULT_USER_ID;
  private conversationId: string = DEFAULT_CONVERSATION_ID;
  private listeners: Partial<MessageServiceEvents> = {};

  constructor() {
    this.connect = this.connect.bind(this);
    this.disconnect = this.disconnect.bind(this);
    this.sendMessage = this.sendMessage.bind(this);
  }

  connect() {
    if (this.ws) {
      this.disconnect();
    }

    try {
        console.log('Connecting to WebSocket:', WS_URL);
      this.ws = new WebSocket(WS_URL);

      this.ws.onopen = () => {
        console.log('WebSocket connection established');
        this.isConnected = true;
        
        // Join the conversation once connected
        this.joinConversation();
        
        if (this.listeners.connected) {
          this.listeners.connected();
        }
      };

      this.ws.onmessage = (event) => {
        let dataStr = event.data;
        let isEcho = false;
        if (typeof dataStr === 'string' && dataStr.startsWith("ECHO:")) {
          isEcho = true;
          dataStr = dataStr.substring(5).trim();
        }
        let message: ChatMessage;
        try {
          message = JSON.parse(dataStr) as ChatMessage;
          // Attach echo flag if detected
          if (isEcho) {
            (message as any).isEcho = true;
          }
        } catch (error) {
          console.error('Error parsing JSON message, using fallback:', error);
          // Fallback: wrap the raw data in a message object
          message = {
            type: 'unknown',
            content: event.data,
            timestamp: new Date().toISOString(),
            sender: 'system'
          };
        }
        console.log('Received message:', message);
        
        // Transform welcome messages to match chat message format
        if (message.type === 'welcome' && message.message) {
          const formattedMessage: ChatMessage = {
            type: message.type,
            content: message.message,
            timestamp: message.timestamp,
            sender: 'system'
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

      this.ws.onerror = (error) => {
        console.error('WebSocket error:', error);
        if (this.listeners.error) {
          this.listeners.error(error);
        }
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket connection closed:', event.code, event.reason);
        this.isConnected = false;
        
        if (this.listeners.disconnected) {
          this.listeners.disconnected(event.reason);
        }
      };
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
      if (this.listeners.error) {
        this.listeners.error(error);
      }
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.isConnected = false;
    }
  }

  private joinConversation() {
    if (!this.isConnected || !this.ws) {
      console.error('Cannot join conversation: WebSocket not connected');
      return false;
    }

    const message = {
      type: 'join_conversation',
      user_id: this.userId,
      conversation_id: this.conversationId
    };

    console.log('Joining conversation:', message);

    try {
      this.ws.send(JSON.stringify(message));
      console.log('Join conversation message sent');
      return true;
    } catch (error) {
      console.error('Error sending join message:', error);
      return false;
    }
  }

  sendMessage(content: string): boolean {
    if (!this.isConnected || !this.ws) {
      console.error('Cannot send message: WebSocket not connected');
      return false;
    }

    const message = {
      type: 'chat',
      from: this.userId,
      conversation_id: this.conversationId,
      content: content,
      timestamp: new Date().toISOString()
    };

    try {
      this.ws.send(JSON.stringify(message));
      console.log('Message sent:', content);
      return true;
    } catch (error) {
      console.error('Error sending message:', error);
      return false;
    }
  }

  on<K extends keyof MessageServiceEvents>(
    event: K,
    callback: MessageServiceEvents[K]
  ) {
    this.listeners[event] = callback;
  }

  off<K extends keyof MessageServiceEvents>(event: K) {
    delete this.listeners[event];
  }
}

export const messageService = new MessageService();
