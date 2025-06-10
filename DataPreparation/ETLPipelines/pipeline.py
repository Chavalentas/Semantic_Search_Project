from abc import ABC, abstractmethod
import datetime

class ETLPipeline(ABC):
    """Represents an abstract ETL pipeline.

    Args:
        ABC (_type_): The abstract base class.
    """
    @abstractmethod
    def extract(self):
        """Extracts data.
        """
        pass

    @abstractmethod
    def transform(self):
        """Transforms data.
        """
        pass

    @abstractmethod
    def load(self):
        """Loads data.
        """
        pass

    def execute(self):
        """Executes the pipeline.
        """
        print("Extraction started: " + str(datetime.datetime.now()))
        self.extract()
        print("Extraction ended: " + str(datetime.datetime.now()))
        print("Transformation started: " + str(datetime.datetime.now()))
        self.transform()
        print("Transformation ended: " + str(datetime.datetime.now()))
        print("Loading started: " + str(datetime.datetime.now()))
        self.load()
        print("Loading ended: " +  str(datetime.datetime.now()))