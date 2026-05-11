import Link from "next/link";

const navItems = [
  { href: "/dashboard", label: "Início", icon: "🏠" },
  { href: "/lancamento", label: "Lançar", icon: "+" },
  { href: "/transacoes", label: "Histórico", icon: "📋" },
  { href: "/perguntar", label: "Perguntar", icon: "💬" },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex flex-col min-h-screen">
      <main className="flex-1 pb-16">{children}</main>
      <nav className="fixed bottom-0 left-0 right-0 border-t bg-white">
        <ul className="flex">
          {navItems.map((item) => (
            <li key={item.href} className="flex-1">
              <Link
                href={item.href}
                className="flex flex-col items-center gap-1 py-2 text-xs text-gray-500 hover:text-blue-600"
              >
                <span className="text-lg">{item.icon}</span>
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}
