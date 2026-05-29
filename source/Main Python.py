import tkinter as tk
from tkinter import ttk, messagebox
import datetime

BG="#F0EDD8"; GOLD="#A9882E"; DARK="#1A1A1A"; WHITE="#FFFFFF"
CYAN="#00BFEA"; GREEN="#27AE60"; RED="#E74C3C"; MUTED="#7F8C8D"; CARD="#F5EDD0"
FT=("Georgia",20,"bold"); FH=("Georgia",14,"bold"); FS=("Helvetica",10)
FB=("Helvetica",11,"bold"); FL=("Helvetica",9)

users={}; bookings=[]; ratings_db=[]; logged_user={}
ROOMS=["Twin Room","Queen Room","Triple Room","Triple Room XL","Deluxe Ocean View","Family Room"]
ROOM_PRICES={"Twin Room":4500,"Queen Room":6000,"Triple Room":7500,
             "Triple Room XL":8500,"Deluxe Ocean View":10000,"Family Room":14000}

# ── Helpers ────────────────────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LuxeVista - Luxury Resorts & Hotels")
        self.geometry("420x780"); self.resizable(False,False); self.configure(bg=BG)
        self.frame=None; self.go("Login")

    def go(self, page, **kw):
        if self.frame: self.frame.destroy()
        pages={"Login":LoginPage,"Register":RegisterPage,"Home":HomePage,"Book":BookPage,
               "Reservations":ReservationsPage,"Rooms":RoomsPage,"Spa":SpaPage,
               "Ratings":RatingsPage,"Profile":ProfilePage,"Checkin":CheckinPage,"Checkout":CheckoutPage}
        self.frame=pages.get(page,HomePage)(self,self,**kw)
        self.frame.pack(fill="both",expand=True)

def hdr(parent,app,title="LuxeVista",back=None):
    bar=tk.Frame(parent,bg=DARK,height=58); bar.pack(fill="x"); bar.pack_propagate(False)
    tk.Label(bar,text="LuxeVista",font=("Georgia",13,"bold"),bg=DARK,fg=GOLD).pack(side="left",padx=14,pady=14)
    tk.Label(bar,text=title,font=("Helvetica",10),bg=DARK,fg=WHITE).pack(side="right",padx=10)
    if back:
        tk.Button(bar,text="< Back",font=FL,bg=DARK,fg=GOLD,bd=0,cursor="hand2",
                  activebackground=DARK,activeforeground=GOLD,
                  command=lambda:app.go(back)).pack(side="right",padx=8)

def nav(parent,app):
    bar=tk.Frame(parent,bg=DARK,height=56); bar.pack(side="bottom",fill="x"); bar.pack_propagate(False)
    for lbl,pg in [("Home","Home"),("Reservations","Reservations"),("Ratings","Ratings"),("Profile","Profile")]:
        tk.Button(bar,text=lbl,font=("Helvetica",9,"bold"),bg=DARK,fg=GOLD,bd=0,cursor="hand2",
                  activebackground="#2A2A2A",activeforeground=WHITE,
                  command=lambda p=pg:app.go(p)).pack(side="left",expand=True,fill="y")

def gbtn(parent,text,cmd,bg=GOLD,abg="#9A7D30"):
    tk.Button(parent,text=text,font=FB,bg=bg,fg=WHITE,bd=0,relief="flat",padx=8,pady=10,
              cursor="hand2",activebackground=abg,command=cmd).pack(pady=5,padx=20,fill="x")

def entry_field(parent,label,bg=BG,show=""):
    tk.Label(parent,text=label,font=("Helvetica",10,"bold"),bg=bg,fg=DARK,anchor="w").pack(fill="x",padx=24,pady=(6,0))
    v=tk.StringVar()
    tk.Entry(parent,textvariable=v,font=FS,bg=WHITE,bd=0,
             highlightthickness=1,highlightbackground=GOLD,show=show).pack(fill="x",padx=24,ipady=8,pady=(2,4))
    return v

def scrollable(parent):
    c=tk.Canvas(parent,bg=BG,bd=0,highlightthickness=0)
    sb=ttk.Scrollbar(parent,orient="vertical",command=c.yview)
    inner=tk.Frame(c,bg=BG)
    inner.bind("<Configure>",lambda e:c.configure(scrollregion=c.bbox("all")))
    c.create_window((0,0),window=inner,anchor="nw",width=400)
    c.configure(yscrollcommand=sb.set)
    c.pack(side="left",fill="both",expand=True); sb.pack(side="right",fill="y")
    return inner

# ── Pages ──────────────────────────────────────────────────────────────────────
class LoginPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); self.app=app
        tk.Label(self,text="LuxeVista",font=("Georgia",28,"bold"),bg=BG,fg=GOLD).pack(pady=(50,2))
        tk.Label(self,text="LUXURY RESORTS & HOTELS",font=FL,bg=BG,fg=MUTED).pack()
        tk.Label(self,text="Welcome Back!",font=FT,bg=BG,fg=DARK).pack(pady=(20,2))
        tk.Label(self,text="Login to continue your booking",font=FS,bg=BG,fg=MUTED).pack(pady=(0,18))
        self.em=entry_field(self,"Email Address")
        self.pw=entry_field(self,"Password",show="*")
        tk.Label(self,text="Forgot password?",font=FL,bg=BG,fg=CYAN,anchor="e").pack(fill="x",padx=24)
        tk.Frame(self,bg=BG,height=10).pack()
        gbtn(self,"  Log In",self.login,bg=CYAN,abg="#009DC4")
        tk.Label(self,text="or",font=FL,bg=BG,fg=MUTED).pack(pady=4)
        tk.Button(self,text="Create Account",font=FB,bg=WHITE,fg=GOLD,bd=1,relief="solid",
                  padx=8,pady=8,width=28,cursor="hand2",command=lambda:app.go("Register")).pack()

    def login(self):
        em,pw=self.em.get().strip(),self.pw.get().strip()
        if not em or not pw: messagebox.showwarning("Empty","Please fill in all fields."); return
        if em in users and users[em]["password"]==pw:
            logged_user.update(users[em]); logged_user["email"]=em; self.app.go("Home")
        else: messagebox.showerror("Failed","Invalid email or password.")

class RegisterPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); self.app=app
        tk.Label(self,text="LuxeVista",font=("Georgia",22,"bold"),bg=BG,fg=GOLD).pack(pady=(30,2))
        tk.Label(self,text="Create Your Account",font=FT,bg=BG,fg=DARK).pack(pady=(10,2))
        tk.Label(self,text="Fill in the details below to get started",font=FS,bg=BG,fg=MUTED).pack(pady=(0,10))
        self.nm=entry_field(self,"Full Name"); self.em=entry_field(self,"Email Address")
        self.ph=entry_field(self,"Phone Number (+63)")
        self.pw=entry_field(self,"Password",show="*"); self.p2=entry_field(self,"Confirm Password",show="*")
        tk.Label(self,text="At least 8 characters with letters and numbers",font=FL,bg=BG,fg=MUTED).pack()
        tk.Frame(self,bg=BG,height=8).pack()
        gbtn(self,"Create Account",self.register,bg=CYAN,abg="#009DC4")
        tk.Button(self,text="Already have an account? Log in",font=FL,bg=BG,fg=GOLD,bd=0,
                  cursor="hand2",command=lambda:app.go("Login")).pack(pady=6)

    def register(self):
        n,em,ph,pw,p2=self.nm.get().strip(),self.em.get().strip(),self.ph.get().strip(),self.pw.get(),self.p2.get()
        if not all([n,em,ph,pw,p2]): messagebox.showwarning("Missing","Please complete all fields."); return
        if pw!=p2: messagebox.showerror("Mismatch","Passwords do not match."); return
        if len(pw)<8: messagebox.showerror("Short","Password must be at least 8 characters."); return
        if em in users: messagebox.showerror("Exists","Email already registered."); return
        users[em]={"name":n,"phone":ph,"password":pw}
        messagebox.showinfo("Success!","Account created! Please log in."); self.app.go("Login")

class HomePage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); self.app=app; hdr(self,app)
        hero=tk.Frame(self,bg=DARK,height=160); hero.pack(fill="x"); hero.pack_propagate(False)
        tk.Label(hero,text="🏨",font=("Helvetica",70),bg=DARK).pack(expand=True)
        tk.Label(self,text="A new window into luxury",font=("Georgia",15,"bold"),bg=BG,fg=DARK).pack(pady=(12,0))
        tk.Label(self,text="Your Perfect Stay Starts Here",font=FS,bg=BG,fg=GOLD).pack()
        pill=tk.Frame(self,bg=WHITE,pady=10,padx=8); pill.pack(fill="x",padx=18,pady=10)
        pill.columnconfigure((0,1,2),weight=1)
        for i,(lbl,pg) in enumerate([("Check-in","Checkin"),("Check-out","Checkout"),("Guest","Reservations")]):
            tk.Button(pill,text=lbl,font=("Helvetica",10,"bold"),bg="#F0F0F0",fg=DARK,bd=0,
                      relief="flat",padx=6,pady=10,cursor="hand2",activebackground=CARD,
                      command=lambda p=pg:app.go(p)).grid(row=0,column=i,padx=4,sticky="ew")
        gbtn(self,"  BOOK NOW",lambda:app.go("Book"))
        cats=tk.Frame(self,bg=BG); cats.pack(fill="x",padx=18,pady=4)
        cats.columnconfigure((0,1),weight=1)
        for col,(lbl,pg) in enumerate([("Rooms","Rooms"),("Spa","Spa")]):
            tk.Button(cats,text=lbl,font=("Helvetica",13,"bold"),bg=CARD,fg=DARK,bd=0,
                      relief="flat",padx=10,pady=28,cursor="hand2",activebackground="#E8D9A0",
                      command=lambda p=pg:app.go(p)).grid(row=0,column=col,padx=6,sticky="nsew")
        nav(self,app)

class BookPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); self.app=app; hdr(self,app,"Book Now",back="Home")
        tk.Label(self,text="BOOK NOW",font=FT,bg=BG,fg=GOLD).pack(pady=(12,2))
        tk.Label(self,text="Your Perfect Stay Starts Here",font=FL,bg=BG,fg=MUTED).pack()
        card=tk.Frame(self,bg=WHITE,padx=16,pady=14); card.pack(fill="x",padx=18,pady=10)

        def re(par,lbl,val=""):
            tk.Label(par,text=lbl,font=("Helvetica",9,"bold"),bg=WHITE,fg=DARK,anchor="w").pack(fill="x")
            v=tk.StringVar(value=val)
            tk.Entry(par,textvariable=v,font=FL,bg="#F9F9F9",bd=0,
                     highlightthickness=1,highlightbackground=GOLD).pack(fill="x",ipady=6,pady=(2,8))
            return v

        self.gname=re(card,"Full Name",logged_user.get("name",""))
        self.gemail=re(card,"Email",logged_user.get("email",""))
        drow=tk.Frame(card,bg=WHITE); drow.pack(fill="x"); drow.columnconfigure((0,1),weight=1)
        lf=tk.Frame(drow,bg=WHITE); lf.grid(row=0,column=0,padx=(0,4),sticky="ew")
        rf=tk.Frame(drow,bg=WHITE); rf.grid(row=0,column=1,padx=(4,0),sticky="ew")
        today=datetime.date.today().strftime("%Y-%m-%d")
        tomorrow=(datetime.date.today()+datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        def se(par,lbl,val):
            tk.Label(par,text=lbl,font=FL,bg=WHITE,fg=DARK,anchor="w").pack(fill="x")
            v=tk.StringVar(value=val)
            tk.Entry(par,textvariable=v,font=FL,bg="#F9F9F9",bd=0,
                     highlightthickness=1,highlightbackground=GOLD).pack(fill="x",ipady=5,pady=(2,8))
            return v

        self.cin=se(lf,"Check-in (YYYY-MM-DD)",today); self.cout=se(rf,"Check-out (YYYY-MM-DD)",tomorrow)
        tk.Label(card,text="Number of Guests",font=("Helvetica",9,"bold"),bg=WHITE,fg=DARK,anchor="w").pack(fill="x")
        self.guests=ttk.Combobox(card,font=FL,state="readonly",
                                  values=["1 Adult","2 Adults","3 Adults","2 Adults + 1 Kid","Family (4+)"])
        self.guests.set("Select guests"); self.guests.pack(fill="x",ipady=3,pady=(2,8))
        tk.Label(card,text="Choose Your Room",font=("Helvetica",9,"bold"),bg=WHITE,fg=DARK,anchor="w").pack(fill="x")
        self.room=ttk.Combobox(card,font=FL,state="readonly",values=ROOMS)
        self.room.set("Select room type"); self.room.pack(fill="x",ipady=3,pady=(2,4))
        gbtn(self,"BOOK NOW",self.do_book); nav(self,app)

    def do_book(self):
        name,email,cin,cout=self.gname.get().strip(),self.gemail.get().strip(),self.cin.get().strip(),self.cout.get().strip()
        guests,room=self.guests.get(),self.room.get()
        if not all([name,email,cin,cout]) or "Select" in guests or "Select" in room:
            messagebox.showwarning("Incomplete","Please fill in all fields."); return
        try:
            d1=datetime.date.fromisoformat(cin); d2=datetime.date.fromisoformat(cout)
            nights=(d2-d1).days
            if nights<=0: raise ValueError
        except ValueError: messagebox.showerror("Date Error","Check-out must be after Check-in."); return
        rate=ROOM_PRICES.get(room,6000); sub=rate*nights; tax=int(sub*0.20); total=sub+tax
        b={"id":f"LV{1000+len(bookings)+1}","name":name,"email":email,"cin":cin,"cout":cout,
           "nights":nights,"guests":guests,"room":room,"rate":rate,"sub":sub,"tax":tax,
           "total":total,"status":"Confirmed","booked_on":str(datetime.date.today())}
        bookings.append(b)
        messagebox.showinfo("Booking Confirmed!",
            f"Booking ID  : {b['id']}\nRoom        : {room}\nCheck-in    : {cin}\n"
            f"Check-out   : {cout}\nNights      : {nights}\nGuests      : {guests}\n"
            f"Room Rate   : P{sub:,}\nTax & Fees  : P{tax:,}\nTOTAL PAID  : P{total:,}")
        self.app.go("Home")

class ReservationsPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); hdr(self,app,"Reservations",back="Home")
        tk.Label(self,text="My Reservations",font=FH,bg=BG,fg=DARK).pack(pady=12)
        inner=scrollable(self)
        my=[b for b in bookings if b.get("email")==logged_user.get("email","")]
        if not my:
            tk.Label(inner,text="No reservations yet.\nBook a room to get started!",
                     font=FS,bg=BG,fg=MUTED,justify="center").pack(pady=50)
        else:
            for b in reversed(my):
                card=tk.Frame(inner,bg=WHITE,pady=12,padx=16); card.pack(fill="x",padx=12,pady=6)
                tk.Label(card,text=f"  {b['room']}",font=("Helvetica",12,"bold"),bg=WHITE,fg=DARK).pack(anchor="w")
                tk.Label(card,text=f"  {b['cin']}  to  {b['cout']}  ({b['nights']} nights)",font=FL,bg=WHITE,fg=MUTED).pack(anchor="w")
                tk.Label(card,text=f"  Guests: {b['guests']}   ID: {b['id']}",font=FL,bg=WHITE,fg=MUTED).pack(anchor="w")
                tk.Label(card,text=f"  {b['status']}   P{b['total']:,}",font=("Helvetica",10,"bold"),
                         bg=WHITE,fg=GREEN if b["status"]=="Confirmed" else RED).pack(anchor="w",pady=(4,0))
        nav(self,app)

class RoomsPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); hdr(self,app,"Rooms",back="Home")
        tk.Label(self,text="Room Rates",font=("Georgia",17,"bold"),bg=BG,fg=GOLD).pack(pady=(10,2))
        tk.Label(self,text="Stay in Luxury, Wake up to the View",font=FL,bg=BG,fg=MUTED).pack()
        inner=scrollable(self)
        for name,beds,occ,price in [
            ("Twin Room","2 Single Beds","Max 2 Adults",1500),
            ("Queen Room","1 Queen Bed + Balcony","Max 2 Adults + 1 Kid",2500),
            ("Triple Room","1 Queen + 1 Single","Max 3 Adults",3500),
            ("Triple Room XL","3 Single + 1 Queen","Max 3 Adults + 1 Kid",4000),
            ("Deluxe Ocean View","1 King Bed, Ocean View","Max 2 Adults",4500),
            ("Family Room","2 Queen + 1 Single","Max 6 Adults + 2 Kids",6000)]:
            card=tk.Frame(inner,bg=WHITE,pady=10,padx=14); card.pack(fill="x",padx=10,pady=5)
            top=tk.Frame(card,bg=WHITE); top.pack(fill="x")
            tk.Label(top,text=f"  {name}",font=("Helvetica",12,"bold"),bg=WHITE,fg=DARK).pack(side="left")
            tk.Label(top,text=f"P{price:,}/night",font=("Helvetica",11,"bold"),bg=WHITE,fg=GOLD).pack(side="right")
            tk.Label(card,text=f"   {beds}  |  {occ}",font=FL,bg=WHITE,fg=MUTED).pack(anchor="w")
            tk.Label(card,text="   Free WiFi  |  Air-Con  |  Mini Fridge  |  Toiletries",
                     font=("Helvetica",8),bg=WHITE,fg=MUTED).pack(anchor="w")
            tk.Button(card,text="Book This Room",font=FL,bg=GOLD,fg=WHITE,bd=0,cursor="hand2",
                      padx=8,pady=4,command=lambda p=name:app.go("Book")).pack(anchor="e",pady=(4,0))
        nav(self,app)

class SpaPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); hdr(self,app,"Spa",back="Home")
        tk.Label(self,text="Spa & Wellness",font=("Georgia",17,"bold"),bg=BG,fg=DARK).pack(pady=(12,2))
        tk.Label(self,text="Relax. Rejuvenate. Restore.",font=FL,bg=BG,fg=MUTED).pack()
        for name,desc,price in [
            ("Wellness Massage","Relieve stress and improve circulation.","P1,500session"),
            ("Signature Facial","Deep cleanse and skin revitalization.","P1,800/session"),
            ("Aromatherapy Massage","Essential oils for mind and body balance.","P2,000/session"),
            ("Hot Stone Therapy","Relaxes muscles and enhances relaxation.","P2,300/session"),
            ("Sauna and Steam","Detoxify and improve blood circulation.","P1,000/session")]:
            card=tk.Frame(self,bg=WHITE,pady=12,padx=16); card.pack(fill="x",padx=18,pady=5)
            top=tk.Frame(card,bg=WHITE); top.pack(fill="x")
            tk.Label(top,text=name,font=("Helvetica",11,"bold"),bg=WHITE,fg=DARK).pack(side="left")
            tk.Label(top,text=price,font=("Helvetica",10,"bold"),bg=WHITE,fg=GOLD).pack(side="right")
            tk.Label(card,text=desc,font=FL,bg=WHITE,fg=MUTED,anchor="w").pack(fill="x")
        nav(self,app)

def _checkin_checkout_page(cls_self,parent,app,title,time_str,steps,note_title,note_body):
    """Shared builder for CheckinPage and CheckoutPage."""
    hdr(cls_self,app,title,back="Home")
    tk.Label(cls_self,text=f"{title} Details",font=FH,bg=BG,fg=DARK).pack(pady=14)
    my=[b for b in bookings if b.get("email")==logged_user.get("email","")]
    if not my:
        tk.Label(cls_self,text="No active bookings found.\nPlease make a reservation first.",
                 font=FS,bg=BG,fg=MUTED,justify="center").pack(pady=30)
        gbtn(cls_self,"Book Now",lambda:app.go("Book"))
    else:
        b=my[-1]
        info=tk.Frame(cls_self,bg=WHITE,padx=20,pady=16); info.pack(fill="x",padx=20,pady=8)
        tk.Label(info,text=f"{title} Date & Time",font=("Helvetica",11,"bold"),bg=WHITE,fg=GOLD).pack(anchor="w")
        tk.Label(info,text=f"{b['cin'] if 'in' in title.lower() else b['cout']}  at  {time_str}",
                 font=("Georgia",13,"bold"),bg=WHITE,fg=DARK).pack(anchor="w",pady=(2,10))
        for step_title,step_desc in steps:
            row=tk.Frame(info,bg=WHITE); row.pack(fill="x",pady=4)
            tk.Label(row,text=step_title,font=("Helvetica",10,"bold"),bg=WHITE,fg=DARK).pack(anchor="w")
            tk.Label(row,text=step_desc,font=FL,bg=WHITE,fg=MUTED).pack(anchor="w")
        note=tk.Frame(cls_self,bg=CARD,padx=14,pady=10); note.pack(fill="x",padx=20,pady=6)
        tk.Label(note,text=note_title,font=("Helvetica",10,"bold"),bg=CARD,fg=DARK).pack(anchor="w")
        tk.Label(note,text=note_body,font=FL,bg=CARD,fg=MUTED).pack(anchor="w")
    nav(cls_self,app)

class CheckinPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG)
        _checkin_checkout_page(self,parent,app,"Check-in","2:00 PM",[
            ("Arrival & Welcome","Our staff will greet and assist you."),
            ("ID Verification","Please present a valid government ID."),
            ("Payment Confirmation","We will verify your reservation details."),
            ("Room Key","You will receive your room key and WiFi access."),
            ("Enjoy Your Stay!","Your perfect luxury stay begins here.")],
            "Need early check-in?","Contact our front desk for availability.")

class CheckoutPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG)
        _checkin_checkout_page(self,parent,app,"Check-out","12:00 PM",[
            ("Express Check-out","Quick and seamless check-out process."),
            ("Bill Settlement","We will review charges and process payment."),
            ("Room Inspection","A quick room check ensures everything is in order."),
            ("Thank You!","Thank you for staying. We hope to see you again!")],
            "Need late check-out?","Contact our front desk for availability.")

class RatingsPage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); self.app=app; self.star=0
        hdr(self,app,"Ratings",back="Home")
        tk.Label(self,text="Rate Your Stay",font=FH,bg=BG,fg=DARK).pack(pady=(14,2))
        tk.Label(self,text="Your feedback helps us improve!",font=FL,bg=BG,fg=MUTED).pack()
        sf=tk.Frame(self,bg=BG); sf.pack(pady=12); self.slbls=[]
        for i in range(1,6):
            b=tk.Button(sf,text="*",font=("Helvetica",28),bg=BG,fg=GOLD,bd=0,cursor="hand2",
                        activebackground=BG,command=lambda s=i:self.set_star(s))
            b.pack(side="left",padx=2); self.slbls.append(b)
        tk.Label(self,text="Write a Review",font=("Helvetica",10,"bold"),bg=BG,fg=DARK,anchor="w").pack(fill="x",padx=24)
        self.txt=tk.Text(self,font=FS,height=4,bd=0,highlightthickness=1,highlightbackground=GOLD,wrap="word")
        self.txt.pack(fill="x",padx=24,pady=(4,8))
        gbtn(self,"Submit Rating",self.submit)
        tk.Label(self,text="Guest Reviews",font=("Helvetica",10,"bold"),bg=BG,fg=GOLD).pack(pady=(10,4))
        self.rf=tk.Frame(self,bg=BG); self.rf.pack(fill="both",expand=True,padx=18)
        self.show_reviews(); nav(self,app)

    def set_star(self,s):
        self.star=s
        for i,b in enumerate(self.slbls): b.config(text="*" if i<s else "-",fg=GOLD if i<s else MUTED)

    def submit(self):
        if self.star==0: messagebox.showwarning("No Rating","Please select a star rating first."); return
        rev=self.txt.get("1.0","end").strip()
        ratings_db.append({"user":logged_user.get("name","Guest"),"stars":self.star,
                           "review":rev if rev else "No comment.","date":str(datetime.date.today())})
        messagebox.showinfo("Thank you!",f"You rated us {self.star} star(s). We appreciate it!")
        self.set_star(0); self.txt.delete("1.0","end"); self.show_reviews()

    def show_reviews(self):
        for w in self.rf.winfo_children(): w.destroy()
        if not ratings_db:
            tk.Label(self.rf,text="No reviews yet. Be the first!",font=FL,bg=BG,fg=MUTED).pack(pady=10); return
        for r in reversed(ratings_db[-5:]):
            card=tk.Frame(self.rf,bg=WHITE,pady=8,padx=12); card.pack(fill="x",pady=4)
            top=tk.Frame(card,bg=WHITE); top.pack(fill="x")
            tk.Label(top,text=r["user"],font=("Helvetica",10,"bold"),bg=WHITE,fg=DARK).pack(side="left")
            tk.Label(top,text=("*"*r["stars"])+("-"*(5-r["stars"])),
                     font=("Helvetica",13,"bold"),bg=WHITE,fg=GOLD).pack(side="right")
            tk.Label(card,text=r["review"],font=FL,bg=WHITE,fg=MUTED,
                     wraplength=310,justify="left",anchor="w").pack(fill="x")
            tk.Label(card,text=r["date"],font=("Helvetica",7),bg=WHITE,fg="#BBBBBB").pack(anchor="e")

class ProfilePage(tk.Frame):
    def __init__(self,parent,app,**kw):
        super().__init__(parent,bg=BG); self.app=app; hdr(self,app,"Profile",back="Home")
        av=tk.Frame(self,bg=DARK,width=72,height=72); av.pack(pady=(20,8)); av.pack_propagate(False)
        tk.Label(av,text="U",font=("Georgia",30,"bold"),bg=DARK,fg=GOLD).pack(expand=True)
        name,email,phone=logged_user.get("name","Guest"),logged_user.get("email","--"),logged_user.get("phone","--")
        tk.Label(self,text=name,font=("Georgia",15,"bold"),bg=BG,fg=DARK).pack()
        tk.Label(self,text=email,font=FL,bg=BG,fg=MUTED).pack(pady=(0,12))
        card=tk.Frame(self,bg=WHITE,pady=16,padx=20); card.pack(fill="x",padx=20)
        tk.Label(card,text="Personal Details",font=("Helvetica",12,"bold"),bg=WHITE,fg=GOLD).pack(anchor="w")
        tk.Frame(card,bg=GOLD,height=1).pack(fill="x",pady=6)
        for lbl,val in [("Full Name",name),("Email",email),("Phone",phone)]:
            row=tk.Frame(card,bg=WHITE); row.pack(fill="x",pady=4)
            tk.Label(row,text=lbl,font=FL,bg=WHITE,fg=MUTED,width=14,anchor="w").pack(side="left")
            tk.Label(row,text=val,font=("Helvetica",10,"bold"),bg=WHITE,fg=DARK).pack(side="left")
        tk.Frame(self,bg=BG,height=16).pack()
        tk.Button(self,text="Log Out",font=FB,bg=RED,fg=WHITE,bd=0,padx=20,pady=10,width=28,
                  cursor="hand2",activebackground="#C0392B",command=self.logout).pack()
        nav(self,app)

    def logout(self):
        if messagebox.askyesno("Log Out","Are you sure you want to log out?"):
            logged_user.clear(); self.app.go("Login")

# ── Main ───────────────────────────────────────────────────────────────────────
if __name__=="__main__":
    users["demo@luxevista.com"]={"name":"Juan Dela Cruz","phone":"+63 962 553 1020","password":"demo1234"}
    App().mainloop()
