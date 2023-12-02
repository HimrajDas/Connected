import customtkinter

def change_appearence_mode_event(self, new_appearence_mode: str):
    customtkinter.set_appearance_mode(new_appearence_mode)

    
def change_scaling_event(self, new_scaling: str):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    customtkinter.set_widget_scaling(new_scaling_float)