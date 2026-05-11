"use client";

import { useState } from "react";

interface NLInputProps {
  onSubmit: (text: string) => void;
  isLoading?: boolean;
}

export function NLInput({ onSubmit, isLoading = false }: NLInputProps) {
  const [text, setText] = useState("");

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (text.trim()) {
      onSubmit(text.trim());
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-3">
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder='Ex: "Gastei 42 no almoço hoje" ou "Recebi meu salário de 3.500"'
        maxLength={500}
        rows={3}
        className="w-full resize-none rounded-xl border px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        disabled={isLoading}
      />
      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-400">{text.length}/500</span>
        <button
          type="submit"
          disabled={!text.trim() || isLoading}
          className="rounded-lg bg-blue-600 px-6 py-2 text-sm font-medium text-white hover:bg-blue-700 disabled:opacity-50"
        >
          {isLoading ? "Analisando..." : "Registrar"}
        </button>
      </div>
    </form>
  );
}
