import { FontAwesome5 } from "@expo/vector-icons";
import { router, useGlobalSearchParams, useLocalSearchParams, useFocusEffect } from "expo-router";
import { useState, useEffect, useRef, useCallback } from "react";
import {
  View,
  TextInput,
  TouchableOpacity,
  ScrollView as RNScrollView,
  KeyboardAvoidingView,
  Platform,
  ActivityIndicator,
} from "react-native";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import { Text } from "@/components/common/ThemedText";
import { icons } from "@/constants";
import { useTheme } from "@/context/ThemeContext";
import { messageService, ChatMessage, getUserConversations, createConversation } from "@/services/messageService";
import { formatTimestamp } from "@/utils/formatTime";
import { getCurrentUserId } from "@/services/authService";
import BookingAmendmentModal from "@/components/Chat/BookingAmendmentModal";
import AmendmentRequestBubble from "@/components/Chat/AmendmentRequestBubble";
import { AddBookingAmmendmentRequest, addBookingAmmendment, approveBookingAmmendment, getBookings, getJourneys } from "@/services/bookingService";

/*
  Helper function to generate unique message IDs internally for categorisation
*/
const generateUniqueId = () => {
  return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

/*
  ChatDetail
  Screen for viewing and sending messages in a chat
*/
const ChatDetail = () => {
  const { id, name, initialMessage } = useLocalSearchParams();
  const [chat, setChat] = useState<any>(null);
  const [newMessage, setNewMessage] = useState(typeof initialMessage === "undefined" ? "" : initialMessage as string);
  const { isDarkMode } = useTheme();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(true);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);
  const [connectionError, setConnectionError] = useState<string | null>(null);
  const [hasSetChatVars, setHasSetChatVars] = useState(false);
  const [currentUserId, setCurrentUserId] = useState<string>("");
  const scrollViewRef = useRef<RNScrollView>(null);
  const inputRef = useRef<TextInput>(null);
  const lastSentMessageRef = useRef<string>("");
  const [showAmendmentModal, setShowAmendmentModal] = useState(false);
  const [selectedBookingId, setSelectedBookingId] = useState<string | null>(null);
  const [autoCreateChat, setAutoCreateChat] = useState(true);
  const previousIdRef = useRef<string | null>(null);
  const [isDriverMode, setIsDriverMode] = useState(false); // Default to passenger view until determined

  // Ensure we have a current user ID
  useEffect(() => {
    const getUserId = async () => {
      // Get user ID directly from auth service
      try {
        const userId = await getCurrentUserId();
        if (userId) {
          console.log("Retrieved user ID:", userId);
          setCurrentUserId(userId);
        }
      } catch (error) {
        console.error("Failed to get user ID:", error);
      }
    };

    getUserId();
  }, []);

  // Add focus effect to refresh data when screen comes into focus
  useFocusEffect(
    useCallback(() => {
      if (currentUserId) {
        fetchChatData();
      }
      return () => {
        // Cleanup if needed
      };
    }, [currentUserId])
  );

  // Add this effect to reset state when the ID parameter changes
  useEffect(() => {
    // Skip if this is the initial render with the same ID
    if (previousIdRef.current === id) return;
    
    console.log(`Chat ID changed from ${previousIdRef.current} to ${id}`);
    previousIdRef.current = id as string;
    
    // Reset state for new chat thread
    setChat(null);
    setMessages([]);
    setHasSetChatVars(false);
    setIsLoadingHistory(false);
    setConnectionError(null);
    
    // Disconnect from current chat
    messageService.disconnect();
    
    // Only auto-create when there's an initial message
    const shouldAutoCreate = !!initialMessage || 
                          (typeof initialMessage !== 'undefined' && initialMessage !== '');
    setAutoCreateChat(shouldAutoCreate);
    
    // If we have a user ID, fetch the new chat data
    if (currentUserId) {
      fetchChatData();
    }
  }, [id, currentUserId]);

  // Determine if the current user is a driver or passenger based on their bookings/journeys
  useEffect(() => {
    const determineUserRole = async () => {
      if (!currentUserId) return;
      
      try {
        // First check if the user has any journeys (rides they're driving)
        const driverBookings = await getBookings(true);
        
        // If user has driver bookings, they're a driver in at least some context
        const isDriver = driverBookings.bookings?.some(booking => 
          booking.Journey?.User?.UserId === currentUserId
        );
        
        // Set driver mode based on the results
        setIsDriverMode(isDriver);
        console.log(`User role determined: ${isDriver ? 'Driver' : 'Passenger'}`);
        
      } catch (error) {
        console.error("Error determining user role:", error);
        // Default to passenger view if there's an error
        setIsDriverMode(false);
      }
    };
    
    determineUserRole();
  }, [currentUserId]);

  /*
    Fetch chat details
  */
  const fetchChatData = async () => {
    try {
      // Only allow one fetch operation at a time
      if (chatFetchInProgress) return;
      
      // Set a flag to prevent multiple fetches
      let chatFetchInProgress = true;
      
      // Fetch conversation details from API
      console.log("Fetching conversation details for:", id);
      const response = await getUserConversations();
      
      // Normalise conversation data
      const normalisedConversations = response.conversations.map((conv: any) => ({
        ...conv,
        type: conv.Type ? conv.Type.toLowerCase() : conv.type,
        id: conv.id || conv.ConversationId,
        title: conv.Name,
        lastMessage: conv.lastMessage || "",
        timestamp: new Date(conv.CreateDate).getTime()
      }));
      
      // First check for conversations with the user ID we're looking for
      let selectedChat = normalisedConversations.find((c: any) => {
        // Check if conversation ID matches
        if (c.id === id || c.ConversationId === id) {
          console.log("Found exact conversation match by ID");
          return true;
        }
        
        // Check if the user is a participant
        if (c.participants && c.participants.includes(id.toString())) {
          console.log("Found conversation where target is a participant");
          return true;
        }
        
        // Check if conversation name contains the user name
        const targetName = name?.toString().toLowerCase() || id?.toString().toLowerCase();
        if (c.Name && c.Name.toLowerCase().includes(targetName)) {
          console.log("Found conversation match by name");
          return true;
        }
        
        // Check if user is mentioned in title
        if (c.title && c.title.toLowerCase().includes(targetName)) {
          console.log("Found conversation match by title");
          return true;
        }
        
        // No match
        return false;
      });
      
      if (selectedChat) {
        // Found existing chat - always use it
        console.log("Using existing chat:", selectedChat.id);
        setAutoCreateChat(false);
        setHasSetChatVars(true);
        setChat(selectedChat);
        chatFetchInProgress = false;
        return;
      }
      
      // No existing conversation was found
      console.log("No existing conversation found for:", id);
      
      // Only create a conversation if explicitly allowed to
      if (!autoCreateChat || typeof initialMessage === 'undefined' || initialMessage === '') {
        console.log("Auto-creation disabled or no initial message. Not creating a new chat.");
        chatFetchInProgress = false;
        return;
      }
      
      // Clear to create a new conversation
      console.log("Will attempt to create new conversation");
      const userName: any = typeof name === "undefined" ? id.toString() : name as string;
      
      try {
        // Create new conversation
        console.log(`Creating new conversation with ${userName}`);
        const response = await createConversation({
          ConversationType: "direct",
          name: `Chat with ${userName}`,
          participants: [id.toString()]
        });
        
        console.log("Conversation created successfully:", response);
        
        // Immediately disable auto-creation to prevent further attempts
        setAutoCreateChat(false);
        
        // Set chat details
        setHasSetChatVars(true);
        setChat({
          id: response.ConversationId,
          ConversationId: response.ConversationId,
          type: response.Type,
          title: response.Name,
          lastMessage: "",
          timestamp: new Date().getTime(),
          UserId: currentUserId
        });
      } catch (error) {
        console.error("Failed to create conversation:", error);
        
        // If conversation already exists but we didn't find it, try fetching again
        if (String(error).includes("Conversation already exists")) {
          console.log("Conversation exists but wasn't found initially, retrying fetch");
          setTimeout(() => fetchChatData(), 1000);
        }
      } finally {
        chatFetchInProgress = false;
      }
    } catch (error) {
      console.error("Error in fetchChatData:", error);
    }
  };

  // Fix issue with double fetch on mount
  useEffect(() => {
    // This effect is responsible for the initial data fetch
    // and should only run once the user ID is available
    if (currentUserId && !chat) {
      fetchChatData();
    }
  }, [currentUserId]);

  // Add this effect to reset auto-create when ID changes
  useEffect(() => {
    if (id !== previousIdRef.current) {
      console.log(`ID changed from ${previousIdRef.current} to ${id}, checking if auto-create needed`);
      // Only auto-create when there's an initial message
      const shouldAutoCreate = !!initialMessage && initialMessage !== '';
      setAutoCreateChat(shouldAutoCreate);
      previousIdRef.current = id as string;
    }
  }, [id, initialMessage]);

  useEffect(() => {
    console.log("Chat updated:", chat);
    // Only proceed if we have both a chat and a current user ID
    if (chat && messageService && currentUserId) {
      messageService.setConversationId(chat.id);
      console.log("Outputting chat" + JSON.stringify(chat));
      if (hasSetChatVars) {
        console.log("Setting user ID:", currentUserId);
        messageService.setUserId(currentUserId);

        console.log("Setting conversation ID:", chat.ConversationId);
        messageService.setConversationId(chat.ConversationId);
      }
    }

    // Clear messages when switching chats
    setMessages([]);
    setIsLoadingHistory(false);
  }, [chat?.id, chat?.ConversationId, currentUserId]);

  // Handle connection events
  useEffect(() => {
    // Handle connection events
    messageService.on("connected", () => {
      setIsConnected(true);
      setIsConnecting(false);
      setConnectionError(null);

      // Once connected, request message history
      if (chat) {
        setIsLoadingHistory(true);
        messageService.requestMessageHistory();
      }
    });

    // Handle disconnection events
    messageService.on("disconnected", (reason) => {
      setIsConnected(false);
      setIsLoadingHistory(false);
      if (reason) {
        setConnectionError(`Disconnected: ${reason}`);
      }
    });

    // Handle connection error events
    messageService.on("error", (error) => {
      setConnectionError(`Connection error: ${error}`);
      setIsConnecting(false);
    });

    // Handle message history loaded event
    messageService.on("historyLoaded", (historyMessages) => {
      console.log("History loaded:", historyMessages.length, "messages");
      setIsLoadingHistory(false);

      // Merge new messages with existing messages
      // Only add messages that are not already in the list
      setMessages((prevMessages: any[]) => {
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

      // Scroll to bottom after loading history
      // Derived from: https://reactnative.dev/docs/scrollview
      // Delay scroll to ensure messages are rendered
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: false });
      }, 100);
    });

    // Handle incoming messages
    messageService.on("message", (message) => {
      // Handle user message sent event
      if (message.type === "conversation_joined") {
        console.log("Initial message:", initialMessage);

        if (initialMessage) {
          setNewMessage(initialMessage as string);
          sendMessage();
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
            sender: message.from === currentUserId ? "user" : "other",
          }
        ]);
        
        // Scroll to bottom
        setTimeout(() => {
          scrollViewRef.current?.scrollToEnd({ animated: true });
        }, 100);
        return;
      }
      
      // Handle incoming chat messages
      if (message.type === "chat" && message.content) {
        // Determine sender based on user ID 
        console.log("Chat user id: ", chat?.UserId);
        console.log("Chat message from: ", message.from);
        const sender = message.from === chat?.UserId ? "user" : "other";
        
        // Update message status based on sender
        // If the message is from the user, update the status to "sent"
        setMessages((prev: any[]) => {
          if (sender === "user") {
            const idx = prev.findIndex((m: { status: string; content: string | undefined; }) => m.status === "sending" && m.content === message.content);
            if (idx !== -1) {
              const newMessages = [...prev];
              newMessages[idx] = { ...newMessages[idx], ...message, status: "sent" };
              return newMessages;
            }
          }

          // Add new message
          // If the message doesn't have an ID, generate one
          // IDs are generated server-side so this is a local categorisation technique
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
        setMessages((prev: any) => [
          ...prev,
          { ...message, id: generateUniqueId(), sender: "system" },
        ]);
      }
      // Scroll to bottom
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    });

    // Connect to WebSocket
    messageService.connect();

    // Clean up on unmount
    return () => {
      messageService.disconnect();
      messageService.off("connected");
      messageService.off("disconnected");
      messageService.off("error");
      messageService.off("message");
      messageService.off("historyLoaded");
    };
  }, [chat?.id]);

  /*
    Scroll to bottom when new messages are added
  */
  useEffect(() => {
    if (messages.length > 0 && !isLoadingHistory) {
      scrollViewRef.current?.scrollToEnd({ animated: false });
    }  
  }, [messages.length, isLoadingHistory]);

  /*
    Send a message to the chat
  */
  const sendMessage = () => {
    if (!newMessage.trim() || !isConnected) return;

    // Store last sent message before sending
    lastSentMessageRef.current = newMessage.trim();

    const success = messageService.sendMessage(newMessage.trim());
    if (success) {
      setNewMessage("");
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  };

  /*
    Send a booking amendment request
  */
  const sendBookingAmendmentRequest = async (amendment: AddBookingAmmendmentRequest) => {
    if (!isConnected) return;
  
    try {
      // First save the amendment to booking service
      const result = await addBookingAmmendment(amendment);
      
      // Check for success response - handle both structures
      if (result.success || result.Status === "Success") {
        // Get the amendment ID from either response format
        const amendmentId = result.id || result.BookingAmmendmentId || "";
        console.log("Amendment created with ID:", amendmentId);
        
        // Auto-approve the amendment for the creator
        // This saves the requester from having to explicitly approve their own request
        const approvalResult = await approveBookingAmmendment(
          amendmentId,
          amendment.CancellationRequest
        );
        
        if (!approvalResult.success) {
          console.error("Failed to auto-approve amendment:", approvalResult.message);
        } else {
          console.log("Amendment auto-approved for requester");
        }
        
        // Create a special message formatted specifically for booking amendments
        const amendmentMessage = {
          type: "booking_amendment",
          from: currentUserId,
          conversation_id: chat.ConversationId,
          content: JSON.stringify(amendment),
          amendmentId: amendmentId,
          timestamp: new Date().toISOString(),
          // Add requester approval flag to show it's already approved by sender
          requesterApproved: true
        };
        
        // Log the message before sending
        console.log("Sending amendment message:", amendmentMessage);
        
        // Send the amendment message directly
        const success = messageService.sendMessage(JSON.stringify(amendmentMessage));
        if (!success) {
          console.error("Failed to send amendment message");
        } else {
          console.log("Amendment message sent successfully");
        }
        
        // Reset state
        setShowAmendmentModal(false);
        setSelectedBookingId(null);
      } else {
        // Handle error
        console.error("Failed to create booking amendment:", result.message || "Unknown error");
      }
    } catch (error) {
      console.error("Error sending booking amendment:", error);
    }
  };

  /*
    Handle approval of booking amendment
  */
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
          
          // Log the booking ID we're looking for
          console.log("Looking for booking ID:", content.BookingId);
          
          // Make sure to get bookings with the driver view parameter matching our current view
          const bookingsResponse = await getBookings(isDriverMode);
          if (!bookingsResponse.success) {
            console.error("Failed to fetch bookings for amendment approval");
            return;
          }
          
          // Log all the booking IDs we received
          console.log("Received booking IDs:", bookingsResponse.bookings.map(b => b.Booking.BookingId));
          
          // Find the booking that matches this amendment
          const booking = bookingsResponse.bookings.find(b => 
            b.Booking.BookingId === content.BookingId
          );
          
          if (!booking) {
            console.log("Booking not found directly. Proceeding with amendment approval anyway.");
            // If we can't find the booking, we'll still try to approve the amendment
            // using the isDriverMode flag to determine if this is a driver approval
            const result = await approveBookingAmmendment(
              amendmentId, 
              isCancellation,
              isDriverMode // Use the driver mode flag directly
            );
            
            if (result.success) {
              console.log("Successfully approved amendment without finding booking");
              
              // Update the amendment status in memory to reflect the approval
              updateAmendmentStatus(amendmentId, content, isDriverMode);
              
              // Send approval confirmation message
              const approvalMessage = {
                type: "amendment_approved",
                from: currentUserId,
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
          const isDriver = booking.Journey.User.UserId === currentUserId;
          const isPassenger = booking.Booking.User.UserId === currentUserId;
          
          console.log("User roles:", { 
            currentUserId, 
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
          
          // Pass the appropriate approval type parameter
          const result = await approveBookingAmmendment(
            amendmentId, 
            isCancellation,
            isDriverMode // Use isDriverMode consistently instead of isDriver which may be incorrect
          );
          
          if (result.success) {
            // Update the amendment status in memory to reflect the approval
            updateAmendmentStatus(amendmentId, content, isDriverMode);
            
            // Send approval confirmation message
            const approvalMessage = {
              type: "amendment_approved",
              from: currentUserId,
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

  /**
   * Update the amendment status in the local messages state
   */
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

  /*
    MessageBubble
    Component for rendering chat messages
  */
  const MessageBubble = ({ message }: { message: ChatMessage }) => {
    console.log(message);
    const isUser = message.sender === "user";
    const isSystem = message.sender === "system";
    
    // Enhanced logging for all messages to help debug
    console.log(`Rendering message: type=${message.type}, amendmentId=${message.amendmentId}`, message);
    
    // Improved detection of booking amendment messages
    if (message.type === "booking_amendment" || message.amendmentId) {
      try {
        console.log("Processing amendment message:", message);
        
        // Parse the content if it's a stringified JSON
        let amendmentData = message.content;
        
        // Handle different message formats
        if (typeof amendmentData === 'string') {
          try {
            // First try direct parsing
            amendmentData = JSON.parse(amendmentData);
          } catch (e) {
            console.error("Failed to parse amendment data:", e);
            return (
              <View className="flex-row justify-center mb-4">
                <View className={`rounded-2xl px-4 py-2 max-w-[90%] ${isDarkMode ? "bg-red-800" : "bg-red-100"}`}>
                  <Text className={`text-center ${isDarkMode ? "text-white" : "text-red-600"}`}>
                    Booking amendment request (Unable to display details)
                  </Text>
                  <Text className={`text-center text-xs ${isDarkMode ? "text-white" : "text-red-600"}`}>
                    Raw content: {typeof amendmentData === 'string' ? amendmentData.substring(0, 50) : 'Non-string content'}
                  </Text>
                </View>
              </View>
            );
          }
        }
        
        console.log("Processed amendment data:", amendmentData);
        console.log("Current user is in driver mode:", isDriverMode);
        
        // Render amendment request bubble with the parsed data
        return (
          <AmendmentRequestBubble 
            amendment={amendmentData}
            amendmentId={message.amendmentId || ''}
            isFromCurrentUser={isUser}
            timestamp={message.timestamp}
            onApprove={handleAmendmentApproval}
            isDriverView={isDriverMode} // Explicitly set driver view mode here
          />
        );
      } catch (error) {
        console.error("Error rendering amendment message:", error);
        // Return a fallback UI for errors
        return (
          <View className="flex-row justify-center mb-4">
            <View className={`rounded-2xl px-4 py-2 max-w-[90%] ${isDarkMode ? "bg-red-800" : "bg-red-100"}`}>
              <Text className={`text-center ${isDarkMode ? "text-white" : "text-red-600"}`}>
                Error displaying booking amendment
              </Text>
              <Text className={`text-center text-xs ${isDarkMode ? "text-white" : "text-red-600"}`}>
                Error: {error.message}
              </Text>
            </View>
          </View>
        );
      }
    }

    // Special styling for system messages
    if (isSystem) {
      return (
        <View className="flex-row justify-center mb-4">
          <View
            className={`rounded-2xl px-4 py-2 max-w-[90%] ${
              isDarkMode ? "bg-slate-800" : "bg-gray-100"
            }`}
          >
            <Text
              className={`text-center ${isDarkMode ? "text-blue-300" : "text-blue-600"}`}
            >
              {message.content}
            </Text>
            <Text
              className={`text-xs mt-1 text-center ${
                isDarkMode ? "text-gray-400" : "text-gray-500"
              }`}
            >
              {formatTimestamp(new Date(message.timestamp).getTime())}
            </Text>
          </View>
        </View>
      );
    }

    return (
      <View
        className={`flex-row mb-4 ${isUser ? "justify-end" : "justify-start"}`}
      >
        <View
          className={`rounded-2xl px-4 py-3 max-w-[80%] ${
            isUser ? "bg-blue-600" : isDarkMode ? "bg-slate-700" : "bg-gray-100"
          }`}
        >
          <Text className={isUser ? "text-white" : undefined}>
            {message.content}
          </Text>
          <View className="flex-row items-center justify-between mt-1">
            <Text
              className={`text-xs ${
                isUser
                  ? "text-blue-200"
                  : isDarkMode
                  ? "text-gray-400"
                  : "text-gray-500"
              }`}
            >
              {formatTimestamp(new Date(message.timestamp).getTime())}
            </Text>
          </View>
        </View>
      </View>
    );
  };

  /* 
    Note: Styling and class names are derived from Tailwind CSS docs
    https://tailwindcss.com/docs/
    Additional design elements have been generated using Figma -> React Native (Tailwind)
    https://www.figma.com/community/plugin/821138713091291738/figma-react-native
    https://www.figma.com/community/plugin/1283055580669946018/tailwind-react-code-generator-by-pagesloft
    KeyboardAvoidingView derived from: https://reactnative.dev/docs/keyboardavoidingview
  */
  return (
    <ThemedSafeAreaView
      className={isDarkMode ? "flex-1 bg-slate-900" : "flex-1 bg-white"}
    >
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        keyboardVerticalOffset={80}
        className="flex-1"
      >
        { !chat ? (
          <View className="flex-1 items-center justify-center">
            <Text>Loading...</Text>
          </View>
        ) : (
          <>
            {/* Header */}
            <View className={`flex-row items-center p-4 border-b ${isDarkMode ? "border-slate-700" : "border-gray-200"}`}>
              <TouchableOpacity onPress={() => router.back()} className="mr-4">
                <FontAwesome5 name={icons.backArrow} size={24} color={isDarkMode ? "#FFF" : "#000"} />
              </TouchableOpacity>
              <View className="flex-row items-center flex-1">
                <View className={`w-10 h-10 rounded-full items-center justify-center mr-3 ${isDarkMode ? "bg-slate-700" : "bg-gray-100"}`}>
                  <FontAwesome5 name={chat.type === "support" ? icons.chat : icons.person} size={20} color="#2563EB" />
                </View>
                <Text className="font-JakartaBold text-lg">{chat.title}</Text>
              </View>

              {/* Connection status indicator */}
              <View className="flex-row items-center">
                {isConnecting ? (
                  <ActivityIndicator size="small" color="#2563EB" />
                ) : isConnected ? (
                  <View className="w-3 h-3 rounded-full bg-green-500 mr-1"></View>
                ) : (
                  <View className="w-3 h-3 rounded-full bg-red-500 mr-1"></View>
                )}
              </View>
            </View>
      
            {connectionError && (
              <View className="bg-red-500 p-2">
                <Text className="text-white text-center">{connectionError}</Text>
              </View>
            )}
      
            <RNScrollView ref={scrollViewRef} className="flex-1 px-4" contentContainerStyle={{ paddingVertical: 20 }}>
              {/* History loading indicator */}
              {isLoadingHistory && (
                <View className="flex-row justify-center mb-4">
                  <ActivityIndicator size="small" color="#2563EB" />
                  <Text className="ml-2 text-gray-500">Loading message history...</Text>
                </View>
              )}
      
              {messages.filter(message => message.type !== "welcome" && message.content !== undefined).map((message: ChatMessage, index: any) => (
                <MessageBubble key={message.id || `msg-${index}-${message.timestamp}`} message={message} />
              ))}
            </RNScrollView>
      
            {/* Message Input */}
            <View className="p-4 border-t border-gray-200 flex-row items-center">
              {/* Plus button for booking amendment */}
              <TouchableOpacity
                className={`w-10 h-10 rounded-full items-center justify-center mr-2 ${
                  isDarkMode ? "bg-slate-700" : "bg-gray-100"
                  }`}
                  onPress={() => setShowAmendmentModal(true)}
                  >
                  <FontAwesome5 name="plus" size={18} color={isDarkMode ? "#FFF" : "#000"} />
                  </TouchableOpacity>
              
              <TextInput
                ref={inputRef}
                className={`flex-1 px-4 py-2 mr-2 rounded-full ${isDarkMode ? "bg-slate-700 text-white" : "bg-gray-100 text-black"}`}
                placeholder="Type a message..."
                placeholderTextColor={isDarkMode ? "#9CA3AF" : "#6B7280"}
                value={newMessage}
                onChangeText={setNewMessage}
                multiline
              />
              <TouchableOpacity
                className={`w-10 h-10 rounded-full items-center justify-center ${
                  !newMessage.trim() || !isConnected ? "bg-blue-300" : "bg-blue-600"
                }`}
                disabled={!newMessage.trim() || !isConnected}
                onPress={sendMessage}
              >
                <FontAwesome5 name="paper-plane" size={18} color="#FFF" />
              </TouchableOpacity>
            </View>
          </>
        )}
      </KeyboardAvoidingView>

      {/* Booking Amendment Modal */}
      <BookingAmendmentModal
        visible={showAmendmentModal}
        onClose={() => setShowAmendmentModal(false)}
        onSubmit={sendBookingAmendmentRequest}
      />
    </ThemedSafeAreaView>
  );
};

export default ChatDetail;
