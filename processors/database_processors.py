from sqlalchemy.orm import Session
from sqlmodel import select

from models import UserData, UserFile


class UserDBProcessor:
    def __init__(self, session: Session):
        self._session = session

    def get_user_by_id(self, user_id: int):
        query = select(UserData).where(UserData.user_id == user_id)
        user_instance = self._session.execute(query).scalar()

        if user_instance:
            return user_instance

        return None

    def create_user(self, user_id: int, commit: bool = True):
        new_user = UserData(user_id=user_id)
        self._session.add(new_user)
        self._session.flush()

        if commit:
            self._session.commit()
            return new_user

        return

    def create_user_if_not_exists(self, user_id: int):
        user_instance = self.get_user_by_id(user_id=user_id)
        if user_instance:
            return

        self.create_user(user_id=user_id)


class FileDBProcessor:
    def __init__(self, session: Session):
        self._session = session

    def get_file_link_by_user_id(self, user_id: int):
        query = select(UserFile).where(UserFile.user_id == user_id)
        file_link_instance = self._session.execute(query).scalar()

        if file_link_instance:
            return file_link_instance

        return None

    def create_file_link(self, user_id: int, file_link: str, commit: bool = True):
        new_file_link = UserFile(user_id=user_id, file_link=file_link)
        self._session.add(new_file_link)
        self._session.flush()

        if commit:
            self._session.commit()
            return new_file_link

        return

    def create_file_link_if_not_exists(self, user_id: int, file_link: str, commit: bool = True):
        file_link_instance = self.get_file_link_by_user_id(user_id=user_id)
        if file_link_instance:
            return

        self.create_file_link(user_id=user_id, file_link=file_link)
