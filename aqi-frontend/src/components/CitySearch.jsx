import React, { useState } from "react";
import axios from "axios";
import { TextField, Autocomplete } from "@mui/material";

export default function CitySearch({ onSelect }) {
  const [options, setOptions] = useState([]);

  const fetchCities = async (value) => {
    if (!value) return;

    const res = await axios.get(
      "https://geocoding-api.open-meteo.com/v1/search",
      {
        params: {
          name: value,
          count: 8,
          language: "en",
        },
      }
    );

    setOptions(res.data.results || []);
  };

  return (
    <Autocomplete
      fullWidth
      options={options}
      getOptionLabel={(opt) => `${opt.name}, ${opt.country}`}
      onInputChange={(e, value) => fetchCities(value)}
      onChange={(e, value) => {
        if (value && onSelect) {
          onSelect(value.latitude, value.longitude, value.name);
        }
      }}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Search city"
          fullWidth
        />
      )}
    />
  );
}
