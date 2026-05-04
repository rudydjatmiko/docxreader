import streamlit as st
import mammoth
import io

# Konfigurasi halaman agar memenuhi layar (Full Width)
st.set_page_config(layout="wide", page_title="Word Doc Viewer")

def convert_docx_to_html(file):
    """
    Mengonversi file docx ke HTML menggunakan mammoth.
    Mammoth fokus pada konversi semantik dan penanganan gambar.
    """
    try:
        # Membaca file sebagai binary stream
        custom_styles = "b => strong" # Contoh kustomisasi gaya
        result = mammoth.convert_to_html(file, style_map=custom_styles)
        html = result.value  # Konten HTML
        messages = result.messages  # Pesan jika ada error/warning
        return html
    except Exception as e:
        return f"<p>Error saat konversi: {e}</p>"

def main():
    st.title("📄 Word Document Viewer (Full Screen)")
    st.write("Unggah file .docx untuk melihat isinya termasuk tabel, gambar, dan format lainnya.")

    # Sidebar untuk kontrol
    uploaded_file = st.sidebar.file_uploader("Pilih file Word", type=['docx'])

    if uploaded_file is not None:
        # Melakukan konversi
        with st.spinner('Sedang memproses dokumen...'):
            html_content = convert_docx_to_html(uploaded_file)

        # Menambahkan script MathJax untuk mendukung rumus matematika
        # Dan CSS agar tampilan tabel serta gambar rapi
        full_html = f"""
        <html>
            <head>
                <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
                <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
                <style>
                    body {{ font-family: sans-serif; line-height: 1.6; padding: 20px; }}
                    img {{ max-width: 100%; height: auto; }}
                    table {{ border-collapse: collapse; width: 100%; }}
                    table, th, td {{ border: 1px solid #ddd; padding: 8px; }}
                    tr:nth-child(even){{background-color: #f2 f2 f2;}}
                </style>
            </head>
            <body>
                {html_content}
            </body>
        </html>
        """

        # Menampilkan hasil di area utama
        # height bisa disesuaikan atau menggunakan CSS untuk auto-expand
        st.components.v1.html(full_html, height=1000, scrolling=True)
    else:
        st.info("Silakan unggah file melalui sidebar.")

if __name__ == "__main__":
    main()
