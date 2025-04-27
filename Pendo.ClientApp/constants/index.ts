// Fontawesome icon mappings
export const icons = {
  home: "home",
  search: "search",
  chat: "comment",
  profile: "user",
  backArrow: "arrow-left",
  out: "sign-out-alt",
  star: "star",
  target: "map-marker-alt",
  time: "clock",
  to: "location-arrow",
  person: "user",
  marker: "map-marker",
  close: "times",
  plus: "plus",
  minus: "minus",
  check: "check",
  alert: "exclamation-circle",
  support: "headset",
  car: "car",
  card: "credit-card",
  flag: "flag",
  repeat: "redo",
  list: "clipboard-list",
  chevronRight: "chevron-right",
  cog: "cog",
};

// Onboarding messages & images
export const onboarding = [
  {
    id: 1,
    title: "Plan your perfect ride with ease",
    description:
      "With Pendolare, you can schedule shared rides in advance, ensuring a smooth and stress-free journey.",
    // The test pic was generated using canva's generative AI tooling
    image: require("../assets/images/test-pic.jpg"),
  },
  {
    id: 2,
    title: "Shared travel, smarter journeys",
    description:
      "Reduce costs and your carbon footprint by sharing rides with others heading in the same direction.",
    // The test pic was generated using canva's generative AI tooling
    image: require("../assets/images/test-pic.jpg"),
  },
  {
    id: 3,
    title: "Reliable, pre-booked rides",
    description:
      "Choose your pickup time, connect with fellow travellers, and enjoy a convenient ride—on your schedule.",
    // The test pic was generated using canva's generative AI tooling
    image: require("../assets/images/test-pic.jpg"),
  },
];

// API Constants
export const API_BASE_URL = "https://pendo-gateway.clsolutions.dev/api";

export const AUTH_ENDPOINTS = {
  REQUEST_OTP: "/Identity/RequestOtp",
  VERIFY_OTP: "/Identity/VerifyOtp",
  UPDATE_USER: "/Identity/UpdateUser",
  GET_USER: "/Identity/GetUser"
};

// Admin endpoints
export const ADMIN_ENDPOINTS = {
  GET_DISCOUNTS: "/Admin/Discounts",
};

// Booking endpoints
export const BOOKING_ENDPOINTS = {
  GET_BOOKINGS: "/Booking/GetBookings",
  CREATE_BOOKING: "/Booking/CreateBooking",
  ADD_BOOKING_AMMENDMENT: "/Booking/AddBookingAmmendment",
  APPROVE_BOOKING_AMMENDMENT: "/Booking/ApproveBookingAmmendment",
  APPROVE_BOOKING: "/Booking/ApproveBooking",
  CONFIRM_AT_PICKUP: "/Booking/ConfirmAtPickup",
  COMPLETE_BOOKING: "/Booking/CompleteBooking",
};

// Journey endpoints
export const JOURNEY_ENDPOINTS = {
  CREATE_JOURNEY: "/Journey/CreateJourney",
  GET_JOURNEYS: "/Journey/ViewJourney",
  LOCK_JOURNEY: "/Journey/LockJourney",
  ADJUST_PRICE: "/Journey/AdjustPrice",
};

// Payment endpoints
export const PAYMENT_ENDPOINTS = {
  VIEW_BALANCE: "/PaymentService/ViewBalance",
  PAYMENT_SHEET: "/PaymentService/PaymentSheet",
  CREATE_PAYOUT: "/PaymentService/CreatePayout",
  PAYMENT_METHODS: "/PaymentService/PaymentMethods",
};

export const MESSAGE_API_BASE_URL = "wss://pendo-message.clsolutions.dev/ws";

// Message endpoints
export const MESSAGE_ENDPOINTS = {
  GET_USER_CONVERSATIONS: "/Message/UserConversation",
  CREATE_CONVERSATION: "/Message/CreateConversation",
};

// Cancellation reasons
export const cancelReasons = [
  "Plans changed",
  "Found alternative transport",
  "Price too high",
  "Emergency",
  "Other",
];
