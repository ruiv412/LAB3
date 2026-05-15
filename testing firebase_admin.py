import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("certificado.json")
firebase_admin.initialize_app(cred)

### criar um documento
db = firestore.client()
dados = {
    "nome": "Ana",
    "curso": "Firebase",
    "nota": 17
}
db.collection("c-academy-lab3").document("aluno_004").set(dados)
print("Documento criado com ID aluno_004")

### ler um documento
doc_id = "aluno_001"
doc_ref = db.collection("c-academy-lab3").document(doc_id)
doc = doc_ref.get()

print("Existe?", doc.exists)

### listar todos os documentos
docs = db.collection("c-academy-lab3").stream()
for doc in docs:
    print(doc.id, doc.to_dict())

### eliminar um documento
doc_ref = db.collection("c-academy-lab3").document(doc_id)
doc = doc_ref.get()

if doc.exists:
    doc_ref.delete()
    print("Documento eliminado")
else:
    print("Documento NÃO encontrado")
