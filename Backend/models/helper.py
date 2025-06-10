import re


class Helper:
    """Represents a helper class."""

    @staticmethod
    def ensure_type(input_var, type_to_ensure, error_message: str):
        """Ensures that the input variable has the correct type and raises a custom error message
        if it does not have the correct type.

        Args:
            input_var (_type_): The input variable.
            type_to_ensure (_type_): The type of the input variable to ensure.
            error_message (str): The error message to raise.

        Raises:
            TypeError: Is thrown if the type of the variable error_message is not a str.
            TypeError: Is thrown if the type of the variable input_var does not match type_to_ensure.
        """
        if type(error_message) != str:
            raise TypeError("error_message must be a string!")
        if type(input_var) != type_to_ensure:
            raise TypeError(error_message)

    @staticmethod
    def ensure_instance(input_var, class_to_ensure, error_message: str):
        """Ensures that the input variable is of correct instance and raises a custom error message
        if it does not have the correct class.

        Args:
            input_var (_type_): The input variable.
            class_to_ensure (_type_): The class of the input variable to ensure.
            error_message (str): The error message to raise.

        Raises:
            TypeError: Is thrown if the type of the variable error_message is not a str.
            TypeError: Is thrown if the type of the variable input_var does not match class_to_ensure.
        """
        if type(error_message) != str:
            raise TypeError("error_message must be a string!")
        if not (isinstance(input_var, class_to_ensure)):
            raise TypeError(error_message)

    @staticmethod
    def ensure_list_of_type(input_var, type_to_ensure, no_list_error_message: str, wrong_elem_type_error_message: str):
        """Ensures that the input variable is a list of correct types and raises a custom error message
        if its elements do not have the correct type.

        Args:
            input_var (_type_): The input variable.
            type_to_ensure (_type_): The type of the input variable to ensure.
            no_list_error_message (str): Error message to raise if the input variable is not a list.
            wrong_elem_type_error_message (str): Error message to raise if the input variable contains elements of wrong types.
        """
        Helper.ensure_type(input_var, list, no_list_error_message)

        for el in input_var:
            Helper.ensure_type(el, type_to_ensure, wrong_elem_type_error_message)

    @staticmethod
    def ensure_list_of_instance(input_var, class_to_ensure, no_list_error_message: str, wrong_elem_class_error_message: str):
        """Ensures that the input variable is a list of correct classes and raises a custom error message
        if its elements do not have the correct class.

        Args:
            input_var (_type_): The input variable.
            type_to_ensure (_type_): The class of the input variable to ensure.
            no_list_error_message (str): Error message to raise if the input variable is not a list.
            wrong_elem_type_error_message (str): Error message to raise if the input variable contains elements of wrong classes.
        """
        Helper.ensure_type(input_var, list, no_list_error_message)

        for el in input_var:
            Helper.ensure_type(el, class_to_ensure, wrong_elem_class_error_message)

    @staticmethod
    def try_parse(value, type_to_parse) -> bool:
        """Tries to parse the value to the given type.

        Args:
            value (_type_): The value to parse.
            type_to_parse (_type_): Type to parse to.

        Returns:
            bool: Boolean indicating the the value can be parsed to the given type.
        """
        try:
            type_to_parse(value)
            return True
        except:
            return False

    @staticmethod
    def get_match_count(search_el: str, to_search_through: str) -> int:
        """Gets the amount of matches the lowercased term
        can be found in the lowercased search text.

        Args:
            search_el (str): The element to search for.
            to_search_through (str): The text to search through.

        Raises:
            TypeError: Is thrown if the type of the variable search_el is not a str.
            TypeError: Is thrown if the type of the variable to_search_through is not a str.

        Returns:
            int: The amount of matches.
        """
        if type(search_el) != str:
            raise TypeError("seatch_el must be a str!")

        if type(to_search_through) != str:
            raise TypeError("to_search_through must be a str!")

        search_el = search_el.lower()
        to_search_through = to_search_through.lower()
        search_count = len(re.findall(search_el, to_search_through))
        return search_count
