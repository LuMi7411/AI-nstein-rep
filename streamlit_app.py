import streamlit as st
import random
import os
import requests

st.set_page_config(page_title="AI-nstein - Scienze", page_icon="🧬", layout="centered")
st.title("🔬 AI-nstein - Ripasso di Scienze")
st.markdown("💪 **Powered by MICHELE CASTRIOTTA** v1 del 22/06/2025")
st.markdown("Rispondi alle domande di Scienze! Se sbagli, ti spiego. 🤓")

# Domande (Il tuo array di domande è corretto, lo ometto per brevità)
domande = [
    {
        "domanda": "Secondo quale teoria geologica i continenti migrano, spostandosi sullo strato inferiore della crosta terrestre?",
        "opzioni": ["Tettonica a zolle", "Deriva dei continenti", "Espansione dei fondali"],
        "corretta": "Deriva dei continenti",
        "spiegazione": "La deriva dei continenti è una teoria geologica secondo la quale i continenti migrano sullo strato inferiore della crosta terrestre. Le zolle o placche che costituiscono la crosta terrestre si spostano di appena pochi centimetri ogni anno. Tuttavia, nei milioni di anni d'età del nostro pianeta, hanno percorso migliaia di chilometri. Fonte: Wikipedia/Deriva dei continenti",
        "immagine": "pangea.png"
    },
    {
        "domanda": "Il magma a differenza della lava, è materiale fuso ricco di?",
        "opzioni": ["Gas", "Ferro", "Ghiaccio"],
        "corretta": "Gas",
        "spiegazione": "Dal punto di vista geochimico, il magma è distinto dalla lava, poiché possiede ancora la componente gassosa disciolta. Fonte: Wikipedia\Magma",
        "immagine": "lava.png"
    },
    {
        "domanda": "Le rocce clastiche sono rocce:",
        "opzioni": [
            "Ignee intrusive",
            "Ignee effusive ",
            "Sedimentarie"
        ],
        "corretta": "Sedimentarie",
        "spiegazione": "Le rocce sedimentarie clastiche derivano da sedimenti i cui elementi costituenti a loro volta derivano principalmente dall'accumulo di frammenti litici di altre rocce alterate trasportati in genere da agenti esogeni diversi. Fonte: Wikipedia\Roccia sedimentaria clastica.",
        "immagine": "rocce.png"
    },
    {
        "domanda": "Quali onde sismiche sono più pericolose?",
        "opzioni": ["Onde S", "Onde P", "Onde superficiali"],
        "corretta": "Onde superficiali",
        "spiegazione": "Le onde di superficie che si generano nell'epicentro a causa dell'arrivo delle onde P ed S. Sono le onde più pericolose, quelle che causano la maggior parte dei danni nei terremoti. Fonte: Wikiversità\Terremoti.",
        "immagine": "terremoto.png"
    },
    {
        "domanda": "Qual é la probabilità che lanciando due volte una moneta esca testa in entrambi i lanci?",
        "opzioni": ["25%", "50%", "75%"],
        "corretta": "25%",
        "spiegazione": "Il caso favorevole è uno mentre i casi possibili sono quattro: testa-testa, testa-croce, croce-testa, croce-croce.",
        "immagine": "moneta.png"
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
            st.rerun() # Forza un re-run per mostrare la nuova domanda subito
else:
    st.balloons()
    st.success(f"Hai completato il quiz! ✅ Punteggio: {st.session_state.punteggio} su {len(domande)}")
    if st.button("Ricomincia"):
        st.session_state.indice = 0
        st.session_state.punteggio = 0
        st.session_state.fine = False
        st.session_state.risposto = False
        st.rerun() # Forza un re-run per ricominciare il quiz

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
