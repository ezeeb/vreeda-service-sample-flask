import { useEffect, useState } from 'react';

export interface SessionData {
  loggedIn: boolean;
  user?: SessionUser;
}

export interface SessionUser {
  id?: string;
  name?: string;
  email?: string;
}

const useSession = () => {
  const [loggedIn, setLoggedIn] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const [user, setUser] = useState<SessionUser>({});

  useEffect(() => {
    const checkSessionStatus = async () => {
      try {
        setLoading(true);
        const response = await fetch('/api/auth/session', {
          credentials: 'include',  // Stellt sicher, dass das Cookie gesendet wird
        });
        const data = await response.json() as SessionData;

        if (data.loggedIn) {
          setLoggedIn(true);
          setUser({
              id: data.user?.id,
              name: data.user?.name,
              email: data.user?.email,
          });
        } else {
          setLoggedIn(false);
          setUser({});
        }
      } catch (error) {
        console.error('Fehler beim Überprüfen des Session-Status:', error);
        setLoggedIn(false);
        setUser({});
      } finally {
        setLoading(false);
      }
    };

    checkSessionStatus();
  }, []);

  return { loggedIn, loading, user };
};

export default useSession;
