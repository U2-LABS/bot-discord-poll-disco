import os

from dotenv import load_dotenv
from peewee import TextField, IntegerField, Model
from playhouse.postgres_ext import PostgresqlExtDatabase, ArrayField

load_dotenv()
conn = PostgresqlExtDatabase(
    database=os.getenv("NAME_DB"),
    user=os.getenv("USER_DB"),
    password=os.getenv("PASSWORD_DB"),
    host=os.getenv("HOST_DB"),
    port=os.getenv("PORT_DB")
)


class BaseModel(Model):
    class Meta:
        database = conn


class Song(BaseModel):
    title = TextField(column_name='title')
    pos = IntegerField(column_name='pos')
    link = TextField(column_name='link')
    id_music = IntegerField(column_name="id_music", primary_key=True)
    author = TextField(column_name='author')
    voted_users = ArrayField(IntegerField, column_name="voted_users")
    mark = IntegerField(column_name="mark")

    class Meta:
        table_name = 'music'
