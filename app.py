import os
import tempfile
from flask import Flask, render_template, request, send_file
from ebooklib import epub
from bs4 import BeautifulSoup
from weasyprint import HTML

# Define explicitamente onde está a pasta de templates (mesmo diretório deste arquivo)
template_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__, template_folder=os.path.join(template_dir, 'templates'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'epub_file' not in request.files:
        return "Nenhum arquivo enviado", 400
    
    file = request.files['epub_file']
    if file.filename == '':
        return "Arquivo inválido", 400

    with tempfile.TemporaryDirectory() as tmpdir:
        epub_path = os.path.join(tmpdir, "input.epub")
        file.save(epub_path)

        try:
            book = epub.read_epub(epub_path)
            
            html_content = "<html><head><meta charset='utf-8'><style>body { font-family: sans-serif; line-height: 1.6; margin: 20px; }</style></head><body>"
            
            for item in book.get_items():
                if item.get_type() == epub.ITEM_DOCUMENT:
                    soup = BeautifulSoup(item.get_content(), 'html.parser')
                    body = soup.find('body')
                    if body:
                        html_content += str(body)
                    else:
                        html_content += str(soup)
                        
            html_content += "</body></html>"

            pdf_path = os.path.join(tmpdir, "output.pdf")
            HTML(string=html_content).write_pdf(pdf_path)

            return send_file(
                pdf_path, 
                as_attachment=True, 
                download_name=os.path.splitext(file.filename)[0] + ".pdf",
                mimetype='application/pdf'
            )

        except Exception as e:
            return f"Erro ao processar o EPUB: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
