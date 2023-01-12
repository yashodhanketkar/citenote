import functools
from typing import Callable, Tuple

from ...models.data_models import Manuscript, Paper, db
from ..CitenoteError import (
    ManuscriptFoundError,
    ManuscriptNotFoundError,
    PaperFoundError,
    PaperNotFoundError,
    SameValueError,
)
from .helper_main import bcolors, get_form_data


def replace_check(
    replace: bool,
    updated_id: str = "",
    updated_name: str = "",
    updated_abstract: str = "",
) -> bool:
    """Replace or udpate check

    Args:
        replace (bool): Confirmation from the user/function.
        updated_id (str): New id for the manuscript/papers (defalut="")
        updated_name (str): New name for the manuscript/papers (defalut="")
        updated_abstract (str): New abstract for the manuscript/papers (defalut="")

    Returns:
        (bool): Returns true if correct values are provided.

    """

    if replace and updated_id:
        bcolors.print_message("Id is immutable in replace operation")
        return False

    elif replace and not all((updated_name, updated_abstract)):
        bcolors.print_message("Missing data.")
        return False

    elif not any((updated_id, updated_name, updated_abstract)):
        bcolors.print_message("No input was provided, hence no modifications were made.")
        return False

    else:
        return True


def model_handler(func: Callable) -> Callable:
    """Handles error for route helpers

    Args:
        func (Callable): Function to run inside the wrapper

    Returns:
        wrapper (Callabel): Wrapper for the function

    """

    @functools.wraps(func)
    def wrapper(**kwargs) -> Tuple[dict, int]:
        """Wrapper function to return

        Args:
            **kwargs: Keyword arguments provided for the operations

        Vars:
            response (tuple): Tuple of response and status code

        Returns:
            response (tuple): Tuple of response and status code if present else predefined responses

        """

        operation_name = func.__name__.upper()
        try:
            response = func(**kwargs)

            if response:
                return response
            return {}, 200

        except (
            ManuscriptFoundError,
            ManuscriptNotFoundError,
            PaperFoundError,
            PaperNotFoundError,
            SameValueError,
        ) as err:
            err.print_error()
            return {}, 500

        except ValueError as err:
            bcolors.print_warning("Wrong input type", repr(err))
            return {}, 500

        except Exception as err:
            bcolors.print_warning(f"'{operation_name}' operation failed", repr(err))
            return {}, 500

    return wrapper


def update_message(field_name: str, val: str | int) -> None:
    """Prints update message

    Args:
        field_name (str): Name of the field updated.
        val (int | str): New value of field.

    """

    bcolors.print_success(f"Updated {field_name} to: {str(val)}")


def update_field(field: str | int, field_name: str, val: str | int):
    """Return updated value for assignment.

    Check new value and old value. If new value is different prints message and returns old value.

    Args:
        field (str | int): Current value of the field.
        field_name (str): Name of the field.
        val (str | int): New value for assignment.

    Returns:
        val (str | int): Returns new value for assignment.

    Raise:
        SameValueError: If new value and old value are same.

    """

    if str(field) == val:
        raise SameValueError

    update_message(field_name, val)
    return val


def model_formatter(object: Manuscript | Paper) -> dict:
    """Formats manuscript object

    Get manuscript object from functions and convert it into formatted dictionary

    Args:
        manuscripts (Manuscript): Manuscript object obtained from function

    Returns:
        val (dict): Formatted dictionary output of manuscripts object

    """

    val = {
        "id": object.id,
        "name": object.name,
        "abstract": object.abstract,
    }

    return val


def get_update_papers_data(manuscript_id: str):
    """Returns manuscript and paper objects

    Get manuscript and paper object from provided ids.

    Args:
        manuscript_id (str): ID of required manuscript

    Variables:
        paper_id (str): ID of required paper.

    Returns:
        manuscript (Manuscript): Manuscript object
        paper (Paper): Paper object

    Raises:
        PaperNotFoundError: Raises if paper not found in database.

    """

    manuscript: Manuscript = Manuscript.query.filter_by(id=manuscript_id).first()
    paper_id = get_form_data("paper_id")

    if not paper_id:
        raise ValueError("Paper ID not provided")

    paper: Paper = Paper.query.filter_by(id=paper_id).first()

    if not paper:
        raise PaperNotFoundError

    return manuscript, paper


def get_paper_list(manuscript: Manuscript):
    """Get list of papers associated with manuscript

    Args:
        manuscripts (Manuscript): Manuscript object

    """

    return [paper[0] for paper in db.session.execute(manuscript.papers).all()]


def check_papers(manuscript: Manuscript, paper: Paper):
    """Check if paper is already associated with manuscript

    Args:
        manuscripts (Manuscript): Manuscript object
        paper (Paper): Paper object

    Raise:
        PaperFoundError: Raises if paper is associated with manuscript

    """

    papers = get_paper_list(manuscript)
    paper_ids = [paper.id for paper in papers]
    if paper.id in paper_ids:
        raise PaperFoundError
