"use client";

import type { Transaction } from "@/types";
import { formatCurrency, formatDate } from "@/lib/utils";

interface TransactionListProps {
  transactions: Transaction[];
  onDelete?: (id: string) => void;
}

export function TransactionList({ transactions, onDelete }: TransactionListProps) {
  if (transactions.length === 0) {
    return (
      <div className="rounded-xl border p-8 text-center text-gray-400">
        <p>Nenhuma transação encontrada</p>
      </div>
    );
  }

  return (
    <ul className="space-y-2">
      {transactions.map((tx) => (
        <li
          key={tx.id}
          className="flex items-center justify-between rounded-xl border px-4 py-3"
        >
          <div className="space-y-0.5">
            <p className="text-sm font-medium">{tx.description ?? tx.category_id ?? "—"}</p>
            <p className="text-xs text-gray-400">{formatDate(tx.date)}</p>
          </div>
          <div className="flex items-center gap-3">
            <span
              className={`text-sm font-medium ${tx.type === "receita" ? "text-green-600" : "text-red-600"}`}
            >
              {tx.type === "receita" ? "+" : "-"}
              {formatCurrency(tx.amount)}
            </span>
            {onDelete && (
              <button
                onClick={() => onDelete(tx.id)}
                className="text-xs text-gray-400 hover:text-red-500"
              >
                ✕
              </button>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}
