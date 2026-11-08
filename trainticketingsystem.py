# train_ticket_system_final.py
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime

DB_NAME = "train_system"   # <-- your confirmed DB name

# ------------------ Database helpers ------------------
def connect_db():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",         # change if needed
            password="Shyam200812",         # change if needed
            database=DB_NAME
        )
    except Exception as e:
        messagebox.showerror("DB Error", f"Cannot connect to database:\n{e}")
        return None

def run_select(query, params=()):
    conn = connect_db()
    if not conn:
        return []
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows

def run_commit(query, params=()):
    conn = connect_db()
    if not conn:
        return False
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close()
    return True

# ------------------ UI helpers ------------------
def center_window(win, width=500, height=400):
    win.update_idletasks()
    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    x = (screen_w // 2) - (width // 2)
    y = (screen_h // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# ------------------ Main window creator ------------------
def create_main_window():
    main = tk.Tk()
    main.title("Train Ticketing System - Main")
    main.configure(bg="#f0f8ff")

    # center-ish
    center_window(main, width=520, height=420)

    tk.Label(main, text="🚆 Train Ticketing System", font=("Comic Sans MS", 18, "bold"),
             bg="#f0f8ff", fg="#0b3d91").pack(pady=20)

    btn_frame = tk.Frame(main, bg="#f0f8ff")
    btn_frame.pack(pady=20)

    # User login button
    tk.Button(btn_frame, text="User Login", width=18, height=2, bg="#32CD32", fg="white",
              font=("Arial", 11, "bold"),
              command=lambda: [main.destroy(), open_user_login()]).grid(row=0, column=0, padx=16, pady=10)

    # Admin login button
    tk.Button(btn_frame, text="Admin Login", width=18, height=2, bg="#800080", fg="white",
              font=("Arial", 11, "bold"),
              command=lambda: [main.destroy(), open_admin_login()]).grid(row=0, column=1, padx=16, pady=10)

    # short instructions
    tk.Label(main, text="Choose: User Login (students) or Admin Login (teacher/demo)",
             bg="#f0f8ff", fg="#333").pack(pady=10)

    main.mainloop()

# ------------------ User login window ------------------
def open_user_login():
    login = tk.Tk()
    login.title("User Login")
    login.configure(bg="#fffaf0")
    center_window(login, width=420, height=320)

    tk.Label(login, text="User Login", font=("Arial", 16, "bold"), bg="#fffaf0", fg="#b35900").pack(pady=12)
    tk.Label(login, text="Email", bg="#fffaf0").pack()
    entry_email = tk.Entry(login, width=35); entry_email.pack(pady=4)
    tk.Label(login, text="Password", bg="#fffaf0").pack()
    entry_pass = tk.Entry(login, width=35, show="*"); entry_pass.pack(pady=4)

    def do_login():
        em = entry_email.get().strip()
        pw = entry_pass.get().strip()
        if not em or not pw:
            messagebox.showwarning("Input", "Enter both email and password")
            return
        rows = run_select("SELECT * FROM users WHERE email=%s AND password=%s", (em, pw))
        if rows:
            login.destroy()
            open_user_panel(em)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials or not registered")

    def open_register_window():
        reg = tk.Toplevel(login)
        reg.title("Register")
        reg.configure(bg="#f7fff0")
        center_window(reg, width=380, height=260)
        tk.Label(reg, text="Register New User", font=("Arial", 14, "bold"), bg="#f7fff0").pack(pady=10)
        tk.Label(reg, text="Email", bg="#f7fff0").pack(); e1 = tk.Entry(reg, width=35); e1.pack(pady=4)
        tk.Label(reg, text="Password", bg="#f7fff0").pack(); e2 = tk.Entry(reg, show="*", width=35); e2.pack(pady=4)
        def do_reg():
            em = e1.get().strip(); pw = e2.get().strip()
            if not em or not pw:
                messagebox.showwarning("Input", "Fill both fields"); return
            try:
                ok = run_commit("INSERT INTO users (email, password) VALUES (%s,%s)", (em, pw))
                if ok:
                    messagebox.showinfo("Registered", "Registration successful! Please login.")
                    reg.destroy()
            except Exception as ex:
                messagebox.showerror("Error", f"Registration failed:\n{ex}")
        tk.Button(reg, text="Register", bg="#ff8c00", fg="white", command=do_reg).pack(pady=10)

    tk.Button(login, text="Login", bg="#228B22", fg="white", width=14, command=do_login).pack(pady=8)
    tk.Button(login, text="Register", bg="#1E90FF", fg="white", width=14, command=open_register_window).pack()

    login.mainloop()

# ------------------ Admin login window ------------------
def open_admin_login():
    login = tk.Tk()
    login.title("Admin Login")
    login.configure(bg="#f5f0ff")
    center_window(login, width=420, height=280)

    tk.Label(login, text="Admin Login", font=("Arial", 16, "bold"), bg="#f5f0ff", fg="#6a006a").pack(pady=12)
    tk.Label(login, text="Username", bg="#f5f0ff").pack()
    entry_user = tk.Entry(login, width=35); entry_user.pack(pady=4)
    tk.Label(login, text="Password", bg="#f5f0ff").pack()
    entry_pass = tk.Entry(login, width=35, show="*"); entry_pass.pack(pady=4)

    def do_login():
        u = entry_user.get().strip()
        p = entry_pass.get().strip()
        if u == "sss123" and p == "Shyam200812":
            login.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Login Failed", "Invalid admin credentials")

    tk.Button(login, text="Login as Admin", bg="#800080", fg="white", width=16, command=do_login).pack(pady=12)
    login.mainloop()

# ------------------ User Panel ------------------
def open_user_panel(user_email):
    user_win = tk.Tk()
    user_win.title(f"User Panel - {user_email}")
    center_window(user_win, width=800, height=600)
    user_win.configure(bg="#e6f7ff")

    tk.Label(user_win, text=f"Welcome, {user_email}", font=("Comic Sans MS", 14, "bold"), bg="#e6f7ff", fg="#3b1f7a").pack(pady=12)

    # Action buttons area
    btn_frame = tk.Frame(user_win, bg="#e6f7ff"); btn_frame.pack(pady=6)
    tk.Button(btn_frame, text="Search & Book Trains", bg="#32CD32", fg="white", width=20, height=2,
              command=lambda: open_search_book_window(user_win, user_email)).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="View / Cancel Bookings", bg="#FF4500", fg="white", width=20, height=2,
              command=lambda: open_view_cancel_window(user_win, user_email)).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Logout", bg="#808080", fg="white", width=12, height=2,
              command=lambda: [user_win.destroy(), create_main_window()]).grid(row=0, column=2, padx=10)

    user_win.mainloop()

# ------------------ Search & Book window ------------------
def open_search_book_window(parent, user_email):
    win = tk.Toplevel(parent)
    win.title("Search & Book Trains")
    center_window(win, width=760, height=520)
    win.configure(bg="#fffaf0")

    tk.Label(win, text="Search and Book", font=("Arial", 14, "bold"), bg="#fffaf0").pack(pady=10)

    frame = tk.Frame(win, bg="#fffaf0"); frame.pack(pady=6)
    cities = ["Delhi", "Mumbai", "Chennai", "Kolkata", "Bangalore", "Hyderabad", "Agra", "Goa"]

    tk.Label(frame, text="From:", bg="#fffaf0").grid(row=0, column=0, padx=6, pady=6, sticky="e")
    cb_from = ttk.Combobox(frame, values=cities, state="readonly", width=20); cb_from.grid(row=0, column=1)
    tk.Label(frame, text="To:", bg="#fffaf0").grid(row=1, column=0, padx=6, pady=6, sticky="e")
    cb_to = ttk.Combobox(frame, values=cities, state="readonly", width=20); cb_to.grid(row=1, column=1)
    tk.Label(frame, text="Seats:", bg="#fffaf0").grid(row=2, column=0, padx=6, pady=6, sticky="e")
    entry_seats = tk.Entry(frame, width=10); entry_seats.grid(row=2, column=1, sticky="w")

    # result tree
    cols = ("train_no","train_name","from_place","to_place","fare","available_seats")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=8)
    for c in cols:
        tree.heading(c, text=c.replace("_"," ").title()); tree.column(c, width=120)
    tree.pack(pady=12, fill="x")

    def search():
        f = cb_from.get().strip(); t = cb_to.get().strip()
        if not f or not t:
            messagebox.showwarning("Input", "Choose both From and To")
            return
        rows = run_select("SELECT train_no, train_name, from_place, to_place, fare, available_seats FROM trains WHERE from_place=%s AND to_place=%s AND available_seats>0", (f,t))
        tree.delete(*tree.get_children())
        if not rows:
            messagebox.showinfo("No Trains", "No trains found for the selected route.")
            return
        for r in rows:
            tree.insert("", "end", values=r)

    def book_selected():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a train to book")
            return
        seats = entry_seats.get().strip()
        if not seats.isdigit() or int(seats) <= 0:
            messagebox.showerror("Error", "Enter a valid number of seats")
            return
        seats = int(seats)
        vals = tree.item(sel[0])["values"]
        tno, tname, frm, to, fare, avail = vals
        if seats > avail:
            messagebox.showerror("Error", f"Only {avail} seats available")
            return
        total = seats * fare

        # Payment simulation window
        pay = tk.Toplevel(win); pay.title("Payment"); pay.configure(bg="#f0fff0"); center_window(pay, width=340, height=240)
        tk.Label(pay, text=f"Train: {tname} ({tno})", bg="#f0fff0").pack(pady=6)
        tk.Label(pay, text=f"Seats: {seats}   Total: ₹{total}", bg="#f0fff0").pack(pady=4)
        tk.Label(pay, text="Enter Card No (simulation):", bg="#f0fff0").pack(pady=6)
        card = tk.Entry(pay); card.pack(pady=4)
        def confirm_payment():
            if card.get().strip() == "":
                messagebox.showerror("Error", "Enter card info (any digits)")
                return
            # insert booking and decrease available seats
            ok1 = run_commit("INSERT INTO bookings (email, train_no, train_name, from_place, to_place, seats, total_fare) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                             (user_email, tno, tname, frm, to, seats, total))
            ok2 = run_commit("UPDATE trains SET available_seats = available_seats - %s WHERE train_no = %s", (seats, tno))
            if ok1 and ok2:
                messagebox.showinfo("Success", "Payment successful and ticket booked!")
                pay.destroy()
                search()   # refresh available seats listing
            else:
                messagebox.showerror("Error", "Booking failed (DB error).")
        tk.Button(pay, text="Confirm Payment", bg="#32CD32", fg="white", command=confirm_payment).pack(pady=10)

    # buttons
    btn_frame = tk.Frame(win, bg="#fffaf0"); btn_frame.pack(pady=6)
    tk.Button(btn_frame, text="Search", bg="#ff8c00", fg="white", command=search, width=12).grid(row=0, column=0, padx=8)
    tk.Button(btn_frame, text="Book Selected", bg="#4CAF50", fg="white", command=book_selected, width=12).grid(row=0, column=1, padx=8)

# ------------------ View & Cancel bookings ------------------
def open_view_cancel_window(parent, user_email):
    win = tk.Toplevel(parent)
    win.title("My Bookings")
    center_window(win, width=760, height=480)
    win.configure(bg="#fff0f5")

    tk.Label(win, text="My Bookings", font=("Arial", 14, "bold"), bg="#fff0f5").pack(pady=10)

    cols = ("id","train_no","train_name","from_place","to_place","seats","total_fare","booking_date")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
    for c in cols:
        tree.heading(c, text=c.replace("_"," ").title()); tree.column(c, width=100)
    tree.pack(pady=8, fill="both", expand=True)

    def load():
        tree.delete(*tree.get_children())
        rows = run_select("SELECT id, train_no, train_name, from_place, to_place, seats, total_fare, booking_date FROM bookings WHERE email=%s ORDER BY booking_date DESC", (user_email,))
        for r in rows:
            tree.insert("", "end", values=r)

    def cancel_selected():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a booking to cancel")
            return
        val = tree.item(sel[0])["values"]
        bid = val[0]; tno = val[1]; seats = val[5]
        if messagebox.askyesno("Confirm", "Cancel this booking?"):
            ok1 = run_commit("DELETE FROM bookings WHERE id=%s", (bid,))
            ok2 = run_commit("UPDATE trains SET available_seats = available_seats + %s WHERE train_no = %s", (seats, tno))
            if ok1 and ok2:
                messagebox.showinfo("Cancelled", "Booking cancelled and seats restored")
                load()
            else:
                messagebox.showerror("Error", "Cancel failed (DB error)")

    tk.Button(win, text="Cancel Selected Booking", bg="#ff3333", fg="white", command=cancel_selected).pack(pady=6)
    load()

# ------------------ Admin Panel ------------------
def open_admin_panel():
    admin_win = tk.Tk()
    admin_win.title("Admin Panel")
    center_window(admin_win, width=900, height=640)
    admin_win.configure(bg="#fffaf0")

    tk.Label(admin_win, text="Admin Dashboard", font=("Comic Sans MS", 16, "bold"), bg="#fffaf0", fg="#8b008b").pack(pady=12)

    # Buttons row
    btnf = tk.Frame(admin_win, bg="#fffaf0"); btnf.pack(pady=8)
    tk.Button(btnf, text="View All Bookings", bg="#4CAF50", fg="white", width=18, command=lambda: admin_view_bookings()).grid(row=0, column=0, padx=8)
    tk.Button(btnf, text="Manage Trains", bg="#1E90FF", fg="white", width=18, command=lambda: admin_manage_trains()).grid(row=0, column=1, padx=8)
    tk.Button(btnf, text="Payment Reports", bg="#FF8C00", fg="white", width=18, command=lambda: admin_payment_reports()).grid(row=0, column=2, padx=8)
    tk.Button(btnf, text="Logout", bg="#808080", fg="white", width=12, command=lambda: [admin_win.destroy(), create_main_window()]).grid(row=0, column=3, padx=12)

    admin_win.mainloop()

# Admin helpers (each opens its own window)
def admin_view_bookings():
    win = tk.Toplevel()
    win.title("All Bookings")
    center_window(win, width=900, height=460)
    cols = ("id","email","train_name","from","to","seats","fare","date")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c.title()); tree.column(c, width=110)
    tree.pack(fill="both", expand=True)
    rows = run_select("SELECT id, email, train_name, from_place, to_place, seats, total_fare, booking_date FROM bookings ORDER BY booking_date DESC")
    for r in rows: tree.insert("", "end", values=r)

def admin_manage_trains():
    win = tk.Toplevel(); win.title("Manage Trains"); center_window(win, width=880, height=540); win.configure(bg="#f7fff0")
    cols = ("train_no","train_name","from_place","to_place","fare","available_seats")
    tree = ttk.Treeview(win, columns=cols, show="headings", height=12)
    for c in cols:
        tree.heading(c, text=c.replace("_"," ").title()); tree.column(c, width=130)
    tree.pack(pady=8, fill="x")

    def refresh():
        tree.delete(*tree.get_children())
        rows = run_select("SELECT train_no, train_name, from_place, to_place, fare, available_seats FROM trains")
        for r in rows: tree.insert("", "end", values=r)

    def add_train():
        at = tk.Toplevel(win); at.title("Add Train"); center_window(at, width=360, height=420); at.configure(bg="#fffaf0")
        labels = ["Train No","Name","From","To","Fare","Available Seats"]; entries={}
        for L in labels:
            tk.Label(at, text=L, bg="#fffaf0").pack(pady=3); e=tk.Entry(at); e.pack(); entries[L]=e
        def save():
            try:
                run_commit("INSERT INTO trains (train_no, train_name, from_place, to_place, fare, available_seats) VALUES (%s,%s,%s,%s,%s,%s)",
                           (entries["Train No"].get(), entries["Name"].get(), entries["From"].get(), entries["To"].get(),
                            entries["Fare"].get(), entries["Available Seats"].get()))
                messagebox.showinfo("Added", "Train added")
                at.destroy(); refresh()
            except Exception as ex:
                messagebox.showerror("Error", f"Add failed:\n{ex}")
        tk.Button(at, text="Save", bg="#33aa33", fg="white", command=save).pack(pady=10)

    def edit_train():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a train"); return
        val = tree.item(sel[0])["values"]
        et = tk.Toplevel(win); et.title("Edit Train"); center_window(et, width=360, height=420); et.configure(bg="#f0fff0")
        labels = ["Name","From","To","Fare","Available Seats"]; entries={}
        for i,L in enumerate(labels):
            tk.Label(et, text=L, bg="#f0fff0").pack(pady=3); e=tk.Entry(et); e.pack(); e.insert(0, val[i+1]); entries[L]=e
        def save_edit():
            try:
                run_commit("UPDATE trains SET train_name=%s, from_place=%s, to_place=%s, fare=%s, available_seats=%s WHERE train_no=%s",
                           (entries["Name"].get(), entries["From"].get(), entries["To"].get(), entries["Fare"].get(), entries["Available Seats"].get(), val[0]))
                messagebox.showinfo("Updated", "Train updated")
                et.destroy(); refresh()
            except Exception as ex:
                messagebox.showerror("Error", f"Update failed:\n{ex}")
        tk.Button(et, text="Save Changes", bg="#3388ff", fg="white", command=save_edit).pack(pady=8)

    def delete_train():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a train"); return
        tno = tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirm", "Delete this train?"):
            run_commit("DELETE FROM trains WHERE train_no=%s", (tno,))
            messagebox.showinfo("Deleted", "Train removed")
            refresh()

    # buttons
    btnf = tk.Frame(win, bg="#f7fff0"); btnf.pack(pady=6)
    tk.Button(btnf, text="Add Train", bg="#00b300", fg="white", command=add_train).pack(side="left", padx=6)
    tk.Button(btnf, text="Edit Selected", bg="#1E90FF", fg="white", command=edit_train).pack(side="left", padx=6)
    tk.Button(btnf, text="Delete Selected", bg="#ff3333", fg="white", command=delete_train).pack(side="left", padx=6)

    refresh()

def admin_payment_reports():
    win = tk.Toplevel(); win.title("Payment Reports"); center_window(win, width=900, height=520); win.configure(bg="#fffdf0")
    tk.Label(win, text="Train-wise Payments", font=("Arial", 12, "bold"), bg="#fffdf0").pack(pady=6)
    t1 = ttk.Treeview(win, columns=("Train","Total"), show="headings"); t1.heading("Train", text="Train"); t1.heading("Total", text="Total (₹)"); t1.pack(fill="x", padx=10)
    tk.Label(win, text="Date-wise Payments", font=("Arial", 12, "bold"), bg="#fffdf0").pack(pady=10)
    t2 = ttk.Treeview(win, columns=("Date","Total"), show="headings"); t2.heading("Date", text="Date"); t2.heading("Total", text="Total (₹)"); t2.pack(fill="x", padx=10)
    rows = run_select("SELECT train_name, SUM(total_fare) FROM bookings GROUP BY train_name")
    for r in rows: t1.insert("", "end", values=r)
    rows2 = run_select("SELECT DATE(booking_date), SUM(total_fare) FROM bookings GROUP BY DATE(booking_date)")
    for r in rows2: t2.insert("", "end", values=r)

# ------------------ Start the app ------------------
if __name__ == "__main__":
    create_main_window()
