from sqlmodel import Field, SQLModel, create_engine, Session, select, func, Relationship
from sqlalchemy import between
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

def update_expense(exp_id, new_date=None, new_cat=None, new_amount=None):
    with Session(engine) as session:
        expense = select(Expense).where(Expense.id==exp_id)

    if new_date:
        Expense.date = new_date
    
    if new_cat:
        Expense.cat_id = new_cat
    
    if new_amount:
        Expense.amount = new_amount
    
    session.add(expense)
    session.commit()

def del_expense(exp_id):
    with Session(engine) as session:
        expense = session.get(Expense, exp_id)
        session.delete(expense)
        session.commit()

def get_expenses_by_category(start_date=None, end_date=None, category_id=None):
    with Session(engine) as session:
        query = select(Category.name, func.sum(Expense.amount)).join(Expense).group_by(Category.name)
        
        if start_date and end_date:
            query = query.where(Expense.date.between(start_date, end_date))
        
        if category_id:
            query = query.where(Expense.cat_id == category_id)
        
        result = session.exec(query).all()
        return dict(result)

def add_category(name):
    with Session(engine) as session:
        category = Category(name=name)
        session.add(category)
        session.commit()

def update_category(cat_id, new_name=None):
    with Session(engine) as session:
        category = select(Category).where(Category.id==cat_id)
    
    if new_name:
        Category.name = new_name
    
    session.add(category)
    session.commit()

def del_category(cat_id):
    with Session(engine) as session:
        category = session.get(Category, cat_id)
    
    session.exec(select(Expense).where(Expense.id==cat_id)).delete(synchronize_session=False)
    session.delete(category)
    session.commit()

def get_categories():
    with Session(engine) as session:
        return session.exec(select(Category)).all()
    

def get_expenses_grouped_by_date():
    with Session(engine) as session:
        query = select(
            func.strftime('%Y-%m', Expense.date),
            func.sum(Expense.montant)  
        ).group_by(func.strftime('%Y-%m', Expense.date))

        return session.exec(query).all()


def main():
    create_db()
    add_expense()
    update_expense()
    del_expense()
    get_expenses_by_category()
    add_category()
    update_category()
    del_category()
    get_categories()


if __name__ == '__main__':
    main()