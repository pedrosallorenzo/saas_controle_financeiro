import { formatCurrency } from "@/lib/utils";
import type { DashboardSummary, TopCategory } from "@/types";

interface DashboardStatsProps {
  summary: DashboardSummary;
  topCategories: TopCategory[];
}

export function DashboardStats({ summary, topCategories }: DashboardStatsProps) {
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-3 gap-3">
        <div className="rounded-xl bg-green-50 p-4">
          <p className="text-xs text-green-600">Receitas</p>
          <p className="mt-1 text-lg font-bold text-green-700">
            {formatCurrency(summary.receitas)}
          </p>
        </div>
        <div className="rounded-xl bg-red-50 p-4">
          <p className="text-xs text-red-600">Despesas</p>
          <p className="mt-1 text-lg font-bold text-red-700">
            {formatCurrency(summary.despesas)}
          </p>
        </div>
        <div className={`rounded-xl p-4 ${summary.saldo >= 0 ? "bg-blue-50" : "bg-orange-50"}`}>
          <p className={`text-xs ${summary.saldo >= 0 ? "text-blue-600" : "text-orange-600"}`}>Saldo</p>
          <p className={`mt-1 text-lg font-bold ${summary.saldo >= 0 ? "text-blue-700" : "text-orange-700"}`}>
            {formatCurrency(summary.saldo)}
          </p>
        </div>
      </div>

      {topCategories.length > 0 && (
        <div className="space-y-2">
          <h2 className="text-sm font-medium text-gray-500">Top categorias</h2>
          <ul className="space-y-2">
            {topCategories.map((cat) => (
              <li key={cat.slug} className="flex items-center justify-between rounded-lg border px-4 py-3">
                <span className="text-sm">
                  {cat.icon && <span className="mr-2">{cat.icon}</span>}
                  {cat.name}
                </span>
                <span className="text-sm font-medium text-red-600">{formatCurrency(cat.total)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
