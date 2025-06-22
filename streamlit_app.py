import streamlit as st
import random
import os
import requests

st.set_page_config(page_title="AI-nstein - Scienze", page_icon="🧬", layout="centered")
st.title("🔬 AI-nstein - Ripasso di Scienze")
st.markdown("Rispondi alle domande di Scienze! Se sbagli, ti spiego. 😄")

# Domande (Il tuo array di domande è corretto, lo ometto per brevità)
domande = [
    {
        "domanda": "Quale parte della cellula contiene il materiale genetico?",
        "opzioni": ["Mitocondrio", "Nucleo", "Citoplasma", "Membrana"],
        "corretta": "Nucleo",
        "spiegazione": "Il nucleo contiene il DNA, il materiale genetico.",
        "immagine": "nucleo.png"
    },
    {
        "domanda": "Qual è la funzione principale dei mitocondri?",
        "opzioni": ["Digestione", "Produzione di energia", "Difesa", "Controllo cellulare"],
        "corretta": "Produzione di energia",
        "spiegazione": "I mitocondri producono energia (ATP) nella cellula.",
        "immagine": "mitocondrio.png"
    },
    {
        "domanda": "Che cos'è la fotosintesi?",
        "opzioni": [
            "Un processo di respirazione",
            "La trasformazione della luce in energia chimica",
            "La digestione delle proteine",
            "L’assorbimento dell'acqua dal terreno"
        ],
        "corretta": "La trasformazione della luce in energia chimica",
        "spiegazione": "La fotosintesi trasforma luce, CO₂ e acqua in zuccheri.",
        "immagine": "fotosintesi.png"
    },
    {
        "domanda": "Quale organo pompa il sangue nel corpo umano?",
        "opzioni": ["Polmone", "Cervello", "Fegato", "Cuore"],
        "corretta": "Cuore",
        "spiegazione": "Il cuore è l’organo che pompa il sangue in tutto il corpo.",
        "immagine": "cuore.png"
    },
    {
        "domanda": "Qual è il gas più abbondante nell'atmosfera terrestre?",
        "opzioni": ["Ossigeno", "Anidride carbonica", "Azoto", "Idrogeno"],
        "corretta": "Azoto",
        "spiegazione": "L'azoto costituisce circa il 78% dell'atmosfera.",
        "immagine": "atmosfera.png"
    },
    {
        "domanda": "In che organo avviene la digestione delle proteine?",
        "opzioni": ["Bocca", "Stomaco", "Intestino", "Fegato"],
        "corretta": "Stomaco",
        "spiegazione": "Le proteine iniziano a essere digerite nello stomaco.",
        "immagine": "stomaco.png"
    },
    {
        "domanda": "Quale pianeta è noto come il pianeta rosso?",
        "opzioni": ["Venere", "Giove", "Marte", "Saturno"],
        "corretta": "Marte",
        "spiegazione": "Marte è chiamato così per il suo colore rosso.",
        "immagine": "marte.png"
    },
    {
        "domanda": "Cosa producono i globuli rossi?",
        "opzioni": ["Ossigeno", "Anticorpi", "Emoglobina", "Energia"],
        "corretta": "Emoglobina",
        "spiegazione": "I globuli rossi trasportano l'ossigeno grazie all'emoglobina.",
        "immagine": "globuli_rossi.png"
    },
    {
        "domanda": "Come si chiama il processo con cui le cellule si dividono?",
        "opzioni": ["Respirazione", "Mitòsi", "Fotosintesi", "Osmosi"],
        "corretta": "Mitòsi",
        "spiegazione": "La mitosi è la divisione cellulare che genera due cellule figlie.",
        "immagine": "mitosi.png"
    },
    {
        "domanda": "Quale apparato è responsabile della respirazione?",
        "opzioni": ["Circolatorio", "Digestivo", "Respiratorio", "Nervoso"],
        "corretta": "Respiratorio",
        "spiegazione": "L’apparato respiratorio scambia gas tra corpo e ambiente.",
        "immagine": "respiratorio.png"
    }
]

# Stato dell'app (il tuo codice è corretto, lo ometto per brevità)
if "indice" not in st.session_state:
    st.session_state.indice = 0
    st.session_state.punteggio = 0
    st.session_state.fine = False
    st.session_state.risposto = False

# Mostra domanda (il tuo codice è corretto, lo ometto per brevità)
if not st.session_state.fine:
    q = domande[st.session_state.indice]
    
    # Assicurati che il percorso dell'immagine sia corretto.
    # Se le immagini sono nella stessa directory dello script o in una sottocartella "immagini", questo va bene.
    # Altrimenti, potresti dover modificare il percorso.
    try:
        st.image(os.path.join("immagini", q["immagine"]), width=300)
    except FileNotFoundError:
        st.warning(f"Immagine non trovata: immagini/{q['immagine']}. Assicurati che il file esista nel percorso specificato.")
        st.image("https://via.placeholder.com/300x200?text=Immagine+non+trovata", width=300) # Immagine placeholder

    st.subheader(q["domanda"])
    scelta = st.radio("Scegli una risposta:", q["opzioni"], key=f"domanda_{st.session_state.indice}") # Usiamo una chiave unica

    if st.button("Verifica risposta", key=f"verifica_{st.session_state.indice}") and not st.session_state.risposto:
        st.session_state.risposto = True
        if scelta == q["corretta"]:
            st.success("Bravo! Hai risposto correttamente 🎉")
            st.session_state.punteggio += 1
        else:
            st.error("Risposta sbagliata 😕")
            st.info(f"Spiegazione: {q['spiegazione']}")

    if st.session_state.risposto:
        if st.button("Prossima domanda", key=f"prossima_{st.session_state.indice}"):
            st.session_state.indice += 1
            st.session_state.risposto = False
            if st.session_state.indice >= len(domande):
                st.session_state.fine = True
            st.experimental_rerun() # Forza un re-run per mostrare la nuova domanda subito
else:
    st.balloons()
    st.success(f"Hai completato il quiz! ✅ Punteggio: {st.session_state.punteggio} su {len(domande)}")
    if st.button("Ricomincia"):
        st.session_state.indice = 0
        st.session_state.punteggio = 0
        st.session_state.fine = False
        st.session_state.risposto = False
        st.experimental_rerun() # Forza un re-run per ricominciare il quiz

st.markdown("---")

### Sezione chatbot AI con Hugging Face (Modificata)

st.markdown("---")
st.header("🤖 Chatta con AI-nstein")

user_question = st.text_input("Fai una domanda di scienze:", key="chatbot_input") # Aggiunto key

if "hf_api_key" not in st.session_state:
    # È buona pratica chiedere la chiave direttamente se non è nei secrets
    st.session_state.hf_api_key = st.secrets.get("HF_API_KEY", "") 

def chiedi_a_huggingface(messaggio_utente):
    MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.3" # Il tuo modello

    # --- QUESTA È LA RIGA DA MODIFICARE ---
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}" # URL CORRETTO per l'API di inferenza

    headers = {"Authorization": f"Bearer {st.session_state.hf_api_key}"}
    payload = {
        "inputs": f"[INST] Sei un assistente simpatico ma scientificamente rigoroso. Rispondi alla seguente domanda per studenti delle scuole medie: {messaggio_utente} [/INST]",
        "options": {"wait_for_model": True}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status() # Lancia un'eccezione per codici di stato HTTP errati (4xx o 5xx)
        
        if response.json() and isinstance(response.json(), list) and len(response.json()) > 0 and "generated_text" in response.json()[0]:
            generated_text = response.json()[0]["generated_text"]
            return generated_text.split("[/INST]")[-1].strip()
        else:
            return "❌ Errore nella risposta dell'API di Hugging Face: formato inatteso."
    except requests.exceptions.RequestException as e:
        return f"❌ Errore di connessione o API: {e}"
    except Exception as e:
        return f"❌ Si è verificato un errore inaspettato: {e}"

if user_question and st.session_state.hf_api_key:
    with st.spinner("AI-nstein sta pensando..."):
        risposta = chiedi_a_huggingface(user_question)
        st.success(risposta)
elif user_question:
    st.warning("⚠️ Inserisci la tua Hugging Face API Key nei secrets per usare il chatbot.")
