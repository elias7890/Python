import streamlit as st 
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.document_title, 0, 1, 'C')
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title, font='Arial', size=12):
        self.set_font(font, 'B', size)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(font, '', size)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(filaname, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author(author)
    
    if image_path:
        pdf.image(image_path, x=10, y=25, w=pdf.w - 20)
        pdf.ln(120)

    for chapter in chapters:
        title, body, font, size = chapter
        pdf.chapter_title(title, font, size) 
        pdf.chapter_body(body, font, size)  

    pdf.output(filaname)


def main():
    st.title("Generador de PDF") 
    st.header("Configuración del PDF")
    document_title = st.text_input("Título del documento")
    author = st.text_input("Autor")
    upload_image = st.file_uploader("Subir imagen", type=['jpg', 'jpeg', 'png'])

    st.header("Contenido del PDF")
    chapters = []
    chapter_count = st.number_input("Número de capítulos", min_value=1, max_value=10, value=1)

    for i in range(chapter_count):
        st.subheader(f"Capítulo {i + 1}")
        title = st.text_input(f"Título {i + 1}", f"Capítulo {i + 1}")
        body = st.text_area(f"Contenido {i + 1}", f"Contenido del capítulo {i + 1}")
        font = st.selectbox(f"Fuente {i + 1}", ['Arial', 'Courier', 'Times', 'Helvetica'])
        size = st.slider(f"Tamaño de la fuente {i + 1}", 8, 24, 12)
        chapters.append((title, body, font, size))

    if st.button("Generar PDF"):
        image_path = None
        if image_path:
            with open("imagen.jpg", "wb") as f:
                f.write(upload_image.getbuffer())

        create_pdf("PDFGENERADO.pdf", document_title, author, chapters, image_path)

        with open("PDFGENERADO.pdf", "rb") as pdf_file:
            PDFbyte = pdf_file.read()

        st.download_button(label="Descargar PDF", data=PDFbyte, file_name="PDFGENERADO.pdf", mime="application/pdf")

        st.success("PDF generado con éxito")
            
if __name__ == "__main__":  
    main()