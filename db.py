from sqlmodel import Field, SQLModel, create_engine, Session, select, func, Relationship
from sqlalchemy import between, cast, Float
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
        expense = session.get(Expense, exp_id)  
        if not expense:
            print("Dépense introuvable.")
            return
        
        if new_date:
            expense.date = new_date
        if new_cat:
            expense.cat_id = new_cat
        if new_amount:
            expense.amount = new_amount
        
        session.commit()


def del_expense(exp_id):
    with Session(engine) as session:
        expense = session.get(Expense, exp_id)
        session.delete(expense)
        session.commit()

def get_expenses_by_category(start_date=None, end_date=None, category_id=None):
    with Session(engine) as session:
        query = select(Category.name, cast(func.sum(Expense.amount), Float)).join(Expense).group_by(Category.name)
        result = session.exec(query).all()
        
        print("📊 Données brutes récupérées :", result)  # Debug
        for item in result:
            print(f"🧐 Catégorie : {item[0]}, Valeur : {item[1]}, Type : {type(item[1])}")
       
        return result

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
            func.sum(Expense.amount)  
        ).group_by(func.strftime('%Y-%m', Expense.date))

        return session.exec(query).all()

def populate_db():
    with Session(engine) as session:
        if session.exec(select(Expense)).first():
            print("La base contient déjà des dépenses.")
            return
        
        categories = [
            Category(name="Alimentation"),
            Category(name="Transport"),
            Category(name="Loisirs")
        ]
        
        session.add_all(categories)
        session.commit()

        categories = session.exec(select(Category)).all()  # Récupérer les catégories avec leurs ID

        expenses = [
            Expense(date=date(2024, 1, 5), amount=50, cat_id=categories[0].id),
            Expense(date=date(2024, 1, 10), amount=30, cat_id=categories[1].id),
            Expense(date=date(2024, 2, 15), amount=20, cat_id=categories[2].id),
            Expense(date=date(2024, 2, 20), amount=100, cat_id=categories[0].id),
        ]
        
        session.add_all(expenses)
        session.commit()

        print("Données fictives ajoutées avec succès !")


def main():
    create_db()
    populate_db()
    update_expense()
    del_expense()
    get_expenses_by_category()
    add_category()
    update_category()
    del_category()
    get_categories()
    get_expenses_grouped_by_date()


if __name__ == '__main__':
    main()
