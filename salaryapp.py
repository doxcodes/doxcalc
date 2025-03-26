import tkinter as tk 
from tkinter import ttk, messagebox
import ttkbootstrap as tb 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def calculate_taxes(salary):
    tax_free_allowance = 12570
    basic_rate = (50270 - tax_free_allowance) * 0.2
    higher_rate = (125140 - 50270) * 0.4
    additional_rate = (salary - 125140) * 0.45 if salary > 125140 else 0

    if salary <= tax_free_allowance:
        income_tax = 0
    elif salary <= 50270:
        income_tax = (salary - tax_free_allowance) * 0.20
    elif salary <= 125140:
        income_tax = basic_rate + (salary - 50270) * 0.40
    else:
        income_tax = basic_rate + higher_rate + additional_rate

    ni = 0
    if salary > 12570:
        ni = (min(salary, 50270)- 12570) * 0.12
        if salary > 50270:
            ni += (salary - 50270) * 0.02

    total_tax = income_tax + ni
    take_home = salary - total_tax
    return income_tax, ni, total_tax, take_home

def plot_graph(data, labels, title):
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title(title)
    return fig

def show_tax_graph():
    salary = float(salary_entry.get())
    income_tax, ni, total_tax, take_home = calculate_taxes(salary)

    tax_data = [income_tax, ni, take_home]
    labels = ['Income Tax', 'National Insurance', 'Take Home Pay']

    fig = plot_graph(tax_data, labels, f'Tax Breakdown for £{salary:,}')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

def show_budget_graph():
    take_home = float(take_home_label['text'].split('£')[-1].replace(',', ''))
    budget = {}
    total_budget = 0

    for category, entry in budget_entries.items():
        amount = float(entry.get()) if entry.get() else 0
        budget[category] = amount
        total_budget += amount

    if total_budget > take_home:
        messagebox.showerror("Error", "Your budget exceeds your take-home salary.")
        return
    
    fig = plot_graph(list(budget.values()), list(budget.keys()), 'Budget Allocation')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

def calculate_and_display():
    salary = float(salary_entry.get())
    income_tax, ni, total_tax, take_home = calculate_taxes(salary)

    tax_label.config(text=f"Income Tax: £{income_tax:,.2f}")
    ni_label.config(text=f"National Insurance: £{ni:,.2f}")
    total_tax_label.config(text=f"Total Tax: £{total_tax:,.2f}")
    take_home_label.config(text=f"Take-Home Salary: £{take_home:,.2f}")

root = tb.Window(themename="superhero")
root.title("Uk Salary Tax and Budget Planner")
root.geometry("500x600")

frame = ttk.Frame(root, padding=20)
frame.pack(fill='both', expand=True)

ttk.Label(frame, text="Enter your annual salary (£):", font=("Arial", 12)).pack()
salary_entry = ttk.Entry(frame, font=("Arial", 12))
salary_entry.pack(pady=5)

calculate_btn = ttk.Button(frame, text="Calculator", command=calculate_and_display, style="primary.TButton")
calculate_btn.pack(pady=10)

tax_label = ttk.Label(frame, text="", font=("Arial", 12))
tax_label.pack()
ni_label = ttk.Label(frame, text="", font=("Arial", 12))
total_tax_label = ttk.Label(frame, text="", font=("Arial", 12))
take_home_label = ttk.Label(frame, text="", font=("Arial", 12, "bold"))
ni_label.pack()
total_tax_label.pack()
take_home_label.pack()

tax_graph_btn = ttk.Button(frame, text="Show Tax Breakdown Graph", command=show_tax_graph, style="success.TButton")
tax_graph_btn.pack(pady=10)

ttk.Label(frame, text="Budget Allocation", font=("Arial", 12, "bold")).pack()
budget_entries = {}
categories = ['Rent/Mortage', 'Bills', 'Food', 'Transport', 'Entertainment', 'Savings', 'Other']
for category in categories:
    ttk.Label(frame, text=category, font=("Arial", 10)).pack()
    entry = ttk.Entry(frame)
    entry.pack(pady=3)
    budget_entries[category] = entry

budget_graph_btn = ttk.Button(frame, text="Show Budget Graph", command=show_budget_graph, style="info.TButton")
budget_graph_btn.pack(pady=10)

root.mainloop()
