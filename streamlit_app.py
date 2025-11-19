import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="RizzMaster",
    page_icon="🔥",
    layout="centered"
)

# --- TASARIM ---
st.markdown("""
<style>
    .stApp {background-color: #0E1117;}
    h1 {color: #FF4B4B; text-align: center;}
    .stMarkdown p {text-align: center; color: #FAFAFA;}
    .stButton button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(45deg, #FF4B4B, #FF914D);
        color: white;
        font-weight: bold;
        padding: 12px;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# --- API ANAHTARI ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("⚠️ API Anahtarı yok! Secrets ayarını yapın.")
        st.stop()
except:
    st.stop()

# --- MODELİ OTOMATİK BUL (HATA ÖNLEYİCİ) ---
def get_vision_model():
    genai.configure(api_key=api_key)
    # Sistemdeki modelleri tara
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            # Experimental (ücretli/kotasız) olmayan ve 1.5 olanı bul
            if 'exp' not in m.name and '1.5' in m.name:
                return m.name
    # Bulamazsa varsayılanı döndür
    return 'gemini-1.5-flash'

# --- ARAYÜZ ---
st.title("🔥 RizzMaster")
st.write("Sohbet tıkandı mı? SS'i at, Koç devreye girsin.")

uploaded_file = st.file_uploader("Ekran Görüntüsü Yükle", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    st.image(uploaded_file, caption="Görüntü Alındı", use_container_width=True)
    
    if st.button("🚀 KOÇA SOR (ANALİZ ET)"):
        try:
            target_model = get_vision_model() # Otomatik model seçimi
            model = genai.GenerativeModel(target_model)
            
            with st.spinner(f'Koç analiz ediyor... (Model: {target_model})'):
                image = Image.open(uploaded_file)
                
                prompt = """
                Sen dünyanın en iyi Dating Coach'u ve İletişim Uzmanısın (Red Pill farkındalığına sahip).
                Kullanıcı sana bir flört uygulaması veya WhatsApp sohbet ekran görüntüsü attı.
                
                GÖREVLERİN:
                1. DURUM ANALİZİ: Karşı tarafın ilgisi nasıl? Kullanıcı hata yapmış mı? (Kısa, sert ve gerçekçi ol).
                2. TAKTİK: Sohbeti kurtarmak için 3 FARKLI CEVAP ÖNERİSİ ver.
                
                ÇIKTI FORMATI:
                ### 🧠 KOÇUN ANALİZİ
                ...
                ### 🔥 CEVAP SEÇENEKLERİ
                **1. ALFA (Cesur):** ...
                **2. EĞLENCELİ (Troll):** ...
                **3. GİZEMLİ:** ...
                
                **⚠️ GÜNLÜK GÖREV:** ...
                """
                
                response = model.generate_content([prompt, image])
                
                st.markdown("---")
                st.success("Analiz Tamamlandı!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Hata: {e}")
            st.info("Streamlit sayfasını yenileyip (Reboot) tekrar deneyin.")
else:
    st.info("👆 Ekran görüntüsü yükleyerek başla.")
