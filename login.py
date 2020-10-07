import time
from multiprocessing.pool import ThreadPool
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginErrorPopup(Popup):
    def __init__(self, msg: str, **kw):
        self.msg = msg
        self.title = 'Login Error'
        self.size_hint = (.5, .5)
        super().__init__(**kw)
        self.open()


class LoginForm(BoxLayout):
    username = StringProperty()
    password = StringProperty()
    remember_me = BooleanProperty(False)

    def __init__(self, on_success, on_error, **kw):
        self.on_success = on_success
        self.on_error = on_error
        super().__init__(**kw)
        self.load_login_info()

    def load_login_info(self):
        if app.store.exists('login'):
            self.username = app.store.get('login')['username']
            self.password = app.store.get('login')['password']
            self.remember_me = app.store.get('login')['rememberMe']
            self.ids['usernameField'].text = self.username
            self.ids['passwordField'].text = self.password
            self.ids['rememberMe'].active = self.remember_me

    def submit(self, username: str, password: str, remember_me: bool):
        self._block_inputs()
        self.username, self.password, self.remember_me = username, password, remember_me

        if self.remember_me:
            self.save_login_info()
        elif app.store.exists('login'):
            app.store.clear()

        pool = ThreadPool(processes=1)
        pool.apply_async(self.do_login, callback=self._on_success, error_callback=self._on_error)

    def save_login_info(self):
        app.store.put('login', username=self.username, password=self.password, rememberMe=self.remember_me)

    def do_login(self):
        time.sleep(2)
        print(self.username, self.password, self.remember_me)

    def _block_inputs(self):
        self.ids['submit'].text = 'Loading...'
        self.ids['submit'].disabled = self.ids['rememberMe'].disabled = True
        self.ids['usernameField'].disabled = self.ids['passwordField'].disabled = True

    def _unblock_inputs(self):
        self.ids['submit'].text = 'Submit'
        self.ids['submit'].disabled = self.ids['rememberMe'].disabled = False
        self.ids['usernameField'].disabled = self.ids['passwordField'].disabled = False

    def _on_success(self, e):
        self._unblock_inputs()
        self.on_success(e)

    def _on_error(self, e):
        self._unblock_inputs()
        self.on_error(e)

    @classmethod
    def on_success(cls, e):
        pass

    @classmethod
    def on_error(cls, e):
        pass


class SuccessScreen(Screen):
    pass


class LoginScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.add_widget(LoginForm(on_success=self.success, on_error=self.display_error))

    @classmethod
    def success(cls, e):
        app.manager.current = 'success'

    @classmethod
    def display_error(cls, e):
        LoginErrorPopup(msg='Unable to login at this time.')


class LoginApp(App):
    store = ObjectProperty(JsonStore('storage.json'))
    manager = ObjectProperty(ScreenManager())

    def build(self):
        self.manager.add_widget(LoginScreen(name='login'))
        self.manager.add_widget(SuccessScreen(name='success'))
        return self.manager


if __name__ == "__main__":
    app = LoginApp()
    app.run()
