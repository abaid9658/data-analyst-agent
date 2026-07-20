import { apiClient } from "@/lib/api-client";
import type { AuthResponse, LoginRequest, RegisterRequest, User } from "@/types/auth.types";

export const authService = {
  login: async (body: LoginRequest): Promise<AuthResponse> => {
    const { data } = await apiClient.post<AuthResponse>("/auth/login", body);
    return data;
  },

  register: async (body: RegisterRequest): Promise<User> => {
    const { data } = await apiClient.post<User>("/auth/register", body);
    return data;
  },

  logout: async (refreshToken: string): Promise<void> => {
    await apiClient.post("/auth/logout", { refresh_token: refreshToken });
  },

  refresh: async (refreshToken: string): Promise<{ access_token: string }> => {
    const { data } = await apiClient.post<{ access_token: string }>("/auth/refresh", {
      refresh_token: refreshToken,
    });
    return data;
  },

  getMe: async (): Promise<User> => {
    const { data } = await apiClient.get<User>("/settings/profile");
    return data;
  },
};
