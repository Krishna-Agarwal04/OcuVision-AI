import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon, Group

def create_architecture_diagram():
    # Create a vector drawing for the System Architecture
    # Width: 500, Height: 200
    d = Drawing(520, 220)
    
    # Theme Colors
    primary_color = colors.HexColor("#0b3c5d")
    secondary_color = colors.HexColor("#3282b8")
    accent_color = colors.HexColor("#22c55e")
    bg_color = colors.HexColor("#f4f8fb")
    text_color = colors.HexColor("#1f2d3d")
    
    # 1. Frontend Box
    d.add(Rect(10, 10, 120, 60, fillColor=bg_color, strokeColor=primary_color, strokeWidth=2, rx=5, ry=5))
    d.add(String(25, 45, "Client (Next.js)", fontName="Helvetica-Bold", fontSize=11, fillColor=primary_color))
    d.add(String(20, 25, "Vercel Cloud Hosting", fontName="Helvetica", fontSize=8, fillColor=text_color))
    
    # Arrow 1: Frontend -> Backend
    d.add(Line(130, 40, 190, 40, strokeColor=secondary_color, strokeWidth=2))
    # Arrowhead
    d.add(Polygon([185, 45, 195, 40, 185, 35], fillColor=secondary_color, strokeColor=secondary_color))
    d.add(String(140, 48, "Multipart API", fontName="Helvetica-Oblique", fontSize=7, fillColor=text_color))

    # 2. Backend Box
    d.add(Rect(195, 10, 130, 60, fillColor=bg_color, strokeColor=primary_color, strokeWidth=2, rx=5, ry=5))
    d.add(String(215, 45, "API Server (FastAPI)", fontName="Helvetica-Bold", fontSize=11, fillColor=primary_color))
    d.add(String(225, 25, "Render Web Service", fontName="Helvetica", fontSize=8, fillColor=text_color))
    
    # Arrow 2: Backend -> ML Model
    d.add(Line(325, 40, 385, 40, strokeColor=secondary_color, strokeWidth=2))
    d.add(Polygon([380, 45, 390, 40, 380, 35], fillColor=secondary_color, strokeColor=secondary_color))
    d.add(String(335, 48, "Inference Req", fontName="Helvetica-Oblique", fontSize=7, fillColor=text_color))

    # 3. ML Model Box
    d.add(Rect(390, 10, 120, 60, fillColor=bg_color, strokeColor=primary_color, strokeWidth=2, rx=5, ry=5))
    d.add(String(410, 45, "ML Engine (PyTorch)", fontName="Helvetica-Bold", fontSize=11, fillColor=primary_color))
    d.add(String(415, 25, "ResNet-50 Classifier", fontName="Helvetica", fontSize=8, fillColor=text_color))
    
    # Arrow 3 (Return): ML Model -> Backend
    d.add(Line(385, 20, 325, 20, strokeColor=secondary_color, strokeWidth=1.5))
    d.add(Polygon([330, 23, 320, 20, 330, 17], fillColor=secondary_color, strokeColor=secondary_color))
    d.add(String(335, 10, "Prediction Output", fontName="Helvetica-Oblique", fontSize=7, fillColor=text_color))
    
    # Vertical Arrow: Backend <-> Database
    d.add(Line(260, 70, 260, 130, strokeColor=secondary_color, strokeWidth=2))
    d.add(Polygon([255, 75, 260, 65, 265, 75], fillColor=secondary_color, strokeColor=secondary_color))
    d.add(Polygon([255, 125, 260, 135, 265, 125], fillColor=secondary_color, strokeColor=secondary_color))
    d.add(String(268, 98, "Read/Write SQL", fontName="Helvetica-Oblique", fontSize=7, fillColor=text_color))

    # 4. Database Box
    d.add(Rect(195, 135, 130, 60, fillColor=bg_color, strokeColor=primary_color, strokeWidth=2, rx=5, ry=5))
    d.add(String(220, 170, "Relational DB", fontName="Helvetica-Bold", fontSize=11, fillColor=primary_color))
    d.add(String(205, 150, "SQLite (retino_db.sqlite)", fontName="Helvetica", fontSize=8, fillColor=text_color))

    return d

def build_pdf():
    pdf_path = "OcuVision_AI_Project_Report.pdf"
    
    # Set document properties
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54, # 0.75 in
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Define custom styles
    primary_color = colors.HexColor("#0b3c5d")
    secondary_color = colors.HexColor("#3282b8")
    text_color = colors.HexColor("#1f2d3d")
    muted_color = colors.HexColor("#64748b")
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=primary_color,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=secondary_color,
        spaceAfter=40
    )
    
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=text_color,
        spaceAfter=30
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceBefore=15,
        spaceAfter=12,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=secondary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=text_color,
        spaceAfter=10
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=20,
        bulletIndent=8,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=12,
        textColor=colors.white
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=text_color
    )

    story = []
    
    # ------------------ COVER PAGE ------------------
    story.append(Spacer(1, 40))
    story.append(Paragraph("👁️ OCUVISION AI", title_style))
    story.append(Paragraph("Deep Learning Retinal Screening Platform for Diabetic Retinopathy Detection", subtitle_style))
    
    story.append(Spacer(1, 20))
    
    meta_content = """
    <b>Technical Documentation & Project Report</b><br/><br/>
    <b>Prepared By:</b><br/>
    Krishna Agarwal<br/>
    Prakhar Goel<br/><br/>
    <b>Date:</b> July 2026<br/>
    <b>GitHub Code Link:</b> <font color="#3282b8">https://github.com/Krishna-Agarwal04/OcuVision-AI</font><br/>
    <b>Live App Link:</b> <font color="#3282b8">https://ocu-vision-ai.vercel.app</font>
    """
    story.append(Paragraph(meta_content, meta_style))
    story.append(Spacer(1, 100))
    
    story.append(Paragraph("<font color='#64748b'>This documentation covers the technical specifications, system architecture, database models, deep learning parameters, and production deployment details of the OcuVision AI platform.</font>", body_style))
    story.append(PageBreak())
    
    # ------------------ SECTION 1: EXECUTIVE SUMMARY ------------------
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "Diabetic Retinopathy (DR) is a severe microvascular complication of diabetes mellitus and remains a primary cause of blindness in working-class adults worldwide. Early screening and staging are critical to prevent total visual loss. However, local screening in rural areas is hindered by a severe shortage of qualified ophthalmologists and diagnostic machinery.",
        body_style
    ))
    story.append(Paragraph(
        "<b>OcuVision AI</b> solves this accessibility barrier by providing a high-performance, web-based intelligent diagnostic platform. Using <b>ResNet-50 Convolutional Neural Networks</b>, the system classifies retinal fundus images into five distinct severity stages (No DR, Mild, Moderate, Severe, Proliferative DR) in real-time. Designed as a production monorepo, the project provides a fully integrated clinician login portal, an interactive screening dashboard, and historical patient scan log tables.",
        body_style
    ))
    
    story.append(Spacer(1, 10))

    # ------------------ SECTION 2: TECHNOLOGY STACK ------------------
    story.append(Paragraph("2. Technical Specifications & Stack", h1_style))
    story.append(Paragraph(
        "The project is architected as a decoupled system featuring a responsive client layer, a transactional REST API gateway, and a dedicated machine learning inference engine:",
        body_style
    ))
    
    # Table data
    data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technology Used", table_header_style), Paragraph("Functional Description", table_header_style)],
        
        [Paragraph("<b>Frontend UI</b>", table_cell_style), 
         Paragraph("Next.js 14, React 18, TypeScript, Tailwind/Vanilla CSS", table_cell_style), 
         Paragraph("Responsive clinician-facing dashboard, authentication, image uploading, and history tracking.", table_cell_style)],
        
        [Paragraph("<b>Backend API</b>", table_cell_style), 
         Paragraph("FastAPI, Python 3.10, Uvicorn, SQLAlchemy", table_cell_style), 
         Paragraph("Handles registration, secure login password validation, database session binding, and routes.", table_cell_style)],
        
        [Paragraph("<b>Database</b>", table_cell_style), 
         Paragraph("SQLite (retino_db.sqlite)", table_cell_style), 
         Paragraph("Relational DB tables to store user details (hashed) and scanning diagnosis logs.", table_cell_style)],
         
        [Paragraph("<b>ML Inference</b>", table_cell_style), 
         Paragraph("PyTorch, Torchvision, ResNet-50", table_cell_style), 
         Paragraph("Runs CPU-optimized forward inference checks on uploaded fundus images and returns predictions.", table_cell_style)]
    ]
    
    # Build Table
    t = Table(data, colWidths=[1.1*inch, 2.0*inch, 3.9*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#f8fafc")]),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
    ]))
    
    story.append(t)
    story.append(Spacer(1, 15))
    story.append(PageBreak())

    # ------------------ SECTION 3: SYSTEM ARCHITECTURE ------------------
    story.append(Paragraph("3. System Architecture Diagram", h1_style))
    story.append(Paragraph(
        "The diagram below describes the data flow. The Next.js frontend sends image data in a multipart form-data request to the FastAPI server. FastAPI saves the metadata to the SQLite DB and performs inference through the PyTorch module, returning a JSON response.",
        body_style
    ))
    story.append(Spacer(1, 10))
    story.append(create_architecture_diagram())
    story.append(Spacer(1, 15))
    
    # ------------------ SECTION 4: DEEP LEARNING MODEL ------------------
    story.append(Paragraph("4. Deep Learning & Staging Metrics", h1_style))
    story.append(Paragraph(
        "<b>Model Training & Transfer Learning:</b><br/>"
        "The model is a pre-trained ResNet-50 model fine-tuned on the APTOS 2019 dataset. To ensure high accuracy, early layers are frozen, and deep features in layer3 and layer4 are unfrozen to adapt to retinal artifacts (microaneurysms, hemorrhages, and hard exudates).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Imbalance Optimization:</b><br/>"
        "Retinal datasets often suffer from significant class imbalance (high normal counts vs low proliferative counts). In the training script (<code>train_model.py</code>), we compute class frequencies and feed inverse weight ratios to the <code>CrossEntropyLoss</code> function, ensuring minority severe stages are detected with equal sensitivity.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Performance Metrics:</b><br/>"
        "• <b>Validation Accuracy:</b> 80.0% - 85.0% on 5-class staging.<br/>"
        "• <b>Severe DR Detection Sensitivity:</b> 82%+ recall (critical for medical systems to avoid false negatives).",
        body_style
    ))
    story.append(PageBreak())

    # ------------------ SECTION 5: REAL-WORLD ROADMAP ------------------
    story.append(Paragraph("5. Real-World Deployment Roadmap", h1_style))
    story.append(Paragraph(
        "While the current prototype is fully functional and successfully hosted on Vercel and Render, scaling OcuVision AI into a commercial clinical environment requires the following phases:",
        body_style
    ))
    
    story.append(Paragraph("<b>Phase 1: Clinical Validation & Blind Trials</b>", h2_style))
    story.append(Paragraph("Run parallel validation testing in collaboration with local clinics. Assess the system against double-blind diagnoses by certified ophthalmologists to create a clinical performance baseline.", bullet_style))
    
    story.append(Paragraph("<b>Phase 2: Data Encryption & HIPAA Compliance</b>", h2_style))
    story.append(Paragraph("• Upgrade database layer to a secure PostgreSQL cluster.<br/>"
                           "• Implement AES-256 encryption at rest for patient images and personal health identifiers (PHI).<br/>"
                           "• Transition to OAuth2 JWT Token authentication with automated expiration.", bullet_style))
    
    story.append(Paragraph("<b>Phase 3: Production Auto-Scaling</b>", h2_style))
    story.append(Paragraph("• Package the FastAPI service in Docker container layers and deploy to AWS ECS (Elastic Container Service) behind an Application Load Balancer.<br/>"
                           "• Attach GPU instances (such as AWS G4dn instances) to handle high concurrent screening volumes with sub-100ms API response time.", bullet_style))
                           
    story.append(Paragraph("<b>Phase 4: Portable Edge Devices Integration</b>", h2_style))
    story.append(Paragraph("Convert PyTorch models to optimized ONNX or TensorFlow Lite formats to run local, offline predictions directly on handheld fundus camera tablets in remote areas without internet.", bullet_style))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph("6. Conclusion", h1_style))
    story.append(Paragraph(
        "OcuVision AI demonstrates how modern web technologies and deep learning can democratize medical screening. By deploying this system onto cloud platforms like Vercel and Render, we prove that accessible, low-latency, and high-fidelity screening platforms are viable, cost-effective solutions to prevent global diabetic blindness.",
        body_style
    ))
    
    # Build Document
    doc.build(story)
    print("Report PDF generated successfully!")

if __name__ == "__main__":
    build_pdf()
