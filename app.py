import customtkinter
import utils


class TextboxFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure((0, 1), weight=1)

        # for outgoing messages
        self.outgoing_text = customtkinter.CTkTextbox(
            self,
            width=200,
            height=60,
            corner_radius=10,
            text_color="white",
            border_width=2,
            border_color="#FFFFDD",
            fg_color="#0C356A",
        )

        self.outgoing_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.outgoing_text.insert("0.0", "bam! outgoing")

        # incoming text
        self.incoming_text = customtkinter.CTkTextbox(
            self,
            width=200,
            height=60,
            corner_radius=10,
            text_color="white",
            border_width=2,
            border_color="#FFFFDD",
            fg_color="#0C356A",
        )

        self.incoming_text.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.incoming_text.insert("0.0", "bam! incoming")
        self.incoming_text.configure(state="disabled")


class Sidebar(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.logo_label = customtkinter.CTkLabel(
            self, text="Packets", font=customtkinter.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(
            self, text="Appearence Mode: ", anchor="w"
        )
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=20)
        self.appearance_mode_optionMenu = customtkinter.CTkOptionMenu(
            self,
            values=["light", "dark", "system"],
            command=self.change_appearence_mode_event,
        )
        self.appearance_mode_optionMenu.grid(row=2, column=0, padx=20, pady=20)

        self.scaling_label = customtkinter.CTkLabel(
            self, text="UI-Scaling:", anchor="w"
        )
        self.scaling_label.grid(row=3, column=0, padx=20, pady=20)
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(
            self,
            values=["80%", "90%", "100%", "110%", "120%"],
            command=self.change_scaling_event,
        )
        self.scaling_optionmenu.grid(row=4, column=0, padx=20, pady=20)
    

    def change_appearence_mode_event(self, new_appearence_mode: str):
        customtkinter.set_appearance_mode(new_appearence_mode)

    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("packets")
        self.geometry("1100x580")

        # create a 2x2 grid.
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        # self.grid_rowconfigure(1, weight=1)

        self.sidebar_frame = Sidebar(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.text_box = TextboxFrame(self)
        self.text_box.grid(row=0, column=1, rowspan=2, sticky="nsew")




if __name__ == "__main__":
    app = App()
    app.mainloop()
