import { useAuthStore } from "@/store/auth.store";
import { authService } from "@/services/auth.service";
import { useCallback } from "react";
import { useRouter } from "next/navigation";

/**
 * Central auth hook — wraps Zustand auth store and exposes login/register/logout with routing.
 */
export function useAuth() {
  const {
    user,
    accessToken,
    isAuthenticated,
    login: storeLogin,
    register: storeRegister,
    logout: storeLogout,
  } = useAuthStore();

  const router = useRouter();

  const login = useCallback(
    async (email: string, password: string) => {
      await storeLogin(email, password);
      router.push("/chat");
    },
    [storeLogin, router]
  );

  const register = useCallback(
    async (email: string, password: string, fullName: string) => {
      await storeRegister(email, password, fullName);
      router.push("/chat");
    },
    [storeRegister, router]
  );

  const logout = useCallback(async () => {
    await storeLogout();
    router.push("/login");
  }, [storeLogout, router]);

  return {
    user,
    accessToken,
    isAuthenticated,
    login,
    register,
    logout,
  };
}
