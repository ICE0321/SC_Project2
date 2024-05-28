import tkinter as tk
from tkinter import messagebox
import requests
import datetime
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_commit_data(username):
    url = f"https://api.github.com/users/{username}/events"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None

    data = response.json()
    commit_data = [0] * 35
    current_month_commit_count = 0
    today = datetime.date.today()
    for event in data:
        if event['type'] == 'PushEvent':
            date_str = event['created_at']
            date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").date()
            delta = (today - date).days
            if delta < 35:
                commit_data[delta] += 1
            if date.month == today.month and date.year == today.year:
                current_month_commit_count += 1
    return commit_data[::-1], current_month_commit_count


def draw_graph(data, username, commit_count):
    fig = Figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    heatmap_data = np.array(data).reshape(5, 7)
    im = ax.imshow(heatmap_data, cmap='Greens', aspect='auto')
    ax.set_title(f"{username}'s Commit Graph")
    ax.set_yticks(range(5))
    ax.set_yticklabels(['Week ' + str(i) for i in range(5, 0, -1)])
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    # Display the current month's commit count
    fig.text(0.5, 0.01, f"Commits this month: {commit_count}", ha='center')

    return fig


def show_graph():
    username = entry.get()
    data, current_month_commit_count = get_commit_data(username)
    if data is None:
        messagebox.showerror("Error", "Invalid username or failed to fetch data")
        return

    fig = draw_graph(data, username, current_month_commit_count)

    # Clear previous canvas if exists
    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


window = tk.Tk()
window.title("GitHub Commit Graph")
window.geometry("600x500")

entry = tk.Entry(window)
entry.pack(pady=10)

button = tk.Button(window, text="Show Graph", command=show_graph)
button.pack(pady=10)

frame = tk.Frame(window)
frame.pack(pady=10)

window.mainloop()


