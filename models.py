from sqlmodel import SQLModel, Field


class UserData(SQLModel, table=True):
    user_id: int = Field(primary_key=True, index=True)


class UserFile(SQLModel, table=True):
    user_id: int = Field(primary_key=True, index=True)
    file_link: str = Field(nullable=False)
