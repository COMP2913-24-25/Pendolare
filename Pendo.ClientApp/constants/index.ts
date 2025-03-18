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
  flag: "flag",
};

export const onboarding = [
  {
    id: 1,
    title: "Plan your perfect ride with ease",
    description:
      "With Pendolare, you can schedule shared rides in advance, ensuring a smooth and stress-free journey.",
    image: require("../assets/images/test-pic.jpg"),
  },
  {
    id: 2,
    title: "Shared travel, smarter journeys",
    description:
      "Reduce costs and your carbon footprint by sharing rides with others heading in the same direction.",
    image: require("../assets/images/test-pic.jpg"),
  },
  {
    id: 3,
    title: "Reliable, pre-booked rides",
    description:
      "Choose your pickup time, connect with fellow travellers, and enjoy a convenient ride—on your schedule.",
    image: require("../assets/images/test-pic.jpg"),
  },
];

export const data = {
  onboarding,
};

// API Constants
export const API_BASE_URL = "https://pendo-gateway.clsolutions.dev/api";

export const AUTH_ENDPOINTS = {
  REQUEST_OTP: "/Identity/RequestOtp",
  VERIFY_OTP: "/Identity/VerifyOtp",
  UPDATE_USER: "/Identity/UpdateUser",
  GET_USER: "/Identity/GetUser"
};

// Booking endpoints
export const BOOKING_ENDPOINTS = {
  CREATE_BOOKING: "/Booking/CreateBooking",
  GET_BOOKINGS: "/Booking/GetBookings",
};

export const MESSAGE_API_BASE_URL = "wss://pendo-message.clsolutions.dev/ws";

// Message endpoints
export const MESSAGE_ENDPOINTS = {
  GET_USER_CONVERSATIONS: "/Message/UserConversation",
  CREATE_CONVERSATION: "/Message/CreateConversation",
};

// Dummy data generated utilising machine learning models
export const dummyRides = [
  {
    id: 1,
    driverName: "John Smith",
    availableSeats: 3,
    departureTime: "08:00 AM",
    destination: "Leeds Train Station",
    price: "£15",
    rating: 4.8,
    pickup: {
      latitude: 53.806684,
      longitude: -1.555031,
      name: "University of Leeds",
    },
    dropoff: {
      latitude: 53.794304,
      longitude: -1.547692,
      name: "Leeds Train Station",
    },
  },
  {
    id: 2,
    driverName: "Sarah Wilson",
    availableSeats: 2,
    departureTime: Date.now() + 60 * 60 * 1000, // updated: 1 hour from now
    destination: "Hyde Park",
    price: "£25",
    rating: 4.9,
    pickup: {
      latitude: 53.806684,
      longitude: -1.555031,
      name: "University of Leeds",
    },
    dropoff: {
      latitude: 53.809402,
      longitude: -1.560743,
      name: "Hyde Park",
    },
  },
  // ...existing rides
];

interface DemoChat {
  id: number;
  type: "support" | "driver";
  category?: string;
  title: string;
  lastMessage: string;
  timestamp: number;
  unread: number;
  avatar: null;
  messages: {
    id: number;
    sender: string;
    text: string;
    timestamp: number;
  }[];
}

export const demoChats: DemoChat[] = [
  {
    id: 1,
    type: "support",
    category: "billing",
    title: "Billing Support",
    lastMessage: "Thank you for contacting billing support. How can we help?",
    timestamp: Date.now() - 1000 * 60 * 30, // 30 minutes ago
    unread: 2,
    avatar: null,
    messages: [
      {
        id: 1,
        sender: "support",
        text: "Hello! Thank you for contacting billing support. How can we help you today?",
        timestamp: Date.now() - 1000 * 60 * 35, // 35 minutes ago
      },
      {
        id: 2,
        sender: "user",
        text: "Hi, I have a question about my last ride payment",
        timestamp: Date.now() - 1000 * 60 * 32, // 32 minutes ago
      },
      {
        id: 3,
        sender: "support",
        text: "Of course, I'd be happy to help. Could you provide the date of the ride?",
        timestamp: Date.now() - 1000 * 60 * 30, // 30 minutes ago
      },
    ],
  },
  {
    id: 2,
    type: "driver",
    title: "John Smith",
    lastMessage: "I'll be there in 5 minutes",
    timestamp: Date.now() - 1000 * 60 * 75, // 1 hour and 15 minutes ago
    unread: 1,
    avatar: null,
    messages: [
      {
        id: 1,
        sender: "driver",
        text: "Hi, I'm your driver for today",
        timestamp: Date.now() - 1000 * 60 * 80, // 1 hour and 20 minutes ago
      },
      {
        id: 2,
        sender: "user",
        text: "Great! I'm ready at the pickup point",
        timestamp: Date.now() - 1000 * 60 * 78, // 1 hour and 18 minutes ago
      },
      {
        id: 3,
        sender: "driver",
        text: "I'll be there in 5 minutes",
        timestamp: Date.now() - 1000 * 60 * 75, // 1 hour and 15 minutes ago
      },
    ],
  },
];

export const upcomingRides = [
  {
    id: 1,
    driverName: "John Smith",
    driverId: 2, // matches the chat thread id
    // Set departure time to 14 minutes from now for testing late cancellation
    departureTime: Date.now() + 14 * 60 * 1000,
    price: "£15",
    pickup: {
      latitude: 53.806684,
      longitude: -1.555031,
      name: "University of Leeds",
    },
    dropoff: {
      latitude: 53.794304,
      longitude: -1.547692,
      name: "Leeds Train Station",
    },
    status: "confirmed",
  },
  {
    id: 2,
    driverName: "Sarah Wilson",
    driverId: 3,
    // Set departure time to tomorrow for comparison
    departureTime: Date.now() + 24 * 60 * 60 * 1000,
    price: "£20",
    pickup: {
      latitude: 53.806684,
      longitude: -1.555031,
      name: "University of Leeds",
    },
    dropoff: {
      latitude: 53.809402,
      longitude: -1.560743,
      name: "Hyde Park",
    },
    status: "confirmed",
  },
];

export const pastRides = [
  {
    id: 101,
    driverName: "Michael Brown",
    driverId: 4,
    departureTime: Date.now() - 7 * 24 * 60 * 60 * 1000, // 7 days ago
    price: "£18",
    pickup: {
      latitude: 53.806684,
      longitude: -1.555031,
      name: "University of Leeds",
    },
    dropoff: {
      latitude: 53.797365,
      longitude: -1.54484,
      name: "Leeds City Centre",
    },
    status: "completed",
  },
  {
    id: 102,
    driverName: "Emma Wilson",
    driverId: 5,
    departureTime: Date.now() - 3 * 24 * 60 * 60 * 1000, // 3 days ago
    price: "£12",
    pickup: {
      latitude: 53.806684,
      longitude: -1.555031,
      name: "University of Leeds",
    },
    dropoff: {
      latitude: 53.819191,
      longitude: -1.5356,
      name: "Chapel Allerton",
    },
    status: "completed",
  },
];

export const cancelReasons = [
  "Plans changed",
  "Found alternative transport",
  "Price too high",
  "Emergency",
  "Other",
];
