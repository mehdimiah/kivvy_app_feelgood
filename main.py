from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
import json
from datetime import datetime
import glob
from pathlib import Path
import random
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

Builder.load_file("design.kv")

class LoginScreen(Screen):
    
    def sign_up(self):
        self.manager.current = "sign_up_screen"
        #self is refering to the class
        #manager is a property from screen
        #current gets the name of the screen we switch too which is found under RootWidget

    def login(self,uname,pword):
        with open("users.json",'r') as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or Password!"
            #here i am writing text into the kv file. using an id to refer to the Label inside the kv file
    
    def forgotten_password(self):
        self.manager.current = "forgotten_password"

class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    
    def add_user(self,uname,pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {"username" : uname, "password":pword,
        "created" : datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        
        with open("users.json",'w') as file:
            json.dump(users,file)
            #dumping the users dictionary made by the sign up page
        self.manager.current = "sign_up_screen_success"
    
    def main_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_Screen"


class SignUpScreenSuccess(Screen):
    
    def main_screen(self):
        self.manager.current = "login_Screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_Screen"
    def get_quote(self,feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes\*txt")

        available_feelings = [Path(filename).stem for filename in
                                available_feelings]
        #extracting the file names and returning them in a list

        if feel in available_feelings:
            with open(f"quotes/{feel}.txt",'r',encoding = "utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"

class ImageButton(ButtonBehavior,HoverBehavior,Image):
    pass

class ForgottonPassword(Screen):
    
    def main_screen(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_Screen"
    
    def reset_pass(self, rpass):
        rpass = rpass
        
        with open("users.json") as file:
            users = json.load(file)
        
        users[rpass] = {"username" : rpass, "password":""}

        with open("users.json",'w') as file:
            json.dump(users,file)
        
        self.ids.preset.text = "Password has been reset"
        
        




class MainApp(App):
    def build(self):
        return RootWidget()
        #must be the object not the class
    
if __name__ == "__main__":
    MainApp().run()
