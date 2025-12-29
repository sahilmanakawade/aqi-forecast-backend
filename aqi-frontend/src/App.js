import React, { useState } from "react";
import axios from "axios";
import {
  Container,
  Box,
  Paper,
  Button,
  CircularProgress,
} from "@mui/material";

import Header from "./components/Header";
import CitySearch from "./components/CitySearch";
import TodaySummary from "./components/TodaySummary";
import ForecastCalendar from "./components/ForecastCalendar";
import LoadingAQI from "./components/LoadingAQI";

function App() {
  const [forecast, setForecast] = useState([]);
  const [city, setCity] = useState("");
  const [coords, setCoords] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchForecast = async () => {
    if (!coords) return;

    setLoading(true);
    try {
      const res = await axios.get("http://127.0.0.1:8000/forecast", {
        params: coords,
      });
      setForecast(res.data);
    } catch (err) {
      console.error("Forecast error:", err);
    }
    setLoading(false);
  };

  return (
    <Container
      maxWidth={false}
      disableGutters
      sx={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-start",
        pt: 6,
        pb: 8,
      }}
    >
      <Paper
        className="glass-card"
        sx={{
          width: "100%",
          maxWidth: 900,
          p: { xs: 3, md: 5 },
        }}
      >
        {/* HEADER */}
        <Header />

        {/* CITY SEARCH */}
        <Box mt={4}>
          <CitySearch
            onSelect={(lat, lon, name) => {
              setCoords({ lat, lon });
              setCity(name);
            }}
          />
        </Box>

        {/* SUBMIT BUTTON */}
        <Box mt={3}>
          <Button
            fullWidth
            size="large"
            variant="contained"
            onClick={fetchForecast}
            sx={{
              py: 1.4,
              fontSize: "1.1rem",
              borderRadius: 3,
            }}
          >
            {loading ? <CircularProgress size={26} color="inherit" /> : "SUBMIT"}
          </Button>
        </Box>

        {/* LOADING */}
        {loading && <LoadingAQI />}

        {/* RESULTS */}
        {!loading && forecast.length > 0 && (
          <>
            <TodaySummary data={forecast[0]} city={city} />
            <ForecastCalendar forecast={forecast.slice(1)} />
          </>
        )}
      </Paper>
    </Container>
  );
}

export default App;
