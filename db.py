from sqlmodel import Field, SQLModel, create_engine, Session, select
from datetime import date

class Expense(SQLModel, table = True):
    id: int | None = Field(default= None, primary_key=True)
    amount: float
    date: date
    description: str | None = None
    cat_id: int | None = Field(default=None, foreign_key='category.id')

class Category(SQLModel, table=True):
    id: int | None = Field(default= None, primary_key=True)
    name: str

db_name = 'budget.db'
db_url = f"sqlite:///{db_name}"
engine = create_engine(db_url, echo = True)

def create_db():
    SQLModel.metadata.create_all(engine)

def add_expense(date, amount, cat_id):
    with Session(engine) as session:
        expense = Expense(date=date, amount=amount, cat_id=cat_id)
        session.add(expense)
        session.commit()

def add_category(nom):
    with Session(engine) as session:
        category = Category(nom=nom)
        session.add(category)
        session.commit

def get_expenses():
    pass


def get_categories():
    with Session(engine) as session:
        return session.exec(select(Category)).all()



if __name__ == '__main__':
    create_db()