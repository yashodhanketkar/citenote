from ...models.data_models import Paper, db
from ..CitenoteError import PaperFoundError, PaperNotFoundError
from .helper_main import get_form_data
from .helper_models import model_handler, replace_check, update_field


@model_handler
def get():
    """Handles paper.get request

    Get paper object from database.

    Variables:
        paper_name (str): Name of the paper.
        paper (Paper): Paper object if present in dataset.
        val (dict): Response dictionary

    Returns:
        (dict, int): Returns the response to the user.

    Raises:
        PaperNotFoundError: Raises if paper is not present in database.

    """

    paper_name = get_form_data("paper_name")
    paper: Paper = Paper.query.filter_by(name=paper_name).first()

    if not paper:
        raise PaperNotFoundError

    val = {
        "id": paper.id,
        "name": paper.name,
        "abstract": paper.abstract,
    }

    return val, 200


@model_handler
def post():
    """Handles paper.post request

    Create user object in database.

    Variables:
        paper_name (str): Name of the paper.
        paper_abstract (str): Abstract of the paper.
        paper (Paper): Paper object if present in dataset.

    Returns:
        (dict, int): Returns the response to the user.

    Raises:
        PaperFoundError: Raises if paper already present in database.

    """

    paper_name = get_form_data("paper_name")
    paper_abstract = get_form_data("paper_abstract")

    if Paper.query.filter_by(name=paper_name).first():
        raise PaperFoundError

    paper = Paper(name=paper_name, abstract=paper_abstract)
    db.session.add(paper)
    db.session.commit()

    return {}, 201


@model_handler
def update(replace: bool = False):
    """Handles paper.update request

    Updates or replaces the value in database.

    Args:
        replace (bool): True if request method is put else defaults to false.

    Variables:
        paper_name (str): Name of paper
        updated_id (str): New id for paper if provided
        updated_name (str): New name for paper if provided
        updated_absract (str): New abstract for paper if provided
        paper (Paper): Paper object if present in database

    Raises:
        PaperNotFoundError: Raises if paper is not present in database.

    """

    paper_name = get_form_data("paper_name", True)
    updated_id = get_form_data("updated_id")
    updated_name = get_form_data("updated_name")
    updated_abstract = get_form_data("updated_abstract")
    paper: Paper = Paper.query.filter_by(name=paper_name).first()

    if not paper:
        raise PaperNotFoundError

    if not replace_check(replace, updated_id, updated_name, updated_abstract):
        return {}, 204

    if updated_id:
        paper.id = update_field(paper.id, "id", updated_id)

    if updated_name:
        paper.name = update_field(paper.name, "name", updated_name)

    if updated_abstract:
        paper.abstract = update_field(paper.abstract, "abstract", updated_abstract)

    db.session.commit()


@model_handler
def delete():
    """Handles paper.delete request

    Deletes paper object from database.

    Variables:
        paper_name (str): Name of paper to be deleted.
        paper (Paper): Paper object to be deleted.

    Raises:
        PaperNotFoundError: Raise if paper is not present in database.

    """

    paper_name = get_form_data("paper_name")
    paper: Paper = Paper.query.filter_by(name=paper_name).first()

    if not paper:
        raise PaperNotFoundError

    db.session.delete(paper)
    db.session.commit()


if __name__ == "__main__":
    ...
