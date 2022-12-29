from ...models.data_models import Manuscript, db
from ..CitenoteError import ManuscriptFoundError, ManuscriptNotFoundError
from .helper_main import get_form_data
from .helper_models import model_handler, replace_check


@model_handler
def get():
    """Handles manuscript.get request

    Get manuscript object from database.

    Variables:
        manuscript_name (str): Name of the manuscript.
        manuscript (Manuscript): Manuscript object if present in dataset.
        val (dict): Response dictionary

    Returns:
        (dict, int): Returns the response to the user.

    Raises:
        ManuscriptNotFoundError: Raises manuscript is not present in database.

    """

    manuscript_name = get_form_data("manuscript_name")
    manuscript: Manuscript = Manuscript.query.filter_by(name=manuscript_name).first()

    if not manuscript:
        raise ManuscriptNotFoundError

    val = {
        "id": manuscript.id,
        "name": manuscript.name,
        "abstract": manuscript.abstract,
    }

    return val, 200


@model_handler
def post():
    """Handles manuscript.post request

    Variables:
        manuscript_name (str): Name of the manuscript.
        manuscript_abstract (str): Abstract of the manuscript.
        manuscript (Manuscript): Manuscript object if present in dataset.

    Returns:
        (dict, int): Returns the response to the user.

    Raises:
        ManuscriptFoundError: Raises if manuscript already present in database.

    """

    manuscript_name = get_form_data("manuscript_name")
    manuscript_abstract = get_form_data("manuscript_abstract")

    if Manuscript.query.filter_by(name=manuscript_name).all():
        raise ManuscriptFoundError

    manuscript = Manuscript(name=manuscript_name, abstract=manuscript_abstract)
    db.session.add(manuscript)
    db.session.commit()

    return {}, 201


@model_handler
def update(replace=False):
    """Handles manuscript.update request

    Updates or replaces the value in database.

    Args:
        replace (bool): True if request method is put else defaults to false.

    Variables:
        manuscript_name (str): Name of manuscript
        updated_id (str): New id for manuscript if provided
        updated_name (str): New name for manuscript if provided
        updated_absract (str): New abstract for manuscript if provided
        manuscript (Manuscript): Manuscript object if present in database

    Raises:
        ManuscriptNotFoundError: Raises if manuscript is not present in database.

    """

    manuscript_name = get_form_data("manuscript_name", True)
    updated_id = get_form_data("updated_id")
    updated_name = get_form_data("updated_name")
    updated_abstract = get_form_data("updated_abstract")
    manuscript: Manuscript = Manuscript.query.filter_by(name=manuscript_name).first()

    if not manuscript:
        raise ManuscriptNotFoundError

    if not replace_check(replace, updated_id, updated_name, updated_abstract):
        return {}, 204

    if updated_id:
        print("Updated the id to:", updated_id)
        manuscript.id = int(updated_id)

    if updated_name:
        print("Updated the name to:", updated_name)
        manuscript.name = updated_name

    if updated_abstract:
        print("Updated the abstract to:", updated_abstract)
        manuscript.abstract = updated_abstract

    db.session.commit()


@model_handler
def delete():
    """Handles manuscript.delete request

    Deletes manuscript object from database.

    Variables:
        manuscript_name (str): Name of manuscript to be deleted.
        manuscript (Manuscript): Manuscript object to be deleted.

    Raises:
        ManuscriptNotFoundError: Raise if manuscript is not present in database.

    """

    manuscript_name = get_form_data("manuscript_name", True)
    mansucript = Manuscript.query.filter_by(name=manuscript_name).first()

    if not mansucript:
        raise ManuscriptNotFoundError

    db.session.delete(mansucript)
    db.session.commit()


if __name__ == "__main__":
    ...
