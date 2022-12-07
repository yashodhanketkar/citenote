CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(255)
);

CREATE TABLE manuscripts(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    abstract TEXT
);

CREATE TABLE papers(
    id INTEGER PRIMARY KEY,
    name VARCHAR(255),
    abstract TEXT
);

CREATE TABLE citation(
    id INTEGER PRIMARY KEY,
    type VARCHAR(255),
    address VARCHAR(255),
    annote VARCHAR(255),
    author VARCHAR(255),
    booktitle VARCHAR(255),
    chapter VARCHAR(255),
    crossref VARCHAR(255),
    edition VARCHAR(255),
    editor VARCHAR(255),
    howpublished VARCHAR(255),
    institution VARCHAR(255),
    journal VARCHAR(255),
    citation_key VARCHAR(255),
    month VARCHAR(255),
    note VARCHAR(255),
    number VARCHAR(255),
    organization VARCHAR(255),
    pages VARCHAR(255),
    publisher VARCHAR(255),
    school VARCHAR(255),
    series VARCHAR(255),
    title VARCHAR(255),
    volume VARCHAR(255),
    year VARCHAR(255),
    paper_id INTEGER NOT NULL,
    CONSTRAINT fk_paper FOREIGN KEY(paper_id) REFERENCES papers(id)
);

CREATE TABLE manuscript_paper(
    manuscript_id INTEGER,
    paper_id INTEGER,
    PRIMARY KEY (manuscript_id, paper_id),
    CONSTRAINT fk_manuscript FOREIGN KEY(manuscript_id) REFERENCES manuscripts(id),
    CONSTRAINT fk_paper FOREIGN KEY(paper_id) REFERENCES papers(id)
);
