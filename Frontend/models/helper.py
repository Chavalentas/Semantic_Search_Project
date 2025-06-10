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
        if not(isinstance(input_var, class_to_ensure)):
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
    def replace_pattern(input_str: str, pattern: str, to_replace_with_func, case_sensitive: bool) -> str:
        """Replaces a pattern in the input variable with a result of a function that should be applied 
        to every pattern match.

        Args:
            input_str (str): The input string.
            pattern (str): The pattern to look for.
            to_replace_with_func (_type_): The function to apply to every match.
            case_sensitive (bool): Boolean indicating whether the case sensitivity should be applied.

        Returns:
            str: Result string with replaced patterns.
        """
        Helper.ensure_type(input_str, str, "input_str must be a str!")
        Helper.ensure_type(pattern, str, "pattern must be a str!")
        Helper.ensure_type(case_sensitive, bool, "case_sensitive must be a bool!")

        if case_sensitive:
            return re.sub(pattern, to_replace_with_func(pattern), input_str)
        
        matches = list(set(re.findall(pattern, input_str, flags=re.IGNORECASE)))
        result = input_str

        for el in matches:
            result = re.sub(el, to_replace_with_func(el), result)

        return result
    
    @staticmethod
    def replace_patterns(input_str: str, pattern_to_replace_with_list: list, case_sensitive: bool) -> str:
        """Replaces the patterns in the input variable with the corresponding replacement values.

        Args:
            input_str (str): The input string.
            pattern_to_replace_with_list (list): List of pattern-to-replace value tuplesl. 
            case_sensitive (bool): Boolean indicating whether the case sensitivity should be applied.

        Returns:
            str: Result string with replaced patterns.
        """
        Helper.ensure_type(input_str, str, "input_str must be a str!")
        Helper.ensure_type(pattern_to_replace_with_list, list, "pattern_to_replace_with_list must be a list!")
        Helper.ensure_type(case_sensitive, bool, "case_sensitive must be a bool!")

        result = input_str

        for el in pattern_to_replace_with_list:
            result = Helper.replace_pattern(result, el[0], lambda x: el[1], case_sensitive)

        return result
