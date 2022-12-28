import functools

from typing import Callable

from ...models.data_models import Manuscript, db
from .helper_main import get_form_data, bcolors
from .helper_models import replace_check
from ..CitenoteError import CitenoteException


class ManuscriptFoundError(CitenoteException):
    """Manuscript already exist."""

    def __init__(self):
        super().__init__("ManuscriptFoundError", "Manuscript already exists in database.")


class ManuscriptNotFoundError(CitenoteException):
    """Manuscript does not exist."""

    def __init__(self):
        super().__init__("ManuscriptNotFoundError", "Manuscript not found in database.")


def manuscript_handler(mfunc: Callable) -> Callable:
    """Error and output handler"""

    @functools.wraps(mfunc)
    def wrapper(**kwargs):
        try:
            response = mfunc(**kwargs)
            if response:
                return response
            return {}, 200

        except (ManuscriptFoundError, ManuscriptNotFoundError) as err:
            err.print_error()
            return {}, 500

        except ValueError as err:
            bcolors.print_warning("Wrong input type", repr(err))
            return {}, 500

        except Exception as err:
            bcolors.print_warning("Some error", repr(err))
            return {}, 500

    return wrapper


@manuscript_handler
def get():
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


@manuscript_handler
def post():
    manuscript_name = get_form_data("manuscript_name")
    manuscript_abstract = get_form_data("manuscript_abstract")

    if Manuscript.query.filter_by(name=manuscript_name).all():
        raise ManuscriptFoundError

    manuscript = Manuscript(name=manuscript_name, abstract=manuscript_abstract)
    db.session.add(manuscript)
    db.session.commit()

    return {}, 201


@manuscript_handler
def update(replace=False):
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


@manuscript_handler
def delete():
    manuscript_name = get_form_data("manuscript_name", True)
    mansucript = Manuscript.query.filter_by(name=manuscript_name).first()

    if not mansucript:
        raise ManuscriptNotFoundError

    db.session.delete(mansucript)
    db.session.commit()


if __name__ == "__main__":
    ...
