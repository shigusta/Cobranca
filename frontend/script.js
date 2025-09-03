const API = "http://127.0.0.1:8000/upload"; // ajuste se necessário
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const btnUpload = document.getElementById("btnUpload");
const btnClear = document.getElementById("btnClear");
const mensagemFld = document.getElementById("mensagem");
const delayFld = document.getElementById("delay");
const resultBox = document.getElementById("result");
const connInd = document.getElementById("connection-indicator");
const modeLabel = document.getElementById("modeLabel");

let selectedFile = null;

fileInput.addEventListener("change", e => {
  selectedFile = e.target.files[0] || null;
  fileName.textContent = selectedFile ? selectedFile.name : "Nenhum arquivo selecionado";
});

btnClear.addEventListener("click", () => {
  fileInput.value = "";
  selectedFile = null;
  fileName.textContent = "Nenhum arquivo selecionado";
  mensagemFld.value = "";
  delayFld.value = 20;
  writeResult("Limpo.");
});

function writeResult(txt){
  resultBox.textContent = txt;
}

// verifica conexão simples com a API
async function checkConnection(){
  try{
    const r = await fetch("http://127.0.0.1:8000/status");
    if(r.ok){
      connInd.classList.add("ok");
      modeLabel.textContent = "API conectada";
    } else {
      connInd.classList.remove("ok");
      modeLabel.textContent = "API não respondeu";
    }
  }catch(e){
    connInd.classList.remove("ok");
    modeLabel.textContent = "Sem conexão com API";
  }
}
checkConnection();

btnUpload.addEventListener("click", async () => {
  if(!selectedFile){
    writeResult("Selecione uma planilha (.xlsx) antes de enviar.");
    return;
  }

  const mensagem = mensagemFld.value.trim();
  if(!mensagem){
    writeResult("Digite a mensagem que será enviada.");
    return;
  }

  const delay = Number(delayFld.value) || 20;

  writeResult("Enviando arquivo para o servidor...");

  const fd = new FormData();
  fd.append("file", selectedFile);
  fd.append("mensagem", mensagem);
  fd.append("delay", String(delay));

  try{
    const res = await fetch(API, { method: "POST", body: fd });
    const data = await res.json();

    if(!res.ok){
      writeResult("Erro do servidor: " + (data.detail || JSON.stringify(data)));
      connInd.classList.add("err");
      return;
    }

    writeResult("Upload aceito. Processamento iniciado (em background). " + JSON.stringify(data));
    connInd.classList.add("ok");
  }catch(err){
    writeResult("Erro ao conectar com a API: " + String(err));
    connInd.classList.remove("ok");
  }
});
