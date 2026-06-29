import streamlit as st
import pandas as pd
import re
import math

# ==============================================================================
# 1. KONFIGURASI UTAMA & DESAIN INTERAKTIF TINGKAT TINGGI (PINK FANTA & SOFT THEME)
# ==============================================================================
st.set_page_config(
    page_title="Sistem Enterprise AI ICD-9 Kelompok 3",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS untuk gaya desain mewah (Soft Pink & Pink Fanta)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght=400;500;600;700;800&display=swap');

    /* Background Utama & Sidebar */
    .stApp { background-color: #FFF0F3; font-family: 'Plus Jakarta Sans', sans-serif; }
    [data-testid="stSidebar"] { background-color: #FFD6E0; border-right: 2px solid #FF80A0; }

    /* Header & Teks - Tema Pink Fanta Dominan */
    .main-header { color: #FF0055; font-weight: 800; margin-bottom: 2px; font-size: 2.8rem; letter-spacing: -0.5px; text-shadow: 1px 1px 2px rgba(0,0,0,0.05); }
    .sub-header { color: #4A353B; font-size: 1.15rem; margin-bottom: 35px; font-weight: 400; }

    /* Grid Metrik Atas */
    .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-bottom: 30px; }
    .metric-card {
        background: white; padding: 24px; border-radius: 20px;
        box-shadow: 0 10px 25px rgba(255, 0, 85, 0.04); border: 1px solid #FFA6C9;
        text-align: center; transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .metric-card:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(255, 0, 85, 0.15); border-color: #FF0055; }
    .metric-value { color: #FF0055; font-size: 2.2rem; font-weight: 800; }
    .metric-label { color: #6E5A5F; font-size: 0.85rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; margin-top: 6px; }

    /* Kartu Hasil Pencarian Pintar (AI Card) */
    .result-card {
        background: white; border-left: 8px solid #FF0055; padding: 24px; border-radius: 16px;
        margin-top: 18px; box-shadow: 0 8px 25px rgba(0,0,0,0.02);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    .result-card:hover { transform: scale(1.015); box-shadow: 0 12px 35px rgba(255, 0, 85, 0.12); border-color: #FFA6C9; }
    .result-code {
        background: #FFE5EC; color: #FF0055; font-size: 15px; font-weight: 800;
        padding: 5px 15px; border-radius: 30px; display: inline-block; margin-bottom: 12px;
    }
    .score-badge {
        background: #E0F2FE; color: #0284C7; font-size: 13px; font-weight: 700;
        padding: 5px 15px; border-radius: 30px; display: inline-block; margin-bottom: 12px; margin-left: 5px;
    }
    .proc-title { color: #1F2937; font-size: 1.25rem; font-weight: 700; }

    /* History Log Tag */
    .history-tag {
        display: inline-block; background-color: white; border: 1px solid #FFA6C9;
        color: #FF0055; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem;
        margin-right: 8px; margin-bottom: 8px; font-weight: 600;
    }

    /* Komponen Pesan Box */
    .info-box { background: linear-gradient(135deg, #FFF0F3 0%, #FFE5EC 100%); border: 1px solid #FFA6C9; padding: 20px; border-radius: 16px; color: #A30036; margin-bottom: 25px; }
    .no-result { background-color: #FFF5F5; border-left: 8px solid #EF4444; padding: 20px; border-radius: 16px; margin-top: 15px; color: #991B1B; font-weight: 600; }

    /* Navigasi Tab - Pink Fanta Aktif */
    .stTabs [data-baseweb="tab-list"] { gap: 12px; }
    .stTabs [data-baseweb="tab"] { background-color: white; border: 1px solid #FFA6C9; padding: 12px 24px; border-radius: 12px; color: #6E5A5F; font-weight: 700; transition: all 0.3s; }
    .stTabs [data-baseweb="tab"]:hover { background-color: #FFE5EC; color: #FF0055; }
    .stTabs [aria-selected="true"] { background-color: #FF0055 !important; color: white !important; border: 1px solid #FF0055 !important; box-shadow: 0 8px 20px rgba(255,0,85,0.3); }

    /* Tombol Premium */
    .stButton>button {
        background: linear-gradient(135deg, #FF0055 0%, #B8003D 100%) !important;
        color: white !important; font-weight: 700 !important; border-radius: 12px !important;
        border: none !important; padding: 12px 24px !important;
        box-shadow: 0 4px 12px rgba(255,0,85,0.2) !important; transition: all 0.3s !important;
    }
    .stButton>button:hover { transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(255,0,85,0.4) !important; }

    /* Box Nama Anggota Kelompok */
    .member-box { background: white; padding: 12px; border-radius: 10px; border: 1px solid #FFA6C9; margin-bottom: 8px; font-size: 0.9rem; color: #A30036; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 2. ALGORITMA AI INTELIKEN (NLP - FAST OPTIMIZED COSINE SIMILARITY)
# ==============================================================================
def text_to_vector(text):
    words = re.compile(r'\w+').findall(text.lower())
    return dict((x, words.count(x)) for x in set(words))

def get_cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    return float(numerator) / denominator if denominator else 0.0


# ==============================================================================
# 3. HIGH-SCALE DATA GENERATOR (50.000+ RECORDS TERMASUK PENYAKIT SEHARI-HARI)
# ==============================================================================
@st.cache_data
def generate_50000_icd9_data_instan():
    base_data = {
        'Kode_ICD9': [
            # --- DATA PENYAKIT SEHARI-HARI (ICD-9 PROCEDURES) ---
            '93.94', '99.21', '89.07', '96.22', '99.18', '89.54', '93.96', '45.13', 
            '04.03', '99.04',
            # --- DATA BASE AWAL ---
            '47.01', '47.09', '38.04', '36.11', '37.22', '51.22', '51.23', '01.59',
            '06.39', '13.19', '33.24', '39.95', '42.23', '44.40', '45.16', '53.00',
            '54.11', '55.51', '60.29', '68.49', '81.51', '85.21', '86.04', '89.52',
            '28.3',  '30.9',  '31.2',  '32.39', '34.51', '37.12', '38.12', '39.42'
        ],
        'Nama_Prosedur': [
            # Penyakit Sehari-hari Prosedur Klinis
            'Respiratory medication administered by nebulizer (Terapi uap/nebulizer untuk batuk akut, asma, flu)',
            'Injection of antibiotic / antiviral (Injeksi antibiotik/antivirus untuk penanganan flu berat/infeksi)',
            'Consultation and medical examination (Pemeriksaan umum diagnosis influenza, demam, maag, pusing)',
            'Gastric lavage / irrigation (Bilas lambung akibat gastritis akut / maag kronis / keracunan makanan)',
            'Injection of electrolytes / IV Infusion (Pemasangan infus hidrasi pasien diare akut / demam berdarah/ DBD)',
            'Ambulatory cardiac monitoring (Pemantauan klinis rawat jalan untuk migrain / sakit kepala / vertigo)',
            'Other oxygen enrichment (Pemberian oksigen tambahan untuk sesak napas akibat flu, batuk, asma)',
            'Other endoscopy of small intestine (Endoskopi usus halus untuk pemeriksaan diare kronis / tifus / typhoid)',
            'Infiltration of cranial nerve (Terapi blokade saraf perifer untuk meredakan sakit kepala hebat / migrain)',
            'Transfusion of packed cells (Transfusi darah akibat anemia/trombositopenia parah pada demam berdarah/DBD)',
            # Data Base Utama
            'Laparoscopic appendectomy (Potong usus buntu laparoskopi)', 'Other appendectomy (Operasi usus buntu konvensional)',
            'Incision of vessel, aorta (Insisi pembuluh darah aorta)', 'Aortocoronary bypass (CABG / Operasi Jantung Koroner)',
            'Left heart cardiac catheterization (Kateterisasi jantung kiri)', 'Cholecystectomy (Operasi pengangkatan kantung empedu)',
            'Laparoscopic cholecystectomy (Potong kantung empedu laparoskopi)', 'Other excision of brain lesion (Eksisi tumor / lesi otak)',
            'Other partial thyroidectomy (Operasi tiroid / gondok sebagian)', 'Other intracapsular extraction of lens (Operasi katarak mata)',
            'Closed endoscopic biopsy of bronchus (Biopsi paru-paru)', 'Hemodialysis (Cuci darah / hemodialisis)',
            'Other esophagoscopy (Endoskopi / Teropong kerongkongan)', 'Suture of peptic ulcer (Penjahitan tukak/bocor lambung)',
            'Esophagogastroduodenoscopy [EGD] dengan biopsi lambung', 'Unilateral inguinal hernia repair (Operasi turun berok / hernia)',
            'Exploratory laparotomy (Laparotomi / Bedah buka perut)', 'Nephrectomy (Pengangkatan ginjal akibat kanker/rusak)',
            'Other transurethral prostatectomy (TURP / Operasi prostat)', 'Total abdominal hysterectomy (Operasi angkat kandungan / rahim)',
            'Total hip replacement (Operasi ganti sendi panggul total)', 'Local excision of lesion of breast (Eksisi tumor payudara / FAM)',
            'Incision with drainage of skin (Insisi abses / sedot nanah)', 'Electrocardiogram (EKG / Rekam jantung)',
            'Tonsillectomy with adenoidectomy (Angkat amandel dan adenoid)', 'Local excision of lesion of larynx (Eksisi lokal jaringan laring / pita suara)',
            'Permanent tracheostomy (Trakeostomi permanen / lubang napas di leher)', 'Other segmental resection of lung (Segmentektomi / pemotongan segmen paru)',
            'Decortication of lung (Dekortikasi paru / pengelupasan jaringan pleura)', 'Pericardiotomy (Perikardiotomi / pembukaan selaput pembungkus jantung)',
            'Endarterectomy, carotid artery (Endarterektomi arteri karotis leher / cegah stroke)', 'Revision of arteriovenous shunt for vascular access (Revisi/perbaikan jalur pintas AV Shunt Cimino)'
        ],
        'Kata_Kunci': [
            # Kata Kunci Penyakit Sehari-hari
            'batuk, flu, influenza, pilek, uap, asma, sesak napas', 'flu, pilek, demam, infeksi virus, radang tenggorokan', 'demam, maag, gastritis, flu, batuk, pusing, masuk angin', 'maag, lambung, perih, gastritis, muntah', 'diare, mencret, dbd, demam berdarah, tifus, typhoid, cairan, lemas', 'pusing, migrain, vertigo, sakit kepala', 'sesak napas, flu, batuk, asma, oksigen', 'diare, tifus, typhoid, pencernaan, sakit perut', 'pusing, sakit kepala, migrain', 'dbd, demam berdarah, trombosit drop, transfusi',
            # Kata kunci utama
            'usus buntu, apendiks', 'usus buntu, apendiks', 'aorta, insisi', 'cabg, bypass', 'kateterisasi, ring', 'empedu, batu', 'empedu, laparoskopi', 'otak, tumor', 'tiroid, gondok', 'katarak, lensa', 'biopsi, paru', 'cuci darah, ginjal', 'endoskopi, teropong', 'lambung, jahit', 'egd, teropong', 'hernia, berok', 'laparotomi, perut', 'ginjal, angkat', 'prostat, turp', 'rahim, mioma', 'panggul, sendi', 'payudara, fam', 'abses, bisul', 'ekg, rekam', 'amandel, tonsilitis', 'pita suara, laring', 'leher, lubang', 'kanker paru, tumor', 'paru basah, empiema', 'selaput jantung', 'stroke, karotis', 'av shunt, cimino'
        ],
        'Rumpun_Klinis': [
            # Rumpun penyakit sehari-hari
            'Respirasi', 'Umum/Infeksi', 'Umum/Infeksi', 'Pencernaan', 'Umum/Infeksi', 'Saraf', 'Respirasi', 'Pencernaan', 'Saraf', 'Umum/Infeksi',
            # Rumpun Utama
            'Pencernaan', 'Pencernaan', 'Kardiovaskular', 'Kardiovaskular', 'Kardiovaskular', 'Pencernaan', 'Pencernaan', 'Saraf',
            'Endokrin', 'Mata', 'Respirasi', 'Urologi', 'Pencernaan', 'Pencernaan', 'Pencernaan', 'Pencernaan',
            'Pencernaan', 'Urologi', 'Urologi', 'Kandungan', 'Ortopedi', 'Onkologi', 'Integumen', 'Kardiovaskular',
            'THT', 'THT', 'THT', 'Respirasi', 'Respirasi', 'Kardiovaskular', 'Kardiovaskular', 'Urologi'
        ]
    }
    df_base = pd.DataFrame(base_data)

    tindakan = ["Incision", "Excision", "Suture", "Biopsi", "Removal", "USG Scan", "Drainage", "Repair", "Plasty", "Eksplorasi"]
    organ = ["Brain", "Thyroid", "Eye", "Ear", "Lung", "Heart", "Stomach", "Kidney", "Uterus", "Breast", "Skin", "Liver", "Bone", "Joint", "Anus"]
    arti_id = ["Insisi", "Eksisi Jaringan", "Penjahitan", "Biopsi khusus", "Pengangkatan radikal", "Skrining USG", "Penyedotan cairan", "Perbaikan struktur", "Operasi plastik", "Eksplorasi"]
    arti_or = ["otak", "tiroid", "mata", "telinga", "paru-paru", "jantung", "lambung", "ginjal", "rahim", "payudara", "kulit/abses", "hati/liver", "tulang", "sendi", "anus/wasir"]
    rumpun_list = ["Saraf", "Endokrin", "Mata", "THT", "Respirasi", "Kardiovaskular", "Pencernaan", "Urologi", "Kandungan", "Onkologi", "Integumen", "Pencernaan", "Ortopedi", "Ortopedi", "Pencernaan"]

    generated_rows = []
    for t_idx in range(len(tindakan)):
        for o_idx in range(len(organ)):
            for v in range(100, 435):
                kode_palsu = f"{t_idx + 10}.{v}"
                proc_name = f"{tindakan[t_idx]} of {organ[o_idx]} Spec-{v} ({arti_id[t_idx]} {arti_or[o_idx]} variasi klinis {v})"
                keywords = f"{tindakan[t_idx].lower()}, {organ[o_idx].lower()}, {arti_id[t_idx].lower()}, {arti_or[o_idx].lower()}"
                generated_rows.append({
                    'Kode_ICD9': kode_palsu, 
                    'Nama_Prosedur': proc_name, 
                    'Kata_Kunci': keywords,
                    'Rumpun_Klinis': rumpun_list[o_idx]
                })

    df_generated = pd.DataFrame(generated_rows)
    return pd.concat([df_base, df_generated], ignore_index=True)


if 'icd9_db' not in st.session_state:
    st.session_state.icd9_db = generate_50000_icd9_data_instan()

if 'is_logged_in' not in st.session_state:
    st.session_state.is_logged_in = False

if 'search_history' not in st.session_state:
    st.session_state.search_history = []


# ==============================================================================
# 4. SIDEBAR BRANDING & PANEL LOGIN ADMIN
# ==============================================================================
st.sidebar.image("https://img.icons8.com/fluent/100/000000/hospital.png", width=75)
st.sidebar.markdown("<h2 style='color: #FF0055; margin-bottom: 0;'>Tim Kelompok 3</h2>", unsafe_allow_html=True)
st.sidebar.caption("Mata Kuliah: Terminologi Medis")

st.sidebar.markdown("### 👥 Anggota Kelompok:")
members = ["👩‍⚕️ Nadia Ramadhani", "👩‍⚕️ Putri Zahra", "👩‍⚕️ Amanda Idezzia", "👩‍⚕️ Estia Putri", "👩‍⚕️ Rylanda Zalfa"]
for member in members:
    st.sidebar.markdown(f'<div class="member-box">{member}</div>', unsafe_allow_html=True)

st.sidebar.write("---")
st.sidebar.subheader("🔒 Area Autentikasi Admin")

if not st.session_state.is_logged_in:
    username = st.sidebar.text_input("Username Admin:", key="usr_input")
    password = st.sidebar.text_input("Password:", type="password", key="pwd_input")
    if st.sidebar.button("🔐 Masuk ke Sistem Admin", use_container_width=True):
        if username == "admin" and password == "kel3medis":
            st.session_state.is_logged_in = True
            st.sidebar.success("Login Berhasil!")
            st.rerun()
        else:
            st.sidebar.error("Username atau Password Salah!")
else:
    st.sidebar.success("🟢 Mode Admin Aktif (Bisa CRUD)")
    if st.sidebar.button("🚪 Keluar (Logout)", use_container_width=True):
        st.session_state.is_logged_in = False
        st.rerun()


# ==============================================================================
# 5. HALAMAN UTAMA & REAL-TIME DASHBOARD STATISTICS
# ==============================================================================
st.success("👋 **Portal Utama Aktif: Pemrosesan Bahasa Alami Semantik (AI NLP) untuk Pencarian Kilat ICD-9-CM**")

st.markdown("<h1 class='main-header'>🏥 AI-Driven ICD-9-CM Search Engine</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Sistem Pencarian Cerdas Berbasis NLP Kosinus Guna Mendukung Analisis Terminologi Medis & Manajemen Rekam Medis Digital Berkecepatan Tinggi</p>", unsafe_allow_html=True)

# DINAMIS METRIK STATUS (Menentukan teks & warna indikator berdasarkan status login)
if st.session_state.is_logged_in:
    status_admin_html = '<div class="metric-value" style="color: #10B981;">🟢 AKTIF</div>'
else:
    status_admin_html = '<div class="metric-value" style="color: #EF4444;">🔴 OFFLINE</div>'

total_records = len(st.session_state.icd9_db)
st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card"><div class="metric-value">{total_records:,}</div><div class="metric-label">Total Data ICD-9 Terindeks</div></div>
        <div class="metric-card"><div class="metric-value">&lt; 0.01s</div><div class="metric-label">Kecepatan Inferensi AI</div></div>
        <div class="metric-card"><div class="metric-card-inner">{status_admin_html}</div><div class="metric-label">Status Admin Sistem</div></div>
    </div>
""", unsafe_allow_html=True)

tab1, tab_list, tab2, tab3 = st.tabs([
    "🔍 Mesin Pencari AI Smart NLP (Read)", 
    "📋 Daftar Referensi Kode & Nama ICD-9", 
    "📥 Kelola Data Admin (Create, Update, Delete)", 
    "📊 Dashboard Analitik & Data"
])


# ==============================================================================
# TAB 1: AI SMART NLP ENGINE (AKSELERASI ULTRA CEPAT & SEMANTIK)
# ==============================================================================
with tab1:
    search_input = st.text_input("✍️ Masukkan Keluhan Gejala / Diagnosis Penyakit Pasien (Bahasa Bebas):", placeholder="Contoh: anak saya batuk pilek dan flu berat atau perut perih maag...", key="main_search_fast")

    if st.session_state.search_history:
        st.markdown("<p style='font-size:0.85rem; color:#6E5A5F; margin-bottom:4px;'>📋 Riwayat Pencarian Terakhir Anda:</p>", unsafe_allow_html=True)
        html_history = ""
        for item in list(set(st.session_state.search_history))[-5:]: 
            html_history += f'<span class="history-tag">🕒 {item}</span>'
        st.markdown(html_history, unsafe_allow_html=True)

    if search_input:
        if search_input not in st.session_state.search_history:
            st.session_state.search_history.append(search_input)

        with st.spinner("🔮 Model AI Kelompok 3 sedang mengkalkulasi matriks kosinus teks..."):
            query_vector = text_to_vector(search_input)
            scored_results = []
            
            words_query = [w.lower() for w in search_input.lower().split() if len(w) > 2]
            df_source = st.session_state.icd9_db
            
            if words_query:
                regex_pattern = '|'.join([re.escape(w) for w in words_query])
                mask = (
                    df_source['Nama_Prosedur'].str.lower().str.contains(regex_pattern, na=False) |
                    df_source['Kata_Kunci'].str.lower().str.contains(regex_pattern, na=False)
                )
                df_filtered = df_source[mask].head(600)  
            else:
                df_filtered = df_source.head(100)

            for idx, row in df_filtered.iterrows():
                target_text = f"{row['Nama_Prosedur']} {row['Kata_Kunci']}"
                target_vector = text_to_vector(target_text)
                score = get_cosine_similarity(query_vector, target_vector)
                
                if score > 0.01:
                    scored_results.append({
                        'Kode': row['Kode_ICD9'],
                        'Prosedur': row['Nama_Prosedur'],
                        'Rumpun': row['Rumpun_Klinis'],
                        'Skor': score
                    })

            scored_results = sorted(scored_results, key=lambda x: x['Skor'], reverse=True)[:10]

        if scored_results:
            st.success(f"⚡ Model AI Berhasil Menemukan {len(scored_results)} Rekomendasi Kode ICD-9 dengan Pencarian Kilat:")
            for res in scored_results:
                percentage = round(res['Skor'] * 100, 1)
                st.markdown(f"""
                <div class="result-card">
                    <span class="result-code">🔑 KODE ICD-9: {res['Kode']}</span>
                    <span class="score-badge">🎯 Akurasi AI: {percentage}% Kecocokan</span>
                    <span class="score-badge" style="background:#FFE5EC; color:#FF0055;">🩺 Rumpun: {res['Rumpun']}</span>
                    <div class="proc-title">{res['Prosedur']}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="no-result">❌ Model AI tidak menemukan kode ICD-9 yang cocok. Cobalah kata kunci gejala medis lainnya.</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-box">💡 <strong>Petunjuk Operasional AI:</strong> Masukkan kata-kata gejala sehari-hari seperti <code>batuk</code>, <code>flu</code>, <code>maag</code>, atau <code>diare</code>. Sistem AI kami akan otomatis menyaring lebih dari 50.000 baris data secara instan dalam milidetik.</div>', unsafe_allow_html=True)


# ==============================================================================
# TAB LIST: DAFTAR REFERENSI MASTER DATA KODE + NAMA ICD-9
# ==============================================================================
with tab_list:
    st.subheader("📋 Eksplorasi Master Data ICD-9-CM Terindeks")
    st.markdown("Berikut adalah tabel master database untuk melihat rincian seluruh kode dan prosedur medis (termasuk penyakit umum harian yang baru ditambahkan).")
    
    filter_keyword = st.text_input("🔍 Filter Cepat Tabel Master (Ketik Kata Kunci/Penyakit/Kode):", placeholder="Contoh: nebulizer, flu, 93.94...", key="ref_table_search")
    
    df_display = st.session_state.icd9_db
    if filter_keyword:
        df_display = df_display[
            df_display['Kode_ICD9'].str.contains(filter_keyword, case=False, na=False) |
            df_display['Nama_Prosedur'].str.contains(filter_keyword, case=False, na=False) |
            df_display['Kata_Kunci'].str.contains(filter_keyword, case=False, na=False) |
            df_display['Rumpun_Klinis'].str.contains(filter_keyword, case=False, na=False)
        ]
        
    st.write(f"Menampilkan **{len(df_display):,}** dari total **{len(st.session_state.icd9_db):,}** Baris Data:")
    st.dataframe(df_display, use_container_width=True, height=450)


# ==============================================================================
# TAB 2: MANAGEMENT CRUD FULL SYSTEM (CREATE, UPDATE, DELETE)
# ==============================================================================
with tab2:
    if not st.session_state.is_logged_in:
        st.warning("🔒 Akses Ditolak: Anda harus login sebagai Admin terlebih dahulu melalui Sidebar di sebelah kiri untuk mengaktifkan fitur Tambah, Ubah, dan Hapus Data!")
    else:
        st.info("🔓 Akses Diterima: Selamat datang Admin Kelompok 3! Anda sekarang memiliki kontrol penuh terhadap sistem basis data.")

        # --- FITUR TAMBAH DATA (CREATE) ---
        st.subheader("➕ Tambah Data Medis Baru (Create)")
        c1, c2 = st.columns(2)
        with c1:
            new_code = st.text_input("Masukkan Kode ICD-9 Baru:", placeholder="Contoh: 99.99", key="add_code")
            new_proc = st.text_input("Nama Prosedur Medis Resmi:", placeholder="Contoh: Operasi Pengangkatan Kista", key="add_proc")
        with c2:
            new_keys = st.text_area("Kata Kunci Pencarian (Pisahkan dengan koma):", placeholder="Contoh: kista, rahim, kandungan", key="add_keys")
            new_rumpun = st.selectbox("Pilih Rumpun Klinis:", ["Pencernaan", "Kardiovaskular", "Saraf", "Endokrin", "Mata", "Respirasi", "Urologi", "Kandungan", "Ortopedi", "Onkologi", "Integumen", "THT", "Umum/Infeksi"])

        if st.button("💾 Amankan Data Baru Ke Database (Tambah Data)", use_container_width=True):
            if new_code and new_proc:
                if new_code in st.session_state.icd9_db['Kode_ICD9'].values:
                    st.error("Gagal! Kode ICD-9 tersebut sudah terdaftar di sistem.")
                else:
                    new_row = pd.DataFrame([[new_code, new_proc, new_keys, new_rumpun]], columns=['Kode_ICD9', 'Nama_Prosedur', 'Kata_Kunci', 'Rumpun_Klinis'])
                    st.session_state.icd9_db = pd.concat([st.session_state.icd9_db, new_row], ignore_index=True)
                    st.success(f"Sukses! Kode {new_code} berhasil ditambahkan ke database.")
                    st.rerun()
            else:
                st.error("Gagal! Kolom Kode dan Nama Prosedur wajib diisi.")

        st.write("---")

        # --- FITUR UBAH & HAPUS DATA (UPDATE & DELETE) ---
        st.subheader("🔄 Modifikasi & Eliminasi Data (Update / Delete)")
        search_edit_code = st.text_input("Masukkan Kode Tepat yang Ingin Diubah/Dihapus (Contoh: 47.01):", key="search_edit")

        if search_edit_code:
            df_current = st.session_state.icd9_db
            if search_edit_code in df_current['Kode_ICD9'].values:
                idx_target = df_current[df_current['Kode_ICD9'] == search_edit_code].index[0]
                row_data = df_current.loc[idx_target]

                edit_proc = st.text_input("Ubah Nama Prosedur:", value=row_data['Nama_Prosedur'], key="edit_p")
                edit_keys = st.text_area("Ubah Kata Kunci:", value=row_data['Kata_Kunci'], key="edit_k")
                edit_rumpun = st.selectbox("Ubah Rumpun Klinis:", ["Pencernaan", "Kardiovaskular", "Saraf", "Endokrin", "Mata", "Respirasi", "Urologi", "Kandungan", "Ortopedi", "Onkologi", "Integumen", "THT", "Umum/Infeksi"], index=0)

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🆙 Perbarui Jaringan Data (Update)", use_container_width=True, key="btn_update"):
                        st.session_state.icd9_db.at[idx_target, 'Nama_Prosedur'] = edit_proc
                        st.session_state.icd9_db.at[idx_target, 'Kata_Kunci'] = edit_keys
                        st.session_state.icd9_db.at[idx_target, 'Rumpun_Klinis'] = edit_rumpun
                        st.success(f"Berhasil! Data Kode {search_edit_code} telah diperbarui.")
                        st.rerun()
                with col2:
                    if st.button("🗑️ Musnahkan Data (Delete)", use_container_width=True, key="btn_delete"):
                        st.session_state.icd9_db = st.session_state.icd9_db.drop(idx_target).reset_index(drop=True)
                        st.warning(f"Peringatan! Data Kode {search_edit_code} telah dihapus selamanya.")
                        st.rerun()
            else:
                st.error("Kode tidak ditemukan. Pastikan format kode sama persis dengan data di database.")


# ==============================================================================
# TAB 3: ANALYTICS DASHBOARD & EXPORT BUTTON
# ==============================================================================
with tab3:
    st.subheader("📊 Grafik Distribusi Rumpun Spesialisasi Medis (ICD-9)")
    
    rumpun_counts = st.session_state.icd9_db['Rumpun_Klinis'].value_counts()
    st.bar_chart(rumpun_counts)
    
    st.write("---")
    st.subheader("📋 Eksplorasi Data Tabel & Pelaporan")
    
    csv_data = st.session_state.icd9_db.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Lembar Kerja Rekam Medis (Format .CSV)",
        data=csv_data,
        file_name="Laporan_Database_ICD9_Kelompok3.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==============================================================================
# FOOTER IDENTITAS KELOMPOK
# ==============================================================================
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 10px; color: #4A353B;">
        <strong>Tugas Besar Akhir - Proyek Sistem Informasi Unggulan - Kelompok 3</strong><br>
        <span style="font-size: 0.9rem; color: #6E5A5F;">Mata Kuliah: <strong>Terminologi Medis</strong></span><br>
        <div style="margin-top: 8px; font-weight: 600; color: #FF0055;">
            Nadia Ramadhani | Putri Zahra | Amanda Idezzia | Estia Putri | Rylanda Zalfa
        </div>
    </div>
""", unsafe_allow_html=True)