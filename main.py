from tkinter import *
from bs4 import *
import requests

# COLORS
WHITE = '#FFFFFF'
BLACK = '#000000'
BLUE = '#0093FF'
GREY_0 = '#D6D6D6'
GREY_1 = '#C6C6C6'


class App:
    def __init__(self):
        self.root = None
        self.width = 500
        self.height = 500
        self.my_canvas = Canvas
        self.my_frame = Frame

        self.wrapper1 = LabelFrame
        self.wrapper2 = LabelFrame

        self.y_scroll = Scrollbar
        self.x_scroll = Scrollbar

        self.url = ""
        self.info_list = []
        self.page_title = ""
        self.div = None
        self.div_tag = None
        self.p_tag = None
        self.a_tag = None
        self.span_tag = None

        self.page_title_label = Label
        self.div_label = Label
        self.p_label = Label
        self.a_label = Label
        self.span_label = Label

        self.div_label_val = Label
        self.p_label_val = Label
        self.a_label_val = Label
        self.span_label_val = Label

        self.url_entry = Entry
        self.get_url_but = Button
        self.show_info = Button

    def run(self):
        self.root = Tk()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)
        self.root.title("Webpage Analyzer")
        self.root.configure(bg=GREY_1)

        self.wrapper1 = LabelFrame(self.root, bg=GREY_0, borderwidth=0)
        self.wrapper2 = LabelFrame(self.root, bg=GREY_0, borderwidth=0)

        self.url_entry = Entry(self.wrapper1, width=50,
                               bg=WHITE, fg=BLACK, borderwidth=0)
        self.url_entry.insert(INSERT, " Enter URL")
        self.get_url_but = Button(self.wrapper1, text="Get Info", command=self.get_url,
                                  bg=BLUE, fg=WHITE, borderwidth=0)
        self.show_info = Button(self.wrapper1, text="Show Info", command=self.print_info,
                                bg=BLUE, fg=WHITE, borderwidth=0)

        self.url_entry.place(x=10, y=10, width=350, height=25)
        self.get_url_but.place(x=380, y=10, width=70, height=25)
        self.show_info.place(x=380, y=50, width=70, height=25)

        self.wrapper1.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        self.wrapper2.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        self.root.mainloop()

# ----------------------------------------------------------------------------------------------------------------------

    def scroll(self):
        self.my_canvas = Canvas(self.wrapper2, width=0, height=0, bg=GREY_0)
        self.my_canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        self.y_scroll = Scrollbar(self.wrapper2, orient=VERTICAL, command=self.my_canvas.yview)
        self.y_scroll.pack(side=RIGHT, fill=Y)
        self.x_scroll = Scrollbar(self.root, orient=HORIZONTAL, command=self.my_canvas.xview)
        self.x_scroll.pack(side=BOTTOM, fill=X)

        self.my_canvas.configure(xscrollcommand=self.x_scroll.set, yscrollcommand=self.y_scroll.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox('all')))

        self.my_frame = Frame(self.my_canvas, bg=GREY_0)
        self.my_canvas.create_window((0, 0), window=self.my_frame)

# ----------------------------------------------------------------------------------------------------------------------

    def get_url(self):
        try:
            self.info_list = []
            a = self.wrapper1.winfo_children()
            for i in range(3, 20):
                a[i].destroy()

        except:
            print("..")

        try:
            self.info_list = []
            for i in self.wrapper2.winfo_children():
                i.destroy()
            a = self.root.winfo_children()
            a[2].destroy()

        except:
            print("..")

        self.url = ""
        self.info_list = []
        self.url = self.url_entry.get()
        self.url.replace(" ", "")

        try:
            self.decode_url()
            self.get_general_info()
            Label(self.wrapper1, text="Got Information", bg=GREY_0).place(x=10, y=40)
        except:
            Label(self.wrapper1, text="Invalid Url", bg=GREY_0).place(x=10, y=40)

    def decode_url(self):
        response = requests.get(self.url)
        page = response.content
        soup = BeautifulSoup(page, "html.parser")
        self.page_title = soup.title.string
        self.div = soup.find('div')
        self.div_tag = soup.find_all('div')
        self.p_tag = self.div.find_all('p')
        self.a_tag = self.div.find_all('a')
        self.span_tag = self.div.find_all('span')

        if len(self.p_tag) == 0:
            for i in self.div_tag:
                self.info_list.append(i.get_text())
            for i in self.span_tag:
                self.info_list.append(i.get_text())
        else:
            for i in self.p_tag:
                self.info_list.append(i.get_text())

    def get_general_info(self):

        div_num = len(self.div)
        p_num = len(self.p_tag)
        a_num = len(self.a_tag)

        self.page_title_label = Label(self.wrapper1, text=self.page_title, bg=GREY_0, fg=BLACK)
        self.div_label = Label(self.wrapper1, text="Number of <div> tags", bg=GREY_0, fg=BLACK)
        self.p_label = Label(self.wrapper1, text="Number of <p> tags", bg=GREY_0, fg=BLACK)
        self.a_label = Label(self.wrapper1, text="Number of <a> tags", bg=GREY_0, fg=BLACK)
        self.span_label = Label(self.wrapper1, text="Number of <span> tags", bg=GREY_0, fg=BLACK)

        self.div_label_val = Label(self.wrapper1, text=str(div_num), bg=WHITE, fg=BLACK)
        self.p_label_val = Label(self.wrapper1, text=str(p_num), bg=WHITE, fg=BLACK)
        self.a_label_val = Label(self.wrapper1, text=str(a_num), bg=WHITE, fg=BLACK)
        self.span_label_val = Label(self.wrapper1, text=str(a_num), bg=WHITE, fg=BLACK)

        self.page_title_label.place(x=self.width/2 - (len(self.page_title)*6)/2, y=80)
        self.div_label.place(x=10, y=110)
        self.p_label.place(x=10, y=130)
        self.a_label.place(x=10, y=150)
        self.span_label.place(x=10, y=170)

        self.div_label_val.place(x=150, y=110, width=25)
        self.p_label_val.place(x=150, y=130, width=25)
        self.a_label_val.place(x=150, y=150, width=25)
        self.span_label_val.place(x=150, y=170, width=25)

    def print_info(self):

        if len(self.root.winfo_children()) >= 3:
            a = self.root.winfo_children()
            a[2].destroy()

        if len(self.wrapper2.winfo_children()) > 0:
            for i in self.wrapper2.winfo_children():
                i.destroy()

        if len(self.info_list) != 0:
            self.scroll()

        for i in self.info_list:
            Label(self.my_frame, text=i, bg=GREY_0).pack()


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    App().run()


# --- Example Website ---
# https://blog.hubspot.com/blog/tabid/6307/bid/34006/15-examples-of-brilliant-homepage-design.aspx
