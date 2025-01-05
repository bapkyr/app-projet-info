from sqlmodel import Field, SQLModel, create_engine, Session, select, func
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

def add_category(name):
    with Session(engine) as session:
        category = Category(name=name)
        session.add(category)
        session.commit()

def get_expenses_by_category(start_date=None, end_date=None, category_id=None):
    with Session(engine) as session:
        query = select(Category.name, SQLModel.func.sum(Expense.amount)).join(Expense).group_by(Category.name)
        
        if start_date and end_date:
            query = query.where(Expense.date.between(start_date, end_date))
        
        if category_id:
            query = query.where(Expense.cat_id == category_id)
        
        result = session.exec(query).all()
        return dict(result)

def get_categories():
    with Session(engine) as session:
        return session.exec(select(Category)).all()



if __name__ == '__main__':
    create_db()