export interface User {
  id: string;
  email: string;
  name: string | null;
  profile: string | null;
  objective: string | null;
  income_type: string | null;
  onboarding_done: boolean;
}

export interface Category {
  id: string;
  user_id: string;
  name: string;
  slug: string;
  icon: string | null;
  is_default: boolean;
}

export interface Transaction {
  id: string;
  user_id: string;
  category_id: string | null;
  type: "receita" | "despesa";
  amount: number;
  description: string | null;
  date: string;
  raw_input: string | null;
  ai_confidence: "alta" | "media" | "baixa" | null;
}

export interface ParseResponse {
  tipo: "receita" | "despesa" | null;
  valor: number | null;
  categoria: string | null;
  data: string | null;
  descricao: string | null;
  confianca: "alta" | "media" | "baixa" | "nenhuma";
}

export interface DashboardSummary {
  mes: string;
  receitas: number;
  despesas: number;
  saldo: number;
}

export interface TopCategory {
  name: string;
  slug: string;
  icon: string | null;
  total: number;
}
