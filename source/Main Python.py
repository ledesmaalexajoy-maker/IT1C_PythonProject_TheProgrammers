import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# Colors
BG    = "#F0EDD8"
GOLD  = "#B8973A"
DARK  = "#1A1A1A"
WHITE = "#FFFFFF"
CYAN  = "#00BFEA"
GREEN = "#27AE60"
RED   = "#E74C3C"
MUTED = "#7F8C8D"
CARD  = "#F5EDD0"

FT = ("Georgia", 20, "bold")
FH = ("Georgia", 14, "bold")
FS = ("Helvetica", 10)
FB = ("Helvetica", 11, "bold")
FL = ("Helvetica", 9)

# In-memory database
users       = {}
bookings    = []
ratings_db  = []
logged_user = {}

ROOMS = ["Twin Room", "Queen Room", "Triple Room",
         "Triple Room XL", "Deluxe Ocean View", "Family Room"]

ROOM_PRICES = {
    "Twin Room": 4500, "Queen Room": 6000, "Triple Room": 7500,
    "Triple Room XL": 8500, "Deluxe Ocean View": 10000, "Family Room": 14000
}


# ─────────────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LuxeVista - Luxury Resorts & Hotels")
        self.geometry("420x780")
        self.resizable(False, False)
        self.configure(bg=BG)
        self.frame = None
        self.go("Login")

    def go(self, page, **kw):
        if self.frame:
            self.frame.destroy()
        pages = {
            "Login": LoginPage, "Register": RegisterPage,
            "Home": HomePage, "Book": BookPage,
            "Reservations": ReservationsPage, "Rooms": RoomsPage,
            "Spa": SpaPage, "Ratings": RatingsPage, "Profile": ProfilePage,
            "Checkin": CheckinPage, "Checkout": CheckoutPage,
        }
        cls = pages.get(page, HomePage)
        self.frame = cls(self, self, **kw)
        self.frame.pack(fill="both", expand=True)

# ─── Reusable widgets ─────────────────────────────────────────────────────────
def make_header(parent, app, title="LuxeVista", back=None):
    bar = tk.Frame(parent, bg=DARK, height=58)
    bar.pack(fill="x")
    bar.pack_propagate(False)
    tk.Label(bar, text="LuxeVista", font=("Georgia", 13, "bold"),
             bg=DARK, fg=GOLD).pack(side="left", padx=14, pady=14)
    tk.Label(bar, text=title, font=("Helvetica", 10),
             bg=DARK, fg=WHITE).pack(side="right", padx=10)
    if back:
        btn = tk.Button(bar, text="< Back", font=FL, bg=DARK, fg=GOLD,
                        bd=0, cursor="hand2", activebackground=DARK,
                        activeforeground=GOLD,
                        command=lambda: app.go(back))
        btn.pack(side="right", padx=8)


def make_nav(parent, app):
    bar = tk.Frame(parent, bg=DARK, height=56)
    bar.pack(side="bottom", fill="x")
    bar.pack_propagate(False)
    nav_items = [("Home", "Home"), ("Reservations", "Reservations"),
                 ("Ratings", "Ratings"), ("Profile", "Profile")]
    for label, page in nav_items:
        btn = tk.Button(bar, text=label, font=("Helvetica", 9, "bold"),
                        bg=DARK, fg=GOLD, bd=0, cursor="hand2",
                        activebackground="#2A2A2A", activeforeground=WHITE,
                        command=lambda p=page: app.go(p))
        btn.pack(side="left", expand=True, fill="y")


def gold_button(parent, text, cmd, w=32):
    b = tk.Button(parent, text=text, font=FB, bg=GOLD, fg=WHITE,
                  bd=0, relief="flat", padx=8, pady=10,
                  width=w, cursor="hand2", activebackground="#9A7D30",
                  command=cmd)
    b.pack(pady=5, padx=20, fill="x")
    return b


def cyan_button(parent, text, cmd, w=32):
    b = tk.Button(parent, text=text, font=FB, bg=CYAN, fg=WHITE,
                  bd=0, relief="flat", padx=8, pady=10,
                  width=w, cursor="hand2", activebackground="#009DC4",
                  command=cmd)
    b.pack(pady=5, padx=20, fill="x")
    return b


def labeled_entry(parent, label, bg=BG, show=""):
    tk.Label(parent, text=label, font=("Helvetica", 10, "bold"),
             bg=bg, fg=DARK, anchor="w").pack(fill="x", padx=24, pady=(6, 0))
    var = tk.StringVar()
    e = tk.Entry(parent, textvariable=var, font=FS, bg=WHITE, bd=0,
                 highlightthickness=1, highlightbackground=GOLD, show=show)
    e.pack(fill="x", padx=24, ipady=8, pady=(2, 4))
    return var

# ─────────────────────────────────── PAGES ───────────────────────────────────
class LoginPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=BG)
        self.app = app
        tk.Label(self, text="LuxeVista", font=("Georgia", 28, "bold"),
                 bg=BG, fg=GOLD).pack(pady=(50, 2))
        tk.Label(self, text="LUXURY RESORTS & HOTELS", font=FL,
                 bg=BG, fg=MUTED).pack()
        tk.Label(self, text="Welcome Back!", font=FT, bg=BG, fg=DARK).pack(pady=(20, 2))
        tk.Label(self, text="Login to continue your booking",
                 font=FS, bg=BG, fg=MUTED).pack(pady=(0, 18))
        self.em = labeled_entry(self, "Email Address")
        self.pw = labeled_entry(self, "Password", show="*")
        tk.Label(self, text="Forgot password?", font=FL,
                 bg=BG, fg=CYAN, anchor="e").pack(fill="x", padx=24)
        tk.Frame(self, bg=BG, height=10).pack()
        cyan_button(self, "  Log In", self.login)
        tk.Label(self, text="or", font=FL, bg=BG, fg=MUTED).pack(pady=4)
        tk.Button(self, text="Create Account", font=FB, bg=WHITE, fg=GOLD,
                  bd=1, relief="solid", padx=8, pady=8, width=28,
                  cursor="hand2", command=lambda: app.go("Register")).pack()

    def login(self):
        em, pw = self.em.get().strip(), self.pw.get().strip()
        if not em or not pw:
            messagebox.showwarning("Empty", "Please fill in all fields."); return
        if em in users and users[em]["password"] == pw:
            logged_user.update(users[em])
            logged_user["email"] = em
            self.app.go("Home")
        else:
            messagebox.showerror("Failed", "Invalid email or password.")


class RegisterPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=BG)
        self.app = app
        tk.Label(self, text="LuxeVista", font=("Georgia", 22, "bold"),
                 bg=BG, fg=GOLD).pack(pady=(30, 2))
        tk.Label(self, text="Create Your Account", font=FT, bg=BG, fg=DARK).pack(pady=(10, 2))
        tk.Label(self, text="Fill in the details below to get started",
                 font=FS, bg=BG, fg=MUTED).pack(pady=(0, 10))
        self.nm = labeled_entry(self, "Full Name")
        self.em = labeled_entry(self, "Email Address")
        self.ph = labeled_entry(self, "Phone Number (+63)")
        self.pw = labeled_entry(self, "Password", show="*")
        self.p2 = labeled_entry(self, "Confirm Password", show="*")
        tk.Label(self, text="At least 8 characters with letters and numbers",
                 font=FL, bg=BG, fg=MUTED).pack()
        tk.Frame(self, bg=BG, height=8).pack()
        cyan_button(self, "Create Account", self.register)
        tk.Button(self, text="Already have an account? Log in", font=FL,
                  bg=BG, fg=GOLD, bd=0, cursor="hand2",
                  command=lambda: app.go("Login")).pack(pady=6)

    def register(self):
        n  = self.nm.get().strip()
        em = self.em.get().strip()
        ph = self.ph.get().strip()
        pw = self.pw.get()
        p2 = self.p2.get()
        if not all([n, em, ph, pw, p2]):
            messagebox.showwarning("Missing", "Please complete all fields."); return
        if pw != p2:
            messagebox.showerror("Mismatch", "Passwords do not match."); return
        if len(pw) < 8:
            messagebox.showerror("Short", "Password must be at least 8 characters."); return
        if em in users:
            messagebox.showerror("Exists", "Email already registered."); return
        users[em] = {"name": n, "phone": ph, "password": pw}
        messagebox.showinfo("Success!", "Account created! Please log in.")
        self.app.go("Login")


class HomePage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=BG)
        self.app = app
        make_header(self, app)
        # Hero
        hero = tk.Frame(self, bg=DARK, height=160)
        hero.pack(fill="x")
        hero.pack_propagate(False)
        tk.Label(hero, text="🏨", font=("Helvetica", 70), bg=DARK).pack(expand=True)
        tk.Label(self, text="A new window into luxury",
                 font=("Georgia", 15, "bold"), bg=BG, fg=DARK).pack(pady=(12, 0))
        tk.Label(self, text="Your Perfect Stay Starts Here",
                 font=FS, bg=BG, fg=GOLD).pack()

# Quick pills — all clickable
        pill = tk.Frame(self, bg=WHITE, pady=10, padx=8)
        pill.pack(fill="x", padx=18, pady=10)
        pill.columnconfigure((0, 1, 2), weight=1)
        pill_items = [("Check-in", "Checkin"), ("Check-out", "Checkout"), ("Guest", "Reservations")]
        for i, (lbl, pg) in enumerate(pill_items):
            f = tk.Button(pill, text=lbl, font=("Helvetica", 10, "bold"),
                          bg="#F0F0F0", fg=DARK, bd=0, relief="flat",
                          padx=6, pady=10, cursor="hand2",
                          activebackground=CARD,
                          command=lambda p=pg: app.go(p))
            f.grid(row=0, column=i, padx=4, sticky="ew")
        # Book Now button
        gold_button(self, "  BOOK NOW", lambda: app.go("Book"))
        # Rooms & Spa cards
        cats = tk.Frame(self, bg=BG)
        cats.pack(fill="x", padx=18, pady=4)
        cats.columnconfigure((0, 1), weight=1)
        for col, (lbl, pg) in enumerate([("Rooms", "Rooms"), ("Spa", "Spa")]):
            btn = tk.Button(cats, text=lbl, font=("Helvetica", 13, "bold"),
                            bg=CARD, fg=DARK, bd=0, relief="flat",
                            padx=10, pady=28, cursor="hand2",
                            activebackground="#E8D9A0",
                            command=lambda p=pg: app.go(p))
            btn.grid(row=0, column=col, padx=6, sticky="nsew")
        make_nav(self, app)


class BookPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=BG)
        self.app = app
        make_header(self, app, "Book Now", back="Home")
        tk.Label(self, text="BOOK NOW", font=FT, bg=BG, fg=GOLD).pack(pady=(12, 2))
        tk.Label(self, text="Your Perfect Stay Starts Here", font=FL, bg=BG, fg=MUTED).pack()

        card = tk.Frame(self, bg=WHITE, padx=16, pady=14)
        card.pack(fill="x", padx=18, pady=10)

        def row_entry(par, lbl, val="", bg=WHITE):
            tk.Label(par, text=lbl, font=("Helvetica", 9, "bold"),
                     bg=bg, fg=DARK, anchor="w").pack(fill="x")
            v = tk.StringVar(value=val)
            e = tk.Entry(par, textvariable=v, font=FL, bg="#F9F9F9",
                         bd=0, highlightthickness=1, highlightbackground=GOLD)
            e.pack(fill="x", ipady=6, pady=(2, 8))
            return v

        self.gname  = row_entry(card, "Full Name", logged_user.get("name", ""))
        self.gemail = row_entry(card, "Email",     logged_user.get("email", ""))

        drow = tk.Frame(card, bg=WHITE)
        drow.pack(fill="x")
        drow.columnconfigure((0, 1), weight=1)

        lf = tk.Frame(drow, bg=WHITE); lf.grid(row=0, column=0, padx=(0, 4), sticky="ew")
        rf = tk.Frame(drow, bg=WHITE); rf.grid(row=0, column=1, padx=(4, 0), sticky="ew")

        today = datetime.date.today().strftime("%Y-%m-%d")
        tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        def small_entry(par, lbl, val):
            tk.Label(par, text=lbl, font=FL, bg=WHITE, fg=DARK, anchor="w").pack(fill="x")
            v = tk.StringVar(value=val)
            e = tk.Entry(par, textvariable=v, font=FL, bg="#F9F9F9",
                         bd=0, highlightthickness=1, highlightbackground=GOLD)
            e.pack(fill="x", ipady=5, pady=(2, 8))
            return v

        self.cin  = small_entry(lf, "Check-in (YYYY-MM-DD)", today)
        self.cout = small_entry(rf, "Check-out (YYYY-MM-DD)", tomorrow)

        tk.Label(card, text="Number of Guests", font=("Helvetica", 9, "bold"),
                 bg=WHITE, fg=DARK, anchor="w").pack(fill="x")
        self.guests = ttk.Combobox(card, font=FL, state="readonly",
                                   values=["1 Adult", "2 Adults", "3 Adults",
                                           "2 Adults + 1 Kid", "Family (4+)"])
        self.guests.set("Select guests")
        self.guests.pack(fill="x", ipady=3, pady=(2, 8))

        tk.Label(card, text="Choose Your Room", font=("Helvetica", 9, "bold"),
                 bg=WHITE, fg=DARK, anchor="w").pack(fill="x")
        self.room = ttk.Combobox(card, font=FL, state="readonly", values=ROOMS)
        self.room.set("Select room type")
        self.room.pack(fill="x", ipady=3, pady=(2, 4))

        gold_button(self, "BOOK NOW", self.do_book)
        make_nav(self, app)

    def do_book(self):
        name   = self.gname.get().strip()
        email  = self.gemail.get().strip()
        cin    = self.cin.get().strip()
        cout   = self.cout.get().strip()
        guests = self.guests.get()
        room   = self.room.get()

        if not all([name, email, cin, cout]) or "Select" in guests or "Select" in room:
            messagebox.showwarning("Incomplete", "Please fill in all fields."); return
        try:
            d1 = datetime.date.fromisoformat(cin)
            d2 = datetime.date.fromisoformat(cout)
            nights = (d2 - d1).days
            if nights <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Date Error", "Check-out must be after Check-in."); return

        rate  = ROOM_PRICES.get(room, 6000)
        sub   = rate * nights
        tax   = int(sub * 0.20)
        total = sub + tax
class CheckinPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=BG)
        make_header(self, app, "Check-in", back="Home")
        tk.Label(self, text="Check-in Details", font=FH, bg=BG, fg=DARK).pack(pady=14)

        my = [b for b in bookings if b.get("email") == logged_user.get("email", "")]
        if not my:
            tk.Label(self, text="No active bookings found.\nPlease make a reservation first.",
                     font=FS, bg=BG, fg=MUTED, justify="center").pack(pady=30)
            gold_button(self, "Book Now", lambda: app.go("Book"))
        else:
            b = my[-1]
            info_card = tk.Frame(self, bg=WHITE, padx=20, pady=16)
            info_card.pack(fill="x", padx=20, pady=8)
            tk.Label(info_card, text="Check-in Date & Time",
                     font=("Helvetica", 11, "bold"), bg=WHITE, fg=GOLD).pack(anchor="w")
            tk.Label(info_card, text=f"{b['cin']}  at  2:00 PM",
                     font=("Georgia", 13, "bold"), bg=WHITE, fg=DARK).pack(anchor="w", pady=(2, 10))

            steps = [
                ("Arrival & Welcome",   "Our staff will greet and assist you."),
                ("ID Verification",     "Please present a valid government ID."),
                ("Payment Confirmation","We will verify your reservation details."),
                ("Room Key",            "You will receive your room key and WiFi access."),
                ("Enjoy Your Stay!",    "Your perfect luxury stay begins here."),
            ]
            for title, desc in steps:
                row = tk.Frame(info_card, bg=WHITE); row.pack(fill="x", pady=4)
                tk.Label(row, text=title, font=("Helvetica", 10, "bold"),
                         bg=WHITE, fg=DARK).pack(anchor="w")
                tk.Label(row, text=desc, font=FL, bg=WHITE, fg=MUTED).pack(anchor="w")

            note = tk.Frame(self, bg=CARD, padx=14, pady=10)
            note.pack(fill="x", padx=20, pady=6)
            tk.Label(note, text="Need early check-in?", font=("Helvetica", 10, "bold"),
                     bg=CARD, fg=DARK).pack(anchor="w")
            tk.Label(note, text="Contact our front desk for availability.",
                     font=FL, bg=CARD, fg=MUTED).pack(anchor="w")
        make_nav(self, app)


class CheckoutPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=BG)
        make_header(self, app, "Check-out", back="Home")
        tk.Label(self, text="Check-out Details", font=FH, bg=BG, fg=DARK).pack(pady=14)

        my = [b for b in bookings if b.get("email") == logged_user.get("email", "")]
        if not my:
            tk.Label(self, text="No active bookings found.",
                     font=FS, bg=BG, fg=MUTED).pack(pady=30)
            gold_button(self, "Book Now", lambda: app.go("Book"))
        else:
            b = my[-1]
            info_card = tk.Frame(self, bg=WHITE, padx=20, pady=16)
            info_card.pack(fill="x", padx=20, pady=8)
            tk.Label(info_card, text="Check-out Date & Time",
                     font=("Helvetica", 11, "bold"), bg=WHITE, fg=GOLD).pack(anchor="w")
            tk.Label(info_card, text=f"{b['cout']}  at  12:00 PM",
                     font=("Georgia", 13, "bold"), bg=WHITE, fg=DARK).pack(anchor="w", pady=(2, 10))

            steps = [
                ("Express Check-out", "Quick and seamless check-out process."),
                ("Bill Settlement",   "We will review charges and process payment."),
                ("Room Inspection",   "A quick room check ensures everything is in order."),
                ("Thank You!",        "Thank you for staying. We hope to see you again!"),
            ]
            for title, desc in steps:
                row = tk.Frame(info_card, bg=WHITE); row.pack(fill="x", pady=4)
                tk.Label(row, text=title, font=("Helvetica", 10, "bold"),
                         bg=WHITE, fg=DARK).pack(anchor="w")
                tk.Label(row, text=desc, font=FL, bg=WHITE, fg=MUTED).pack(anchor="w")

            note = tk.Frame(self, bg=CARD, padx=14, pady=10)
            note.pack(fill="x", padx=20, pady=6)
            tk.Label(note, text="Need late check-out?", font=("Helvetica", 10, "bold"),
                     bg=CARD, fg=DARK).pack(anchor="w")
            tk.Label(note, text="Contact our front desk for availability.",
                     font=FL, bg=CARD, fg=MUTED).pack(anchor="w")
        make_nav(self, app)


class RatingsPage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=BG)
        self.app = app
        self.star = 0
        make_header(self, app, "Ratings", back="Home")
        tk.Label(self, text="Rate Your Stay", font=FH, bg=BG, fg=DARK).pack(pady=(14, 2))
        tk.Label(self, text="Your feedback helps us improve!",
                 font=FL, bg=BG, fg=MUTED).pack()

        sf = tk.Frame(self, bg=BG); sf.pack(pady=12)
        self.slbls = []
        for i in range(1, 6):
            lbl = tk.Button(sf, text="*", font=("Helvetica", 28), bg=BG, fg=GOLD,
                            bd=0, cursor="hand2", activebackground=BG,
                            command=lambda s=i: self.set_star(s))
            lbl.pack(side="left", padx=2)
            self.slbls.append(lbl)

        tk.Label(self, text="Write a Review", font=("Helvetica", 10, "bold"),
                 bg=BG, fg=DARK, anchor="w").pack(fill="x", padx=24)
        self.txt = tk.Text(self, font=FS, height=4, bd=0,
                           highlightthickness=1, highlightbackground=GOLD, wrap="word")
        self.txt.pack(fill="x", padx=24, pady=(4, 8))
        gold_button(self, "Submit Rating", self.submit)

        tk.Label(self, text="Guest Reviews", font=("Helvetica", 10, "bold"),
                 bg=BG, fg=GOLD).pack(pady=(10, 4))
        self.rf = tk.Frame(self, bg=BG)
        self.rf.pack(fill="both", expand=True, padx=18)
        self.show_reviews()
        make_nav(self, app)

    def set_star(self, s):
        self.star = s
        for i, b in enumerate(self.slbls):
            b.config(text="*" if i < s else "-", fg=GOLD if i < s else MUTED)

    def submit(self):
        if self.star == 0:
            messagebox.showwarning("No Rating", "Please select a star rating first."); return
        rev = self.txt.get("1.0", "end").strip()
        ratings_db.append({
            "user": logged_user.get("name", "Guest"),
            "stars": self.star,
            "review": rev if rev else "No comment.",
            "date": str(datetime.date.today())
        })
        messagebox.showinfo("Thank you!", f"You rated us {self.star} star(s). We appreciate it!")
        self.set_star(0)
        self.txt.delete("1.0", "end")
        self.show_reviews()

    def show_reviews(self):
        for w in self.rf.winfo_children(): w.destroy()
        if not ratings_db:
            tk.Label(self.rf, text="No reviews yet. Be the first!",
                     font=FL, bg=BG, fg=MUTED).pack(pady=10)
            return
        for r in reversed(ratings_db[-5:]):
            card = tk.Frame(self.rf, bg=WHITE, pady=8, padx=12)
            card.pack(fill="x", pady=4)
            top = tk.Frame(card, bg=WHITE); top.pack(fill="x")
            tk.Label(top, text=r["user"], font=("Helvetica", 10, "bold"),
                     bg=WHITE, fg=DARK).pack(side="left")
            stars_txt = ("*" * r["stars"]) + ("-" * (5 - r["stars"]))
            tk.Label(top, text=stars_txt, font=("Helvetica", 13, "bold"),
                     bg=WHITE, fg=GOLD).pack(side="right")
            tk.Label(card, text=r["review"], font=FL, bg=WHITE, fg=MUTED,
                     wraplength=310, justify="left", anchor="w").pack(fill="x")
            tk.Label(card, text=r["date"], font=("Helvetica", 7),
                     bg=WHITE, fg="#BBBBBB").pack(anchor="e")


class ProfilePage(tk.Frame):
    def __init__(self, parent, app, **kw):
        super().__init__(parent, bg=BG)
        self.app = app
        make_header(self, app, "Profile", back="Home")

        av = tk.Frame(self, bg=DARK, width=72, height=72)
        av.pack(pady=(20, 8))
        av.pack_propagate(False)
        tk.Label(av, text="U", font=("Georgia", 30, "bold"),
                 bg=DARK, fg=GOLD).pack(expand=True)

        name  = logged_user.get("name", "Guest")
        email = logged_user.get("email", "--")
        phone = logged_user.get("phone", "--")

        tk.Label(self, text=name, font=("Georgia", 15, "bold"), bg=BG, fg=DARK).pack()
        tk.Label(self, text=email, font=FL, bg=BG, fg=MUTED).pack(pady=(0, 12))

        card = tk.Frame(self, bg=WHITE, pady=16, padx=20)
        card.pack(fill="x", padx=20)
        tk.Label(card, text="Personal Details", font=("Helvetica", 12, "bold"),
                 bg=WHITE, fg=GOLD).pack(anchor="w")
        tk.Frame(card, bg=GOLD, height=1).pack(fill="x", pady=6)

        for lbl, val in [("Full Name", name), ("Email", email), ("Phone", phone)]:
            row = tk.Frame(card, bg=WHITE); row.pack(fill="x", pady=4)
            tk.Label(row, text=lbl, font=FL, bg=WHITE, fg=MUTED,
                     width=14, anchor="w").pack(side="left")
            tk.Label(row, text=val, font=("Helvetica", 10, "bold"),
                     bg=WHITE, fg=DARK).pack(side="left")

        tk.Frame(self, bg=BG, height=16).pack()
        tk.Button(self, text="Log Out", font=FB, bg=RED, fg=WHITE,
                  bd=0, padx=20, pady=10, width=28,
                  cursor="hand2", activebackground="#C0392B",
                  command=self.logout).pack()
        make_nav(self, app)

    def logout(self):
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            logged_user.clear()
            self.app.go("Login")
# ─────────────────────────────────── MAIN ────────────────────────────────────
if _name_ == "_main_":
    users["demo@luxevista.com"] = {
        "name": "Juan Dela Cruz",
        "phone": "+63 962 553 1020",
        "password": "demo1234"
    }
    App().mainloop()
Compose
Write
