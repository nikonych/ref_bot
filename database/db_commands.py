from sqlalchemy import and_, select, insert, delete, update, func
from sqlalchemy.ext.asyncio import AsyncSession


class DBCommands:
    def __init__(self, table, session: AsyncSession):
        """
        Common database commands

        :param table: Table
        """

        self.table = table
        self.session = session

    async def get(self, _first=True, order_by=None, **kwargs):
        """
        Get item

        :param _first: True - first item, False - all items
        :param order_by: Sort by
        """

        result = []

        _param = kwargs.get('_param')
        if _param:
            kwargs.pop('_param')

        for attr_name, value in kwargs.items():
            if _param and _param == '!=':
                result.append(getattr(self.table, attr_name) != value)
            else:
                result.append(getattr(self.table, attr_name) == value)

        request = select(self.table).where(and_(*result))
        if order_by is not None:
            request = request.order_by(order_by)

        data = await self.session.execute(request)
        data = data.scalars()

        return data.first() if _first else data.all()

    async def add(self, **kwargs):
        new_item_id = await self.session.execute(insert(self.table).values(**kwargs).returning(self.table.user_id))
        await self.session.commit()

        return await self.get(_first=True, user_id=new_item_id.scalars().first())

    async def delete(self, **kwargs):
        """
        Delete item
        """

        result = []

        for attr_name, value in kwargs.items():
            result.append(getattr(self.table, attr_name) == value)

        await self.session.execute(delete(self.table).where(*result))
        await self.session.commit()

    async def update(self, values: dict, where: dict = None):
        """
        Update item's values
        """

        where_result = []
        if where:
            for attr_name, value in where.items():
                where_result.append(getattr(self.table, attr_name) == value)

        await self.session.execute(update(self.table).values(values).where(and_(*where_result)))
        await self.session.commit()

    async def count(self, **kwargs):
        """
        Count items
        """

        result = []
        for attr_name, value in kwargs.items():
            result.append(getattr(self.table, attr_name) == value)

        count = await self.session.execute(select(func.count(self.table.id)).where(and_(*result)))

        return count.scalars().first()
