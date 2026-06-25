import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import base64

# ====================================
# 1. CONFIG
# ====================================
st.set_page_config(
    page_title="Dashboard Angkutan Barang",
    layout="wide"
)

# ====================================
# 2. INISIALISASI SESSION STATE
# ====================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# Fungsi helper untuk convert gambar lokal ke base64
def get_base64_img(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()
    except Exception:
        return None

# ====================================
# 3. HALAMAN LOGIN 
# ====================================
if not st.session_state.logged_in:
    # Membaca gambar login background.jpg milikmu
    bg_base64 = get_base64_img("bg login.png")

    if bg_base64:
        st.markdown(f"""
            <style>
            /* Mengunci gambar background kamu di elemen paling dasar aplikasi agar tidak hilang */
            .stApp {{
                background-image: url('data:image/jpeg;base64,{bg_base64}') !important;
                background-size: 100% 100% !important;
                background-position: center center !important;
                background-repeat: no-repeat !important;
                height: 100vh !important;
                overflow: hidden !important;
            }}
            
            header {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            
            /* Menghilangkan padding bawaan Streamlit agar layout presisi mengikuti gambar */
            .block-container {{
                max-width: 90% !important;
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                padding-left: 26rem !important;
                padding-right: 1rem !important;
            }}
            
            /* Kontainer penahan form di kolom kanan (Area Putih) */
            .right-login-container {{
                margin-top: 35vh; /* Mengatur tinggi vertikal posisi form agar pas dengan kotak di gambar */
                margin-left: auto;
                margin-right: auto;
                max-width: 400px; /* Lebar box input dikunci mirip ukuran tombol biru gambar */
            }}

            /* Hilangkan border bawaan form streamlit */
            div[data-testid="stForm"] {{
                border: none !important;
                padding: 10 !important;
                background: transparent !important;
            }}
            
            /* Gaya label teks di ATAS input box (Username & Password) */
            div[data-testid="stForm"] label p {{
                font-size: 18px !important;
                font-weight: 600 !important;
                color: #2D3748 !important; /* Abu-abu gelap */
                margin-bottom: 0px !important;
            }}
            
            /* Ganti warna background box input menjadi PUTIH padat seperti tombol Log In */
            .stTextInput input {{
                border-radius: 0px !important; 
                background-color: #FFFFFF !important; /* Putih Solid */
                border: 0px solid #D1D5DB !important; /* Border tipis rapi */
                height: 50px !important;
                color: #1F2937 !important;
                padding-left: 8px !important; /* Teks rata kiri normal karena box sudah putih */
                font-size: 15px !important;
            }}
            
            /* Mengubah warna teks placeholder menjadi abu-abu gelap kontras */
            .stTextInput input::placeholder {{
                color: #555555 !important;
                opacity: 1 !important;
            }}
            
            /* Hilangkan highlight biru bawaan streamlit saat kotak diklik */
            .stTextInput input:focus {{
                border: 1px solid #A0AEC0 !important;
                box-shadow: none !important;
            }}
            
            
            div.stButton > button:first-child {{
                background-color: rgba(3, 51, 107, 0.0) !important; /* Transparan agar warna biru KAI asli gambar terlihat */
                color: white !important;
                border-radius: 100px !important;
                border: none !important;
                height: 50px !important;
                font-weight: 700 !important;
                font-size: 18px !important;
                width: % !important;
                box-shadow: none !important;
                cursor: pointer;
            }}
            
            /* Efek hover tipis di atas tombol */
            div.stButton > button:first-child:hover {{
                background-color: rgba(255, 255, 255, 0.1) !important;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<style>.stApp {{ background: #022049 !important; }}</style>", unsafe_allow_html=True)

    # Membagi kolom layout: Kolom kiri dibiarkan kosong sebagai tameng area gambar kereta
    # Kolom kanan digunakan untuk mengunci form login agar menetap di area putih
    col_blank, col_form = st.columns([1.32, 1], gap="small")
    
    with col_form:
        # Membuka struktur kontainer khusus sisi kanan
        st.markdown('<div class="right-login-container">', unsafe_allow_html=True)
        
        with st.form("login_form_secure"):
            # Input Username (Label di atas, teks placeholder abu-abu gelap, box putih)
            username = st.text_input("Username", placeholder="Enter your username")
            
            # Input Password (Label di atas, teks placeholder abu-abu gelap, box putih)
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Tombol login transparan yang menimpa pas di tengah tombol biru gambar
            submit_button = st.form_submit_button("Login")
            
            if submit_button:
                if username == "Aresa" and password == "angbar8":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Login berhasil!")
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah")
                    
        st.markdown('</div>', unsafe_allow_html=True)
# ====================================
# 4. DASHBOARD UTAMA (Logged In)
# ====================================
else:
    # Inject CSS khusus halaman utama Dashboard
    st.markdown("""
        <style>
        /* Kembalikan background aplikasi ke putih bersih */
        .stApp {
            background: #FFFFFF !important;
        }
        
        .block-container {
            padding-top: 1.5rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        /* Styling Dropdown Selectbox */
        div[data-testid="stSelectbox"] > div[data-baseweb="select"] {
            height: 35px !important;
            min-height: 35px !important;
        }

        div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
            height: 35px !important;
            min-height: 35px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            display: flex !important;
            align-items: center !important;
        }

        div[data-testid="stSelectbox"] div[data-baseweb="select"] div {
            font-size: 13px !important;
        }

        div[data-testid="stSelectbox"] label p {
            font-size: 13px !important;
            margin-bottom: 4px !important;
            font-weight: 600;
        }

        /* CONTAINER BANNER UTAMA (Kereta Tidak Terpotong) */
        .banner-container {
            background-size: contain;
            background-repeat: no-repeat;
            background-position: right center;
            background-color: #062B66;
            border-radius: 15px;
            padding: 50px;
            height: 280px; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
                                        
        .banner-title {
            color: #FFFFFF;
            font-size: 38px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: 0.5px;
        }

        .banner-subtitle {
            color: #E5E7EB;
            font-size: 16px;
            line-height: 1.6;
        }
        </style>
    """, unsafe_allow_html=True)

    # HEADER LOGO & JUDUL (HTML Murni agar rapi & presisi)
    # ====================================
    logo_base64 = get_base64_img("logo_kai.png")
    
    col_header, col_logout = st.columns([6, 1])

    with col_header:
        if logo_base64:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 20px; margin-top: 5px;">
                <img src="data:image/png;base64,{logo_base64}" style="height: 55px; width: auto; object-fit: contain;">
                <h1 style="color:#1F2937; margin: 0; font-size:36px; font-weight:700; text-align: center;">
                </h1>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; margin-top: 10px; width: 100%;">
                <h1 style="color:#1F2937; margin: 0; padding: 0; font-size:36px; font-weight:700;">
                    Dashboard Angkutan Barang PT KAI DAOP 8 Surabaya
                </h1>
            </div>
            """, unsafe_allow_html=True)

    with col_logout:
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    st.markdown("---")
    # ====================================
    # BANNER WELCOME GENERATOR
    # ====================================
    nama_user = st.session_state.get("username", "USER").upper()
    bg_base64 = get_base64_img("background_welcome.png")

    st.markdown("""
    <style>
    .banner-container {
        padding: 35px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(2, 32, 73, 0.2);
        background-size: cover;
        background-position: center;
    }
    .banner-title {
        font-size: 28px;
        font-weight: 800;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
        font-family: 'Source Sans Pro', sans-serif;
    }
    .banner-subtitle {
        font-size: 18px; /* Ukuran font diperbesar */
        font-weight: 500;
        white-space: nowrap; /* Memaksa teks tetap dalam 1 baris */
        font-family: 'Source Sans Pro', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)

    if bg_base64:
        st.markdown(f"""
        <div class="banner-container" style="background-image: linear-gradient(to right, rgba(6,43,102,1) 40%, rgba(6,43,102,0) 80%), url('data:image/png;base64,{bg_base64}');">
            <div class="banner-title">HALO, {nama_user}</div>
            <div class="banner-subtitle">Selamat datang di Dashboard Volume Angkutan Barang UPT Terminal Babat KAI DAOP 8 Surabaya</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="banner-container" style="background: linear-gradient(135deg, #022049 0%, #0547a2 100%);">
            <div class="banner-title">HALO, {nama_user}</div>
            <div class="banner-subtitle">Selamat datang di Dashboard Volume Angkutan Barang UPT Terminal Babat KAI DAOP 8 Surabaya</div>
        </div>
        """, unsafe_allow_html=True)

    # ====================================
    # UPLOAD FILE SECTION
    # ====================================
    st.subheader("Tarik Data dari Excel")
    uploaded_files = st.file_uploader(
        "Upload file Excel BBT, BJ, atau SBI",
        type=["xlsx"],
        accept_multiple_files=True
    )

    all_data = []

    if uploaded_files:
        for file in uploaded_files:
            nama_file = file.name

            if "BBT" in nama_file.upper():
                kategori = "BBT"
            elif "BJ" in nama_file.upper():
                kategori = "BJ"
            elif "SBI" in nama_file.upper():
                kategori = "SBI"
            else:
                kategori = "LAINNYA"

            try:
                excel_file = pd.ExcelFile(file)
                for sheet in excel_file.sheet_names:
                    try:
                        df = pd.read_excel(excel_file, sheet_name=sheet, header=11)
                        df = df.replace(r'^\s*$', np.nan, regex=True)
                        df = df.dropna(axis=1, how="all")
                        
                        df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]

                        if "Nomor SA" in df.columns:
                            df = df.dropna(subset=["Nomor SA"])
                        elif len(df.columns) > 0:
                            df = df.dropna(subset=[df.columns[0]])

                        if not df.empty:
                            df["Kategori"] = kategori
                            df["Sheet"] = sheet
                            all_data.append(df)

                    except Exception as e:
                        st.warning(f"⚠️ Gagal membaca sheet '{sheet}' pada file {nama_file}: {e}")
            except Exception as e:
                st.error(f"❌ Gagal memproses file {nama_file}: {e}")

    # ====================================
    # VALIDASI & RENDER DASHBOARD VISUALISASI
    # ====================================
    if len(all_data) > 0:
        data = pd.concat(all_data, ignore_index=True)
        st.success(f"✅ Berhasil memuat dan menyatukan {len(uploaded_files)} file data!")
        st.markdown("---")

        if "Tanggal SA" in data.columns:
            data["Tanggal SA"] = pd.to_datetime(data["Tanggal SA"], errors="coerce")

        # --- SEKSI FILTER & KONTROL ---
        col_title, col_filters = st.columns([1, 3])
        with col_title:
            st.subheader("Preview Data Excel")

        with col_filters:
            f_col1, f_col2, f_col3 = st.columns(3)

            with f_col1:
                kategori_filter = st.multiselect(
                    "Kategori File",
                    options=data["Kategori"].unique(),
                    default=data["Kategori"].unique()
                )

            with f_col2:
                if "Tanggal SA" in data.columns:
                    tanggal_unik = data["Tanggal SA"].dt.strftime('%Y-%m-%d').dropna().unique()
                    tanggal_unik = sorted(tanggal_unik, reverse=True)
                    tanggal_opsi = ["Semua"] + list(tanggal_unik)
                    tanggal_filter = st.selectbox("Tanggal Keberangkatan Asal KA", options=tanggal_opsi)
                else:
                    tanggal_filter = "Semua"

            with f_col3:
                sort_customer = st.selectbox(
                    "Urutan Nama Customer",
                    options=["Tidak diurutkan", "Abjad A - Z", "Abjad Z - A"]
                )

        # Proses Filter Data
        filtered_data = data.copy()
        if kategori_filter:
            filtered_data = filtered_data[filtered_data["Kategori"].isin(kategori_filter)]

        if "Tanggal SA" in filtered_data.columns and tanggal_filter != "Semua":
            filtered_data = filtered_data[filtered_data["Tanggal SA"].dt.strftime('%Y-%m-%d') == tanggal_filter]

        if "Nama Customer" in filtered_data.columns:
            if sort_customer == "Abjad A - Z":
                filtered_data = filtered_data.sort_values(by="Nama Customer", ascending=True)
            elif sort_customer == "Abjad Z - A":
                filtered_data = filtered_data.sort_values(by="Nama Customer", ascending=False)

        # --------------------------------------------------------
        # PERBAIKAN: INISIALISASI VARIABEL AWAL AGAR TIDAK NAMEERROR
        # --------------------------------------------------------
        status_col = None
        for col in ["Keterangan", "Status", "Keterangan SA", "Status SA"]:
            if col in filtered_data.columns:
                status_col = col
                break

        # Tampilkan Dataframe utama
        if not filtered_data.empty:
            st.dataframe(filtered_data, use_container_width=True)
        else:
            st.info("ℹ️ Tidak ada baris data yang cocok dengan filter terpilih.")

        with st.expander("Lihat Daftar Semua Kolom"):
            st.write(list(filtered_data.columns))

        # --- SEKSI KARTU RINGKASAN KPI ---
        st.subheader("Ringkasan Performa")
        col1, col2, col3 = st.columns(3)

        # Hitung total dokumen batal untuk visualisasi
        total_batal = 0
        if status_col:
            total_batal = filtered_data[filtered_data[status_col].astype(str).str.upper().str.contains("BATAL|VOID", na=False)].shape[0]

        with col1:
            st.metric("Total Transaksi Data", f"{len(filtered_data):,}")

        with col2:
            if status_col:
                st.metric("Total Surat Angkutan (SA) Batal", f"{total_batal:,}")
            else:
                st.metric("Jumlah Kategori Aktif", filtered_data["Kategori"].nunique())

        with col3:
            if "Volume Berat KAI" in filtered_data.columns:
                total_volume = pd.to_numeric(filtered_data["Volume Berat KAI"], errors="coerce").sum()
                st.metric("Total Volume Berat KAI", f"{total_volume:,.2f} Kg")
            else:
                st.metric("Total Volume", "Kolom 'Volume Berat KAI' tidak ditemukan")

        # --- SEKSI GRAFIK VISUALISASI VOLUME ---
        st.markdown("---")

        bulan_map = {
            1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei", 6: "Juni",
            7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober", 11: "November", 12: "Desember"
        }
        urutan_bulan = list(bulan_map.values())

        if "Tanggal SA" in filtered_data.columns and "Volume Berat KAI" in filtered_data.columns:
            filtered_data["Tanggal SA"] = pd.to_datetime(filtered_data["Tanggal SA"], errors="coerce")
            filtered_data["Bulan"] = filtered_data["Tanggal SA"].dt.month.map(bulan_map)
            filtered_data["Volume Berat KAI"] = pd.to_numeric(filtered_data["Volume Berat KAI"], errors="coerce")

            volume_bulanan = filtered_data.groupby("Bulan")["Volume Berat KAI"].sum().reindex(urutan_bulan).reset_index()
            volume_bulanan["Volume Berat KAI"] = volume_bulanan["Volume Berat KAI"].fillna(0)
            volume_bulanan = volume_bulanan.rename(columns={"Volume Berat KAI": "Realisasi"})

            # Line Chart Volume
            fig_volume = px.line(
                volume_bulanan, x="Bulan", y="Realisasi", markers=True,
                title=" Volume Bulanan Angkutan Barang",
                labels={"Bulan": "Bulan", "Realisasi": "Volume Realisasi (Kg)"} 
            )

            # MAKSIMALKAN UKURAN FONT LINE CHART
            fig_volume.update_layout(
                title_font=dict(size=24, family="Source Sans Pro, sans-serif", color="black"), # Judul Grafik Besar & Tegas
                font=dict(size=16),                                        # Font Dasar Global
                xaxis=dict(
                    title_font=dict(size=20, family="Source Sans Pro, sans-serif", weight="bold", color="black"),              # Tulisan nama axis "Bulan"
                    tickfont=dict(size=18)                                 # Tulisan nama-nama bulan
                ),
                yaxis=dict(
                    title_font=dict(size=20, family="Source Sans Pro, sans-serif", weight="bold", color="black"),                               # Tulisan nama axis "Realisasi"
                    tickfont=dict(size=18)                                 # Angka volume di sumbu Y
                ),
                margin=dict(t=80, b=40, l=60, r=40)
            )

            fig_volume.update_traces(
                line=dict(color="#ff6600", width=4), 
                marker=dict(color="#003366", size=12)
            )

            st.plotly_chart(
                fig_volume, 
                use_container_width=True,
                config={
                    'displayModeBar': True,        # Memaksa modebar selalu muncul
                    'displaylogo': False,          # Menghapus logo "Produced with Plotly"
                    'modeBarButtonsToRemove': [    # Menghapus tombol navigasi zoom, pan, dkk
                        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                        'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                    ],
                    'toImageButtonOptions': {      
                        'format': 'png',
                        'filename': 'Distribusi_Transaksi_Kategori'
                    }
                }
            )    

            # Bar Chart Volume
            st.markdown("---")
  
            fig_bar = px.bar(
                volume_bulanan, x="Bulan", y="Realisasi", text_auto=".2s",
                labels={"Bulan": "Bulan", "Realisasi": "Volume Realisasi (Kg)"},
                color_discrete_sequence=["#003366"]
            )

            # MAKSIMALKAN UKURAN FONT BAR CHART
            fig_bar.update_layout(
                bargap=0.3  # bargap dipindahkan ke update_layout jika melempar error, namun bawaan bar trace menerimanya. Lebih aman gunakan di layout atau px.bar
            )
            fig_bar.update_layout(
                title=dict(text=""), # KUNCI 1: Paksa teks komponen judul plotly bernilai kosong
                bargap=0.3,          
                font=dict(size=16, family="Source Sans Pro, sans-serif"),
                xaxis=dict(
                    title_font=dict(size=20, family="Source Sans Pro, sans-serif", weight="bold", color="black"), 
                    tickfont=dict(size=18, family="Source Sans Pro, sans-serif")
                ),
                yaxis=dict(
                    title_font=dict(size=20, family="Source Sans Pro, sans-serif", weight="bold", color="black"), 
                    tickfont=dict(size=18, family="Source Sans Pro, sans-serif")
                ),
                margin=dict(t=10, b=40, l=60, r=40) # KUNCI 2: Ubah t=80 menjadi t=10 agar bug teks hilang dan posisi grafik presisi
            )
            st.plotly_chart(
                fig_bar, 
                use_container_width=True,
                config={
                    'displayModeBar': True,        # Memaksa modebar selalu muncul
                    'displaylogo': False,          # Menghapus logo "Produced with Plotly"
                    'modeBarButtonsToRemove': [    # Menghapus tombol navigasi zoom, pan, dkk
                        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                        'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                    ],
                    'toImageButtonOptions': {      
                        'format': 'png',
                        'filename': 'Distribusi_Transaksi_Kategori'
                    }
                }
            )
        else:
            st.info("ℹ️ Grafik Tren tidak dapat dimuat karena kolom 'Tanggal SA' atau 'Volume Berat KAI' hilang.")

        # ========================================================
        # GRAFIK VISUALISASI PEMBATALAN SA PER BULAN (Sudah Fix)
        # ========================================================
        st.markdown("---")
        
        if "Tanggal SA" in filtered_data.columns and status_col:
            # Yakinkan tanggal ter-parsing baik dan kolom penanda bulan tersedia
            filtered_data["Tanggal SA"] = pd.to_datetime(filtered_data["Tanggal SA"], errors="coerce")
            filtered_data["Bulan"] = filtered_data["Tanggal SA"].dt.month.map(bulan_map)
            
            # Memfilter baris data yang mengandung kata Batal / Void di kolom statusnya
            df_batal = filtered_data[filtered_data[status_col].astype(str).str.upper().str.contains("BATAL|VOID", na=False)].copy()
            
            # Kelompokkan data per bulan dengan melampirkan bulan kosong tetap bernilai 0
            batal_bulanan = df_batal.groupby("Bulan").size().reindex(urutan_bulan, fill_value=0).reset_index(name="Jumlah Batal")
            
            #--- POSISI ATAS: Line Chart Tren ---
            fig_line_batal = px.line(
                batal_bulanan, x="Bulan", y="Jumlah Batal", markers=True,
                title="Jumlah Pembatalan Dokumen SA (Surat Angkutan) Per Bulan",
                labels={"Jumlah Batal": "Frekuensi Kasus Pembatalan"}
            )
            fig_line_batal.update_traces(
                line=dict(color="#E63946", width=4), 
                marker=dict(color="#022049", size=12)
            )

        #Detail Ukuran Font
            fig_line_batal.update_layout(
                title_font=dict(size=24, family="Source Sans Pro, sans-serif", color="black"), # Judul Grafik
                font=dict(size=16),                                        # Font Dasar Global
                xaxis=dict(
                    title_font=dict(size=20, family="Source Sans Pro, sans-serif", weight="bold", color="black"), # Sumbu X "Bulan" jadi Bold & Hitam
                    tickfont=dict(size=18)                                 # Tulisan nama bulan
                ),
                yaxis=dict(
                    title_font=dict(size=20, family="Source Sans Pro, sans-serif", weight="bold", color="black"), # Sumbu Y "Frekuensi..." jadi Bold & Hitam
                    tickfont=dict(size=18)                                 # Angka di sumbu Y
                ),
                margin=dict(t=80, b=40, l=60, r=40)                        # Margin seragam t=80
            )
            
            st.plotly_chart(
                fig_line_batal,
                use_container_width=True,
                config={
                    'displayModeBar': True,        # Memaksa modebar selalu muncul
                    'displaylogo': False,          # Menghapus logo "Produced with Plotly"
                    'modeBarButtonsToRemove': [    # Menghapus tombol navigasi zoom, pan, dkk
                        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                        'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                    ],
                    'toImageButtonOptions': {      
                        'format': 'png',
                        'filename': 'Distribusi_Transaksi_Kategori'
                    }
                }
            )

            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
   
            # --- POSISI BAWAH: Bar Chart Angka Mutlak ---
            fig_bar_batal = px.bar(
                batal_bulanan, x="Bulan", y="Jumlah Batal", text="Jumlah Batal",
                labels={"Jumlah Batal": "Total Pembatalan", "Bulan": "Bulan"}
            )
            fig_bar_batal.update_traces(marker_color="#003366", textposition="outside", textfont_size=16, textfont_family="Source Sans Pro, sans-serif")
 
            # Judul grafik diubah menjadi warna HITAM
            fig_bar_batal.update_layout(
                title=dict(text=""), # KUNCI EMAS: Memaksa judul internal Plotly kosong total
                bargap=0.3,
                font=dict(size=16, family="Source Sans Pro, sans-serif"),                                        
                xaxis=dict(
                    title_font=dict(size=20, family="Source Sans Pro, sans-serif", weight="bold", color="black"), 
                    tickfont=dict(size=18, family="Source Sans Pro, sans-serif")                                 
                ),
                yaxis=dict(
                    title_font=dict(size=20, family="Source Sans Pro, sans-serif", weight="bold", color="black"), 
                    tickfont=dict(size=18, family="Source Sans Pro, sans-serif")                                 
                ),
                margin=dict(t=10, b=40, l=60, r=40) # Margin atas (t) diperkecil jadi 10 agar mepet rapi di bawah subheader                      
            )

            st.plotly_chart(
                fig_bar_batal,
                use_container_width=True,
                config={
                    'displayModeBar': True,        # Memaksa modebar selalu muncul
                    'displaylogo': False,          # Menghapus logo "Produced with Plotly"
                    'modeBarButtonsToRemove': [    # Menghapus tombol navigasi zoom, pan, dkk
                        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                        'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                    ],
                    'toImageButtonOptions': {      
                        'format': 'png',
                        'filename': 'Distribusi_Transaksi_Kategori'
                    }
                }
            )
            
        else:
            st.info("ℹ️ Grafik Analisis Pembatalan tidak dapat ditampilkan. Pastikan file Excel Anda memuat kolom penanggalan dan kolom keterangan/status pembatalan.")

        # --- GRAFIK DISTRIBUSI KATEGORI ---
        st.markdown("---")
        kategori_count = filtered_data["Kategori"].value_counts().reset_index()
        kategori_count.columns = ["Kategori", "Jumlah"]

        fig1 = px.bar(
            kategori_count, x="Kategori", y="Jumlah", color="Kategori",
            text="Jumlah", title="Distribusi Jumlah Transaksi berdasarkan Kategori Per Stasiun",
            template="plotly_white",
            color_discrete_sequence=["#034398", "#5B92E5", "#A5C7F7"],
            labels={"Kategori": "Kategori Stasiun", "Jumlah": "Jumlah Transaksi"}
        )

        fig1.update_traces(
            textposition="outside",
            textfont_size=16,
            textfont_family="Source Sans Pro, sans-serif"
        ) 

        fig1.update_layout(
            showlegend=False, # Sembunyikan colorbar legenda di samping agar rapi
            title_font=dict(size=24, family="Source Sans Pro, sans-serif", color="black"), 
            font=dict(size=16, family="Source Sans Pro, sans-serif"),                                        
            xaxis=dict(
                title_font=dict(size=20, weight="bold", color="black", family="Source Sans Pro, sans-serif"), 
                tickfont=dict(size=18, family="Source Sans Pro, sans-serif")                                 
            ),
            yaxis=dict(
                title_font=dict(size=20, weight="bold", color="black", family="Source Sans Pro, sans-serif"), 
                tickfont=dict(size=18, family="Source Sans Pro, sans-serif")                                 
            ),
            margin=dict(t=80, b=40, l=60, r=40)
        )

        st.plotly_chart(
            fig1, 
            use_container_width=True,
            config={
                'displayModeBar': True,        # Memaksa modebar selalu muncul
                'displaylogo': False,          # Menghapus logo "Produced with Plotly"
                'modeBarButtonsToRemove': [    # Menghapus tombol navigasi zoom, pan, dkk
                    'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                    'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                ],
                'toImageButtonOptions': {      
                    'format': 'png',
                    'filename': 'Distribusi_Transaksi_Kategori'
                }
            }
        )

        # --- GRAFIK TOP 10 STASIUN TUJUAN ---
        st.markdown("---")
        if "Stasiun Tujuan SA" in filtered_data.columns:
            tujuan_data = filtered_data["Stasiun Tujuan SA"].value_counts().reset_index()
            tujuan_data.columns = ["Tujuan", "Jumlah"]

            # Ambil 10 data teratas
            df_top10 = tujuan_data.head(10).copy()
            warna_kustom = [
                "#034398",  # Peringkat 1 (SBI) -> Biru Tua Pekat KAI
                "#2563EB",  # Peringkat 2 (BJ) -> Biru Medium
                "#3B82F6",  # Peringkat 3 (BBT) -> Biru Terang
                "#60A5FA",  # Peringkat 4 (JAKG) -> Biru Muda 1
                "#93C5FD",  # Peringkat 5 (SMT) -> Biru Muda 2
                "#FF6B00",  # Peringkat 6 (CKP) -> Oranye KAI
                "#FF6B00",  # Peringkat 7 (CNP) -> Oranye KAI
                "#FF6B00",  # Peringkat 8 (PK) -> Oranye KAI
                "#FF6B00",  # Peringkat 9 (TG) -> Oranye KAI
                "#FF6B00"   # Peringkat 10 (JTB) -> Oranye KAI
            ]

            fig2 = px.bar(
                df_top10, x="Tujuan", y="Jumlah",
                text="Jumlah", title="Urutan Stasiun Tujuan Muatan Terbanyak",
                template="plotly_white",
                labels={"Tujuan": "Stasiun Tujuan", "Jumlah": "Jumlah Transaksi"}
            )

            fig2.update_traces(
                marker_color=warna_kustom, 
                textposition="outside",
                textfont_size=16,
                textfont_family="Source Sans Pro, sans-serif"
            )

            fig2.update_layout(
                bargap=0.3,
                title_font=dict(size=24, family="Source Sans Pro, sans-serif", color="black"), 
                font=dict(size=16, family="Source Sans Pro, sans-serif"),                                        
                xaxis=dict(
                    title_font=dict(size=20, weight="bold", color="black", family="Source Sans Pro, sans-serif"), 
                    tickfont=dict(size=18, family="Source Sans Pro, sans-serif")                                 
                ),
                yaxis=dict(
                    title_font=dict(size=20, weight="bold", color="black", family="Source Sans Pro, sans-serif"), 
                    tickfont=dict(size=18, family="Source Sans Pro, sans-serif")                                 
                ),
                margin=dict(t=80, b=40, l=60, r=40)
            )
            st.plotly_chart(
                fig2, 
                use_container_width=True,
                config={
                    'displayModeBar': True,        # Memaksa modebar selalu muncul
                    'displaylogo': False,          # Menghapus logo "Produced with Plotly"
                    'modeBarButtonsToRemove': [    # Menghapus tombol navigasi zoom, pan, dkk
                        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                        'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                    ],
                    'toImageButtonOptions': {      
                        'format': 'png',
                        'filename': 'Urutan_Stasiun_Tujuan'
                    }
                }
            )
        else:
            st.info("ℹ️ Kolom 'Stasiun Tujuan SA' tidak ditemukan dalam berkas data.")


        # --- GRAFIK TOP 10 CUSTOMER (PIE) ---
        st.markdown("---")
        if "Nama Customer" in filtered_data.columns:
            st.subheader("Top 10 Mitra Berdasarkan Volume Muatan")
            customer_data = filtered_data["Nama Customer"].value_counts().reset_index()
            customer_data.columns = ["Customer", "Jumlah"]

            warna_sesuai_contoh = [
                "#0066CC", "#75C3FF", "#FF2323", "#FFA3A3", "#2BB594", 
                "#86E397", "#FF9900", "#A3E4D7", "#D5F5E3", "#EAECEE"
            ]

            # Mengosongkan title dari inisialisasi awal
            fig3_pie = px.pie(
                customer_data.head(10), 
                names="Customer", 
                values="Jumlah", 
                hole=0.3, 
                template="plotly_white",
                color_discrete_sequence=warna_sesuai_contoh
            )

            # Menyetel posisi teks persentase di dalam kue
            fig3_pie.update_traces(
                textposition="inside",
                textinfo="percent", 
                textfont=dict(size=14, family="Source Sans Pro, sans-serif", color="white")
            )

            # KUNCI UTAMA: Mengosongkan komponen teks judul internal Plotly secara eksplisit
            fig3_pie.update_layout(
                title=dict(text=""), # Mengunci teks judul internal menjadi string kosong agar kata 'undefined' hilang
                showlegend=True, 
                font=dict(size=16, family="Source Sans Pro, sans-serif"),
                legend=dict(
                    font=dict(size=14, family="Source Sans Pro, sans-serif"),
                    orientation="v", 
                    yanchor="middle",
                    y=0.5
                ),
                margin=dict(t=10, b=20, l=40, r=40) # Mengurangi margin atas (t) agar visualisasi naik dan rapi
            )

            st.plotly_chart(
                fig3_pie, 
                use_container_width=True,
                config={
                    'displayModeBar': True,        # Memaksa modebar selalu muncul
                    'displaylogo': False,          # Menghapus logo "Produced with Plotly"
                    'modeBarButtonsToRemove': [    # Menghapus tombol navigasi yang tidak diinginkan
                        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                        'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                    ],
                    'toImageButtonOptions': {      # Opsional: Mengatur nama file saat download
                        'format': 'png',
                        'filename': 'Top_Mitra_Pie'
                    }
                }
            )
        else:
            st.info("ℹ️ Kolom 'Nama Customer' tidak ditemukan dalam berkas data.")

        # --- GRAFIK MITRA EKSPEDISI (BAR CHART HORIZONTAL) ---
        st.markdown("---")
        if "Nama Customer" in filtered_data.columns:
            
            customer_data = filtered_data["Nama Customer"].value_counts().reset_index()
            customer_data.columns = ["Customer", "Jumlah"]
            
            top_customer = customer_data.head(7).sort_values(by="Jumlah", ascending=True)

            fig3_bar = px.bar(
                top_customer, 
                x="Jumlah", 
                y="Customer", 
                orientation='h',
                text="Jumlah",
                template="plotly_white",
                labels={"Jumlah": "Volume", "Customer": "Nama Mitra Ekspedisi"}
            )
            
            warna_gradasi_biru = [
                "#60A5FA",  # Peringkat 7 (Paling pendek, di bawah)
                "#60A5FA",  # Peringkat 6
                "#60A5FA",  # Peringkat 5
                "#3B82F6",  # Peringkat 4
                "#2563EB",  # Peringkat 3
                "#1E40AF",  # Peringkat 2
                "#034398"  # Peringkat 1 (Paling panjang, di atas) -> Biru Tua Pekat KAI
            ]

            fig3_bar.update_traces(
                marker_color=warna_gradasi_biru,
                textposition="outside",
                textfont_size=16,
                textfont_family="Source Sans Pro, sans-serif"
            )

            fig3_bar.update_layout(
                title=dict(text=""), # <--- Memaksa judul internal Plotly kosong agar 'undefined' hilang
                bargap=0.3, 
                font=dict(size=16, family="Source Sans Pro, sans-serif"),
                xaxis=dict(
                    title_font=dict(size=20, weight="bold", color="black", family="Source Sans Pro, sans-serif"), 
                    tickfont=dict(size=18, family="Source Sans Pro, sans-serif")                                 
                ),
                yaxis=dict(
                    title_font=dict(size=20, weight="bold", color="black", family="Source Sans Pro, sans-serif"), 
                    tickfont=dict(size=16, family="Source Sans Pro, sans-serif")                                 
                ),
                margin=dict(t=10, b=40, l=60, r=60) # Margin atas (t) diperkecil agar grafik naik rapi mendekati subheader
            )
            st.plotly_chart(
                fig3_bar, 
                use_container_width=True,
                config={
                    'displayModeBar': True,        # Memaksa modebar selalu muncul
                    'displaylogo': False,          # KUNCI: Menghapus logo "Produced with Plotly"
                    'modeBarButtonsToRemove': [    # Menghapus logo yang tidak diinginkan
                        'zoom2d', 'pan2d', 'select2d', 'lasso2d', 
                        'zoomIn2d', 'zoomOut2d', 'autoScale2d', 'resetScale2d'
                    ],
                    'toImageButtonOptions': {      # Opsional: Mengatur format download jika ditekan
                        'format': 'png',
                        'filename': 'Top_Mitra_Ekspedisi'
                    }
                }
            )
        else:
            st.info("ℹ️ Kolom 'Nama Customer' tidak ditemukan dalam berkas data.")

    else:
        st.info("📂 Dashboard Siap. Silakan unggah satu atau beberapa berkas file Excel (.xlsx) di atas untuk melihat visualisasi data.")