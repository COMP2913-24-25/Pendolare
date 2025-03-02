from .journey_repository import JourneyRepository, Journey

class GetJourneysCommand:

    def __init__(self, request, logger):

        self.journey_repository = JourneyRepository()
        self.request = request
        self.logger = logger

    def Execute(self):

        self.logger.debug("Getting all journeys")
        journeys = self.journey_repository.GetAllJourneys()
        self.logger.debug(f"Retrieved [{0 if journeys is None else len(journeys)}].")

        return journeys if journeys is not None else []