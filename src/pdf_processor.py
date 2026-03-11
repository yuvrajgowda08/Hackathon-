import fitz


def extract_text_from_pdf(file):

    file.seek(0)  # reset file pointer

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    text = ""

    for page in pdf:
        text += page.get_text()

    return text