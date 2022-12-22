from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship


db = SQLAlchemy()


manuscript_paper = db.Table(
    "manuscripts_papers",
    db.Column("manuscript_id", db.Integer, db.ForeignKey("manuscripts.id")),
    db.Column("paper_id", db.Integer, db.ForeignKey("papers.id")),
)


class Manuscript(db.Model):  # type: ignore
    __tablename__ = "manuscripts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    abstract = db.Column(db.String)

    def __init__(self, name, abstract):
        self.name = name
        self.abstract = abstract


class Paper(db.Model):  # type: ignore
    __tablename__ = "papers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    abstract = db.Column(db.String)
    bibtex = relationship("Citation", back_populates="papers", uselist=False)

    def __init__(self, name, abstract):
        self.name = name
        self.abstract = abstract


class Citation(db.Model):  # type: ignore
    __tablename__ = "citations"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    address = db.Column(db.String)
    annote = db.Column(db.String)
    author = db.Column(db.String)
    booktitle = db.Column(db.String)
    chapter = db.Column(db.String)
    crossref = db.Column(db.String)
    edition = db.Column(db.String)
    editor = db.Column(db.String)
    howpublished = db.Column(db.String)
    institution = db.Column(db.String)
    journal = db.Column(db.String)
    citation_key = db.Column(db.String)
    month = db.Column(db.String)
    note = db.Column(db.String)
    number = db.Column(db.String)
    organization = db.Column(db.String)
    pages = db.Column(db.String)
    publisher = db.Column(db.String)
    school = db.Column(db.String)
    series = db.Column(db.String)
    title = db.Column(db.String)
    volume = db.Column(db.String)
    year = db.Column(db.String)
    paper_id = db.Column(db.Integer, db.ForeignKey("papers.id"))

    paper = relationship("Paper", back_populates="citations")

    def __init__(self, title, author):
        self.title = title
        self.author = author
