import { Box, Typography } from "@mui/material";
import AirIcon from "@mui/icons-material/Air";

export default function Header() {
  return (
    <Box
      display="flex"
      alignItems="center"
      gap={2}
      flexWrap="wrap"
    >
      <AirIcon sx={{ fontSize: 42, color: "#4fc3f7" }} />

      <Box>
        <Typography
          variant="h4"
          fontWeight={700}
          sx={{
            fontSize: { xs: "1.8rem", md: "2.2rem" },
          }}
        >
          AQI Forecast
        </Typography>

        <Typography
          variant="subtitle2"
          sx={{ opacity: 0.75 }}
        >
          Real-time air quality & 10-day ML prediction
        </Typography>
      </Box>
    </Box>
  );
}
