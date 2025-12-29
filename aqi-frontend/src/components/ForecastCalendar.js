import { Box, Card, CardContent, Typography } from "@mui/material";
import { getAQIColor } from "../utils/aqiColor";

/* Helper: format date nicely */
const formatDate = (dateStr) =>
  new Date(dateStr).toLocaleDateString("en-IN", {
    weekday: "short",
    day: "numeric",
    month: "short",
  });

export default function ForecastCalendar({ forecast }) {
  return (
    <Box mt={6}>
      {/* Section Header */}
      <Typography
        variant="h6"
        sx={{
          fontWeight: 600,
          letterSpacing: 0.4,
          mb: 2,
        }}
      >
        📅 10-Day AQI Outlook
      </Typography>

      {/* Horizontal Scroll */}
      <Box
        sx={{
          display: "flex",
          gap: 2.5,
          overflowX: "auto",
          pb: 2,
          scrollSnapType: "x mandatory",
        }}
      >
        {forecast.map((day, i) => (
          <Card
            key={i}
            sx={{
              minWidth: 180,
              scrollSnapAlign: "start",
              borderRadius: 4,
              color: "#fff",
              background: `
                linear-gradient(
                  180deg,
                  rgba(255,255,255,0.15),
                  rgba(255,255,255,0.05)
                ),
                ${getAQIColor(day.AQI)}
              `,
              backdropFilter: "blur(14px)",
              border: "1px solid rgba(255,255,255,0.15)",
              boxShadow: "0 8px 30px rgba(0,0,0,0.35)",
              transition: "all 0.35s ease",
              "&:hover": {
                transform: "translateY(-6px) scale(1.02)",
                boxShadow: "0 14px 45px rgba(0,0,0,0.45)",
              },
            }}
          >
            <CardContent sx={{ p: 2.2 }}>
              {/* Date */}
              <Typography
                variant="subtitle2"
                sx={{
                  opacity: 0.9,
                  letterSpacing: 0.3,
                  mb: 1,
                }}
              >
                {formatDate(day.date)}
              </Typography>

              {/* AQI */}
              <Typography
                variant="h4"
                sx={{
                  fontWeight: 700,
                  lineHeight: 1.1,
                }}
              >
                {Math.round(day.AQI)}
              </Typography>

              <Typography
                variant="caption"
                sx={{
                  opacity: 0.85,
                  letterSpacing: 0.5,
                }}
              >
                Air Quality Index
              </Typography>

              {/* Divider */}
              <Box
                sx={{
                  height: 1,
                  my: 1.5,
                  background: "rgba(255,255,255,0.3)",
                }}
              />

              {/* PM Values */}
              <Typography variant="body2">
                PM2.5: <strong>{day["pm2.5"].toFixed(1)}</strong>
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.85 }}>
                PM10: <strong>{day.pm10.toFixed(1)}</strong>
              </Typography>
            </CardContent>
          </Card>
        ))}
      </Box>
    </Box>
  );
}
