import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- MOBİL GÖRÜNÜM AYARLARI ---
st.set_page_config(
    page_title="RizzMaster",
    page_icon="🔥",
    layout="centered"
)

# --- TASARIM (CSS) ---
# Uygulamayı karanlık mod ve modern butonlarla süsleyelim
st.markdown("""
<style>
    .stApp {background-color: #0E1117;}
    h1 {color: #FF4B4B; text-align: center;}
    .stButton button {
        width: 100%;
        border-radius: 20px;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 15px;
    }
    .reply-box {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
        border-left: 5px solid #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)

# --- API ANAHTARI (OTOMATİK) ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("API Anahtarı yok! Secrets ayarını kontrol et.")
        st.stop()
except:
    st.stop()

# --- BAŞLIK VE LOGO ---
st.title("🔥 RizzMaster")
st.write("Sohbet tıkandı mı? Ekran görüntüsünü (SS) at, koçun devreye girsin.")

# --- FOTOĞRAF YÜKLEME ---
uploaded_file = st.file_uploader("Sohbet SS'ini Yükle", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    # Yüklenen resmi göster
    st.image(uploaded_file, caption="Analiz Ediliyor...", use_column_width=True)
    
    # Analiz Butonu
    if st.button("KOÇA SOR (ANALİZ ET) 🚀"):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('Koç karşı tarafın psikolojisini okuyor...'):
                image = Image.open(uploaded_file)
                
                # --- SİHİRLİ PROMPT (GİZLİ FORMÜL) ---
                prompt = """
                Sen dünyanın en iyi 'Dating Coach'u ve İletişim Uzmanısın (Red Pill farkındalığına sahip).
                Bu bir flört uygulaması veya WhatsApp sohbet ekran görüntüsü.
                
                GÖREVLERİN:
                1. DURUM ANALİZİ: Karşı tarafın ilgisi nasıl? (Yüksek/Düşük/Oynuyor). Kullanıcı çok mu 'muhtaç' (needy) davranmış? (Kısa ve sert yorumla).
                2. TAKTİK: Sohbeti kurtarmak veya zirveye taşımak için 3 FARKLI CEVAP ÖNERİSİ yaz.
                
                ÇIKTI FORMATI (Aynen böyle yaz):
                
                ### 🧠 KOÇUN ANALİZİ
                (Buraya sert ve gerçekçi analizini yaz)
                
                ### 🎯 CEVAP SEÇENEKLERİ
                
                **1. ALFA / ÖZGÜVENLİ (Cesur ol):**
                (Cevap önerisi)
                
                **2. EĞLENCELİ / TROLL (Güldür ve Şaşırt):**
                (Cevap önerisi)
                
                **3. GİZEMLİ (Merak Uyandır):**
                (Cevap önerisi)
                
                **⚠️ GÖREV:** (Bugün yapması gereken ufak bir davranış görevi ver. Örn: 2 saat yazma.)
                """
                
                response = model.generate_content([prompt, image])
                
                # Sonucu Göster
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Hata: {e}")
            st.info("Resim çok büyük olabilir veya API kotası dolmuş olabilir.")

else:
    # Boşken görünen kısım
    st.info("👆 Başlamak için yukarıya tıkla ve ekran görüntüsünü seç.")
    st.caption("Tinder, Bumble, WhatsApp, Instagram DM uyumludur.")
