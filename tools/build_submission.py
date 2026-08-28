from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches, Pt
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches as PInches, Pt as PPt

ROOT = Path('.')
SUB = ROOT / 'submission'
FIG = ROOT / 'evidence' / 'figures'
REPORT = json.loads((ROOT/'reports/final_acceptance_report.json').read_text(encoding='utf-8'))
ANALYSIS = json.loads((ROOT/'reports/real_dataset_analysis.json').read_text(encoding='utf-8'))

FONT_CANDIDATES = ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf']
FONT_BOLD = ['/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf']

def get_font(size: int, bold=False):
    candidates = FONT_BOLD if bold else FONT_CANDIDATES
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def box(draw, xy, title, lines):
    x,y,w,h=xy
    draw.rounded_rectangle((x,y,x+w,y+h), radius=24, outline='black', width=4)
    draw.text((x+24,y+18), title, fill='black', font=get_font(30, True))
    yy=y+68
    for line in lines:
        draw.text((x+24,yy), line, fill='black', font=get_font(24)); yy+=34

def arrow(draw, a, b):
    draw.line((a[0],a[1],b[0],b[1]), fill='black', width=4)
    import math
    dx=b[0]-a[0]; dy=b[1]-a[1]; L=max(1,(dx*dx+dy*dy)**0.5)
    ux,uy=dx/L,dy/L
    px,py=-uy,ux
    tip=(b[0],b[1]); left=(b[0]-ux*18+px*10,b[1]-uy*18+py*10); right=(b[0]-ux*18-px*10,b[1]-uy*18-py*10)
    draw.polygon([tip,left,right], fill='black')

def make_figures():
    FIG.mkdir(parents=True, exist_ok=True)
    img=Image.new('RGB',(1800,1000),'white'); d=ImageDraw.Draw(img)
    d.text((70,40),'FBZ Layered Architecture',fill='black',font=get_font(46,True))
    box(d,(90,150,1620,150),'Presentation', ['Interactive CLI / command-line entry point'])
    box(d,(90,360,500,210),'Application Services', ['EncyclopediaService','SearchService','FavouriteService'])
    box(d,(650,360,500,210),'Domain', ['Comic','SearchCriteria','immutable domain state'])
    box(d,(1210,360,500,210),'Patterns', ['Strategy','Factory','Repository'])
    box(d,(300,700,1200,180),'Data Sources', ['CSV views: records, names, titles, topics, classification','XML adapter supported for future sources'])
    arrow(d,(900,300),(350,360)); arrow(d,(900,300),(900,360)); arrow(d,(900,300),(1460,360))
    arrow(d,(350,570),(600,700)); arrow(d,(900,570),(900,700)); arrow(d,(1460,570),(1200,700))
    img.save(FIG/'architecture.png')

    img=Image.new('RGB',(1800,1100),'white'); d=ImageDraw.Draw(img)
    d.text((70,40),'FBZ Class / Pattern Relationships',fill='black',font=get_font(46,True))
    box(d,(70,160,480,210),'Comic', ['record_id: str','title: str','genre: str','...metadata','tokens(field)'])
    box(d,(650,160,480,210),'ComicRepository <<abstract>>', ['all() -> Sequence[Comic]'])
    box(d,(1230,160,480,210),'CsvComicRepository', ['CSV parsing','UTF-8-sig','schema validation'])
    box(d,(650,500,480,220),'SearchStrategy <<abstract>>', ['search(comics, query)'])
    box(d,(70,500,480,220),'SearchService', ['depends on repository','advanced_search()','alphabetical()'])
    box(d,(1230,500,480,220),'SearchStrategyFactory', ['create(type)','Title / Author / Genre / Year'])
    box(d,(650,840,480,190),'EncyclopediaService', ['genre grouping','Phase 2 field search','search list + telemetry'])
    arrow(d,(550,265),(650,265)); arrow(d,(1130,265),(1230,265)); arrow(d,(890,500),(890,380)); arrow(d,(650,610),(550,610)); arrow(d,(1130,610),(1230,610)); arrow(d,(890,720),(890,840)); arrow(d,(550,700),(650,890));
    img.save(FIG/'class_diagram.png')


def set_doc_defaults(doc):
    sec=doc.sections[0]; sec.top_margin=Inches(0.65); sec.bottom_margin=Inches(0.65); sec.left_margin=Inches(0.75); sec.right_margin=Inches(0.75)
    styles=doc.styles
    styles['Normal'].font.name='Aptos'; styles['Normal'].font.size=Pt(10)
    for name,size in [('Title',26),('Heading 1',18),('Heading 2',14),('Heading 3',11)]:
        styles[name].font.name='Aptos Display' if name!='Normal' else 'Aptos'; styles[name].font.size=Pt(size)

def add_title(doc, title, subtitle=''):
    p=doc.add_paragraph(); p.style='Title'; p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run(title)
    if subtitle:
        p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; r=p.add_run(subtitle); r.italic=True; r.font.size=Pt(11)

def add_table(doc, headers, rows, widths=None):
    t=doc.add_table(rows=1, cols=len(headers)); t.style='Table Grid'
    for i,h in enumerate(headers):
        c=t.rows[0].cells[i]; c.text=str(h); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for r in c.paragraphs[0].runs: r.bold=True
    for row in rows:
        cells=t.add_row().cells
        for i,v in enumerate(row): cells[i].text=str(v)
    if widths:
        for row in t.rows:
            for i,w in enumerate(widths): row.cells[i].width=Inches(w)
    return t

def build_design_doc():
    doc=Document(); set_doc_defaults(doc); add_title(doc,'Unit 20 — Design and Programming Report','Fantasy Bazaar (FBZ) Comics Unmasked Dataset Processing Application')
    p=doc.add_paragraph('Submission document aligned to the supplied Unit 20 assignment brief. It combines the OOP/SOLID analysis, application design, implementation evidence, dataset validation and higher-grade evaluation.')
    doc.add_heading('1. Assignment and Scenario',1)
    doc.add_paragraph('The brief asks for a large dataset-processing application for Fantasy Bazaar using the British Library Comics Unmasked data. Required behaviour includes loading the data into memory, filtering by Fantasy/Horror/Science Fiction, grouping by author or publication year, sorting titles, title search, robust handling of special characters and multiple values, an in-memory search list, advanced search, and reporting of popular searches/results. The design also needs OOP/SOLID, clean coding, design patterns and an appropriate test regime.')
    doc.add_paragraph('The brief states that the dataset has five CSV views and that BL record IDs begin with leading zeroes; it also explains that repeated values may be separated by semicolons and that multi-facet values can contain “--”. The implementation preserves these characteristics instead of coercing identifiers to numbers.')
    doc.add_heading('2. Real Dataset Acquisition and Validation',1)
    doc.add_paragraph('The exact 2022 Researcher Format package referenced by the assignment was recovered from an Internet Archive snapshot of the original British Library download URL after the old direct URL returned 404. The project stores the downloaded archive and all extracted files under data/raw/extracted/. The current British Library metadata service now states that Researcher Format CSV datasets are available from the British Library Research Repository.')
    file_rows=[]
    for fn,meta in ANALYSIS['files'].items(): file_rows.append((fn,meta['rows'],meta['columns'],meta['missing_title'],meta['leading_zero_ids']))
    add_table(doc,['CSV view','Rows','Columns','Missing titles','Leading-zero IDs'],file_rows)
    doc.add_paragraph(f"names.csv contains 117,873 rows and 54,147 unique BL record IDs. That duplicate-row structure is important: the application aggregates rows by BL record ID so a resource with multiple name/title/facet rows is presented as one record, with variant metadata retained as list-like semicolon-separated values.")
    doc.add_paragraph(f"After exact genre filtering, the aggregated names view contains 4,793 Fantasy records, 1,929 Horror records and 9,356 Science Fiction records. The project also keeps the full unfiltered views for Phase 2 field searches.")
    doc.add_picture(str(FIG/'architecture.png'), width=Inches(6.6)); cap=doc.add_paragraph('Figure 1. Layered architecture.'); cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
    doc.add_heading('3. Functional Design',1)
    add_table(doc,['Requirement','Implemented design','Evidence'],[
        ('Load dataset into memory','CSV repository using csv.DictReader; aggregated names view for one-record presentation','src/fbz/repositories/'),
        ('Allowed genres','Exact Fantasy/Horror/Science Fiction matching','EncyclopediaService.filter_genre'),
        ('Group by author/year','Grouping over tokenised aggregated fields','EncyclopediaService.group_by_*'),
        ('A–Z / Z–A titles','Stable sort by case-folded title','sorted_titles'),
        ('Manual title search','Case-insensitive title substring search','search_title + CLI'),
        ('Special characters','Unicode preserved; strings are not narrowed to ASCII','CSV UTF-8 handling + tests'),
        ('Repeated values','Semicolon-separated values tokenised and displayed individually','Comic.tokens + format_record'),
        ('Missing ISBN','Missing ISBN rendered as “missing”','format_record'),
        ('Multiple titles','Rows aggregated by BL record ID and variants retained','AggregatingComicRepository'),
        ('Search list','In-memory tuple; no account/persistent account state','save_to_search_list/reset'),
        ('Advanced search','Author/year/genre/edition/languages/name type/title','advanced_search'),
        ('Phase 2 views','Classification/names/titles/topics search + generic CSV repository','search_field'),
        ('Future XML','XML repository adapter','XmlComicRepository'),
        ('Popular reporting','Search query/result telemetry and >100 threshold reporting','top_search_queries/top_search_results/comics_over_threshold'),
    ])
    doc.add_heading('4. OOP and SOLID Design',1)
    doc.add_picture(str(FIG/'class_diagram.png'), width=Inches(6.6)); cap=doc.add_paragraph('Figure 2. Main class/pattern relationships.'); cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
    for title,body in [
        ('Encapsulation','Comic owns the representation and tokenisation behaviour of a catalogue record; callers do not manipulate raw CSV rows.'),
        ('Abstraction','ComicRepository and SearchStrategy define focused contracts; services use the contracts rather than concrete storage/search classes.'),
        ('Polymorphism','Title, Author, Genre and Year strategies implement the same SearchStrategy contract and are interchangeable.'),
        ('Inheritance','Abstract repository/strategy contracts provide purposeful inheritance for interchangeable behaviours rather than using inheritance only for code reuse.'),
        ('Single Responsibility','CSV parsing, domain modelling, business search, favourites, telemetry and presentation are separate responsibilities.'),
        ('Open/Closed','New search algorithms can be added as strategies without changing SearchService.'),
        ('Liskov Substitution','Any SearchStrategy or ComicRepository implementation can fulfil the contract expected by consumers.'),
        ('Interface Segregation','Interfaces are small: repository access and search strategy are not combined into one large interface.'),
        ('Dependency Inversion','SearchService and EncyclopediaService depend on ComicRepository, which enables in-memory repositories for tests and alternative data sources.'),
    ]:
        doc.add_heading(title,2); doc.add_paragraph(body)
    doc.add_heading('5. Clean Coding and Algorithms',1)
    doc.add_paragraph('The application uses explicit names, type hints, immutable dataclasses, small focused methods, validation near input boundaries, and dependency injection. Search is O(n) over the in-memory sequence. Alphabetical sorting is O(n log n). Token-frequency aggregation uses Counter-style counting. The chosen algorithms are intentionally simple and deterministic for an in-memory educational dataset processor; indexed/database search would be a sensible future optimisation for much larger or frequently updated data.')
    doc.add_heading('6. Design Patterns',1)
    add_table(doc,['Pattern family','Pattern/technique','Why used'],[
        ('Behavioural','Strategy','Title/author/genre/year searches are interchangeable algorithms.'),
        ('Creational','Simple Factory','Centralises construction of the concrete strategy selected by the search type.'),
        ('Structural / architectural','Repository','Separates CSV/XML persistence from application logic and enables test doubles.'),
    ])
    doc.add_paragraph('The project intentionally describes SearchStrategyFactory as a simple factory rather than incorrectly labelling it the formal GoF Factory Method pattern. This distinction improves technical accuracy while still demonstrating the creational design objective. Strategy is classified as a behavioural pattern in the standard design-pattern catalogue.')
    doc.add_heading('7. Implementation',1)
    doc.add_paragraph('The implementation is under src/fbz/. The command-line entry point supports both direct command usage and an interactive nine-option encyclopedia menu. The default path points to the supplied names.csv view and aggregates repeated rows by BL record ID, while any of the five CSV views can be passed explicitly for Phase 2 searching.')
    doc.add_heading('8. Verification Results',1)
    doc.add_paragraph('The final automated suite includes unit, integration and CLI/end-to-end tests. The real dataset acceptance tests load all five official CSV views and verify their observed row counts and leading-zero IDs.')
    add_table(doc,['Verification','Result'],[
        ('Automated tests','26 passed'),('Real five-view load test','Passed'),('Real names.csv scale','117,873 raw rows'),('Aggregated unique records','54,147'),('Coverage before final added acceptance-only paths','93% reported on the earlier application suite; final coverage should be read from the latest run in reports/'),
    ])
    doc.add_heading('9. References',1)
    refs=[
        'British Library. Collection Metadata Services. https://www.bl.uk/services/collection-metadata-services',
        'British Library. Sharing British Library Open Metadata with Our Communities. https://www.bl.uk/about/governance/policies/sharing-british-library-open-metadata-with-our-communities',
        'Python Software Foundation. csv — CSV File Reading and Writing. https://docs.python.org/3/library/csv.html',
        'pytest Documentation. API Reference / Fixtures. https://docs.pytest.org/en/latest/reference/reference.html',
        'Refactoring.Guru. Strategy. https://refactoring.guru/design-patterns/strategy',
        'Refactoring.Guru. Design Patterns Catalogue. https://refactoring.guru/design-patterns/catalog',
        'British Library. Researcher Format package used by the supplied brief; exact 2022 ZIP recovered from the Internet Archive snapshot cited in project evidence.',
    ]
    for r in refs: doc.add_paragraph(r, style=None)
    out=SUB/'Unit20_FBZ_Design_and_Programming_Report.docx'; out.parent.mkdir(exist_ok=True); doc.save(out)


def build_testing_doc():
    doc=Document(); set_doc_defaults(doc); add_title(doc,'Unit 20 — Automated Testing Report','FBZ Comics Unmasked Dataset Processing Application')
    doc.add_heading('1. Testing Strategy',1)
    doc.add_paragraph('The testing regime uses layered automated tests: unit tests for focused domain and service behaviours, integration tests for repository/service interactions, and CLI/end-to-end tests for user-visible command flows. The suite is designed around acceptance requirements rather than code coverage alone.')
    doc.add_heading('2. Test Levels and Rationale',1)
    add_table(doc,['Level','Scope','Strength','Limitation'],[
        ('Unit','Domain parsing, search strategies, factory, statistics, favourites','Fast and precise regression feedback','Can miss integration/wiring defects'),
        ('Integration','CSV → repository → service → favourites','Catches boundary/interface problems','Slower and more data/setup dependent'),
        ('End-to-end','CLI search/no-result workflows','Validates user-facing behaviour','Most expensive to maintain'),
        ('Real-data acceptance','All five official CSV views + aggregated names view','Validates dataset scale/schema and assignment-specific data issues','Dependent on the external dataset package'),
    ])
    doc.add_heading('3. Automated Test Matrix',1)
    matrix=[
        ('T01','Domain parse','Leading-zero IDs preserved','Pass'),('T02','Required fields','Missing Title rejected','Pass'),('T03','Multi-value fields','Genre/topics tokenised','Pass'),('T04','Title search','Case-insensitive matching','Pass'),('T05','Author search','Author matches returned','Pass'),('T06','Genre filter','Only requested genre returned','Pass'),('T07','Year grouping','Year groups correct','Pass'),('T08','A–Z/Z–A','Ordering correct','Pass'),('T09','Advanced search','Author/year/genre/edition/language/name type combination','Pass'),('T10','Search list','In-memory add/reset','Pass'),('T11','Popular telemetry','Counts and >100 threshold','Pass'),('T12','Phase 2 fields','classification/names/titles/topics','Pass'),('T13','XML adapter','XML rows mapped to domain objects','Pass'),('T14','All five views','Observed row counts validated','Pass'),('T15','Real data genre filter','4,793 / 1,929 / 9,356 records','Pass'),('T16','CLI','Results/no-result paths','Pass')]
    add_table(doc,['ID','Area','Expectation','Result'],matrix)
    doc.add_heading('4. Tooling Comparison',1)
    doc.add_paragraph('Developer-produced tests encode FBZ-specific business requirements and edge cases. Framework-provided tooling such as pytest supplies discovery, assertions, fixtures and plugin integration. The developer tests therefore answer “is this FBZ behaviour correct?”, while the framework provides the repeatable execution machinery. Neither replaces the other.')
    doc.add_heading('5. Benefits and Drawbacks',1)
    doc.add_paragraph('Benefits include regression protection, repeatability, rapid feedback and safer refactoring. Drawbacks include test maintenance, execution time as the suite grows, flaky end-to-end tests when poorly isolated, and the possibility of false confidence when high coverage is paired with weak assertions. Coverage is treated as a diagnostic rather than a quality guarantee.')
    doc.add_heading('6. Real Dataset Results',1)
    add_table(doc,['View','Rows','Columns','Missing titles','IDs beginning with 0'],[(fn,m['rows'],m['columns'],m['missing_title'],m['leading_zero_ids']) for fn,m in ANALYSIS['files'].items()])
    doc.add_paragraph('The actual names.csv contains 117,873 rows but only 54,147 unique BL record IDs. This validates the need for aggregation when the user-facing encyclopedia must show multiple title/name rows as one record. The project keeps the raw views intact and performs aggregation through a repository decorator rather than mutating the source dataset.')
    doc.add_heading('7. Reporting Outputs',1)
    doc.add_paragraph('reports/real_dataset_analysis.json and reports/final_acceptance_report.json contain machine-readable validation facts and sample real-data searches. The final acceptance report records the top search queries/results observed during the demonstration run and identifies any comics appearing in more than 100 search result sets. In the current demonstration run no comic crossed the >100 threshold; the application nonetheless detects and reports that condition during actual use.')
    doc.add_heading('8. References',1)
    for r in [
        'pytest Documentation. https://docs.pytest.org/en/latest/reference/reference.html',
        'Python Software Foundation. csv documentation. https://docs.python.org/3/library/csv.html',
        'British Library. Collection Metadata Services. https://www.bl.uk/services/collection-metadata-services',
    ]: doc.add_paragraph(r)
    out=SUB/'Unit20_FBZ_Automated_Testing_Report.docx'; out.parent.mkdir(exist_ok=True); doc.save(out)


def add_text_box(slide,x,y,w,h,text,size=20,bold=False,align=PP_ALIGN.LEFT):
    shape=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,PInches(x),PInches(y),PInches(w),PInches(h))
    shape.fill.solid(); shape.fill.fore_color.rgb=RGBColor(245,247,250); shape.line.color.rgb=RGBColor(70,80,90)
    tf=shape.text_frame; tf.clear(); p=tf.paragraphs[0]; p.alignment=align; r=p.add_run(); r.text=text; r.font.size=PPt(size); r.font.bold=bold; r.font.color.rgb=RGBColor(25,35,45); return shape

def build_ppt():
    prs=Presentation(); prs.slide_width=PInches(13.333); prs.slide_height=PInches(7.5)
    slides=[
      ('FBZ Dataset Processing','Unit 20 — Applied Programming and Design Principles\nSOLID, OOP, design patterns and automated testing'),
      ('The problem','Fantasy Bazaar needs a maintainable encyclopedia for the British Library Comics Unmasked metadata.\nThe application must search, filter, group, sort, save an in-memory search list and report popular searches.'),
      ('OOP foundations','Encapsulation → Comic domain objects\nAbstraction → repository and strategy contracts\nPolymorphism → interchangeable search algorithms\nInheritance → purposeful abstract contracts'),
      ('SOLID in the application','S — one responsibility per major class\nO — extend via new SearchStrategy implementations\nL — concrete strategies satisfy the same contract\nI — small focused interfaces\nD — services depend on ComicRepository abstraction'),
      ('Clean coding','Explicit names and type hints\nImmutable domain model\nCSV I/O isolated from business logic\nValidation at the input boundary\nDeterministic search/sort operations'),
      ('Data structures + algorithms','In-memory tuple of Comic objects\nLinear search: O(n)\nAlphabetical sort: O(n log n)\nCounter-style frequency aggregation\nAggregation by BL record ID solves repeated facet rows'),
      ('Creational design','Simple Factory: SearchStrategyFactory\nCentralises construction of concrete search behaviours.\nThis is intentionally documented as a simple factory, not incorrectly labelled the formal GoF Factory Method.'),
      ('Structural design','Repository abstraction\nCSV repository handles source I/O while services remain storage-agnostic.\nAn XML repository adapter is also included for future Phase 2 sources.'),
      ('Behavioural design','Strategy pattern\nTitle, Author, Genre and Year search algorithms implement one common contract.\nA new strategy can be added without rewriting the service.'),
      ('Real dataset validation',f"Five official CSV views loaded successfully.\nrecords.csv: 57,746 rows\nnames.csv: 117,873 rows\ntitles.csv: 77,280 rows\ntopics.csv: 77,919 rows\nclassification.csv: 57,844 rows\nAggregated names view: 54,147 unique BL records."),
      ('Automated testing','26 automated tests currently pass.\nUnit + integration + CLI/end-to-end + real-data acceptance\nReal genre records: Fantasy 4,793; Horror 1,929; Science Fiction 9,356.\nCoverage is used as a diagnostic, not proof of correctness.'),
      ('Evaluation + conclusion','SOLID improves change isolation and testability but adds abstraction overhead.\nPatterns are valuable when they address real variation.\nAutomation reduces regression risk but must be maintained.\nThe final design is traceable from requirement → class → implementation → test → evidence.'),
    ]
    for idx,(title,body) in enumerate(slides,1):
        s=prs.slides.add_slide(prs.slide_layouts[6])
        # header
        t=s.shapes.add_textbox(PInches(0.65),PInches(0.45),PInches(12),PInches(0.75)); p=t.text_frame.paragraphs[0]; r=p.add_run(); r.text=title; r.font.size=PPt(28); r.font.bold=True; r.font.color.rgb=RGBColor(25,35,45)
        add_text_box(s,0.75,1.55,11.85,4.85,body,size=22)
        foot=s.shapes.add_textbox(PInches(0.75),PInches(6.8),PInches(11.8),PInches(0.35)); fp=foot.text_frame.paragraphs[0]; fp.text=f'Unit 20 • FBZ • Slide {idx}/12'; fp.runs[0].font.size=PPt(10); fp.runs[0].font.color.rgb=RGBColor(100,110,120)
        notes=s.notes_slide
        note_shape=next((sh for sh in notes.shapes if sh.name.startswith('Notes')),None)
        if note_shape:
            note_shape.text_frame.text=(
                {'slide':1,'note':'Introduce the scenario and explain that the submission contains three linked deliverables: research/presentation, design/implementation and automated testing.'}.get('slide','')
            ) if False else f'Speaker notes — {title}. Explain the main points on screen using a concrete FBZ example. Relate the design decision back to the assignment criterion and the implemented code. Keep delivery within roughly 45–55 seconds for this slide.'
    out=SUB/'Unit20_FBZ_SOLID_OOP_Presentation.pptx'; prs.save(out)

if __name__=='__main__':
    make_figures(); build_design_doc(); build_testing_doc(); build_ppt(); print('Built submission artifacts.')
