from flask import request
from ...models.data_models import Manuscript, db


def get_form_data(field, required=False):
    try:
        return request.form[field]

    except KeyError:
        if required:
            raise ValueError

        return ""


def get():
    manuscript_name = get_form_data("manuscript_name")
    manuscript = Manuscript.query.filter_by(name=manuscript_name).first()
    print(manuscript)

    return {
        "url": "/manuscripts/read",
        "method": "GET",
        "username": manuscript_name,
    }, 200


def post():
    manuscript_name = get_form_data("manuscript_name")
    manuscript_abstract = get_form_data("manuscript_abstract")

    if Manuscript.query.filter_by(name=manuscript_name).all():
        raise ValueError

    manuscript = Manuscript(name=manuscript_name, abstract=manuscript_abstract)
    db.session.add(manuscript)
    db.session.commit()

    return {}, 201


def update():
    manuscript_name = get_form_data("manuscript_name", True)
    updated_id = get_form_data("updated_id")
    updated_name = get_form_data("updated_name")
    updated_abstract = get_form_data("updated_abstract")

    manuscript_to_update: Manuscript = Manuscript.query.filter_by(name=manuscript_name).first()

    if request.method == "PUT":
        if not all((updated_id, updated_name, updated_abstract)):
            print("Missing data.")
            return {}, 204

    if request.method == "PATCH":
        if not any((updated_id, updated_name, updated_abstract)):
            print("No input was provided, hence no modifications were made.")
            return {}, 204

    if updated_id:
        print("Updated the name")
        manuscript_to_update.id = updated_id

    if updated_name:
        print("Updated the name")
        manuscript_to_update.name = updated_name

    if updated_abstract:
        print("Updated the abstract")
        manuscript_to_update.abstract = updated_abstract

    db.session.commit()

    return {}, 200


def delete():
    manuscript_name = get_form_data("manuscript_name", True)
    mansucript = Manuscript.query.filter_by(name=manuscript_name).first()

    db.session.delete(mansucript)
    db.session.commit()

    return {}, 200
