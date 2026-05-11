import { create } from "zustand";
import type { User, Category } from "@/types";

interface AppState {
  user: User | null;
  categories: Category[];
  setUser: (user: User | null) => void;
  setCategories: (categories: Category[]) => void;
}

export const useAppStore = create<AppState>((set) => ({
  user: null,
  categories: [],
  setUser: (user) => set({ user }),
  setCategories: (categories) => set({ categories }),
}));
