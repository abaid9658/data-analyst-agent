import { create } from "zustand";

interface UIState {
  sidebarCollapsed: boolean;
  mobileNavOpen: boolean;
  uploadModalOpen: boolean;
  dbWizardOpen: boolean;
  reportModalOpen: boolean;

  toggleSidebar: () => void;
  setMobileNavOpen: (open: boolean) => void;
  setUploadModalOpen: (open: boolean) => void;
  setDbWizardOpen: (open: boolean) => void;
  setReportModalOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  sidebarCollapsed: false,
  mobileNavOpen: false,
  uploadModalOpen: false,
  dbWizardOpen: false,
  reportModalOpen: false,

  toggleSidebar: () =>
    set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
  setMobileNavOpen: (open) => set({ mobileNavOpen: open }),
  setUploadModalOpen: (open) => set({ uploadModalOpen: open }),
  setDbWizardOpen: (open) => set({ dbWizardOpen: open }),
  setReportModalOpen: (open) => set({ reportModalOpen: open }),
}));
