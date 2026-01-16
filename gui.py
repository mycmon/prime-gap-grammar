# gui.py
import tkinter as tk
from tkinter import ttk, messagebox
import math
import random

from sympy import isprime

from grammar import classify_gap, typical_g_for_symbol
from markov import initial_symbol, next_symbol
from filters import is_allowed_mod30, passes_small_prime_filter
from granville import granville_probability

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run_gui():
    root = tk.Tk()
    root.title("Simulateur de nombres premiers — Grammaire normalisée")

    # Variables
    var_a = tk.StringVar(value="1000000")
    var_b = tk.StringVar(value="2000000")
    var_n = tk.StringVar(value="100")

    # Frame haut
    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10, fill="x")

    tk.Label(frame, text="Borne a :").grid(row=0, column=0, sticky="w")
    tk.Entry(frame, textvariable=var_a, width=12).grid(row=0, column=1, padx=5)

    tk.Label(frame, text="Borne b :").grid(row=0, column=2, sticky="w")
    tk.Entry(frame, textvariable=var_b, width=12).grid(row=0, column=3, padx=5)

    tk.Label(frame, text="Nombre de valeurs simulées :").grid(row=0, column=4, sticky="w")
    tk.Entry(frame, textvariable=var_n, width=8).grid(row=0, column=5, padx=5)

    # Tableau
    columns = ("p", "symbole", "g", "delta", "prime")
    table = ttk.Treeview(root, columns=columns, show="headings", height=15)
    for col in columns:
        table.heading(col, text=col)
    table.column("p", width=120)
    table.column("symbole", width=80)
    table.column("g", width=80)
    table.column("delta", width=80)
    table.column("prime", width=80)
    table.pack(padx=10, pady=10, fill="both", expand=True)

    # Figure taux de réussite
    fig = Figure(figsize=(5, 2.5), dpi=100)
    ax = fig.add_subplot(111)
    ax.set_title("Taux de réussite (%)")
    ax.set_xlabel("Simulation")
    ax.set_ylabel("Pourcentage de vrais premiers")
    success_rates = []
    line, = ax.plot([], [], marker="o")

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack(padx=10, pady=10, fill="x")
    canvas.draw()

    def update_success_plot():
        x = list(range(1, len(success_rates) + 1))
        line.set_data(x, success_rates)
        ax.set_xlim(1, max(1, len(success_rates)))
        ax.set_ylim(0, 100)
        canvas.draw()

    def simulate():
        try:
            a = int(var_a.get())
            b = int(var_b.get())
            n = int(var_n.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des entiers valides.")
            return

        if a >= b:
            messagebox.showerror("Erreur", "Borne a doit être < borne b.")
            return

        table.delete(*table.get_children())

        # Point de départ : on prend le premier nombre >= a autorisé mod 30
        current_p = a
        while not is_allowed_mod30(current_p):
            current_p += 1

        current_sym = initial_symbol()
        true_primes = 0

        for _ in range(n):
            # Choix du symbole suivant
            current_sym = next_symbol(current_sym)
            g_typ = typical_g_for_symbol(current_sym)
            delta = max(2, int(round(g_typ * math.log(max(3, current_p)))))

            # On force delta pair
            if delta % 2 != 0:
                delta += 1

            new_p = current_p + delta

            # Ajustement pour respecter mod 30
            while not is_allowed_mod30(new_p):
                new_p += 2

            # Filtre anti-multiples
            while not passes_small_prime_filter(new_p):
                new_p += 2
                if new_p > b:
                    break

            if new_p > b:
                break

            prime_flag = isprime(new_p)
            if prime_flag:
                true_primes += 1

            g_val = delta / math.log(max(3, current_p))

            table.insert(
                "",
                "end",
                values=(
                    new_p,
                    current_sym,
                    f"{g_val:.2f}",
                    delta,
                    "✓" if prime_flag else "x",
                ),
            )

            current_p = new_p

        if n > 0:
            rate = 100.0 * true_primes / n
            success_rates.append(rate)
            update_success_plot()
            messagebox.showinfo(
                "Résultat",
                f"Taux de vrais premiers : {rate:.2f} %\n"
                f"(sur {n} valeurs simulées)",
            )

    def show_stats():
        rows = table.get_children()
        if not rows:
            messagebox.showinfo("Statistiques", "Aucune donnée.")
            return
        total = len(rows)
        primes = 0
        for row in rows:
            vals = table.item(row)["values"]
            if vals[4] == "✓":
                primes += 1
        rate = 100.0 * primes / total
        messagebox.showinfo(
            "Statistiques",
            f"Nombre de valeurs : {total}\n"
            f"Vrais premiers : {primes}\n"
            f"Taux : {rate:.2f} %",
        )

    def compare_granville():
        rows = table.get_children()
        if not rows:
            messagebox.showinfo("Comparaison", "Aucune donnée.")
            return

        model_results = []
        granville_results = []

        for row in rows:
            p, sym, g, delta, prime_flag = table.item(row)["values"]
            p = int(p)
            model_results.append(1 if prime_flag == "✓" else 0)
            granville_results.append(granville_probability(p))

        fig2 = Figure(figsize=(5, 2.5), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.plot(model_results, label="Ton modèle (0/1)")
        ax2.plot(granville_results, label="Granville (probabilité)")
        ax2.set_title("Comparaison modèle vs Granville")
        ax2.legend()

        win = tk.Toplevel(root)
        win.title("Comparaison Granville")
        canvas2 = FigureCanvasTkAgg(fig2, master=win)
        canvas2.get_tk_widget().pack(fill="both", expand=True)
        canvas2.draw()

    # Boutons
    btn_frame = tk.Frame(root)
    btn_frame.pack(padx=10, pady=5)

    tk.Button(btn_frame, text="Simuler", command=simulate).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Statistiques", command=show_stats).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Comparer Granville", command=compare_granville).grid(row=0, column=2, padx=5)

    root.mainloop()

