"use client";

import Link from "next/link";

export default function LoginPage() {
  return (
    <main className="flex min-h-screen items-center justify-center p-4">
      <div className="w-full max-w-sm space-y-6">
        <div className="space-y-1">
          <h1 className="text-2xl font-bold">Entrar</h1>
          <p className="text-sm text-gray-500">Acesse sua conta</p>
        </div>

        {/* Form — implementar na Semana 1-2 */}
        <div className="space-y-4">
          <input
            type="email"
            placeholder="seu@email.com"
            className="w-full rounded-lg border px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="password"
            placeholder="Senha"
            className="w-full rounded-lg border px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button className="w-full rounded-lg bg-blue-600 py-3 text-sm font-medium text-white hover:bg-blue-700">
            Entrar
          </button>
        </div>

        <p className="text-center text-sm text-gray-500">
          Não tem conta?{" "}
          <Link href="/cadastro" className="text-blue-600 hover:underline">
            Cadastre-se
          </Link>
        </p>
      </div>
    </main>
  );
}
