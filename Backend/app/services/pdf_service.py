"""
PDF Service
Generates PDF documents with requirement analysis results
"""

from typing import List
from io import BytesIO
from datetime import datetime
import html
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from app.schemas.models import RequirementResult, ProcessingResponse
from app.core.config import settings
from app.core.logger import get_logger
from app.core.exceptions import PDFGenerationException

logger = get_logger(__name__)


class PDFService:
    """
    Service for generating PDF reports of requirement analysis
    """

    def __init__(self):
        """Initialize PDF service"""
        logger.info("Initializing PDF Service")
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    @staticmethod
    def _escape_text(text: str) -> str:
        """
        Escape text for safe use in PDF Paragraphs
        Handles special characters like tildes, ñ, etc.

        Args:
            text: Text to escape

        Returns:
            Escaped text safe for ReportLab
        """
        if not text:
            return ""
        # Escape HTML special characters
        return html.escape(str(text))

    def _setup_custom_styles(self):
        """Setup custom paragraph styles - Usability theme"""
        # Title style - Minimalista con color pastel
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=26,
            textColor=colors.HexColor('#059669'),  # Verde menta
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        # Subtitle style - Azul suave
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#0284c7'),  # Azul cielo
            spaceAfter=12,
            spaceBefore=16,
            fontName='Helvetica-Bold'
        ))

        # Requirement style
        self.styles.add(ParagraphStyle(
            name='Requirement',
            parent=self.styles['BodyText'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6,
            leftIndent=20,
            textColor=colors.HexColor('#374151')
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#111827'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))

    def generate_pdf(
        self,
        response: ProcessingResponse,
        filename: str = "requisitos_usabilidad_perseus.pdf"
    ) -> BytesIO:
        """
        Generate a PDF report from processing response

        Args:
            response: Processing response with requirement results
            filename: Output filename

        Returns:
            BytesIO buffer with PDF content

        Raises:
            PDFGenerationException: If PDF generation fails
        """
        try:
            logger.info(f"Generating PDF report with {response.total_comments} comments")

            # Create PDF buffer
            buffer = BytesIO()

            # Create document with UTF-8 support
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18,
                title="Informe de Requisitos de Usabilidad",
                author="Perseus",
                subject="Análisis de Requisitos de Usabilidad ISO 25010:2023"
            )

            # Build content
            story = []

            # Add header
            story.extend(self._build_header(response))

            # Add summary statistics
            story.extend(self._build_summary(response))

            # Add requirements table
            story.extend(self._build_requirements_table(response))

            # Add detailed requirements
            story.extend(self._build_detailed_requirements(response))

            # Build PDF
            doc.build(story)

            # Reset buffer position
            buffer.seek(0)

            logger.info("PDF generated successfully")
            return buffer

        except Exception as e:
            error_msg = f"Failed to generate PDF: {str(e)}"
            logger.error(error_msg)
            raise PDFGenerationException(error_msg, details={"error": str(e)})

    def _build_header(self, response: ProcessingResponse) -> List:
        """Build PDF header section"""
        story = []

        # Title - Enfocado en Usabilidad
        title = Paragraph(
            "Informe de Requisitos de Usabilidad",
            self.styles['CustomTitle']
        )
        story.append(title)

        # Subtitle - ISO 25010:2023
        subtitle = Paragraph(
            "Análisis basado en ISO/IEC 25010:2023",
            self.styles['Normal']
        )
        subtitle.style.alignment = TA_CENTER
        subtitle.style.textColor = colors.HexColor('#6b7280')
        subtitle.style.fontSize = 11
        story.append(subtitle)
        story.append(Spacer(1, 0.3 * inch))

        # Metadata con diseño minimalista
        metadata = f"""
        <para alignment="center" fontSize="10" textColor="#374151">
        <b>Fecha de generación:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}<br/>
        <b>Fuente de datos:</b> {response.source_type.upper()}<br/>
        <b>Sistema:</b> Perseus - Extracción de Requisitos de Usabilidad
        </para>
        """
        story.append(Paragraph(metadata, self.styles['Normal']))
        story.append(Spacer(1, 0.4 * inch))

        return story

    def _build_summary(self, response: ProcessingResponse) -> List:
        """Build summary statistics section - Minimalista"""
        story = []

        # Summary title
        story.append(Paragraph("📊 Resumen del Análisis", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.15 * inch))

        # Statistics table con diseño minimalista y colores pasteles
        data = [
            ["Métrica", "Valor"],
            ["Comentarios procesados", str(response.total_comments)],
            ["Requisitos de usabilidad identificados", str(response.valid_requirements)],
            [
                "Tasa de identificación",
                f"{(response.valid_requirements / response.total_comments * 100):.1f}%"
                if response.total_comments > 0 else "0%"
            ]
        ]

        table = Table(data, colWidths=[3.8 * inch, 2.2 * inch])
        table.setStyle(TableStyle([
            # Header con verde menta pastel
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d1fae5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#059669')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            # Filas alternas con colores pasteles suaves
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#f9fafb')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#ffffff')),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#f9fafb')),
            # Bordes minimalistas
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#6ee7b7')),
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]))

        story.append(table)
        story.append(Spacer(1, 0.4 * inch))

        return story

    def _build_requirements_table(self, response: ProcessingResponse) -> List:
        """Build requirements summary table - Diseño minimalista con colores pasteles"""
        story = []

        # Get only valid requirements
        valid_reqs = [r for r in response.requirements if r.is_requirement]

        if not valid_reqs:
            story.append(Paragraph(
                "No se identificaron requisitos de usabilidad en los comentarios analizados.",
                self.styles['Normal']
            ))
            return story

        # Count by subcharacteristic
        subchar_counts = {}
        for req in valid_reqs:
            subchar = req.subcharacteristic or "Sin clasificar"
            subchar_counts[subchar] = subchar_counts.get(subchar, 0) + 1

        # Colores pasteles para cada subcaracterística de usabilidad
        subchar_colors = {
            "Operabilidad": '#d1fae5',  # Verde menta
            "Aprendizabilidad": '#bae6fd',  # Azul cielo
            "Involucración del usuario": '#fbcfe8',  # Rosa
            "Reconocibilidad de adecuación": '#ddd6fe',  # Lavanda
            "Protección frente a errores de usuario": '#fed7aa',  # Naranja coral
            "Inclusividad": '#fef08a',  # Amarillo
            "Auto descriptividad": '#a5f3fc',  # Turquesa
            "Asistencia al usuario": '#c7d2fe',  # Índigo
        }

        # Distribution table
        story.append(Paragraph(
            "🎯 Distribución por Subcaracterísticas de Usabilidad ISO/IEC 25010:2023",
            self.styles['CustomSubtitle']
        ))
        story.append(Spacer(1, 0.15 * inch))

        data = [["Subcaracterística de Usabilidad", "Cantidad", "Porcentaje"]]
        sorted_subcars = sorted(subchar_counts.items(), key=lambda x: x[1], reverse=True)

        for subchar, count in sorted_subcars:
            percentage = (count / len(valid_reqs) * 100)
            data.append([subchar, str(count), f"{percentage:.1f}%"])

        table = Table(data, colWidths=[3.2 * inch, 1.5 * inch, 1.3 * inch])

        # Estilos base
        table_styles = [
            # Header con azul pastel
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#bae6fd')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0284c7')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            # Bordes minimalistas
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#7dd3fc')),
            ('LINEBELOW', (0, 1), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
            ('TOPPADDING', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ]

        # Aplicar colores pasteles a cada fila según la subcaracterística
        for idx, (subchar, _) in enumerate(sorted_subcars, start=1):
            bg_color = subchar_colors.get(subchar, '#f9fafb')
            table_styles.append(('BACKGROUND', (0, idx), (-1, idx), colors.HexColor(bg_color)))

        table.setStyle(TableStyle(table_styles))

        story.append(table)
        story.append(Spacer(1, 0.4 * inch))

        return story

    def _build_detailed_requirements(self, response: ProcessingResponse) -> List:
        """Build detailed requirements section - Diseño minimalista"""
        story = []

        valid_reqs = [r for r in response.requirements if r.is_requirement]

        if not valid_reqs:
            return story

        # Colores para cada subcaracterística
        subchar_colors = {
            "Operabilidad": '#059669',
            "Aprendizabilidad": '#0284c7',
            "Involucración del usuario": '#db2777',
            "Reconocibilidad de adecuación": '#7c3aed',
            "Protección frente a errores de usuario": '#ea580c',
            "Inclusividad": '#ca8a04',
            "Auto descriptividad": '#0891b2',
            "Asistencia al usuario": '#4f46e5',
        }

        story.append(PageBreak())
        story.append(Paragraph("📋 Requisitos de Usabilidad Identificados", self.styles['CustomSubtitle']))
        story.append(Spacer(1, 0.3 * inch))

        for idx, req in enumerate(valid_reqs, 1):
            # Color según subcaracterística
            subchar_color = subchar_colors.get(req.subcharacteristic, '#374151')

            # Requirement header con color
            subchar_escaped = self._escape_text(req.subcharacteristic)
            header_text = f'<font color="{subchar_color}"><b>Requisito {idx}: {subchar_escaped}</b></font>'
            story.append(Paragraph(header_text, self.styles['SectionHeader']))
            story.append(Spacer(1, 0.1 * inch))

            # Original comment en recuadro minimalista
            comment_escaped = self._escape_text(req.comment)
            comment_text = f'<para fontSize="9" textColor="#6b7280" leftIndent="15" rightIndent="15" spaceBefore="3" spaceAfter="3"><b>💬 Comentario del usuario:</b><br/><i>"{comment_escaped}"</i></para>'
            story.append(Paragraph(comment_text, self.styles['Normal']))
            story.append(Spacer(1, 0.12 * inch))

            # Generated description
            if req.description:
                desc_escaped = self._escape_text(req.description)
                desc_text = f'<para fontSize="10" textColor="#111827" leftIndent="15" rightIndent="15"><b>📝 Requisito formal:</b> {desc_escaped}</para>'
                story.append(Paragraph(desc_text, self.styles['Normal']))
                story.append(Spacer(1, 0.1 * inch))

            # Confidence scores - diseño minimalista
            confidence_text = f'<para fontSize="9" textColor="#6b7280" leftIndent="15"><b>🎯 Nivel de confianza:</b> {req.binary_score:.1%}'
            if req.multiclass_score:
                confidence_text += f' (Clasificación: {req.multiclass_score:.1%})'
            confidence_text += '</para>'
            story.append(Paragraph(confidence_text, self.styles['Normal']))

            # Separador sutil entre requisitos
            story.append(Spacer(1, 0.05 * inch))
            separator = Table([['']], colWidths=[6 * inch])
            separator.setStyle(TableStyle([
                ('LINEBELOW', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
            ]))
            story.append(separator)
            story.append(Spacer(1, 0.25 * inch))

        return story


# Global service instance
pdf_service = PDFService()
