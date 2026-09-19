import streamlit as st
import fitz  # PyMuPDF
import io

st.set_page_config(page_title="PDF Nightshade", layout="centered")

st.title("🌙 PDF Nightshade")
st.write("Upload a PDF to invert its colors for easier night reading.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

def convert_to_dark_mode(input_bytes):
    # Open the PDF from memory
    src = fitz.open(stream=input_bytes, filetype="pdf")
    out = fitz.open()  # New empty PDF

    progress_bar = st.progress(0)
    total_pages = len(src)

    for i, page in enumerate(src):
        # Render at 2x resolution for quality
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csRGB)

        # Invert every pixel
        pix.invert_irect(pix.irect)

        # Create new page and insert inverted image
        new_page = out.new_page(width=page.rect.width, height=page.rect.height)
        new_page.insert_image(new_page.rect, pixmap=pix)
        
        # Update progress
        progress_bar.progress((i + 1) / total_pages)

    # Save to a bytes buffer instead of a file
    output_buffer = io.BytesIO()
    out.save(output_buffer, garbage=4, deflate=True)
    out.close()
    src.close()
    
    return output_buffer.getvalue()

if uploaded_file is not None:
    if st.button("Convert to Dark Mode"):
        with st.spinner("Processing... This may take a moment for large PDFs."):
            try:
                pdf_bytes = uploaded_file.read()
                dark_pdf = convert_to_dark_mode(pdf_bytes)
                
                st.success("✅ Conversion Complete!")
                st.download_button(
                    label="Download Dark Mode PDF",
                    data=dark_pdf,
                    file_name=f"dark_{uploaded_file.name}",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")