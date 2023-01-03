import yaml

from .helper_models import model_handler

from ...models.data_models import db, Citation

# from ...models.data_models import Citation
from .helper_main import get_form_data


def get_field_list(paper_type: str):
    with open("papers.yaml", "r") as t_file:
        data = yaml.safe_load(t_file)
    return data[paper_type]


@model_handler
def get(id):
    print(type(id))
    print("called:advance get")
    return {
        "request": {
            "url": f"/paper/{id}",
            "method": "GET",
        },
        "response": "OK",
    }, 200


@model_handler
def post(id: str):
    paper_type = get_form_data("paper_type")
    title = "Paper_" + id
    print(paper_type)
    data = get_citation(paper_type)

    if db.session.query(Citation).filter_by(title=title).first():
        raise ValueError

    citation = Citation(title=title, paper_id=id, **data)
    db.session.add(citation)
    db.session.commit()

    print("called:advance post")
    return {
        "request": {
            "url": f"/paper/{id}",
            "method": "POST",
        },
        "response": "OK",
    }, 201


@model_handler
def update(id, replace=False):
    if replace:
        print("called:advance put")
    else:
        print("called:advance patch")


@model_handler
def delete(id):
    print("called:advance delete")


def get_citation(type: str) -> dict:
    fields = get_field_list(type)
    optional_list = fields["optional"]
    required_list = fields["required"]
    citation_dict = {}

    for required_item in required_list:
        citation_dict[required_item] = get_form_data(required_item, required=True)

    for optional_item in optional_list:
        citation_dict[optional_item] = get_form_data(optional_item)

    citation_data = {key: val for key, val in citation_dict.items() if val != ""}

    return citation_data
