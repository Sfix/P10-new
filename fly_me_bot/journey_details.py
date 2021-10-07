"""Handle the informations regarding the journey."""


class Journey_details:
    """Handle the details for our journey."""
    def __init__(
        self,
        destination: str = None,
        origin: str = None,
        departure_date: str = None,
        return_date: str = None,
        max_budget: float = None,
    ):
        """Init the class.

        Args:
            destination (str, optional): city to go to. Defaults to None.
            origin (str, optional): city of departure. Defaults to None.
            departure_date (str, optional): date of departure. Defaults to None.
            return_date (str, optional): date to return home. Defaults to None.
            max_budget (float, optional): budget at max. Defaults to None.
        """
        self.destination = destination
        self.origin = origin
        self.departure_date = departure_date
        self.return_date = return_date
        self.max_budget = max_budget
