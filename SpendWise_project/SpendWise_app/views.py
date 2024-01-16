from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Expense, Budget
import calendar
import datetime


def index(request):
    try:
        # Fetch the latest budget from the database
        latest_budget = Budget.objects.latest('created_at')
        budget_amount = latest_budget.amount
    except Budget.DoesNotExist:
        # If no budget exists, create a default budget and fetch it
        Budget.objects.create(amount=0)
        latest_budget = Budget.objects.latest('created_at')
        budget_amount = latest_budget.amount

    if request.method == 'POST':
        expense_name = request.POST.get('expense_name')
        expense_amount = float(request.POST.get('expense_amount'))
        selected_category = request.POST.get('category')
        Expense.objects.create(name=expense_name, amount=expense_amount, category=selected_category)

    expenses = Expense.objects.all()
    summary = summarize_expenses(expenses, budget=budget_amount)

    return render(request, 'SpendWise_app/index.html', {'summary': summary})


def summarize_expenses(expenses, budget):
    amount_by_category = {}
    filtered_expenses = [expense for expense in expenses if expense.amount is not None]

    for expense in filtered_expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    expense_summary = "Expenses By Category:<br>"
    for key, amount in amount_by_category.items():
        expense_summary += f"{key}: ${amount:.2f}<br>"

    total_spent = sum([x.amount for x in filtered_expenses])
    budget_remaining = budget - total_spent

    now = datetime.datetime.now()
    days_in_current_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_current_month - now.day
    daily_budget = budget_remaining / remaining_days

    # Check if any of the variables are None before formatting
    if all(v is not None for v in [total_spent, budget_remaining, remaining_days, daily_budget, budget]):
        summary = (
            f"Your Budget: ${budget:.2f}<br>"
            f"You've spent: ${total_spent:.2f}<br>"
            f"Budget Remaining: ${budget_remaining:.2f}<br>"
            f"Remaining Days in the current month: {remaining_days}<br>"
            f"Budget per Day: ${daily_budget:.2f}<br>"
        )
    else:
        summary = "Error: Unable to calculate summary"

    return summary


def add_budget(request):
    if request.method == 'POST':
        amount = float(request.POST.get('budget_amount'))

        # Get the latest budget object
        latest_budget = Budget.objects.latest('created_at')

        # Update the budget amount
        latest_budget.amount += amount
        latest_budget.save()

    return redirect('index')


def set_budget(request):
    if request.method == 'POST':
        new_budget = float(request.POST.get('new_budget'))

        # Delete existing budgets
        Budget.objects.all().delete()

        # Create a new budget
        Budget.objects.create(amount=new_budget)

    return redirect('index')







