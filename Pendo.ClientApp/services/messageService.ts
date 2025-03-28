// Full Message Service Client in TypeScript

import { MESSAGE_API_BASE_URL } from "@/constants";
import { apiRequest } from "./apiClient";
import { MESSAGE_ENDPOINTS } from "@/constants";

const WS_URL = MESSAGE_API_BASE_URL;

export interface ChatMessage {
  id?: string;
  type: string;
  from?: string;
  conversation_id?: string;
  content?: string;
  message?: string;
  timestamp: string;
  sender?: string;
  status?: "sending" | "sent" | "delivered";
  amendmentId?: string;
}

interface CreateConversationRequest {
  ConversationType: string;
  name: string;
  participants: string[];
}

interface ConversationResponse {
  ConversationId: string;
  Type: string;
  CreateDate: string;
  UpdateDate: string;
  Name: string;
  UserId: string;
}

interface GetUserConversationsResponse {
  conversations: ConversationResponse[];
}

export async function createConversation(
  request: CreateConversationRequest,
): Promise<ConversationResponse> {
  console.log(request)
  return apiRequest<ConversationResponse>(MESSAGE_ENDPOINTS.CREATE_CONVERSATION, {
    method: "POST",
    body: JSON.stringify(request),
  });
}

export async function getUserConversations(): Promise<GetUserConversationsResponse> {
  return await apiRequest<GetUserConversationsResponse>(MESSAGE_ENDPOINTS.GET_USER_CONVERSATIONS, {
    method: "GET",
  });
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

// WebSocket ready states
enum ReadyState {
  CONNECTING = 0,
  OPEN = 1,
  CLOSING = 2,
  CLOSED = 3
}

/*
  Message Service
  WebSocket client for chat messages
*/
class MessageService {
  private ws: WebSocket | null = null;
  private isConnected = false;
  private userId: string = "";
  private conversationId: string = "";
  private listeners: Partial<MessageServiceEvents> = {};
  private historyRequested: boolean = false;
  private reconnectAttempts: number = 0;
  private maxReconnectAttempts: number = 5;
  private reconnectTimeoutId: NodeJS.Timeout | null = null;
  private messageQueue: string[] = []; // Queue for messages that couldn't be sent
  private isReconnecting: boolean = false;

  constructor() {
    this.connect = this.connect.bind(this);
    this.disconnect = this.disconnect.bind(this);
    this.sendMessage = this.sendMessage.bind(this);
    this.requestMessageHistory = this.requestMessageHistory.bind(this);
  }

  // WS Connection handling
  // Utilising: https://github.com/websockets/ws documentation & examples
  connect() {
    if (this.ws && this.ws.readyState === ReadyState.OPEN) {
      console.log("WebSocket already connected, reusing connection");
      return;
    }

    // If we're in the process of reconnecting, don't start another connection
    if (this.isReconnecting) {
      console.log("Already attempting to reconnect, skipping duplicate connect");
      return;
    }

    // Clear any existing reconnect timeout
    if (this.reconnectTimeoutId) {
      clearTimeout(this.reconnectTimeoutId);
      this.reconnectTimeoutId = null;
    }

    // Close any existing connection that might be in a bad state
    if (this.ws) {
      try {
        this.ws.onclose = null; // Remove listener to prevent reconnect loop
        this.ws.onerror = null; // Remove error handler
        this.ws.close();
        this.ws = null;
      } catch (error) {
        console.warn("Error while closing existing WebSocket", error);
      }
    }

    try {
      console.log("Connecting to WebSocket:", WS_URL);
      this.isReconnecting = true;
      this.ws = new WebSocket(WS_URL);

      this.ws.onopen = () => {
        console.log("Successfully connected");
        this.isConnected = true;
        this.isReconnecting = false;
        this.reconnectAttempts = 0; // Reset reconnect attempts on successful connection

        // Send registration message to register client with userId
        if (this.userId) {
          this.registerUser();
        }

        // Join the conversation once registered, if we have a conversation ID
        if (this.conversationId) {
          this.joinConversation();
        }

        if (this.listeners.connected) {
          console.log("Connected listener invoked");
          this.listeners.connected();
        }

        // Reset history requested flag on new connection
        this.historyRequested = false;

        // Process any queued messages
        this.processMessageQueue();
      };

      /*
        Handle incoming messages
        Parse JSON messages and handle them accordingly
      */
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
          if (isEcho) {
            message.isEcho = true;
          }

          // Special handling for booking amendments 
          if (message.type === "booking_amendment" || message.amendmentId) {
            console.log("Received booking amendment message:", message);
            
            // Ensure type is set correctly
            message.type = "booking_amendment";
            
            // Make sure amendmentId is preserved
            if (message.amendmentId && typeof message.content === 'string') {
              try {
                // Try to parse content if it's a string
                const parsedContent = JSON.parse(message.content);
                
                // If parsed content already has BookingId, use it directly
                if (parsedContent.BookingId) {
                  message.content = parsedContent;
                }
              } catch (e) {
                console.error("Error parsing amendment content:", e);
              }
            }
          }

          // Handle history response messages
          if (
            message.type === "history_response" &&
            Array.isArray(message.messages)
          ) {
            console.log(`Successfully loaded ${message.messages.length} messages from history`);
            const normalisedMessages = message.messages.map((msg: any) => {
              // Normalise API response fields to expected keys
              const content = msg.Content || msg.content;
              const timestamp = msg.CreateDate ? new Date(msg.CreateDate).toISOString() : (msg.timestamp || new Date().toISOString());
              const id = msg.MessageId || msg.id;
              const senderId = msg.SenderId || msg.from;
              return {
                ...msg,
                content,
                timestamp,
                id,
                sender: senderId === this.userId ? "user" : "other",
                status: senderId === this.userId ? "delivered" : undefined,
              };
            });
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
          // Try to extract partial JSON if it's truncated
          try {
            // For truncated messages, try to fix common issues
            if (typeof dataStr === 'string' && dataStr.includes('{') && !dataStr.includes('}')) {
              dataStr += '}'; // Add missing closing brace
            }
            message = JSON.parse(dataStr);
          } catch (e) {
            // If still fails, use a fallback message
            message = {
              type: "unknown",
              content: event.data,
              timestamp: new Date().toISOString(),
              sender: "system",
            };
          }
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
        // Don't set isConnected to false here, let onclose handle the state change
      };

      // Handle WebSocket close event
      this.ws.onclose = (event) => {
        console.log("WebSocket connection closed:", event.code, event.reason);
        this.isConnected = false;
        this.isReconnecting = false;
        
        if (this.listeners.disconnected) {
          this.listeners.disconnected(event.reason);
        }
        
        // Attempt to reconnect if not manually disconnected (code 1000)
        if (event.code !== 1000 && this.reconnectAttempts < this.maxReconnectAttempts) {
          this.attemptReconnect();
        }
      };
    } catch (error) {
      console.error("Error connecting to WebSocket:", error);
      this.isReconnecting = false;
      if (this.listeners.error) {
        this.listeners.error(error);
      }
      
      // Attempt to reconnect after an error
      this.attemptReconnect();
    }
  }

  /**
   * Attempt to reconnect with exponential backoff
   */
  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log("Max reconnect attempts reached, giving up");
      return;
    }
    
    // Calculate delay with exponential backoff (1s, 2s, 4s, 8s, 16s)
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    this.reconnectAttempts++;
    
    console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts}) in ${delay}ms`);
    
    this.reconnectTimeoutId = setTimeout(() => {
      this.connect();
    }, delay);
  }

  /**
   * Register the user with the WebSocket service
   */
  private registerUser() {
    if (!this.isWebSocketReady()) {
      console.error("Cannot register user: WebSocket not ready");
      this.queueMessage(JSON.stringify({
        type: "register",
        register: true,
        user_id: this.userId,
      }));
      return false;
    }

    try {
      const registration = {
        type: "register",
        register: true,
        user_id: this.userId,
      };
      this.ws!.send(JSON.stringify(registration));
      return true;
    } catch (error) {
      console.error("Error registering user:", error);
      return false;
    }
  }

  /*
    Join Conversation
    Send a message to join the current conversation
  */
  private joinConversation() {
    if (!this.isWebSocketReady()) {
      console.error("Cannot join conversation: WebSocket not ready");
      // Queue the join message for when connection is ready
      this.queueMessage(JSON.stringify({
        type: "join_conversation",
        user_id: this.userId,
        conversation_id: this.conversationId,
      }));
      return false;
    }

    const message = {
      type: "join_conversation",
      user_id: this.userId,
      conversation_id: this.conversationId,
    };
    console.log("Joining conversation:", message);
    try {
      this.ws!.send(JSON.stringify(message));
      console.log("Join conversation message sent");
      return true;
    } catch (error) {
      console.error("Error sending join message:", error);
      // Queue the message for retry
      this.queueMessage(JSON.stringify(message));
      return false;
    }
  }

  /*
    Request Message History
    Request message history for the current conversation
  */
  requestMessageHistory(sinceTimestamp?: string): boolean {
    if (!this.isWebSocketReady()) {
      console.error("Cannot request history: WebSocket not ready");
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
      this.ws!.send(JSON.stringify(historyRequest));
      console.log("Message history request sent");
      this.historyRequested = true;
      return true;
    } catch (error) {
      console.error("Error requesting message history:", error);
      // Queue the history request
      this.queueMessage(JSON.stringify(historyRequest));
      return false;
    }
  }

  /**
   * Check if the WebSocket is ready to send messages
   */
  private isWebSocketReady(): boolean {
    return !!this.ws && this.ws.readyState === ReadyState.OPEN;
  }

  /**
   * Queue a message to be sent when the connection is ready
   */
  private queueMessage(message: string) {
    console.log("Queuing message for later:", message.substring(0, 50) + "...");
    this.messageQueue.push(message);
    
    // Limit queue size to prevent memory issues
    if (this.messageQueue.length > 50) {
      this.messageQueue.shift(); // Remove oldest message
    }
  }

  /**
   * Process any queued messages
   */
  private processMessageQueue() {
    if (!this.isWebSocketReady() || this.messageQueue.length === 0) {
      return;
    }
    
    console.log(`Processing ${this.messageQueue.length} queued messages`);
    
    // Create a copy of the queue and clear it
    const queueCopy = [...this.messageQueue];
    this.messageQueue = [];
    
    // Send all queued messages
    for (const message of queueCopy) {
      try {
        this.ws!.send(message);
      } catch (error) {
        console.error("Error sending queued message:", error);
        // Re-queue the message
        this.queueMessage(message);
      }
    }
  }

  /*
    Send Message
    Send a chat message to the current conversation
  */
  sendMessage(content: string): boolean {
    if (!this.isWebSocketReady()) {
      console.error("Cannot send message: WebSocket not ready");
      // Auto-reconnect if needed
      if (!this.isReconnecting) {
        this.connect();
      }
      // Queue the message for later
      this.queueMessage(content);
      return false;
    }

    // Check if this is a booking amendment message
    let message = null;
    try {
      const parsedContent = JSON.parse(content);
      
      // If this is a booking amendment, use the original structure
      if (parsedContent.type === "booking_amendment") {
        message = parsedContent;
      } else {
        // Regular message
        message = {
          type: "chat",
          from: this.userId,
          conversation_id: this.conversationId,
          content: content,
          timestamp: new Date().toISOString()
        };
      }
    } catch (e) {
      // Not JSON, treat as regular chat message
      message = {
        type: "chat",
        from: this.userId,
        conversation_id: this.conversationId,
        content: content,
        timestamp: new Date().toISOString()
      };
    }

    // Send the message
    try {
      const messageStr = JSON.stringify(message);
      console.log("Sending message:", messageStr);
      this.ws!.send(messageStr);
      return true;
    } catch (error) {
      console.error("Error sending message:", error);
      // Queue the message for retry
      if (typeof message === 'object') {
        this.queueMessage(JSON.stringify(message));
      } else {
        this.queueMessage(content);
      }
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
    if (this.conversationId !== id) {
      this.conversationId = id;
      this.historyRequested = false;
      
      // Join conversation if already connected
      if (this.isConnected && this.userId) {
        this.joinConversation();
      }
    }
  }
  
  // Set the user ID for the current session
  setUserId(id: string) {
    if (this.userId !== id) {
      this.userId = id;
      
      // Register user if already connected
      if (this.isConnected) {
        this.registerUser();
        
        // Join conversation if we have one
        if (this.conversationId) {
          this.joinConversation();
        }
      }
    }
  }

  // Disconnect from the WebSocket
  disconnect() {
    // Clear reconnect timeout if any
    if (this.reconnectTimeoutId) {
      clearTimeout(this.reconnectTimeoutId);
      this.reconnectTimeoutId = null;
    }
    
    this.isReconnecting = false;
    this.reconnectAttempts = 0;
    
    if (this.ws) {
      try {
        // Use a proper close code for normal closure
        this.ws.close(1000, "User initiated disconnect");
      } catch (error) {
        console.error("Error during disconnect:", error);
      }
      this.ws = null;
      this.isConnected = false;
    }
  }
}

export const messageService = new MessageService();
