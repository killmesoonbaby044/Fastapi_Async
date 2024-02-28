#FOR CONVERTING PYDANTIC variable to DICT use:
variable.model_dump() or jsonable_encoder(variable)

#difference in query parameter and request body its adding pydentic schema(model)

#body
@router.post("/login1")
def current_user(token: schemas.Token):
    

#query
@router.post("/login2")
def current_user(token):


#SQLAlchemy с определенной версии обновил синтаксис.

#Вместо db.query(Task) теперь нужно использовать db.execute(select(Task))

#Пример Раньше работало:

async def fetch_all(db: Session, skip: int = 0, limit: int = 20):
    return db.query(Task).order_by(Task.time.desc()).offset(skip).limit(limit).all()

#Сейчас чтобы работало нужно:

async def fetch_all(db: AsyncSession, skip: int = 0, limit: int = 20):
    result = await db.execute(select(Task).order_by(Task.time.desc()).limit(20))
    return result.scalars().all()