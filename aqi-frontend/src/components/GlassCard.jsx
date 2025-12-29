import { Box } from "@mui/material";

export default function GlassCard({ children }) {
  return (
    <Box
      sx={{
        p: 3,
        borderRadius: 4,
        background: "rgba(255,255,255,0.12)",
        backdropFilter: "blur(14px)",
        border: "1px solid rgba(255,255,255,0.18)",
        boxShadow: "0 8px 32px rgba(0,0,0,0.25)",
      }}
    >
      {children}
    </Box>
  );
}
