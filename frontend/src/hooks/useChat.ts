import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { chatService } from "@/services/chat.service";

/**
 * Fetch all chat sessions for the authenticated user.
 */
export function useConversations() {
  return useQuery({
    queryKey: ["conversations"],
    queryFn: () => chatService.getSessions(),
    staleTime: 30 * 1000,
  });
}

/**
 * Fetch messages for a specific conversation session.
 */
export function useMessages(sessionId: string | undefined) {
  return useQuery({
    queryKey: ["messages", sessionId],
    queryFn: () => chatService.getMessages(sessionId!),
    enabled: !!sessionId,
    staleTime: 60 * 1000,
  });
}

/**
 * Delete a conversation session.
 */
export function useDeleteSession() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (sessionId: string) => chatService.deleteSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
  });
}
