def replace_check(replace: bool, updated_id: str = "", updated_name: str = "", updated_abstract: str = "") -> bool:
    if replace and not all((updated_name, updated_abstract)):
        print("Missing data.")
        return False

    elif not any((updated_id, updated_name, updated_abstract)):
        print("No input was provided, hence no modifications were made.")
        return False

    else:
        return True
