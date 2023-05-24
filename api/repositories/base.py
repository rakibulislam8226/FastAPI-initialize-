import uuid
from typing import Optional, Union, Sequence

from sqlalchemy import delete as sqlalchemy_delete
from sqlalchemy import func
from sqlalchemy import update as sqlalchemy_update
from sqlalchemy import insert as sqlalchemy_insert
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, contains_eager

from api.models.base import BaseModel


class BaseRepository:
    def __init__(self):
        self.model = BaseModel
    

    async def generate_id(self) -> uuid.UUID:
        return uuid.uuid4()
    

    async def create(self, session: AsyncSession, **kwargs) -> BaseModel:
        kwargs['id'] = await self.generate_id()
        entry = self.model(**kwargs)
        session.add(entry)
        await session.commit()
        return entry


    async def update(self, session: AsyncSession, pk: int, **kwargs) -> BaseModel:
        query = (
        sqlalchemy_update(self.model)
        .where(self.model.id == pk)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
        )
        await session.execute(query)
        await session.commit()
        return await self.get(session, pk)


    async def get(self, session: AsyncSession, pk: int) -> BaseModel:
        query = select(self.model).where(self.model.id == pk)  # NOQA
        entries = await session.execute(query)

        first_entry = entries.first()
        if first_entry:
            (entry,) = first_entry
        else:
            entry = None
        return entry


    async def get_by_column_value(self, session: AsyncSession, column_name: str, value: Union[str, int] ) -> Union[str, int]:
        """
        Get an entry by non-pk column value.
        Example call:
            ```
        entry = await self.get_by_column_value(column_name="number", value=number)
            ```
        """
        column_value = getattr(self.model, column_name, None)
        if not column_value:
            raise RuntimeError(f"Non-existing column name '{column_name}' is passed in.")

        query = select(self.model).where(column_value == value)
        entries = await session.execute(query)
        first_entry = entries.first()
        if first_entry:
            (entry,) = first_entry
        else:
            entry = None
        return entry


    async def get_list_all(self, session: AsyncSession):
        query = select(self.model)
        entries = await session.execute(query)
        data = entries.scalars().all()
        return data


    async def get_list_paginated(self, session: AsyncSession, page: int, page_size: int):
        query = select(self.model).limit(page_size).offset(page * page_size)
        entries = await session.execute(query)
        data = entries.scalars().all()
        return data


    async def get_list_sorted(self, session: AsyncSession, sort_column_name: str, sort_order: str):
        sort_column_name = getattr(self.model, sort_column_name, None)

        if not sort_column_name:
            raise RuntimeError(f"Non-existing column name '{sort_column_name}'.")

        if sort_order not in ("asc", "desc"):
            raise RuntimeError(f"Improper sorting order '{sort_order}'.")

        if sort_order == "desc":
            query = select(self.model).order_by(sort_column_name.desc())
        else:
            query = select(self.model).order_by(sort_column_name.asc())

        entries = await session.execute(query)

        data = entries.scalars().all()
        return data
    

    async def get_list_sorted_paginated(
        self, session: AsyncSession,
        # Pagination
        page: int,
        page_size: int,
        # Sorting
        sort_column_name: Optional[str],
        sort_order: Optional[str],
        ):
        """
        Get a list of entries with multiple custom conditions.
        NOTE: create a query builder layer for use in repositories
        """
        query = select(self.model)

        if sort_column_name and sort_order:
            sort_column_name = getattr(self.model, sort_column_name, None)

        if not sort_column_name:
            raise RuntimeError(f"Non-existing column name '{sort_column_name}'.")

        if sort_order and sort_order not in ("asc", "desc"):
            raise RuntimeError(f"Improper sorting order '{sort_order}'.")

        if sort_order == "desc":
            query = query.order_by(sort_column_name.desc())
        else:
            query = query.order_by(sort_column_name.asc())

        if page_size:
            query = query.limit(page_size).offset(page * page_size)

        entries = await session.execute(query)

        data = entries.scalars().all()
        return data
    

    async def get_count(self, session: AsyncSession) -> int:
        query = select(func.count(self.model.id))
        entries = await session.execute(query)
        first_entry = entries.first()

        if first_entry:
            (count,) = first_entry
        else:
            count = None
        return count
    

    async def delete(self, session: AsyncSession, pk: int) -> None:
        query = sqlalchemy_delete(self.model).where(self.model.id == pk)  # NOQA
        await session.execute(query)
        await session.commit()

    
    async def create_with_related(self, session: AsyncSession, *related_fields, **kwargs) -> BaseModel:
        """
        Execute insert statement with related entries involved.
        e.g. creation of an employee with assigned role.
        """
        query = (
        sqlalchemy_insert(self.model)
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        await session.commit()

        (pk,) = result.inserted_primary_key  # NOQA

        return await self.get_with_related(session, pk, *related_fields)


    async def update_with_related(self, session: AsyncSession, pk: int, *related_fields, **kwargs) -> BaseModel:
        query = (
        sqlalchemy_update(self.model)
        .where(self.model.id == pk)  # NOQA
        .values(**kwargs)
        .execution_options(synchronize_session="fetch")
        )
        await session.execute(query)
        await session.commit()

        return await self.get_with_related(session, pk, *related_fields)


    async def get_with_related(
        self, session: AsyncSession,
        pk: int,
        related_fields: Optional[Sequence] = (),
        nested_related_fields: Optional[Sequence[Sequence]] = (),
    ) -> BaseModel:
        query = select(self.model).where(self.model.id == pk) # NOQA

        for related_field in related_fields:
            query = query.options(joinedload(related_field))

        for nested_rel_field in nested_related_fields:
            if len(nested_rel_field) == 2:
                query = query.options(contains_eager(nested_rel_field[0],
                                                    nested_rel_field[1]))
            elif len(nested_rel_field) == 3:
                query = query.options(contains_eager(nested_rel_field[0],
                                                    nested_rel_field[1],
                                                    nested_rel_field[2]))
            else:
                # NOTE: len -> rel_field's number, dynamically:
                #  `foo, bar, *other = funct()` -> go recursively till all unpacked
                raise RuntimeError("Nesting level too deep.")

        entries = await session.execute(query)
        first_entry = entries.first()

        if first_entry:
            (entry,) = first_entry
        else:
            entry = None

        return entry