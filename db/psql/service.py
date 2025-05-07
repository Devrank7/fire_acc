import datetime
from abc import ABC, abstractmethod

from sqlalchemy import select

from db.psql.connect import AsyncSessionMaker
from db.psql.model import Account


class SqlService(ABC):
    @abstractmethod
    async def run(self):
        raise NotImplementedError


class ReadAllAccounts(SqlService):
    async def run(self):
        async with AsyncSessionMaker() as session:
            accounts = await session.scalars(select(Account))
            return accounts.all()


class ReadAccountByID(SqlService):
    def __init__(self, acc_id: int):
        self.acc_id = acc_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            acc = await session.scalar(
                select(Account)
                .where(Account.id == self.acc_id)
            )
            return acc


class ReadAccountByUsername(SqlService):
    def __init__(self, username: str):
        self.username = username

    async def run(self):
        async with AsyncSessionMaker() as session:
            acc = await session.scalar(
                select(Account)
                .where(Account.username == self.username)
            )
            return acc


class CreateAccount(SqlService):
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password

    async def run(self):
        async with AsyncSessionMaker() as session:
            group = Account(username=self.username, password=self.password)
            session.add(group)
            await session.commit()
            return group

from sqlalchemy import exists

class UpdateAccount(SqlService):
    def __init__(self, acc_id: int, username: str = None, password: str = None, fire_data: datetime.datetime = None):
        self.acc_id = acc_id
        self.username = username
        self.password = password
        self.fire_data = fire_data

    async def run(self):
        async with AsyncSessionMaker() as session:
            account = await session.scalar(select(Account).where(Account.id == self.acc_id))
            if not account:
                return None

            # Проверка уникальности username, если он изменяется
            if self.username and self.username != account.username:
                username_exists = await session.scalar(
                    select(exists().where(Account.username == self.username).where(Account.id != self.acc_id))
                )
                if username_exists:
                    raise ValueError("Username already exists")

                account.username = self.username

            if self.password is not None:
                account.password = self.password

            if self.fire_data is not None:
                account.fire_data = self.fire_data

            await session.commit()
            return account

class DeleteAccount(SqlService):
    def __init__(self, acc_id: int):
        self.acc_id = acc_id

    async def run(self):
        async with AsyncSessionMaker() as session:
            account = await session.scalar(select(Account).where(Account.id == self.acc_id))
            if account:
                await session.delete(account)
                await session.commit()
            return account  # Вернет None, если не найден

async def run_sql(runnable: SqlService):
    return await runnable.run()
