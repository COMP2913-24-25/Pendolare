import { useMemo } from 'react';
import { ChatMessage } from '@/services/messageService';

/**
 * Custom hook to handle amendment message parsing and validation
 */
export const useAmendmentMessage = (message: ChatMessage) => {
  return useMemo(() => {
    // Check if this is an amendment message
    const isAmendmentMessage = message.type === "booking_amendment" || !!message.amendmentId;
    
    if (!isAmendmentMessage) {
      return {
        isAmendmentMessage: false,
        amendmentContent: null,
        error: null
      };
    }
    
    try {
      // Parse the content if it's a stringified JSON
      let amendmentContent = message.content;
      
      // Handle different message formats
      if (typeof amendmentContent === 'string') {
        try {
          amendmentContent = JSON.parse(amendmentContent);
        } catch (e) {
          console.error("Failed to parse amendment data:", e);
          return {
            isAmendmentMessage: true,
            amendmentContent: null,
            error: "Invalid amendment data format"
          };
        }
      }
      
      console.log("Processed amendment data:", amendmentContent);
      
      return {
        isAmendmentMessage: true,
        amendmentContent,
        error: null
      };
    } catch (error) {
      console.error("Error processing amendment message:", error);
      return {
        isAmendmentMessage: true,
        amendmentContent: null,
        error: error.message || "Unknown error"
      };
    }
  }, [message]);
};
