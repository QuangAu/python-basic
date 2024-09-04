from sqlalchemy import select
from sqlalchemy.orm import Session
from schemas.club import Club
from models.club import ClubModel, SearchClubModel


def get_clubs(db_context: Session, condition: SearchClubModel):
    query = select(Club.club_name, Club.country, Club.rank, Club.market_value).order_by(
        Club.club_name
    )

    if condition.club_name is not None:
        query = query.filter(Club.club_name.like(f"%{condition.club_name}%"))

    query = query.offset((condition.page - 1) * condition.size).limit(condition.size)
    results = db_context.execute(query)

    return results


def add_new_club(db_context: Session, data: ClubModel):
    club = Club(**data.model_dump())
    db_context.add(club)
    db_context.commit()
    db_context.refresh(club)

    return club
