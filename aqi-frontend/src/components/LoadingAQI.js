import { Box, Typography, CircularProgress } from "@mui/material";

export default function LoadingAQI({ city }) {
  return (
    <Box
      mt={5}
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      sx={{
        color: "#fff",
        minHeight: 180,
      }}
    >
      <CircularProgress
        size={60}
        thickness={4}
        sx={{ color: "#4fc3f7", mb: 2 }}
      />

      <Typography variant="h6">
        Fetching AQI data{city ? ` for ${city}` : ""}...
      </Typography>

      <Typography variant="body2" sx={{ opacity: 0.7, mt: 1 }}>
        Analyzing weather & pollution patterns
      </Typography>
    </Box>
  );
}
