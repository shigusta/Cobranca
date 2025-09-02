import { useState } from "react";

const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [delay, setDelay] = useState(20);
  const [mensagem, setMensagem] = useState(
    "Oi {nome}! Esta é uma mensagem de teste."
  );
  const [status, setStatus] = useState("");

  async function handleEnviar() {
    if (!file) {
      setStatus("Selecione uma planilha .xlsx primeiro.");
      return;
    }
    const fd = new FormData();
    fd.append("file", file);
    fd.append("delay", String(delay));
    fd.append("mensagem", mensagem);

    setStatus("Iniciando… (abra o WhatsApp Web e faça login)");
    try {
      const resp = await fetch(`${API}/upload`, { method: "POST", body: fd });
      const data = await resp.json();
      if (resp.ok) {
        setStatus("Envio iniciado. As abas do WhatsApp vão abrir aos poucos.");
      } else {
        setStatus(`Erro: ${data.detail || "Falha ao iniciar envio"}`);
      }
    } catch (e) {
      setStatus(`Erro ao conectar: ${e}`);
    }
  }

  async function handleParar() {
    try {
      const resp = await fetch(`${API}/parar`, { method: "POST" });
      if (resp.ok) setStatus("Envio interrompido.");
      else setStatus("Não foi possível interromper agora.");
    } catch (e) {
      setStatus(`Erro ao parar: ${e}`);
    }
  }

  const page = {
    wrapper: {
      minHeight: "100vh",
      background: "#0b0b0b",
      color: "#f3f3f3",
      padding: "2rem",
      fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
    },
    input: {
      background: "#111",
      border: "1px solid #333",
      color: "#fff",
      padding: "10px",
      borderRadius: 10,
      width: "100%",
    },
    btn: (bg) => ({
      background: bg,
      padding: "10px 16px",
      borderRadius: 10,
      border: "none",
      color: "#fff",
      fontWeight: 700,
      cursor: "pointer",
    }),
    status: {
      marginTop: 16,
      padding: 12,
      background: "#111",
      border: "1px solid #333",
      borderRadius: 12,
      color: "#a7f3d0",
      fontFamily: "ui-monospace, SFMono-Regular, Menlo, monospace",
    },
  };

  return (
    <div style={page.wrapper}>
      <h1 style={{ fontSize: 32, fontWeight: 800, marginBottom: 8 }}>
        KAYROSLINK planilha — Cobrança
      </h1>

      <label style={{ display: "block", marginTop: 16 }}>Planilha (.xlsx)</label>
      <input
        type="file"
        accept=".xlsx,.xls"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <label style={{ display: "block", marginTop: 16 }}>
        Atraso entre envios (segundos)
      </label>
      <input
        type="number"
        min={5}
        value={delay}
        onChange={(e) => setDelay(Number(e.target.value))}
        style={page.input}
      />

      <label style={{ display: "block", marginTop: 16 }}>Mensagem</label>
      <textarea
        rows={8}
        value={mensagem}
        onChange={(e) => setMensagem(e.target.value)}
        placeholder="Escreva a mensagem. Use {nome} para personalizar."
        style={{ ...page.input, resize: "vertical" }}
      />

      <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
        <button style={page.btn("#16a34a")} onClick={handleEnviar}>
          Iniciar envio
        </button>
        <button style={page.btn("#dc2626")} onClick={handleParar}>
          Parar
        </button>
      </div>

      <div style={page.status}>{status || "Status aparecerá aqui."}</div>

      <p style={{ marginTop: 8, fontSize: 12, color: "#9ca3af" }}>
        Dica: mantenha o <strong>WhatsApp Web</strong> logado no navegador
        padrão.
      </p>
    </div>
  );
}
