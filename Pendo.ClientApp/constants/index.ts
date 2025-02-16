import arrowDown from "@/assets/icons/arrow-down.png";
import arrowUp from "@/assets/icons/arrow-up.png";
import backArrow from "@/assets/icons/back-arrow.png";
import chat from "@/assets/icons/chat.png";
import checkmark from "@/assets/icons/check.png";
import close from "@/assets/icons/close.png";
import dollar from "@/assets/icons/dollar.png";
import email from "@/assets/icons/email.png";
import eyecross from "@/assets/icons/eyecross.png";
import google from "@/assets/icons/google.png";
import home from "@/assets/icons/home.png";
import list from "@/assets/icons/list.png";
import lock from "@/assets/icons/lock.png";
import map from "@/assets/icons/map.png";
import marker from "@/assets/icons/marker.png";
import out from "@/assets/icons/out.png";
import person from "@/assets/icons/person.png";
import pin from "@/assets/icons/pin.png";
import point from "@/assets/icons/point.png";
import profile from "@/assets/icons/profile.png";
import search from "@/assets/icons/search.png";
import selectedMarker from "@/assets/icons/selected-marker.png";
import star from "@/assets/icons/star.png";
import target from "@/assets/icons/target.png";
import to from "@/assets/icons/to.png";

export const icons = {
  arrowDown,
  arrowUp,
  backArrow,
  chat,
  checkmark,
  close,
  dollar,
  email,
  eyecross,
  google,
  home,
  list,
  lock,
  map,
  marker,
  out,
  person,
  pin,
  point,
  profile,
  search,
  selectedMarker,
  star,
  target,
  to,
};

export const onboarding = [
  {
    id: 1,
    title: "Plan your perfect ride with ease",
    description:
      "With Pendolino, you can schedule shared rides in advance, ensuring a smooth and stress-free journey.",
  },
  {
    id: 2,
    title: "Shared travel, smarter journeys",
    description:
      "Reduce costs and your carbon footprint by sharing rides with others heading in the same direction.",
  },
  {
    id: 3,
    title: "Reliable, pre-booked rides",
    description:
      "Choose your pickup time, connect with fellow travellers, and enjoy a convenient ride—on your schedule.",
  },
];

export const data = {
  onboarding,
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
    departureTime: "09:30 AM",
    destination: "Hyde Park",
    price: "$25",
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

export const demoChats = [
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
