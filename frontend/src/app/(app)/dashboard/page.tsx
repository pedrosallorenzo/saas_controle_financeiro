"use client";

export default function DashboardPage() {
  return (
    <div className="p-4 space-y-6">
      <h1 className="text-xl font-bold">Resumo do mês</h1>
      {/* DashboardStats — implementar na Semana 7-8 */}
      <div className="grid grid-cols-3 gap-3">
        <div className="rounded-xl bg-green-50 p-4">
          <p className="text-xs text-green-600">Receitas</p>
          <p className="text-lg font-bold text-green-700">R$ 0</p>
        </div>
        <div className="rounded-xl bg-red-50 p-4">
          <p className="text-xs text-red-600">Despesas</p>
          <p className="text-lg font-bold text-red-700">R$ 0</p>
        </div>
        <div className="rounded-xl bg-blue-50 p-4">
          <p className="text-xs text-blue-600">Saldo</p>
          <p className="text-lg font-bold text-blue-700">R$ 0</p>
        </div>
      </div>
    </div>
  );
}
