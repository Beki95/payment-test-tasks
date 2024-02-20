from sqlalchemy.orm import Session


class CommonRepository:

    def __init__(self, session: Session) -> None:
        self.session = session

    def insert(self, instance: object):
        return self.session.add(instance)
