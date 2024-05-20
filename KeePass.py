import tkinter as tk
import chiff
from pyperclip import copy

class Interface:
    def __init__(self) -> None:
        self.win = tk.Tk()
        self.keypass = chiff.KeyPass()
        self.style()
        self.win.title('KeyPass')
        self.win.geometry('400x600')
        self.setupButtom()
        self.setupResearch()
        self.setupPage()
        self.frameSite = tk.Frame(self.win, bg=self.styleLibrary[2])
        self.frameSite.pack(expand=True, fill='both', side='top')
        self.element = {}
        self.pagePass = 0
        self.win.after(200, self.masterPasswordSetup)
        self.win.mainloop()
    
    def style(self):
        self.styleLibrary = ['#565b5e', '#343638', '#242424', '#2b2b2b', 'white', '#1f6aa5', '#173f5f']
        self.win.config(bg=self.styleLibrary[2])
    
    def setupResearch(self) -> None:
        cadre = tk.Frame(self.win, highlightbackground = self.styleLibrary[0], highlightthickness=2, bg=self.styleLibrary[1])
        cadre.pack(padx=12, pady=(0, 3), fill='x', side='top')
        self.research = tk.Entry(cadre, relief='flat', bg=self.styleLibrary[1], fg=self.styleLibrary[4], font=('Helvetica', 9), insertbackground=self.styleLibrary[4])
        self.research.pack(fill='x', padx=2)
        self.research.insert(0, 'Rechercher...')
        self.research.bind('<FocusIn>', self.researchOnFocus)
        self.research.bind('<FocusOut>', self.researchOffFocus)
        self.research.bind("<KeyRelease>", self.researchBar)
    
    def setupButtom(self) -> None:
        frame = tk.Frame(self.win, bg=self.styleLibrary[2])
        frame.pack(side='top', fill='x')
        tk.Button(frame, text="Nouveau", command=self.new, font=('Helvetica', 12), cursor="hand2", fg=self.styleLibrary[4], bg=self.styleLibrary[5], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4]).pack(side='left', expand=True, fill='x', padx=5, pady=5)
        tk.Button(frame, text="Vérouillage", command=self.lock, font=('Helvetica', 12), cursor="hand2", fg=self.styleLibrary[4], bg=self.styleLibrary[5], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4]).pack(side='left', expand=True, fill='x', padx=5, pady=5)

    def setupPage(self) -> None:
        cadre = tk.Frame(self.win, bg=self.styleLibrary[3], highlightbackground = self.styleLibrary[0], highlightthickness=1)
        cadre.pack(padx=5, pady=5, fill='x', side='bottom')
        self.win.bind("<MouseWheel>", self.scroll)
        tk.Button(cadre, text="<<", command=self.previousPage, cursor="hand2", bg=self.styleLibrary[5], fg=self.styleLibrary[4], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4]).pack(side='left', padx=5, pady=5, fill='x', expand=True)
        self.page = tk.Label(cadre, text="   Page 1   ", anchor='center', font=('Helvetica', 11), bg=self.styleLibrary[3], fg=self.styleLibrary[4])
        self.page.pack(side='left', padx=5, pady=0)
        tk.Button(cadre, text=">>", command=self.nextPage, cursor="hand2", bg=self.styleLibrary[5], fg=self.styleLibrary[4], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4]).pack(side='right', padx=5, pady=5, fill='x', expand=True)
    
    def submitPassword(self, event: tk.Event | None = None) -> None:
        if not self.antiBrutForce:
            try:
                self.keypass.openKey(self.password1.get(), self.password2.get())
                self.setupPass.destroy()
                if not (self.research.get() == '' or self.research.get() == 'Rechercher...'):
                    self.researchBar()
                else:
                    self.printElements()
            except UnicodeDecodeError:
                self.badPass.config(text="Authenticating...") 
                self.antiBrutForce = True
                self.setupPass.after(2000, self.waitSpam)
    
    def waitSpam(self) -> None:
        self.badPass.config(text="Mauvais mot de passe") 
        self.antiBrutForce = False

    def scroll(self, event: tk.Event) -> None:
        if event.delta > 0:
            self.previousPage()
        else:
            self.nextPage()

    def researchOnFocus(self, event: tk.Event) -> None:
        if self.research.get() == 'Rechercher...':
            self.research.delete(0, "end")
            self.research.insert(0, '')

    def researchOffFocus(self, event: tk.Event) -> None:
        if self.research.get() == '':
            self.research.delete(0, "end")
            self.research.insert(0, 'Rechercher...')

    def masterPasswordSetup(self) -> None:
        if not hasattr(self, 'setupPass') or not self.setupPass.winfo_exists():
            self.setupPass = tk.Toplevel(self.win)
            self.setupPass.config(bg=self.styleLibrary[2])
            self.setupPass.title('Password')
            self.setupPass.transient(self.win)
            self.setupPass.geometry(f'200x175+{self.win.winfo_rootx() + (self.win.winfo_width() - 240) // 2}+{self.win.winfo_rooty() + (self.win.winfo_height() - 150) // 2 - 100}')
            self.antiBrutForce = False
            self.badPass = tk.Label(self.setupPass, fg='red', bg=self.styleLibrary[2])
            self.badPass.pack()
            tk.Label(self.setupPass, text="Mot de passe 1 :", fg=self.styleLibrary[4], bg=self.styleLibrary[2]).pack()
            self.password1 = tk.Entry(self.setupPass, show="*", highlightbackground = self.styleLibrary[0], highlightthickness=2, bg=self.styleLibrary[1], fg=self.styleLibrary[4], relief='flat', insertbackground=self.styleLibrary[4])
            self.password1.pack()
            self.password1.focus()
            tk.Label(self.setupPass, text="Mot de passe 2 :", fg=self.styleLibrary[4], bg=self.styleLibrary[2]).pack(pady=(5, 0))
            self.password2 = tk.Entry(self.setupPass, show="*", highlightbackground = self.styleLibrary[0], highlightthickness=2, bg=self.styleLibrary[1], fg=self.styleLibrary[4], relief='flat', insertbackground=self.styleLibrary[4])
            self.password2.pack()
            self.password1.bind('<Return>', lambda event: self.submitPassword())
            self.password2.bind('<Return>', lambda event: self.submitPassword())
            tk.Button(self.setupPass, text="Confirmer", command=self.submitPassword, cursor="hand2", bg=self.styleLibrary[5], fg=self.styleLibrary[4], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4], width=12).pack(padx=5, pady=15)
            self.setupPass.mainloop()
    
    def truncateText(self, label: tk.Label) -> None:
        text = label.cget("text")
        while label.winfo_reqwidth() > 250:
            text = text[:-1]
            label.config(text=text + "...")

    def printElements(self) -> None:
        self.size = self.win.winfo_height()
        self.element = {}
        site = list(self.keypass.key_list.keys())
        for j in site:
            self.element[self.keypass.aes.decrypt(self.keypass.aes.keys[1], j)] = j
        site = [self.element[i] for i in sorted(list(self.element.keys()))]
        n = int((self.win.winfo_height() - 120 ) / 38.5)
        for i in site[self.pagePass*n:self.pagePass*n+n]:
            self.newElement(i)
    
    def newElement(self, site: str) -> None:
        element = self.keypass.aes.decrypt(self.keypass.aes.keys[1], site)
        cadre = tk.Frame(self.frameSite, highlightbackground = self.styleLibrary[0], highlightthickness=2, bg=self.styleLibrary[1])
        cadre.pack(padx=5, pady=2, fill='x')
        label = tk.Label(cadre, text=element, anchor='w', fg=self.styleLibrary[4], bg=self.styleLibrary[1], cursor="hand2")
        label.pack(side='left', padx=5, pady=5)
        self.truncateText(label)
        cadre.bind('<Button-1>', lambda event: self.copySite(event, element))
        label.bind('<Button-1>', lambda event: self.copySite(event, element))
        buttom = tk.Button(cadre, text='Del', cursor="hand2", bg=self.styleLibrary[5], fg=self.styleLibrary[4], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4], width=4)
        buttom.pack(side='right', padx=2)
        buttom.bind('<Button-1>', lambda event: self.delPass(event, site))
        tk.Button(cadre, text='Pass', command=lambda site=site: self.copyPass(site), cursor="hand2", bg=self.styleLibrary[5], fg=self.styleLibrary[4], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4], width=4).pack(side='right', padx=2)
        tk.Button(cadre, text='User', command=lambda site=site: self.copyUser(site), cursor="hand2", bg=self.styleLibrary[5], fg=self.styleLibrary[4], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4], width=4).pack(side='right', padx=2)
    
    def copySite(self, event: tk.Event, site: str):
        copy(site)

    def delPass(self, event: tk.Event,  site: str) -> None:
        if event.widget.cget('background') == 'red':
            self.keypass.key_list.pop(site)
            self.keypass.saveKey()
            self.refreshPass()
        else:
            event.widget.config(bg='red')
    
    def resize(self):
        if self.size != self.win.winfo_height():
            self.size = self.win.winfo_height()
            self.refreshPass()
        self.resizeAfter = self.win.after(500, self.resize)

    def refreshPass(self, event: tk.Event | None = None) -> None:
        for i in self.frameSite.winfo_children():
            i.destroy()
        self.printElements()

    def copyUser(self, site: str) -> None:
        copy(self.keypass.aes.decrypt(self.keypass.aes.deriveKey(self.keypass.aes.keys[2], self.keypass.key_list[site]['Index'])[0], self.keypass.key_list[site]['Username']))

    def copyPass(self, site: str) -> None:
        temp = self.keypass.aes.decrypt(self.keypass.aes.deriveKey(self.keypass.aes.keys[2], self.keypass.key_list[site]['Index'])[1], self.keypass.key_list[site]['Password'])
        copy(temp[:2] + self.keypass.v2[int(self.keypass.key_list[site]['Index'])*5%(len(self.keypass.v2)-len(self.keypass.v2)%5):(int(self.keypass.key_list[site]['Index']))*5%(len(self.keypass.v2)-len(self.keypass.v2)%5)+5].hex()[:5] + temp[2:])

    def submitNew(self, event: tk.Event | None = None) -> None:
        try: 
            if self.passWinNewSite.get() != '':
                self.keypass.newKey(self.passWinNewSite.get(), self.passWinNewUser.get(), self.passWinNewPass.get())
                self.refreshPass()
                self.passWinNew.destroy()
            else:
                self.passWinNewMessage.config(text="Remplir la case site")
        except AttributeError:
            self.passWinNewMessage.config(text="Déverrouiller le KeyPass avant de continuer")

    def new(self) -> None:
        if not hasattr(self, 'passWinNew') or not self.passWinNew.winfo_exists():
            self.passWinNew = tk.Toplevel(self.win)
            self.passWinNew.transient(self.win)
            self.passWinNew.config(bg=self.styleLibrary[2])
            self.passWinNew.geometry('250x220')
            self.passWinNewMessage = tk.Label(self.passWinNew, fg='red', bg=self.styleLibrary[2])
            self.passWinNewMessage.pack()
            tk.Label(self.passWinNew, text="Site :", fg=self.styleLibrary[4], bg=self.styleLibrary[2]).pack()
            self.passWinNewSite = tk.Entry(self.passWinNew, width=30, highlightbackground = self.styleLibrary[0], highlightthickness=2, bg=self.styleLibrary[1], fg=self.styleLibrary[4], relief='flat', insertbackground=self.styleLibrary[4])
            self.passWinNewSite.pack()
            self.passWinNewSite.focus()
            tk.Label(self.passWinNew, text="Nom d'utilisateur :", fg=self.styleLibrary[4], bg=self.styleLibrary[2]).pack(pady=(5, 0))
            self.passWinNewUser = tk.Entry(self.passWinNew, width=30, highlightbackground = self.styleLibrary[0], highlightthickness=2, bg=self.styleLibrary[1], fg=self.styleLibrary[4], relief='flat', insertbackground=self.styleLibrary[4])
            self.passWinNewUser.pack()
            tk.Label(self.passWinNew, text="Mot de passe :", fg=self.styleLibrary[4], bg=self.styleLibrary[2]).pack(pady=(5, 0))
            self.passWinNewPass = tk.Entry(self.passWinNew, width=30, highlightbackground = self.styleLibrary[0], highlightthickness=2, bg=self.styleLibrary[1], fg=self.styleLibrary[4], relief='flat', insertbackground=self.styleLibrary[4])
            self.passWinNewPass.insert(0, self.keypass.genPass())
            self.passWinNewPass.pack()
            self.passWinNewSite.bind('<Return>', lambda event: self.submitNew())
            self.passWinNewUser.bind('<Return>', lambda event: self.submitNew())
            self.passWinNewPass.bind('<Return>', lambda event: self.submitNew())
            tk.Button(self.passWinNew, text="Confirmer", command=self.submitNew, cursor="hand2", bg=self.styleLibrary[5], fg=self.styleLibrary[4], relief='flat', activebackground=self.styleLibrary[6], activeforeground=self.styleLibrary[4], width=12).pack(padx=5, pady=15)
            self.passWinNew.mainloop()
    
    def researchBar(self, event: tk.Event | None = None) -> None:
        self.page.config(text="   Page 1   ")
        self.pagePass = 0
        research = self.research.get()
        if not (research == '' or research == 'Rechercher...'):
            try:
                for i in self.frameSite.winfo_children():
                    i.destroy()
                n = int((self.win.winfo_height() - 120 ) / 38.5)
                for j in sorted([i for i in self.element.keys() if research in i])[self.pagePass*n:self.pagePass*n+n]:
                    self.newElement(self.element[j])
            except AttributeError: 
                pass
        else:
            self.refreshPass()
    
    def nextPage(self) -> None:
        if ((self.pagePass + 1) * self.frameSite.winfo_height() / 40 < len(self.keypass.key_list.keys())) and (self.research.get() == '' or self.research.get() == 'Rechercher...'):
            self.pagePass += 1
            self.page.config(text="   Page " + str(self.pagePass + 1) + "   ")
        self.refreshPass()

    def previousPage(self) -> None:
        if self.pagePass > 0 and (self.research.get() == '' or self.research.get() == 'Rechercher...'):
            self.pagePass -= 1
            self.page.config(text="   Page " + str(self.pagePass + 1) + "   ")
        self.refreshPass()

    def lock(self) -> None:
        try:
            self.keypass.key_list = {}
            del self.keypass.aes.keys, self.keypass.aes, self.keypass.v2
            for i in self.frameSite.winfo_children():
                i.destroy()
            self.masterPasswordSetup()
        except AttributeError:
            self.masterPasswordSetup()

a = Interface()