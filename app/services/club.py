from models.club import ClubModel, SearchClubModel
from schemas.club import Club
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_clubs(db_context: AsyncSession, condition: SearchClubModel):
    query = select(Club.club_name, Club.country, Club.rank, Club.market_value).order_by(
        Club.club_name
    )

    if condition.club_name is not None:
        query = query.filter(Club.club_name.like(f"%{condition.club_name}%"))

    query = query.offset((condition.page - 1) * condition.size).limit(condition.size)
    results = await db_context.execute(query)

    return results


async def add_new_club(db_context: AsyncSession, data: ClubModel):
    club = Club(**data.model_dump())
    await db_context.add(club)
    await db_context.commit()
    await db_context.refresh(club)

    return club
