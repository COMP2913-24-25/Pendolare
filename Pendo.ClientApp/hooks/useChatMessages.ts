import { useState, useEffect, useRef } from 'react';
import { messageService, ChatMessage, createConversation } from '@/services/messageService';
import { approveBookingAmmendment, getBookings } from '@/services/bookingService';

export const useChatMessages = (
  chatId: string | null,
  userId: string,
  initialMessage?: string,
  isDriverMode = false
) => {
  const [chat, setChat] = useState<any>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(true);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const [hasSetChatVars, setHasSetChatVars] = useState(false);
  const lastSentMessageRef = useRef<string>("");
  const [autoCreateChat, setAutoCreateChat] = useState(
    !!initialMessage && initialMessage !== ''
  );

  useEffect(() => {
    // Only set up connection once chatId and userId are available
    if (!chatId || !userId) return;

    // Set up message service event handlers
    messageService.on("connected", handleConnected);
    messageService.on("disconnected", handleDisconnected);
    messageService.on("error", handleError);
    messageService.on("historyLoaded", handleHistoryLoaded);
    messageService.on("message", handleMessage);

    // Clean up on unmount
    return () => {
      messageService.disconnect();
      messageService.off("connected");
      messageService.off("disconnected");
      messageService.off("error");
      messageService.off("message");
      messageService.off("historyLoaded");
    };
  }, [chatId, userId]);

  useEffect(() => {
    // Update message service with new chat info when it changes
    if (chat && messageService && userId) {
      messageService.setConversationId(chat.id);
      
      if (hasSetChatVars) {
        messageService.setUserId(userId);
        messageService.setConversationId(chat.ConversationId);
      }
      
      // Connect to the chat if not already connected
      if (!isConnected && !isConnecting) {
        messageService.connect();
      }
    }
  }, [chat?.id, chat?.ConversationId, userId, hasSetChatVars]);

  const handleConnected = () => {
    setIsConnected(true);
    setIsConnecting(false);
    setConnectionError(null);

    // Once connected, request message history
    if (chat) {
      setIsLoadingHistory(true);
      messageService.requestMessageHistory();
    }
  };

  const handleDisconnected = (reason?: string) => {
    setIsConnected(false);
    setIsLoadingHistory(false);
    if (reason) {
      setConnectionError(`Disconnected: ${reason}`);
    }
  };

  const handleError = (error: string) => {
    setConnectionError(`Connection error: ${error}`);
    setIsConnecting(false);
  };

  const handleHistoryLoaded = (historyMessages: ChatMessage[]) => {
    console.log("History loaded:", historyMessages.length, "messages");
    setIsLoadingHistory(false);

    // Merge new messages with existing messages
    setMessages((prevMessages: ChatMessage[]) => {
      // Create a set of existing message IDs for comparison
      const existingIds = new Set(prevMessages.map((m) => m.id));

      // Filter out messages that are not already in the list
      const newMessages = historyMessages.filter(
        (m) => m.id && !existingIds.has(m.id)
      );

      // Sort messages by timestamp
      return [...prevMessages, ...newMessages].sort(
        (a, b) =>
          new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
      );
    });
  };

  const handleMessage = (message: ChatMessage) => {
    // Handle user joining conversation event
    if (message.type === "conversation_joined") {
      console.log("Initial message:", initialMessage);

      if (initialMessage) {
        sendMessage(initialMessage);
      }
      return;
    }

    if (message.type === "user_message_sent") {
      if (!message.content && lastSentMessageRef.current) {
        message.content = lastSentMessageRef.current;
      }
      // Add user message to list
      setMessages((prev) => [...prev, { ...message, sender: "user", status: "sent" }]);
      lastSentMessageRef.current = "";
      return;
    }
    
    // Special handling for booking amendment messages
    if (message.type === "booking_amendment" || message.amendmentId) {
      console.log("Received booking amendment message:", message);
      // Ensure it has the right type
      message.type = "booking_amendment";
      
      setMessages((prev) => [
        ...prev,
        {
          ...message,
          id: message.id || generateUniqueId(),
          sender: message.from === userId ? "user" : "other",
        }
      ]);
      return;
    }
    
    // Handle incoming chat messages
    if (message.type === "chat" && message.content) {
      // Determine sender based on user ID
      console.log("Chat user id: ", chat?.UserId);
      console.log("Chat message from: ", message.from);
      const sender = message.from === chat?.UserId ? "user" : "other";
      
      // Update message status based on sender
      setMessages((prev: ChatMessage[]) => {
        if (sender === "user") {
          const idx = prev.findIndex((m) => 
            m.status === "sending" && m.content === message.content
          );
          if (idx !== -1) {
            const newMessages = [...prev];
            newMessages[idx] = { ...newMessages[idx], ...message, status: "sent" };
            return newMessages;
          }
        }

        // Add new message
        return [
          ...prev,
          {
            ...message,
            id: message.id,
            sender,
            status: sender === "user" ? "delivered" : undefined,
          },
        ];
      });
    } else if (message.type === "welcome" && message.content) {
      setMessages((prev: ChatMessage[]) => [
        ...prev,
        { ...message, id: generateUniqueId(), sender: "system" },
      ]);
    }
  };

  // Helper function to generate unique message IDs
  const generateUniqueId = () => {
    return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  const sendMessage = (text: string) => {
    if (!text.trim() || !isConnected) return false;

    // Store last sent message before sending
    lastSentMessageRef.current = text.trim();

    return messageService.sendMessage(text.trim());
  };

  const updateAmendmentStatus = (amendmentId: string, content: any, isDriverApproval: boolean) => {
    // Update the amendment in the local messages state
    setMessages(prevMessages => {
      return prevMessages.map(msg => {
        if (msg.amendmentId === amendmentId && msg.content) {
          // Clone the content object to avoid modifying the original
          const updatedContent = typeof msg.content === 'string' 
            ? JSON.parse(msg.content) 
            : { ...msg.content };
          
          // Update the appropriate approval field
          if (isDriverApproval) {
            updatedContent.DriverApproval = true;
          } else {
            updatedContent.PassengerApproval = true;
          }
          
          console.log("Updated amendment content:", updatedContent);
          
          // Return message with updated content
          return {
            ...msg,
            content: JSON.stringify(updatedContent)
          };
        }
        return msg;
      });
    });
  };

  const handleAmendmentApproval = async (amendmentId: string) => {
    try {
      // Get the message with this amendment ID to determine if it's a cancellation
      const amendmentMessage = messages.find(msg => msg.amendmentId === amendmentId);
      let isCancellation = false;
      
      if (amendmentMessage && amendmentMessage.content) {
        try {
          // Try to parse the content to get the cancellation status
          const content = typeof amendmentMessage.content === 'string' 
            ? JSON.parse(amendmentMessage.content) 
            : amendmentMessage.content;
          
          isCancellation = content.CancellationRequest || false;
          
          
          // Make sure to get bookings with the driver view parameter matching our current view
          const bookingsResponse = await getBookings(isDriverMode);
          if (!bookingsResponse.success) {
            console.error("Failed to fetch bookings for amendment approval");
            return;
          }
          
          // Find the booking that matches this amendment
          const booking = bookingsResponse.bookings.find(b => 
            b.Booking.BookingId === content.BookingId
          );
          
          if (!booking) {
            console.log("Booking not found directly. Proceeding with amendment approval anyway.");
            
            // Try to approve the amendment using the isDriverMode flag
            const result = await approveBookingAmmendment(
              amendmentId, 
              isCancellation,
              isDriverMode
            );
            
            if (result.success) {
              console.log("Successfully approved amendment without finding booking");
              
              // Update the amendment status in memory
              updateAmendmentStatus(amendmentId, content, isDriverMode);
              
              // Send approval confirmation message
              const approvalMessage = {
                type: "amendment_approved",
                from: userId,
                conversation_id: chat.ConversationId,
                content: `Amendment ${amendmentId} approved`,
                amendmentId: amendmentId,
                timestamp: new Date().toISOString(),
              };
              
              messageService.sendMessage(JSON.stringify(approvalMessage));
            } else {
              console.error("Failed to approve booking amendment:", result.message);
            }
            return;
          }
          
          // Determine if current user is the driver or passenger
          const isDriver = booking.Journey.User.UserId === userId;
          const isPassenger = booking.Booking.User.UserId === userId;
          
          console.log("User roles:", { 
            currentUserId: userId, 
            isDriver, 
            isPassenger,
            driverId: booking.Journey.User.UserId,
            passengerId: booking.Booking.User.UserId
          });
          
          // If the current user already approved this amendment, don't re-approve
          if ((content.DriverApproval && isDriver) || (content.PassengerApproval && isPassenger)) {
            console.log("This amendment has already been approved by this user");
            return;
          }
          
          // Approve the amendment
          const result = await approveBookingAmmendment(
            amendmentId, 
            isCancellation,
            isDriverMode
          );
          
          if (result.success) {
            // Update the amendment status
            updateAmendmentStatus(amendmentId, content, isDriverMode);
            
            // Send approval confirmation message
            const approvalMessage = {
              type: "amendment_approved",
              from: userId,
              conversation_id: chat.ConversationId,
              content: `Amendment ${amendmentId} approved`,
              amendmentId: amendmentId,
              timestamp: new Date().toISOString(),
            };
            
            messageService.sendMessage(JSON.stringify(approvalMessage));
          } else {
            console.error("Failed to approve booking amendment:", result.message);
          }
        } catch (e) {
          console.log("Error parsing amendment content", e);
        }
      }
    } catch (error) {
      console.error("Error approving booking amendment:", error);
    }
  };

  const setChatData = (chatData: any) => {
    setChat(chatData);
    setHasSetChatVars(true);
  };

  return {
    chat,
    setChatData,
    messages,
    isConnected,
    isConnecting,
    isLoadingHistory,
    connectionError,
    sendMessage,
    handleAmendmentApproval,
    autoCreateChat,
    setAutoCreateChat
  };
};
