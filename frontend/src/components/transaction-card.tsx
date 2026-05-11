"use client";

import type { ParseResponse } from "@/types";
import { formatCurrency } from "@/lib/utils";

interface TransactionCardProps {
  parsed: ParseResponse;
  onConfirm: () => void;
  onCancel: () => void;
}

export function TransactionCard({ parsed, onConfirm, onCancel }: TransactionCardProps) {
  const isLowConfidence = parsed.confianca === "baixa";

  return (
    <div className={`rounded-xl border p-4 space-y-3 ${isLowConfidence ? "border-yellow-400 bg-yellow-50" : "border-gray-200"}`}>
      {isLowConfidence && (
        <p className="text-xs text-yellow-700 font-medium">Confiança baixa — verifique os dados</p>
      )}
      <div className="space-y-1">
        <div className="flex justify-between">
          <span className="text-sm text-gray-500">Tipo</span>
          <span className={`text-sm font-medium capitalize ${parsed.tipo === "receita" ? "text-green-600" : "text-red-600"}`}>
            {parsed.tipo ?? "—"}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm text-gray-500">Valor</span>
          <span className="text-sm font-medium">
            {parsed.valor != null ? formatCurrency(parsed.valor) : "—"}
          </span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm text-gray-500">Categoria</span>
          <span className="text-sm font-medium capitalize">{parsed.categoria ?? "—"}</span>
        </div>
        <div className="flex justify-between">
          <span className="text-sm text-gray-500">Data</span>
          <span className="text-sm font-medium">{parsed.data ?? "—"}</span>
        </div>
        {parsed.descricao && (
          <div className="flex justify-between">
            <span className="text-sm text-gray-500">Descrição</span>
            <span className="text-sm font-medium">{parsed.descricao}</span>
          </div>
        )}
      </div>
      <div className="flex gap-2 pt-2">
        <button
          onClick={onCancel}
          className="flex-1 rounded-lg border py-2 text-sm text-gray-600 hover:bg-gray-50"
        >
          Cancelar
        </button>
        <button
          onClick={onConfirm}
          className="flex-1 rounded-lg bg-blue-600 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          Confirmar
        </button>
      </div>
    </div>
  );
}
