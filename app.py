import streamlit as st
import matplotlib.pyplot as plt
import io
import base64
def plot_to_base64(fig):
    """Konversi plot matplotlib ke base64"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')
import plotly.express as px
import numpy as np
import pandas as pd
import re
from textblob import TextBlob
from scipy.stats import entropy

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Sindrom Down Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Styling
st.markdown("""
    <style>
    .stPlotlyChart {
        background-color: #0E1117;
        border-radius: 5px;
        padding: 1rem;
        margin-bottom: 2rem;
    }
    .st-emotion-cache-1v0mbdj {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

class SindromDownAnalyzer:
    def __init__(self, medical_text):
        self.text = medical_text
        self.sentences = medical_text.split('.')
        self.words = medical_text.split()
    
    def analyze_medical_profile(self):
        metrics = {}
        
        # 1. Karakteristik Genetik
        metrics['chromosome_abnormality'] = len(re.findall(r'trisomy\s+21|chromosome\s+21', self.text.lower())) > 0
        metrics['genetic_variation'] = len(re.findall(r'mosaic|translocation', self.text.lower())) > 0
        
        # 2. Karakteristik Fisik
        physical_features = [
            'epicanthal fold', 'flat facial profile', 'small ears', 
            'low muscle tone', 'short stature', 'single palmar crease'
        ]
        metrics['physical_features_count'] = sum(1 for feature in physical_features if feature in self.text.lower())
        
        # 3. Perkembangan dan Neurologis
        dev_markers = [
            'intellectual disability', 'developmental delay', 
            'cognitive impairment', 'speech delay'
        ]
        metrics['developmental_markers'] = sum(1 for marker in dev_markers if marker in self.text.lower())
        
        # 4. Kondisi Medis Terkait
        medical_conditions = [
            'heart defect', 'congenital heart disease', 'thyroid', 
            'hearing loss', 'vision problems', 'respiratory issues'
        ]
        metrics['associated_conditions'] = sum(1 for condition in medical_conditions if condition in self.text.lower())
        
        # 5. Intervensi dan Manajemen
        intervention_markers = [
            'early intervention', 'therapy', 'support', 
            'educational support', 'occupational therapy'
        ]
        metrics['intervention_strategies'] = sum(1 for marker in intervention_markers if marker in self.text.lower())
        
        # 6. Kualitas Hidup
        quality_of_life_markers = [
            'social skills', 'independence', 'inclusion', 
            'life expectancy', 'quality of life'
        ]
        metrics['quality_of_life_indicators'] = sum(1 for marker in quality_of_life_markers if marker in self.text.lower())
        
        return metrics
    
    def create_visualizations(self):
        metrics = self.analyze_medical_profile()
        figs = []
        
        # 1. Radar Chart untuk Profil Medis
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself'
        ))
        fig_radar.update_layout(
            title='Sindrom Down - Profil Medis Komprehensif',
            polar=dict(radialaxis=dict(visible=True, range=[0, max(values)])),
            template='plotly_dark'
        )
        figs.append(fig_radar)
        
        # 2. Bar Chart untuk Kategori
        fig_bar = go.Figure(data=[go.Bar(
            x=categories,
            y=values,
            marker_color='lightblue'
        )])
        fig_bar.update_layout(
            title='Indikator Kesehatan Sindrom Down',
            xaxis_title='Kategori',
            yaxis_title='Skor',
            template='plotly_dark'
        )
        figs.append(fig_bar)
        
        # 3. Pie Chart untuk Distribusi
        fig_pie = go.Figure(data=[go.Pie(
            labels=categories,
            values=values,
            hole=.3
        )])
        fig_pie.update_layout(
            title='Distribusi Karakteristik Sindrom Down',
            template='plotly_dark'
        )
        figs.append(fig_pie)
        
        return figs, metrics

# Aplikasi Utama Streamlit
def main():
    st.title('Analisis Komprehensif Sindrom Down')
    
    st.sidebar.header('Konfigurasi Analisis')
    
    # Input teks medis
    medical_text = st.text_area(
        "Masukkan Informasi Medis Pasien dengan Sindrom Down",
        """Pasien laki-laki, 8 tahun, dengan diagnosis Sindrom Down (Trisomy 21). 
        Memiliki karakteristik fisik seperti lipatan epikantal, wajah datar, dan telinga kecil. 
        Mengalami keterlambatan perkembangan dan kesulitan bicara. 
        Memiliki defek jantung bawaan yang telah dioperasi. 
        Mengikuti terapi wicara dan okupasi untuk mendukung perkembangannya.""",
        height=300
    )
    
    if st.button("Analisis Profil Medis", type="primary"):
        with st.spinner('Menganalisis informasi medis...'):
            # Buat instance analyzer
            analyzer = SindromDownAnalyzer(medical_text)
            
            # Dapatkan visualisasi dan metrik
            figs, metrics = analyzer.create_visualizations()
            
            # Tampilkan hasil
            st.header('Hasil Analisis')
            
            # Tab untuk visualisasi
            tab1, tab2, tab3 = st.tabs(["Profil Radar", "Bar Chart", "Distribusi"])
            
            with tab1:
                st.plotly_chart(figs[0], use_container_width=True)
            
            with tab2:
                st.plotly_chart(figs[1], use_container_width=True)
            
            with tab3:
                st.plotly_chart(figs[2], use_container_width=True)
            
            # Tampilkan metrik detail
            st.header('Detail Metrik')
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader('Karakteristik Utama')
                for key, value in metrics.items():
                    st.metric(key.replace('_', ' ').title(), value)
            
            with col2:
                st.subheader('Interpretasi')
                st.write("""
                - Analisis ini memberikan gambaran komprehensif tentang profil medis Sindrom Down
                - Setiap metrik menunjukkan aspek penting dalam diagnosis dan manajemen
                - Gunakan informasi ini sebagai panduan untuk intervensi dan dukungan
                """)

# Jalankan aplikasi
if __name__ == "__main__":
    main()

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Alat Analisis Sindrom Down</p>
        <p style='font-size: small'>Menggunakan visualisasi dan analisis mendalam</p>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class SindromDownGenetikAnalyzer:
    def __init__(self, genetic_data):
        self.data = genetic_data
    
    def analisis_genetik_detail(self):
        # Simulasi analisis genetik komprehensif
        metrics = {
            # Tipe Sindrom Down
            'tipe_sindrom_down': {
                'Trisomy 21 Penuh': 95,
                'Mosaic': 3,
                'Translokasi': 2
            },
            
            # Marker Genetik
            'marker_genetik': {
                'DYRK1A': 0.75,
                'SOD1': 0.65,
                'RCAN1': 0.55,
                'APP': 0.45
            },
            
            # Risiko Kondisi Medis
            'risiko_kondisi_medis': {
                'Penyakit Jantung': 0.45,
                'Gangguan Tiroid': 0.35,
                'Leukemia': 0.15,
                'Demensia Dini': 0.25
            },
            
            # Profil Ekspresi Gen
            'ekspresi_gen': {
                'Overekspresi': 0.7,
                'Underekspresi': 0.3,
                'Netral': 0.0
            }
        }
        return metrics
    
    def visualisasi_genetik(self, metrics):
        figs = []
        
        # 1. Pie Chart Tipe Sindrom Down
        fig_tipe = go.Figure(data=[go.Pie(
            labels=list(metrics['tipe_sindrom_down'].keys()),
            values=list(metrics['tipe_sindrom_down'].values()),
            hole=0.3,
            marker_colors=['#FF6384', '#36A2EB', '#FFCE56']
        )])
        fig_tipe.update_layout(
            title='Distribusi Tipe Sindrom Down',
            template='plotly_dark'
        )
        figs.append(fig_tipe)
        
        # 2. Bar Chart Marker Genetik
        fig_marker = go.Figure(data=[go.Bar(
            x=list(metrics['marker_genetik'].keys()),
            y=list(metrics['marker_genetik'].values()),
            marker_color='lightblue'
        )])
        fig_marker.update_layout(
            title='Ekspresi Marker Genetik Utama',
            xaxis_title='Gen',
            yaxis_title='Tingkat Ekspresi',
            template='plotly_dark'
        )
        figs.append(fig_marker)
        
        # 3. Heatmap Risiko Kondisi Medis
        risiko_data = pd.DataFrame.from_dict(
            metrics['risiko_kondisi_medis'], 
            orient='index', 
            columns=['Risiko']
        )
        
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=risiko_data.values,
            x=['Risiko'],
            y=risiko_data.index,
            colorscale='Viridis'
        ))
        fig_heatmap.update_layout(
            title='Peta Risiko Kondisi Medis Terkait',
            template='plotly_dark'
        )
        figs.append(fig_heatmap)
        
        # 4. Pie Chart Ekspresi Gen
        fig_ekspresi = go.Figure(data=[go.Pie(
            labels=list(metrics['ekspresi_gen'].keys()),
            values=list(metrics['ekspresi_gen'].values()),
            hole=0.3,
            marker_colors=['#FF6384', '#36A2EB', '#FFCE56']
        )])
        fig_ekspresi.update_layout(
            title='Profil Ekspresi Gen',
            template='plotly_dark'
        )
        figs.append(fig_ekspresi)
        
        return figs, risiko_data
    
    def generate_laporan_genetik(self, metrics):
        laporan = """
        ## Laporan Analisis Genetik Sindrom Down

        ### Ringkasan Umum
        - **Tipe Dominan**: Trisomy 21 Penuh (95% kasus)
        - **Variasi Genetik**: Terdeteksi beberapa marker gen kunci

        ### Marker Genetik Utama
        {marker_detail}

        ### Potensi Risiko Medis
        {risiko_detail}

        ### Rekomendasi Lanjutan
        - Pemantauan berkala kondisi medis
        - Konsultasi genetik lanjutan
        - Intervensi dini berdasarkan profil genetik
        """.format(
            marker_detail="\n".join([
                f"- **{gen}**: Tingkat Ekspresi {nilai*100:.2f}%"
                for gen, nilai in metrics['marker_genetik'].items()
            ]),
            risiko_detail="\n".join([
                f"- **{kondisi}**: Risiko {nilai*100:.2f}%"
                for kondisi, nilai in metrics['risiko_kondisi_medis'].items()
            ])
        )
        return laporan

def main():
    st.title('Analisis Genetik Sindrom Down Lanjutan')
    
    st.sidebar.header('Konfigurasi Analisis Genetik')
    
    # Contoh data genetik default
    default_genetic_data = {
        'gen_utama': ['DYRK1A', 'SOD1', 'RCAN1', 'APP'],
        'ekspresi': [0.75, 0.65, 0.55, 0.45]
    }
    
    # Input data genetik
    st.subheader('Input Data Genetik')
    col1, col2 = st.columns(2)
    
    with col1:
        gen_input = st.text_input('Gen yang Dianalisis', value='DYRK1A, SOD1, RCAN1, APP')
    
    with col2:
        ekspresi_input = st.text_input('Tingkat Ekspresi (0-1)', value='0.75, 0.65, 0.55, 0.45')
    
    if st.button('Analisis Genetik Mendalam', type='primary'):
        with st.spinner('Menganalisis profil genetik...'):
            # Konversi input
            try:
                gens = [g.strip() for g in gen_input.split(',')]
                ekspresis = [float(e.strip()) for e in ekspresi_input.split(',')]
                
                # Inisialisasi analyzer
                analyzer = SindromDownGenetikAnalyzer(
                    {'gen_utama': gens, 'ekspresi': ekspresis}
                )
                
                # Jalankan analisis
                metrics = analyzer.analisis_genetik_detail()
                figs, risiko_data = analyzer.visualisasi_genetik(metrics)
                laporan = analyzer.generate_laporan_genetik(metrics)
                
                # Tampilkan hasil
                tabs = st.tabs([
                    'Tipe Sindrom Down', 
                    'Marker Genetik', 
                    'Risiko Medis', 
                    'Ekspresi Gen',
                    'Laporan Detail'
                ])
                
                # Isi tab
                with tabs[0]:
                    st.plotly_chart(figs[0], use_container_width=True)
                
                with tabs[1]:
                    st.plotly_chart(figs[1], use_container_width=True)
                
                with tabs[2]:
                    st.plotly_chart(figs[2], use_container_width=True)
                
                with tabs[3]:
                    st.plotly_chart(figs[3], use_container_width=True)
                
                with tabs[4]:
                    st.markdown(laporan)
                    
                    # Tabel risiko tambahan
                    st.subheader('Detail Risiko Kondisi Medis')
                    st.dataframe(risiko_data)
            
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Analisis Genetik Sindrom Down Komprehensif</p>
        <p style='font-size: small'>Teknologi Genomik Canggih</p>
    </div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class SindromDownKlinisPerkembangan:
    def __init__(self, data_pasien):
        self.data = data_pasien
    
    def analisis_perkembangan(self):
        # Simulasi data perkembangan komprehensif
        metrics = {
            # Tahapan Perkembangan
            'perkembangan_motorik': {
                'Kasar': {
                    '0-6 bulan': 0.3,
                    '6-12 bulan': 0.5,
                    '1-2 tahun': 0.7,
                    '2-3 tahun': 0.8
                },
                'Halus': {
                    '0-6 bulan': 0.2,
                    '6-12 bulan': 0.4,
                    '1-2 tahun': 0.6,
                    '2-3 tahun': 0.75
                }
            },
            
            # Perkembangan Kognitif
            'perkembangan_kognitif': {
                'Perhatian': 0.6,
                'Memori': 0.5,
                'Pemecahan Masalah': 0.4,
                'Bahasa': 0.45
            },
            
            # Intervensi Terapi
            'intervensi_terapi': {
                'Terapi Wicara': 0.7,
                'Terapi Okupasi': 0.65,
                'Terapi Fisik': 0.6,
                'Terapi Perilaku': 0.55
            },
            
            # Keterampilan Sosial
            'keterampilan_sosial': {
                'Komunikasi': 0.5,
                'Interaksi Sosial': 0.55,
                'Kemandirian': 0.45,
                'Emosi': 0.4
            }
        }
        return metrics
    
    def visualisasi_perkembangan(self, metrics):
        figs = []
        
        # 1. Perkembangan Motorik - Line Chart
        fig_motorik = go.Figure()
        
        # Motorik Kasar
        fig_motorik.add_trace(go.Scatter(
            x=list(metrics['perkembangan_motorik']['Kasar'].keys()),
            y=list(metrics['perkembangan_motorik']['Kasar'].values()),
            mode='lines+markers',
            name='Motorik Kasar'
        ))
        
        # Motorik Halus
        fig_motorik.add_trace(go.Scatter(
            x=list(metrics['perkembangan_motorik']['Halus'].keys()),
            y=list(metrics['perkembangan_motorik']['Halus'].values()),
            mode='lines+markers',
            name='Motorik Halus'
        ))
        
        fig_motorik.update_layout(
            title='Perkembangan Motorik Anak Sindrom Down',
            xaxis_title='Tahap Usia',
            yaxis_title='Tingkat Perkembangan',
            template='plotly_dark'
        )
        figs.append(fig_motorik)
        
        # 2. Perkembangan Kognitif - Bar Chart
        fig_kognitif = go.Figure(data=[go.Bar(
            x=list(metrics['perkembangan_kognitif'].keys()),
            y=list(metrics['perkembangan_kognitif'].values()),
            marker_color='lightblue'
        )])
        fig_kognitif.update_layout(
            title='Profil Perkembangan Kognitif',
            xaxis_title='Aspek Kognitif',
            yaxis_title='Tingkat Kemampuan',
            template='plotly_dark'
        )
        figs.append(fig_kognitif)
        
        # 3. Intervensi Terapi - Pie Chart
        fig_terapi = go.Figure(data=[go.Pie(
            labels=list(metrics['intervensi_terapi'].keys()),
            values=list(metrics['intervensi_terapi'].values()),
            hole=0.3
        )])
        fig_terapi.update_layout(
            title='Distribusi Intervensi Terapi',
            template='plotly_dark'
        )
        figs.append(fig_terapi)
        
        # 4. Keterampilan Sosial - Radar Chart
        fig_sosial = go.Figure(data=go.Scatterpolar(
            r=list(metrics['keterampilan_sosial'].values()),
            theta=list(metrics['keterampilan_sosial'].keys()),
            fill='toself'
        ))
        fig_sosial.update_layout(
            title='Keterampilan Sosial',
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            template='plotly_dark'
        )
        figs.append(fig_sosial)
        
        return figs
    
    def generate_laporan_perkembangan(self, metrics):
        laporan = """
        ## Laporan Perkembangan Komprehensif Sindrom Down

        ### Ringkasan Perkembangan Motorik
        - **Motorik Kasar**: Perkembangan progresif dari 30% hingga 80%
        - **Motorik Halus**: Peningkatan gradual dari 20% hingga 75%

        ### Profil Kognitif
        {kognitif_detail}

        ### Rekomendasi Intervensi Terapi
        {terapi_detail}

        ### Keterampilan Sosial dan Emosional
        {sosial_detail}

        ### Strategi Pendampingan
        - Terapi berkala sesuai kebutuhan individu
        - Pendekatan holistik dan personal
        - Fokus pada pengembangan potensi unik
        """.format(
            kognitif_detail="\n".join([
                f"- **{aspek}**: {nilai*100:.2f}% kapasitas"
                for aspek, nilai in metrics['perkembangan_kognitif'].items()
            ]),
            terapi_detail="\n".join([
                f"- **{terapi}**: Intensitas {nilai*100:.2f}%"
                for terapi, nilai in metrics['intervensi_terapi'].items()
            ]),
            sosial_detail="\n".join([
                f"- **{keterampilan}**: {nilai*100:.2f}% kemampuan"
                for keterampilan, nilai in metrics['keterampilan_sosial'].items()
            ])
        )
        return laporan

def main():
    st.title('Analisis Perkembangan Klinis Sindrom Down')
    
    st.sidebar.header('Konfigurasi Analisis Perkembangan')
    
    # Input data perkembangan
    st.subheader('Profil Perkembangan Pasien')
    
    col1, col2 = st.columns(2)
    
    with col1:
        usia = st.number_input('Usia (bulan)', min_value=0, max_value=180, value=36)
    
    with col2:
        intervensi = st.multiselect(
            'Terapi yang Diikuti',
            ['Terapi Wicara', 'Terapi Okupasi', 'Terapi Fisik', 'Terapi Perilaku'],
            default=['Terapi Wicara']
        )
    
    if st.button('Analisis Perkembangan', type='primary'):
        with st.spinner('Menganalisis profil perkembangan...'):
            # Inisialisasi analyzer
            data_pasien = {
                'usia': usia,
                'intervensi': intervensi
            }
            
            analyzer = SindromDownKlinisPerkembangan(data_pasien)
            
            # Jalankan analisis
            metrics = analyzer.analisis_perkembangan()
            figs = analyzer.visualisasi_perkembangan(metrics)
            laporan = analyzer.generate_laporan_perkembangan(metrics)
            
            # Tampilkan hasil
            tabs = st.tabs([
                'Perkembangan Motorik', 
                'Profil Kognitif', 
                'Intervensi Terapi',
                'Keterampilan Sosial',
                'Laporan Detail'
            ])
            
            # Isi tab
            with tabs[0]:
                st.plotly_chart(figs[0], use_container_width=True)
            
            with tabs[1]:
                st.plotly_chart(figs[1], use_container_width=True)
            
            with tabs[2]:
                st.plotly_chart(figs[2], use_container_width=True)
            
            with tabs[3]:
                st.plotly_chart(figs[3], use_container_width=True)
            
            with tabs[4]:
                st.markdown(laporan)
                
                # Tambahan rekomendasi berdasarkan usia
                st.subheader('Rekomendasi Berdasarkan Usia')
                if usia < 12:
                    st.info('Fokus: Stimulasi dini dan terapi dasar')
                elif usia < 36:
                    st.info('Fokus: Pengembangan motorik dan komunikasi')
                else:
                    st.info('Fokus: Keterampilan sosial dan kemandirian')

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>Analisis Perkembangan Sindrom Down Komprehensif</p>
        <p style='font-size: small'>Pendekatan Holistik dan Personal</p>
    </div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import io

class ManajemenHolistikSindromDown:
    def __init__(self, data_pasien):
        self.data = data_pasien
    
    def analisis_komprehensif(self):
        # Simulasi data holistik
        metrics = {
            # Aspek Kesehatan
            'kesehatan_medis': {
                'Jantung': 0.7,
                'Tiroid': 0.6,
                'Pendengaran': 0.5,
                'Penglihatan': 0.55
            },
            
            # Aspek Perkembangan
            'perkembangan': {
                'Motorik Kasar': 0.65,
                'Motorik Halus': 0.6,
                'Kognitif': 0.55,
                'Bahasa': 0.5
            },
            
            # Aspek Sosial-Emosional
            'sosial_emosional': {
                'Interaksi Sosial': 0.6,
                'Regulasi Emosi': 0.55,
                'Kemandirian': 0.5,
                'Komunikasi': 0.58
            },
            
            # Intervensi dan Dukungan
            'intervensi': {
                'Terapi Wicara': 0.7,
                'Terapi Okupasi': 0.65,
                'Terapi Perilaku': 0.6,
                'Pendidikan Khusus': 0.58
            }
        }
        return metrics
    
    def visualisasi_holistik(self, metrics):
        figs = []
        
        # 1. Radar Chart Multidimensional
        fig_holistik = go.Figure()
        
        # Tambahkan setiap kategori
        kategoris = list(metrics.keys())
        for kategori in kategoris:
            fig_holistik.add_trace(go.Scatterpolar(
                r=list(metrics[kategori].values()),
                theta=list(metrics[kategori].keys()),
                fill='toself',
                name=kategori
            ))
        
        fig_holistik.update_layout(
            title='Analisis Holistik Sindrom Down',
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            template='plotly_dark'
        )
        figs.append(fig_holistik)
        
        # 2. Heatmap Integrasi Aspek
        data_heatmap = []
        for kategori, values in metrics.items():
            for aspek, skor in values.items():
                data_heatmap.append([kategori, aspek, skor])
        
        df_heatmap = pd.DataFrame(data_heatmap, columns=['Kategori', 'Aspek', 'Skor'])
        
        fig_heatmap = px.density_heatmap(
            df_heatmap, 
            x='Kategori', 
            y='Aspek', 
            z='Skor',
            title='Integrasi dan Korelasi Aspek',
            template='plotly_dark'
        )
        figs.append(fig_heatmap)
        
        # 3. Waterfall Chart Progres
        progres_kumulatif = np.cumsum([np.mean(list(kategori.values())) for kategori in metrics.values()])
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="Progres Kumulatif",
            orientation="v",
            measure=["relative"]*len(kategoris) + ["total"],
            x=kategoris + ["Total"],
            textposition="outside",
            text=[f"{val:.2f}" for val in list(progres_kumulatif) + [progres_kumulatif[-1]]],
            y=list(progres_kumulatif) + [progres_kumulatif[-1]]
        ))
        
        fig_waterfall.update_layout(
            title='Progresivitas Perkembangan',
            template='plotly_dark'
        )
        figs.append(fig_waterfall)
        
        # 4. Kombinasi Area Chart
        fig_area = go.Figure()
        
        for kategori, values in metrics.items():
            fig_area.add_trace(go.Scatter(
                x=list(values.keys()),
                y=list(values.values()),
                mode='lines',
                stackgroup='one',
                name=kategori
            ))
        
        fig_area.update_layout(
            title='Pola Perkembangan Terintegrasi',
            xaxis_title='Aspek',
            yaxis_title='Skor',
            template='plotly_dark'
        )
        figs.append(fig_area)
        
        return figs
    
    def generate_laporan_manajemen(self, metrics):
        # Hitung skor rata-rata
        skor_rata_rata = {
            kategori: np.mean(list(values.values())) 
            for kategori, values in metrics.items()
        }
        
        laporan = f"""
        ## Laporan Manajemen Holistik Sindrom Down

        ### Ringkasan Komprehensif
        {self._buat_ringkasan(skor_rata_rata)}

        ### Rekomendasi Spesifik
        {self._buat_rekomendasi(metrics)}

        ### Rencana Intervensi Personal
        {self._buat_rencana_intervensi(metrics)}
        """
        return laporan
    
    def _buat_ringkasan(self, skor_rata_rata):
        ringkasan = "#### Evaluasi Multidimensional\n"
        for kategori, skor in skor_rata_rata.items():
            status = (
                "Sangat Baik" if skor > 0.75 else
                "Baik" if skor > 0.6 else
                "Cukup" if skor > 0.45 else
                "Perlu Perhatian"
            )
            ringkasan += f"- **{kategori}**: {status} (Skor: {skor*100:.2f}%)\n"
        return ringkasan
    
    def _buat_rekomendasi(self, metrics):
        rekomendasi = "#### Fokus Pengembangan\n"
        for kategori, values in metrics.items():
            aspek_terendah = min(values, key=values.get)
            rekomendasi += f"- **{kategori}**: Prioritaskan pengembangan {aspek_terendah}\n"
        return rekomendasi
    
    def _buat_rencana_intervensi(self, metrics):
        rencana = "#### Strategi Pendampingan\n"
        intervensi = metrics.get('intervensi', {})
        for terapi, intensitas in sorted(intervensi.items(), key=lambda x: x[1], reverse=True):
            rencana += f"- **{terapi}**: Intensitas {intensitas*100:.2f}% - Lanjutkan dan optimalkan\n"
        return rencana

def main():
    st.set_page_config(
        page_title="Manajemen Holistik Sindrom Down",
        page_icon="🧬",
        layout="wide"
    )
    
    st.title('🧬 Platform Manajemen Holistik Sindrom Down')
    
    # Sidebar navigasi
    menu = st.sidebar.radio(
        "Pilih Menu Utama",
        [
            "Profil Pasien", 
            "Analisis Komprehensif", 
            "Rencana Intervensi",
            "Edukasi & Dukungan"
        ]
    )
    
    if menu == "Profil Pasien":
        st.header("Profil dan Asesmen Awal")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Pasien")
            usia = st.number_input("Usia (bulan)", min_value=0, max_value=240, value=36)
        
        with col2:
            jenis_kelamin = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
            tipe_sindrom_down = st.selectbox(
                "Tipe Sindrom Down",
                ["Trisomy 21", "Mosaic", "Translokasi"]
            )
        
        if st.button("Buat Profil"):
            st.success(f"Profil {nama} berhasil dibuat!")
    
    elif menu == "Analisis Komprehensif":
        st.header("Analisis Multidimensional")
        
        # Tombol untuk memulai analisis
        if st.button("Jalankan Analisis Holistik"):
            with st.spinner('Menganalisis data pasien...'):
                # Inisialisasi analyzer
                data_pasien = {
                    'nama': 'Contoh Pasien',
                    'usia': 36
                }
                
                analyzer = ManajemenHolistikSindromDown(data_pasien)
                
                # Jalankan analisis
                metrics = analyzer.analisis_komprehensif()
                figs = analyzer.visualisasi_holistik(metrics)
                laporan = analyzer.generate_laporan_manajemen(metrics)
                
                # Tampilkan hasil
                tabs = st.tabs([
                    'Radar Holistik', 
                    'Peta Integrasi', 
                    'Progresivitas',
                    'Pola Perkembangan',
                    'Laporan Detail'
                ])
                
                # Isi tab
                with tabs[0]:
                    st.plotly_chart(figs[0], use_container_width=True)
                
                with tabs[1]:
                    st.plotly_chart(figs[1], use_container_width=True)
                
                with tabs[2]:
                    st.plotly_chart(figs[2], use_container_width=True)
                
                with tabs[3]:
                    st.plotly_chart(figs[3], use_container_width=True)
                
                with tabs[4]:
                    st.markdown(laporan)
    
    elif menu == "Rencana Intervensi":
        st.header("Rencana Intervensi Personal")
        
        st.write("""
        ### Pendekatan Komprehensif
        - Terapi disesuaikan dengan kebutuhan individual
        - Melibatkan tim multidisiplin
        - Evaluasi berkala
        """)
        
        # Contoh rencana intervensi
        intervensi_options = [
            "Terapi Wicara",
            "Terapi Okupasi",
            "Terapi Fisik",
            "Terapi Perilaku",
            "Pendidikan Khusus"
        ]
        
        intervensi_dipilih = st.multiselect(
            "Pilih Intervensi yang Direkomendasikan",
            intervensi_options
        )
    
    else:
        st.header("Edukasi & Sumber Daya")
        
        # Sumber daya
        st.subheader("Informasi & Dukungan")
        resources = {
            "Yayasan Sindrom Down Indonesia": "https://example.com",
            "Pusat Terapi Anak Berkebutuhan Khusus": "https://example.com",
            "Panduan Orangtua": "https://example.com"
        }
        
        for nama, link in resources.items():
            st.markdown(f"- [{nama}]({link})")

# Footer dengan informasi penting
st.sidebar.markdown("---")
st.sidebar.info("""
### Disclaimer
Alat ini bersifat informatif.
Konsultasi dengan profesional medis 
tetap sangat dianjurkan.
""")

if __name__ == "__main__":
    main()
