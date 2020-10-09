# KivyLoginExample
Login page example using kivy templates

# App Pages

## Login
<p align="center">
  <img src="https://i.ibb.co/QMfkY2V/2020-10-09-10-36-51-Login.png"/>
  <img src="https://i.ibb.co/Wk33vGJ/2020-10-09-10-37-12-Login.png"/>
</p>

## Success Page / Error Pages
<p align="center">
   <img src="https://i.ibb.co/PrTPb7h/2020-10-09-10-37-57-Login.png"/>
   <img src="https://i.ibb.co/YPdyXwh/2020-10-09-10-57-37-Login.png"/>
</p>

# Features

## Threading to Avoid GUI Freeze

```python
class LoginForm(BoxLayout):
  ...
  def submit(self, username: str, password: str, remember_me: bool):
    ...
    
    pool = ThreadPool(processes=1)
    pool.apply_async(self.do_login, callback=self._on_success, error_callback=self._on_error)
   
```

## Login Details Saved in JSON format

```json
// storage.json
{
  "login": {
    "username": "some_username123",
    "password": "some_password123",
    "rememberMe": true
  }
}
```
