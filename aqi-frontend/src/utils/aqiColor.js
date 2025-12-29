// src/utils/aqiColor.js

/**
 * Central AQI design system
 * Used across cards, charts, badges & summaries
 */

const AQI_SCALE = [
  {
    max: 50,
    label: "Good",
    color: "linear-gradient(135deg, #2ecc71, #27ae60)",
    text: "#2e5342ff",
    emoji: "🟢",
    advice: "Air quality is excellent. Ideal for outdoor activities.",
  },
  {
    max: 100,
    label: "Moderate",
    color: "linear-gradient(135deg, #f1c40f, #f39c12)",
    text: "#705f2dff",
    emoji: "🟡",
    advice: "Air quality is acceptable. Sensitive groups should be cautious.",
  },
  {
    max: 200,
    label: "Poor",
    color: "linear-gradient(135deg, #e67e22, #d35400)",
    text: "#49433eff",
    emoji: "🟠",
    advice: "Unhealthy for sensitive groups. Reduce prolonged exertion.",
  },
  {
    max: 300,
    label: "Very Poor",
    color: "linear-gradient(135deg, #e74c3c, #c0392b)",
    text: "#5c2a2eff",
    emoji: "🔴",
    advice: "Unhealthy air. Avoid outdoor activity if possible.",
  },
  {
    max: Infinity,
    label: "Severe",
    color: "linear-gradient(135deg, #8e44ad, #5e3370)",
    text: "#380445ff",
    emoji: "🟣",
    advice: "Hazardous air quality. Stay indoors and use air filtration.",
  },
];

/* Internal helper */
const getAQIData = (aqi) =>
  AQI_SCALE.find((level) => aqi <= level.max);

/* ======================
   PUBLIC EXPORTS
   ====================== */

export const getAQIColor = (aqi) =>
  getAQIData(aqi).color;

export const getAQIStatus = (aqi) =>
  getAQIData(aqi).label;

export const getAQITextColor = (aqi) =>
  getAQIData(aqi).text;

export const getAQIEmoji = (aqi) =>
  getAQIData(aqi).emoji;

export const getAQIAdvice = (aqi) =>
  getAQIData(aqi).advice;
