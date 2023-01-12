from ...models.data_models import Manuscript, db
from ..CitenoteError import ManuscriptFoundError, ManuscriptNotFoundError
from .helper_main import get_form_data
from .helper_models import (
    check_papers,
    get_paper_list,
    get_update_papers_data,
    model_formatter,
    model_handler,
    replace_check,
)


@model_handler
def get():
    """Handles manuscript.get request

    Get manuscript object from database.

    Variables:
        manuscript_name (str): Name of the manuscript.
        manuscript (Manuscript): Manuscript object if present in dataset.
        manuscript_list (list): List of the manuscript objects.
        formatted_manuscript_list (list): List of formatted manuscript objects.
        val (dict): Response dictionary

    Returns:
        (dict, int): Returns the response to the user.

    Raises:
        ManuscriptNotFoundError: Raises manuscript is not present in database.

    """

    manuscript_name = get_form_data("manuscript_name")
    if manuscript_name:
        manuscript: Manuscript = Manuscript.query.filter_by(name=manuscript_name).first()
        if not manuscript:
            raise ManuscriptNotFoundError
        val = model_formatter(object=manuscript)

    else:
        manuscript_list: list = Manuscript.query.all()
        if not manuscript_list:
            raise ManuscriptNotFoundError
        formatted_manuscript_list = []
        for manuscript in manuscript_list:
            formatted_manuscript_list.append(model_formatter(object=manuscript))

        val = {"count": len(manuscript_list), "results": formatted_manuscript_list}

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


@model_handler
def get_paper(manuscript_id: str):
    """Handles manuscript.get_paper request

    Get list of associated papers.

    Args:
        manuscript_id (str): ID of manuscript
    Variables:
        manuscript (Manuscript): Manuscript object
        papers (list): List of paper associated with manuscript
        formatted_papers (list): List of formatted papers associated with manuscript

    Returns:
        (dict, int): Return the response to the user.

    """

    manuscript: Manuscript = Manuscript.query.filter_by(id=manuscript_id).first()
    papers = get_paper_list(manuscript)
    if not papers:
        return {}, 200
    formatted_papers = []
    for paper in papers:
        formatted_papers.append(model_formatter(paper))

    val = {
        "count": len(papers),
        "results": formatted_papers,
    }

    return val, 200


@model_handler
def add_paper(manuscript_id: str):
    """Handles manuscript.add_paper request

    Add paper to association.

    Args:
        manuscript_id (str): ID of manuscript
    Variables:
        manuscript (Manuscript): Manuscript object
        paper (Paper): paper object

    """

    manuscript, paper = get_update_papers_data(manuscript_id)
    check_papers(manuscript, paper)
    manuscript.papers.append(paper)
    db.session.commit()


@model_handler
def remove_paper(manuscript_id: str):
    """Handles manuscript.remove_paper request

    Remove paper from association.

    Args:
        manuscript_id (str): ID of manuscript
    Variables:
        manuscript (Manuscript): Manuscript object
        paper (Paper): paper object

    """

    manuscript, paper = get_update_papers_data(manuscript_id)
    manuscript.papers.remove(paper)
    db.session.commit()


if __name__ == "__main__":
    ...
