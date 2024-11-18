import matplotlib.pyplot as plt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class Reporte:
    def __init__(self, df):
        self.df = df

    def generar_grafico_barras(self, columna):
        plt.figure(figsize=(10, 6))
        self.df[columna].value_counts().plot(kind='bar')
        plt.title(f'Gráfico de barras - {columna}')
        plt.xlabel(columna)
        plt.ylabel('Frecuencia')
        plt.tight_layout()
        return plt.gcf()

    def generar_grafico_pastel(self, columna):
        plt.figure(figsize=(10, 6))
        self.df[columna].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title(f'Gráfico de pastel - {columna}')
        plt.axis('equal')
        plt.tight_layout()
        return plt.gcf()

    def generar_tabla_frecuencias(self, columna):
        return self.df[columna].value_counts().reset_index()

    def exportar_pdf(self, filename):
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Título del reporte
        story.append(Paragraph("Reporte de Encuesta", styles['Title']))
        story.append(Spacer(1, 12))

        # Analizar cada columna
        for columna in self.df.columns:
            # Título de la sección
            story.append(Paragraph(f"Análisis de {columna}", styles['Heading2']))
            story.append(Spacer(1, 12))

            # Tabla de frecuencias
            tabla = self.generar_tabla_frecuencias(columna)
            data = [['Valor', 'Frecuencia']] + tabla.values.tolist()
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 12),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(t)
            story.append(Spacer(1, 12))

            # Gráfico de barras
            fig = self.generar_grafico_barras(columna)
            img_data = io.BytesIO()
            fig.savefig(img_data, format='png')
            img_data.seek(0)
            img = Image(img_data)
            img.drawHeight = 300
            img.drawWidth = 500
            story.append(img)
            story.append(Spacer(1, 12))
            plt.close(fig)

            # Gráfico de pastel
            fig = self.generar_grafico_pastel(columna)
            img_data = io.BytesIO()
            fig.savefig(img_data, format='png')
            img_data.seek(0)
            img = Image(img_data)
            img.drawHeight = 300
            img.drawWidth = 500
            story.append(img)
            story.append(Spacer(1, 12))
            plt.close(fig)

        # Construir el PDF
        doc.build(story)