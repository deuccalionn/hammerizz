import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="RizzMaster",
    page_icon="🔥",
    layout="centered"
)

# --- TASARIM (KARANLIK MOD & MODERN ARAYÜZ) ---
st.markdown("""
<style>
    /* Arka planı koyu yapalım */
    .stApp {background-color: #0E1117;}
    
    /* Başlık Rengi */
    h1 {color: #FF4B4B; text-align: center; font-family: 'Helvetica', sans-serif;}
    
    /* Alt Başlık */
    .stMarkdown p {text-align: center; color: #FAFAFA;}
    
    /* Buton Tasarımı (Büyük ve Çekici) */
    .stButton button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(45deg, #FF4B4B, #FF914D);
        color: white;
        font-weight: bold;
        font-size: 18px;
        padding: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
    }
    .stButton button:hover {
        background: linear-gradient(45deg, #FF914D, #FF4B4B);
    }

    /* Cevap Kutusu Tasarımı */
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# --- GİZLİ ANAHTAR KONTROLÜ ---
try:
    if "GOOGLE_API_KEY" in st.secrets:
        api_key = st.secrets["GOOGLE_API_KEY"]
    else:
        st.error("⚠️ API Anahtarı bulunamadı. Lütfen Streamlit 'Secrets' ayarlarını yapın.")
        st.stop()
except:
    st.stop()

# --- ARAYÜZ ---
st.title("🔥 RizzMaster")
st.write("Flört uygulamasında veya WhatsApp'ta tıkandın mı? Ekran görüntüsünü at, **Koç** senin yerine cevaplasın.")

st.markdown("---")

# Dosya Yükleme
uploaded_file = st.file_uploader("Sohbet SS'ini Buraya Bırak", type=["jpg", "png", "jpeg"], label_visibility="collapsed")

if uploaded_file:
    # Resmi ortalayarak göster
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(uploaded_file, caption="Analiz Ediliyor...", use_container_width=True)
    
    st.write("") # Boşluk
    
    # Analiz Butonu
    if st.button("🚀 KOÇA SOR (ANALİZ ET)"):
        try:
            genai.configure(api_key=api_key)
            # Vision destekli en hızlı model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner('Koç karşı tarafın psikolojisini çözüyor... 🧠'):
                image = Image.open(uploaded_file)
                
                # --- SİHİRLİ PROMPT (RED PILL / FLÖRT KOÇU) ---
                prompt = """
                Sen dünyanın en iyi 'Dating Coach'u ve İletişim Uzmanısın (Red Pill ve Maskülenite farkındalığına sahip).
                Kullanıcı sana bir flört uygulaması (Tinder/Bumble) veya WhatsApp sohbet ekran görüntüsü attı.
                
                GÖREVLERİN:
                1. 🕵️‍♂️ DURUM ANALİZİ: Karşı tarafın ilgisi yüksek mi düşük mü? Kullanıcı hata yapmış mı (fazla 'needy'/muhtaç mı)? Kısa ve net, lafı dolandırmadan söyle.
                2. 🎯 TAKTİK: Sohbeti kurtarmak veya bir sonraki aşamaya (buluşmaya) taşımak için 3 FARKLI CEVAP ÖNERİSİ ver.
                
                ÇIKTI FORMATI:
                
                ### 🧠 KOÇUN ANALİZİ
                (Buraya analizini yaz. Sert ama eğitici ol.)
                
                ### 🔥 CEVAP SEÇENEKLERİ
                
                **1. ALFA / ÖZGÜVENLİ (Risk Al):**
                (Direkt ve cesur bir cevap)
                
                **2. EĞLENCELİ / TROLL (Güldür):**
                (Espri içeren, ortamı yumuşatan cevap)
                
                **3. GİZEMLİ (Merak Uyandır):**
                (Kısa ve düşündüren cevap)
                
                **⚠️ GÜNLÜK GÖREV:** (Kullanıcının özgüvenini artıracak ufak bir görev ver. Örn: Telefonu 1 saat uçak moduna al.)
                """
                
                response = model.generate_content([prompt, image])
                
                # Sonucu Şık Bir Kutuda Göster
                st.markdown("---")
                st.success("Analiz Tamamlandı!")
                st.markdown(response.text)
                
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
            st.info("İpucu: Resim formatı desteklenmiyor olabilir veya API kotası dolmuş olabilir.")

else:
    # Boşken Kullanıcıyı Yönlendir
    st.info("👆 Başlamak için yukarıya tıkla ve ekran görüntüsünü seç.")
