from abc import ABC, abstractmethod


class CrudService(ABC):

    @abstractmethod
    def create_user(self,  *args, **kwargs):
        """Save new entry to db."""

    @abstractmethod
    def get_user_by_id(self, *args):
        """Get entry data by entry id."""

    @abstractmethod
    def update_user_by_id(self, *args, **kwargs):
        """Update some params about entry in db."""
        pass

    @abstractmethod
    def delete_user_by_id(self, *args):
        """Delete entry data from db by entry id."""
