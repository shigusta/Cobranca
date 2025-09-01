import React, { useState } from "react";

export default function App() {
  const [file, setFile] = useState(null);
  const [delay, setDelay] = useState(20);
  const [mensagem, setMensagem] = useState(`Oi! Esperamos que esteja tudo bem com você.
Passando aqui só para lembrar que a sua fatura referente ao mês de *Maio* ainda está em aberto. Você pode
acessá-la pelo nosso app, site ou pelo e-mail que enviamos.
Se o pagamento já foi feito, por favor, desconsidere este aviso. E, se precisar de qualquer ajuda para regularizar a
situação, conte com a gente! Estamos por aqui para o que for preciso.
Com carinho, Kamila
Equipe Financeiro – Kayrós Link`);
  const [status, setStatus] = useState("");
  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  async function handleSubmit(e) {
    e.preventDefault();
    if (!file) {
      setStatus("Selecione um arquivo .xlsx antes de enviar.");
      return;
    }
    setStatus("Enviando arquivo...");
    const form = new FormData();
    form.append("file", file);
    form.append("delay", String(delay));
    form.append("mensagem", mensagem);

    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: form,
      });
      if (!res.ok) {
        const text = await res.text();
        setStatus(`Erro do servidor: ${res.status} ${text}`);
        return;
      }
      const data = await res.json();
      setStatus(`Arquivo enviado. Nome salvo: ${data.filename}\nProcessamento em background.`);
    } catch (err) {
      setStatus("Erro ao enviar: " + String(err));
    }
  }

  return (
    <div style={{fontFamily: 'Arial, sans-serif', padding: 24, maxWidth: 760, margin: '0 auto'}}>
      <h1>Upload de planilha — Cobrança</h1>
      <form onSubmit={handleSubmit}>
        <div style={{marginBottom: 12}}>
          <label>Planilha (.xlsx)</label><br/>
          <input type="file" accept=".xlsx" onChange={(e)=>setFile(e.target.files?.[0]||null)} />
        </div>

        <div style={{marginBottom: 12}}>
          <label>Delay entre envios (segundos)</label><br/>
          <input type="number" value={delay} min={5} onChange={e=>setDelay(Number(e.target.value))} />
        </div>

        <div style={{marginBottom: 12}}>
          <label>Mensagem</label><br/>
          <textarea rows={8} value={mensagem} onChange={e=>setMensagem(e.target.value)} style={{width:'100%'}} />
        </div>

        <button type="submit" style={{padding:'8px 12px'}}>Enviar e processar</button>
      </form>

      <div style={{marginTop:20, whiteSpace:'pre-wrap', background:'#f8f8f8', padding:12}}>
        {status || "Status aparecerá aqui."}
      </div>

      <p style={{marginTop:12, color:'#666'}}>Nota: antes de enviar, abra e faça login no <b>WhatsApp Web</b> no navegador padrão.</p>
    </div>
  );
}
