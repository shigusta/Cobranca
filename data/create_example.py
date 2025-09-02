import pandas as pd
df = pd.DataFrame([
    {"TITULAR":"João da Silva", "TELEFONE":"11999887766", "OBS":"Venc.:2025-09-01"},
    {"TITULAR":"Maria Oliveira", "TELEFONE":"21988776655", "OBS":"Venc.:2025-09-05"}
])
df.to_excel("data/exemplo.xlsx", index=False)
print("exemplo salvo em data/exemplo.xlsx")
