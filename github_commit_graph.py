import tkinter as tk
from tkinter import messagebox
import requests
import datetime
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_commit_data(username):
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    commit_data = [0]*35
    for event in data:
        if event['type'] == 'PushEvent':
            date_str = event['created_at']
            date = datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").date()
            delta = (datetime.date.today() - date).days
            if delta < 35:
                commit_data[delta] += 1
    return commit_data[::-1]

def draw_graph(data, username):
    fig = Figure(figsize=(5, 5))
    ax = fig.add_subplot(111)
    ax.imshow(np.array(data).reshape(5,7), cmap='Greens')
    ax.set_title(f"{username}'s Commit Graph")
    ax.set_yticks(range(5))
    ax.set_yticklabels(['Week '+str(i) for i in range(5, 0, -1)])
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
    return fig

def show_graph():
    username = entry.get()
    data = get_commit_data(username)
    if data is None:
        messagebox.showerror("Error", "Invalid username")
        return
    fig = draw_graph(data, username)
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

window = tk.Tk()
window.title("GitHub Commit Graph")
entry = tk.Entry(window)
entry.pack()
button = tk.Button(window, text="Show Graph", command=show_graph)
button.pack()
window.mainloop()