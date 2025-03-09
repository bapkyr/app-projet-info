import flet as ft
import plotly.express as px
from db import get_expenses_by_category, get_expenses_grouped_by_date

def dashboard_page(page):
    data = get_expenses_by_category()
    categories = [item[0] for item in data]
    totals = [item[1] for item in data]
    