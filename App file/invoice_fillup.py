from docx import Document
from datetime import date

def fill_invoice(data):
    # Load the invoice template
    template_path = r"F:\Python Code-Lab\Store-Management-System-Project\self made invoice template (IMPORTANT).docx"

    doc = Document(template_path)
    output_path = f"{data.get('[Name]', 'Unknown')}_{data.get('[invoice id]', '0000')}invoice_record.docx"

    # Replace all placeholders in paragraphs
    for para in doc.paragraphs:
        for key, value in data.items():
            if key in para.text:
                for run in para.runs:
                    run.text = run.text.replace(key, value)


    # Replace placeholders in tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in data.items():
                    if key in cell.text:
                        cell.text = cell.text.replace(key, value)
                # Clear any missing placeholders in tables
                for i in range(1, 21):
                    product_key = f"[Product{i}]"
                    amount_key = f"[amount{i}]"
                    price_key = f"[price{i}]"
                    cell.text = cell.text.replace(product_key, data.get(product_key, ""))
                    cell.text = cell.text.replace(amount_key, data.get(amount_key, ""))
                    cell.text = cell.text.replace(price_key, data.get(price_key, ""))

    # Save the filled invoice
    doc.save(output_path)

# Example of how the data dictionary might look
data = {
    '[Name]': "Someone",
    '[Phone]': "017145375",
    '[Email]': "",
    '[date]': str(date.today()),
    '[invoice id]': "7567657",
    '[Product1]': "Anker Soundcore Space Q45",
    '[amount1]': "1",
    '[price1]': "1200",
    '[Product2]': "Apple AirPods Pro",
    '[amount2]': "2",
    '[price2]': "3000",
    # Add more products as needed
}

fill_invoice(data)