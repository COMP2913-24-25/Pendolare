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
import { AddBookingAmendmentRequest, addBookingAmmendment } from "@/services/bookingService";
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
  const { id, name, initialMessage, autoCreateChat: autoCreateChatParam } = useLocalSearchParams();
  const [newMessage, setNewMessage] = useState(typeof initialMessage === "undefined" ? "" : initialMessage as string);
  const { isDarkMode } = useTheme();
  const [currentUserId, setCurrentUserId] = useState<string>("");
  const scrollViewRef = useRef<RNScrollView>(null);
  const [showAmendmentModal, setShowAmendmentModal] = useState(false);
  const [selectedBookingId, setSelectedBookingId] = useState<string | null>(null);
  const previousIdRef = useRef<string | null>(null);
  const [isDriverMode, setIsDriverMode] = useState(false);
  const [isFetchingChat, setIsFetchingChat] = useState(false);
  const [autoCreateChat, setAutoCreateChat] = useState(false);

  // Initialise chat hook
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
  } = useChatMessages(
    id as string, 
    currentUserId,
    initialMessage as string,
    isDriverMode
  );

  // Ensure current user ID is set before fetching chat data
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

  useEffect(() => {
    if (chat && currentUserId) {
      messageService.disconnect();
      messageService.setUserId(currentUserId);
      messageService.setConversationId(chat.ConversationId || chat.id);

      messageService.connect();
    }
  }, [chat?.ConversationId, currentUserId]);

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

  useEffect(() => {
    setAutoCreateChat(autoCreateChatParam === 'true');
  }, [autoCreateChatParam]);

  useEffect(() => {
    if (previousIdRef.current === id) return;
    
    console.log(`Chat ID changed from ${previousIdRef.current} to ${id}`);
    previousIdRef.current = id as string;
    
    const shouldAutoCreate = autoCreateChatParam === 'true' || (!!initialMessage && initialMessage !== '');
    setAutoCreateChat(shouldAutoCreate);
    
    if (currentUserId) {
      fetchChatData();
    }
  }, [id, currentUserId, initialMessage, autoCreateChatParam]);

  useEffect(() => {
    const determineUserRole = async () => {
      if (!currentUserId || !id) return;

      try {
        // Get all bookings (both as driver and passenger)
        const [driverBookings, passengerBookings] = await Promise.all([
          getBookings(true),
          getBookings(false)
        ]);

        // Try to find a booking for this chat (by participant)
        let foundBooking = null;
        // Search both driver and passenger bookings for a booking with this chat participant
        for (const booking of [...driverBookings.bookings, ...passengerBookings.bookings]) {
          if (
            (booking.Booking.User?.UserId === id || booking.Journey.User?.UserId === id) ||
            (booking.Booking.User?.UserId === currentUserId || booking.Journey.User?.UserId === currentUserId)
          ) {
            foundBooking = booking;
            break;
          }
        }

        if (foundBooking) {
          if (foundBooking.Journey.User?.UserId === currentUserId) {
            setIsDriverMode(true);
            console.log("User role determined: Driver");
          } else if (foundBooking.Booking.User?.UserId === currentUserId) {
            setIsDriverMode(false);
            console.log("User role determined: Passenger");
          } else {
            setIsDriverMode(false);
            console.log("User role determined: Unknown, defaulting to Passenger");
          }
        } else {
          const isDriver = driverBookings.bookings?.some(booking =>
            booking.Journey?.User?.UserId === currentUserId
          );
          setIsDriverMode(isDriver);
        }
      } catch (error) {
        console.error("Error determining user role:", error);
        setIsDriverMode(false);
      }
    };

    determineUserRole();
  }, [currentUserId, id]);

  // Send initialMessage if present and chat is connected
  useEffect(() => {
    if (
      typeof initialMessage === "string" &&
      initialMessage.trim() !== "" &&
      isConnected &&
      chat
    ) {
      sendMessage(initialMessage.trim());
      setNewMessage(""); // Clear the input after sending
    }
    // Only run when chat connects or initialMessage changes
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isConnected, chat, initialMessage]);

  /*
    Fetch chat details
  */
  const fetchChatData = async () => {
    try {
      // Only allow one fetch operation at a time
      if (isFetchingChat) return;
      
      // Set a flag to prevent multiple fetches
      setIsFetchingChat(true);
      
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
      
      let selectedChat = normalisedConversations.find((c: any) => {
        if (c.id === id || c.ConversationId === id) {
          console.log("Found exact conversation match by ID");
          return true;
        }
        
        if (c.participants && c.participants.includes(id.toString())) {
          console.log("Found conversation where target is a participant");
          return true;
        }
        
        const targetName = name?.toString().toLowerCase() || id?.toString().toLowerCase();
        if (c.Name && c.Name.toLowerCase().includes(targetName)) {
          console.log("Found conversation match by name");
          return true;
        }
        
        if (c.title && c.title.toLowerCase().includes(targetName)) {
          console.log("Found conversation match by title");
          return true;
        }
        
        // No match
        return false;
      });
      
      if (selectedChat) {
        console.log("Using existing chat:", selectedChat.id);
        setChatData(selectedChat);
        setIsFetchingChat(false);
        return;
      }
      
      console.log("No existing conversation found for:", id);
      
      // Only create a conversation if explicitly allowed to
      if (!autoCreateChat) {
        console.log("Auto-creation disabled. Not creating a new chat.");
        setIsFetchingChat(false);
        return;
      }
      
      console.log("Will attempt to create new conversation");
      const userName: any = typeof name === "undefined" ? id.toString() : name as string;
      
      try {
        console.log(`Creating new conversation with ${userName}`);
        const response = await createConversation({
          ConversationType: "direct",
          name: `Chat with ${userName}`,
          participants: [id.toString()]
        });
        
        console.log("Conversation created successfully:", response);
        
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
        setAutoCreateChat(false);
        
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
      setAutoCreateChat(false);
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
  const sendBookingAmendmentRequest = async (amendment: AddBookingAmendmentRequest) => {
    if (!isConnected || !chat) return;
  
    try {
      const result = await addBookingAmmendment(amendment);
      
      if (result.success || result.Status === "Success") {
        // Get the amendment ID from either response format
        const amendmentId = result.id || result.BookingAmmendmentId || "";
        console.log("Amendment created with ID:", amendmentId);
        
        // Create the amendment message
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
        
        console.log("Sending amendment message:", amendmentMessage);
        
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
