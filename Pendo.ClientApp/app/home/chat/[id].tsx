import { useGlobalSearchParams, useLocalSearchParams, useFocusEffect } from "expo-router";
import { useState, useEffect, useRef, useCallback } from "react";
import {
  View,
  ScrollView as RNScrollView,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import ThemedSafeAreaView from "@/components/common/ThemedSafeAreaView";
import { Text } from "@/components/common/ThemedText";
import { useTheme } from "@/context/ThemeContext";
import { getUserConversations, createConversation, messageService } from "@/services/messageService";
import { getCurrentUserId } from "@/services/authService";
import BookingAmendmentModal from "@/components/Chat/BookingAmendmentModal";
import { AddBookingAmmendmentRequest, addBookingAmmendment } from "@/services/bookingService";
import { useChatMessages } from "@/hooks/useChatMessages";
import { getBookings } from "@/services/bookingService";

// Import our components
import ChatHeader from "@/components/Chat/ChatHeader";
import ChatInput from "@/components/Chat/ChatInput";
import ChatMessages from "@/components/Chat/ChatMessages";

/*
  ChatDetail
  Screen for viewing and sending messages in a chat
*/
const ChatDetail = () => {
  const { id, name, initialMessage } = useLocalSearchParams();
  const [newMessage, setNewMessage] = useState(typeof initialMessage === "undefined" ? "" : initialMessage as string);
  const { isDarkMode } = useTheme();
  const [currentUserId, setCurrentUserId] = useState<string>("");
  const scrollViewRef = useRef<RNScrollView>(null);
  const [showAmendmentModal, setShowAmendmentModal] = useState(false);
  const [selectedBookingId, setSelectedBookingId] = useState<string | null>(null);
  const previousIdRef = useRef<string | null>(null);
  const [isDriverMode, setIsDriverMode] = useState(false);
  const [isFetchingChat, setIsFetchingChat] = useState(false); // To track if fetch is in progress
  
  // Initialize chat hook
  const { 
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
  } = useChatMessages(
    id as string, 
    currentUserId,
    typeof initialMessage !== 'undefined' ? initialMessage as string : undefined,
    isDriverMode
  );

  // Ensure we have a current user ID
  useEffect(() => {
    const getUserId = async () => {
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
    
    // Only auto-create when there's an initial message
    const shouldAutoCreate = !!initialMessage && initialMessage !== '';
    setAutoCreateChat(shouldAutoCreate);
    
    // If we have a user ID, fetch the new chat data
    if (currentUserId) {
      fetchChatData();
    }
  }, [id, currentUserId, initialMessage]);

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
      if (isFetchingChat) return;
      
      // Set a flag to prevent multiple fetches
      setIsFetchingChat(true);
      
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
        setChatData(selectedChat);
        setIsFetchingChat(false);
        return;
      }
      
      // No existing conversation was found
      console.log("No existing conversation found for:", id);
      
      // Only create a conversation if explicitly allowed to
      if (!autoCreateChat || typeof initialMessage === 'undefined' || initialMessage === '') {
        console.log("Auto-creation disabled or no initial message. Not creating a new chat.");
        setIsFetchingChat(false);
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
        setChatData({
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
        setIsFetchingChat(false);
      }
    } catch (error) {
      console.error("Error in fetchChatData:", error);
      setIsFetchingChat(false);
    }
  };

  // Handle scrolling to bottom when new messages arrive
  useEffect(() => {
    if (messages.length > 0 && !isLoadingHistory) {
      scrollViewRef.current?.scrollToEnd({ animated: false });
    }  
  }, [messages.length, isLoadingHistory]);

  // Handle sending a new message
  const handleSendMessage = () => {
    if (!newMessage.trim() || !isConnected) return;
    const success = sendMessage(newMessage.trim());
    if (success) {
      setNewMessage("");
      setTimeout(() => {
        scrollViewRef.current?.scrollToEnd({ animated: true });
      }, 100);
    }
  };

  // Handle sending a booking amendment request
  const sendBookingAmendmentRequest = async (amendment: AddBookingAmmendmentRequest) => {
    if (!isConnected || !chat) return;
  
    try {
      // First save the amendment to booking service
      const result = await addBookingAmmendment(amendment);
      
      // Check for success response - handle both structures
      if (result.success || result.Status === "Success") {
        // Get the amendment ID from either response format
        const amendmentId = result.id || result.BookingAmmendmentId || "";
        console.log("Amendment created with ID:", amendmentId);
        
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
        
        // Send the amendment message via the sendMessage function from our hook
        const success = sendMessage(JSON.stringify(amendmentMessage));
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
            <ChatHeader 
              title={chat.title}
              chatType={chat.type}
              isConnecting={isConnecting}
              isConnected={isConnected}
            />
      
            {connectionError && (
              <View className="bg-red-500 p-2">
                <Text className="text-white text-center">{connectionError}</Text>
              </View>
            )}
      
            {/* Messages */}
            <ChatMessages
              ref={scrollViewRef}
              messages={messages}
              isLoadingHistory={isLoadingHistory}
              currentUserId={currentUserId}
              isDriverMode={isDriverMode}
              onApproveAmendment={handleAmendmentApproval}
            />
      
            {/* Message Input */}
            <ChatInput
              message={newMessage}
              onChangeMessage={setNewMessage}
              onSendMessage={handleSendMessage}
              onShowAmendmentModal={() => setShowAmendmentModal(true)}
              isConnected={isConnected}
            />
          </>
        )}
      </KeyboardAvoidingView>

      {/* Booking Amendment Modal */}
      <BookingAmendmentModal
        visible={showAmendmentModal}
        onClose={() => setShowAmendmentModal(false)}
        onSubmit={sendBookingAmendmentRequest}
        isDriver={isDriverMode}
      />
    </ThemedSafeAreaView>
  );
};

export default ChatDetail;
