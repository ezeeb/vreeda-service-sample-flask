import { Box, Button } from '@mui/material';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import useSession from '../hooks/useSession';
import DeviceList from '../components/DeviceList';
import { useEffect, useState } from 'react';
import CustomPatternControl from '../components/CustomPatternControl';

export const Home = () => {
  const { loggedIn, loading, user } = useSession();
  const [grantStatus, setGrantStatus] = useState<"active" | "needs renewal" | null>(null);
  const [loadingGrant, setLoadingGrant] = useState(false);
  const [selectedDevices, setSelectedDevices] = useState<string[]>([]); 

  const fetchSelectedDevices = async () => {
    try {
      const response = await fetch(`/api/user/configuration`);
      if (!response.ok) throw new Error("Failed to fetch configuration");
      const data = await response.json();
      setSelectedDevices(data.devices || []);
    } catch (error) {
      console.error("Error fetching selected devices:", error);
    }
  };

  const handleSelectionChange = async (deviceId: string, isSelected: boolean) => {
    const updatedDevices = isSelected
    ? [...selectedDevices, deviceId]
    : selectedDevices.filter((id) => id !== deviceId);

    setSelectedDevices(updatedDevices);

    try {
      const response = await fetch("/api/user/configuration", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          configuration: { devices: updatedDevices },
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to update configuration");
      }

      console.log("Configuration updated successfully");
    } catch (error) {
      console.error("Error updating configuration:", error);
    }
  };

  const checkGrantStatus = async () => {
    setLoadingGrant(true);
    try {
      const response = await fetch(`/api/user/granted`);
      if (!response.ok) {
        throw new Error("Failed to check grant status");
      }
      const data = await response.json();
      setGrantStatus(data.granted ? "active" : "needs renewal");
    } catch (error) {
      console.error("Error checking grant status:", error);
      setGrantStatus("needs renewal");
    } finally {
      setLoadingGrant(false);
    }
  };

  const revokeGrant = async () => {
    if (!loggedIn) return;
    try {
      const response = await fetch(`/api/user/revoke`, {
        method: "DELETE",
      });
      if (!response.ok) {
        throw new Error("Failed to revoke grant");
      }
      logoutAzureB2C(); // Log out after revoking the grant
    } catch (error) {
      console.error("Error revoking grant:", error);
    }
  };

  const loginAzureADB2C = () => {
    window.location.href = '/api/auth/login';
  };

  const logoutAzureB2C = () => {
    window.location.href = '/api/auth/logout';
  };

  useEffect(() => {
    if (loggedIn) {
      fetchSelectedDevices();
      checkGrantStatus();
    }
  }, [loggedIn]);

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          py: 4,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}
      >
        <Typography variant="h4" gutterBottom>
          VREEDA Sample Service
        </Typography>
        {loading ? (
          <Typography variant="body1">Loading...</Typography>
        ) : loggedIn ? (
          <>
            <Box
              sx={{
                position: "absolute",
                top: 16,
                right: 16,
                display: "flex",
                gap: 2,
              }}
            >
              {/* Logout Button */}
              <Button variant="outlined" color="primary" onClick={logoutAzureB2C}>
                Logout
              </Button>
              {/* Revoke Button */}
              <Button variant="contained" color="error" onClick={revokeGrant}>
                Revoke
              </Button>
            </Box>

            <Typography variant="body1">
              Welcome, {user.name}
            </Typography>

            {/* Display Grant Status */}
            <Box pt={2}>
              <Typography variant="body2">
                Grant Status:{" "}
                {loadingGrant ? "Checking..." : grantStatus === "active" ? "Active" : "Needs Renewal"}
              </Typography>
            </Box>

            <DeviceList selectedDevices={selectedDevices} onSelectionChange={handleSelectionChange}/>

            <Box sx={{ width: '100%', pt: 4 }}>
              <Box display="flex" alignItems="center" justifyContent="space-between">
                <Typography variant="h5" gutterBottom>
                  Custom Patterns
                </Typography>
              </Box>
              <CustomPatternControl selectedDevices={selectedDevices}/>
            </Box>
          </>
        ) : (
          <>
            <Typography variant="body1" gutterBottom>
              Please sign in to activate service.
            </Typography>
            {/* SignIn Button */}
            <Button variant="outlined" color="primary" onClick={loginAzureADB2C}>
              Sign In
            </Button>
          </>
        )}
      </Box>
    </Container>
  );
};