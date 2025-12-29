import { Card, CardContent, Typography, Grid, Box } from "@mui/material";
import { getAQIColor, getAQIStatus } from "../utils/aqiColor";

export default function TodaySummary({ data, city }) {
  const color = getAQIColor(data.AQI);
  const status = getAQIStatus(data.AQI);

  return (
    <Box mt={5}>
      <Typography
        variant="h6"
        gutterBottom
        sx={{ mb: 2 }}
      >
        📍 {city} — Today’s Air Quality
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <Card
            sx={{
  borderRadius: 4,
  background: "rgba(255,255,255,0.1)",
  backdropFilter: "blur(10px)",
  boxShadow: "0 4px 20px rgba(116, 55, 55, 0.3)",
  transition: "0.3s",
  "&:hover": { transform: "translateY(-4px)", boxShadow: "0 8px 30px rgba(0,0,0,0.4)" }
}}

          >
            <CardContent>
              <Typography variant="subtitle2">
                Air Quality Index
              </Typography>
              <Typography variant="h2" fontWeight={700}>
                {Math.round(data.AQI)}
              </Typography>
              <Typography variant="subtitle2">
                {status}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={6} md={4}>
          <Card sx={{
  borderRadius: 4,
  background: "rgba(255,255,255,0.1)",
  backdropFilter: "blur(10px)",
  boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
  transition: "0.3s",
  "&:hover": { transform: "translateY(-4px)", boxShadow: "0 8px 30px rgba(0,0,0,0.4)" }
}}
>
            <CardContent>
              <Typography variant="caption">PM2.5</Typography>
              <Typography variant="h4">
                {data["pm2.5"].toFixed(1)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={6} md={4}>
          <Card sx={{
  borderRadius: 4,
  background: "rgba(255,255,255,0.1)",
  backdropFilter: "blur(10px)",
  boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
  transition: "0.3s",
  "&:hover": { transform: "translateY(-4px)", boxShadow: "0 8px 30px rgba(0,0,0,0.4)" }
}}
>
            <CardContent>
              <Typography variant="caption">PM10</Typography>
              <Typography variant="h4">
                {data.pm10.toFixed(1)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
