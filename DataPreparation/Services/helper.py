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
        
    def ensure_subclass_of(input_var, class_to_ensure, error_message: str):
        """Ensures that the input variable is of correct subclass and raises a custom error message
        if it is not the correct class.

        Args:
            input_var (_type_): The input variable.
            class_to_ensure (_type_): The parent class of the input variable to ensure.
            error_message (str): The error message to raise.

        Raises:
            TypeError: Is thrown if the type of the variable error_message is not a str.
            TypeError: Is thrown if the class of the variable input_var is not a subclass of class_to_ensure.
        """
        if type(error_message) != str:
            raise TypeError("error_message must be a string!")
        if not(issubclass(type(input_var), class_to_ensure)):
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
    def remove_duplicate_entries(dict_list: list[dict], key: str) -> list[dict]:
        """Removes duplicate dictionaries from the list, 
        judging by the key.

        Args:
            dict_list (list[dict]): The list of dictionaries.
            key (str): The key of the dictionary to regard.

        Raises:
            TypeError: Is thrown if the type of the variable dict_list is not a list.
            TypeError: Is thrown if the variable dict_list contains elements that are not of type dict.
            TypeError: Is thrown if the type of the variable key is not a str.

        Returns:
            list[dict]: Modified list of dictionaries.
        """
        if type(dict_list) != list:
            raise TypeError("dict_list must be a list!")
        if any([type(el) != dict for el in dict_list]):
            raise TypeError("dict_list must contain only dicts!")
        if type(key) != str:
            raise TypeError("key must be a string!")
        
        result = []
        checked_values = []

        for el in dict_list:
            if el[key] in checked_values:
                continue
            checked_values.append(el[key])
            result.append(el)
        return result
        
    @staticmethod
    def concat_lists(list_of_lists: list[list]):
        """Concats more lists.

        Args:
            list_of_lists (list[list]): A list of lists.

        Returns:
            list[list]: A list of lists.
        """
        Helper.ensure_list_of_type(list_of_lists, list, "list_of_lists must be a list!", "list_of_lists must contain lists!")

        result = []

        for el in list_of_lists:
            result += el

        return result
