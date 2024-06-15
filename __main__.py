import customtkinter
from PyPDF2 import PdfReader
import os
from tkinter import filedialog
from threading import Thread

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.path = None
        self.pdf_dict = None
        self.pdf_files = None
        self.valid_pdf_name = None

        # configure window
        self.title("PDFInsight - Search Data Inside PDFs")
        self.geometry(f"{950}x{550}")

        # configure grid layout (3x3)
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Author", font=customtkinter.CTkFont(size=24, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.name_label = customtkinter.CTkLabel(self.sidebar_frame, text="Anurag Tiwari\n+918381990926", font=customtkinter.CTkFont("Times New ROman",size=18))
        self.name_label.grid(row=1, column=0, padx=20)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Theme", anchor="w", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.appearance_mode_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light", "System"],command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=8, column=0, padx=20,pady=(5, 30))

        # create mid frame with widgets
        self.mid_frame = customtkinter.CTkFrame(self)
        self.mid_frame.grid(row=0, column=1, rowspan = 3, padx=(20, 20), sticky="nsew")

        self.folder_Textbox = customtkinter.CTkTextbox(self.mid_frame, height=5, width=500, font=customtkinter.CTkFont("Arial",size=11))
        self.folder_Textbox.grid(row=0, column=1, padx=20,  pady=(20,0), sticky="nsew")

        self.filename_Textbox = customtkinter.CTkTextbox(self.mid_frame, height=400, font=customtkinter.CTkFont("Arial",size=12))
        self.filename_Textbox.grid(row=1, column=1, padx=20,  pady=(21,0), sticky="nsew")

        self.search_entry = customtkinter.CTkEntry(self.mid_frame, placeholder_text="Type Here For Search")
        self.search_entry.grid(row=3, column=1,padx=(20, 20), pady=(23, 20), sticky="nsew")

        # create end frame with widgets
        self.end_frame = customtkinter.CTkFrame(self)
        self.end_frame.grid(row=0, column=2, rowspan = 3, sticky="nsew")

        self.select_folder_button = customtkinter.CTkButton(self.end_frame, text = "Select Folder", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.Folderpath)
        self.select_folder_button.grid(row=0, column=2, padx=(33,20), pady=(21, 20), sticky="ew")
    
        self.search_button = customtkinter.CTkButton(self.end_frame, text = "Search", border_width=0, text_color=("gray10", "#DCE4EE"), command=self.Datacheckup)
        self.search_button.grid(row=3, column=2, padx=(33,20), pady=(427, 20), sticky="s")

        # Create a variable to store the selected value
        self.selected_value = customtkinter.IntVar()
        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self, border_width=2)
        self.radiobutton_frame.grid(row=1, column=2, padx = 10, pady=(65,0), sticky="new")
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Search Scope", font=customtkinter.CTkFont(size=16, weight="bold"))
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Current Directory Only", variable=self.selected_value, value=1)
        self.radio_button_1.grid(row=1, column=2, pady=5, padx=10 )
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, text="Include Subdirectories", variable=self.selected_value, value=2)
        self.radio_button_2.grid(row=2, column=2, pady=(5,10), padx=10)
        self.submit_button = customtkinter.CTkButton(self.radiobutton_frame, text = "Submit", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.get_pdf_files)
        self.submit_button.grid(row=3, column=2, pady=(5,10), padx=10, sticky="s")
        

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def bigtextbox(self,text):
        self.filename_Textbox.delete("1.0", customtkinter.END)  # Clear previous content
        self.filename_Textbox.insert(customtkinter.END, text)

    def foldertextbox(self, text):
        self.folder_Textbox.delete("1.0", customtkinter.END)  # Clear previous content
        self.folder_Textbox.insert(customtkinter.END, text)

    def Folderpath(self):
        path = filedialog.askdirectory()
        if path != "" and path !=None and path != tuple():
            # Insert the result into the Text widget
            self.foldertextbox(path)
            self.bigtextbox("")
            self.path = path
        else:
            self.foldertextbox("Please Choose Folder.")

    def get_pdf_files(self):
        self.pdf_files = []
        directory = self.path
        if directory != None and directory != "" and directory != tuple():
            if self.search_entry.get() != "":
                self.bigtextbox("Press Search Button.")
            else:
                self.bigtextbox("Write Something and Press Search Button.")
            try:
                if self.selected_value.get() == 2:
                    for root, dirs, files in os.walk(directory):
                        for file in files:
                            if file.lower().endswith(".pdf"):
                                self.pdf_files.append(os.path.join(root, file))
                elif self.selected_value.get() == 1:
                    for file in os.listdir(directory):
                            if file.lower().endswith(".pdf"):
                                    self.pdf_files.append(os.path.join(directory, file))
                else:
                    self.bigtextbox('Please Choose and Submit A Option From "Search Scope"')
            except TypeError:
                self.bigtextbox("Please Choose Folder.")
            except Exception as e:
                self.bigtextbox(e)
        else:
            self.foldertextbox("Please Choose Folder.")
            self.bigtextbox("Please Choose Folder.")

    
    # Check if user input is present in PDF text
    def Datacheckup(self):

        def Pdftext(file_path):
            try:
                reader = PdfReader(file_path)
                file_data = ""
                for page in reader.pages:
                    text = page.extract_text()
                    file_data += text.upper()
            except Exception as e:
                print(f"{e} : {file_path}")
            return file_data
        
        def threadfunc(inputtext, pdf_files):
            self.bigtextbox("Searching For Data.  Please Wait.")
            data = ""
            for pdf_file in pdf_files:
                text = Pdftext(pdf_file)
                if inputtext in text.upper():
                    pdf_file = pdf_file.replace("\\","/")
                    pdf_file = pdf_file.replace(self.path+"/","")
                    data += pdf_file+"\n"
                    self.after(0, self.bigtextbox, data)
            if len(data) == 0:
                self.bigtextbox("Data Not Found.")
        
        if self.path != "" and self.path != None and self.path != tuple():
            if self.selected_value.get() != 0:
                if self.search_entry.get() != "":
                    inputtext = self.search_entry.get().upper()
                    T1 = Thread(target=threadfunc, args=(inputtext, self.pdf_files), daemon=True)
                    T1.start()
                else:
                    self.bigtextbox("Write Something For Search.")
            else:
                self.bigtextbox('Please Choose and Submit A Option From "Search Scope"')
        else:
            self.foldertextbox("Please Choose Folder.")
            self.bigtextbox("Please Choose Folder.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
    