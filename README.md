# Context

- [Context](#context)
  - [Project Setup](#project-setup)
  - [Custom User Model (AbstractUser)](#custom-user-model-abstractuser)
  - [BasicInfoModel — Name, Age, Gender, Height, Weight](#basicinfomodel--name-age-gender-height-weight)
  - [ConsumedCalories Model](#consumedcalories-model)
  - [Register Models In Admin](#register-models-in-admin)
  - [Connect Custom User Model (`AUTH_USER_MODEL`)](#connect-custom-user-model-auth_user_model)
  - [Migrations](#migrations)
  - [Registration Form (`forms.py`)](#registration-form-formspy)
  - [Login Form (`forms.py`)](#login-form-formspy)
  - [Master Templates Setup](#master-templates-setup)
  - [Shared Form Template (`base-form.html`)](#shared-form-template-base-formhtml)
  - [Passing `form_data` To The Template](#passing-form_data-to-the-template)
  - [App-Level URLs](#app-level-urls)
  - [Connect App URLs To Project URLs](#connect-app-urls-to-project-urls)
  - [Disabling Django's Default Password Validators](#disabling-djangos-default-password-validators)
  - [Registration View — Full Logic](#registration-view--full-logic)
  - [Flash Messages (`message.html`)](#flash-messages-messagehtml)
  - [Login View — Full Logic](#login-view--full-logic)
  - [Dashboard Page](#dashboard-page)
  - [Project Structure](#project-structure)
  - [Final Output](#final-output)

This README follows the actual **commit history** of the project — every section below matches one real commit, in the same order they were built. That way it doubles as both documentation and a step-by-step build log.

## Project Setup

- Create and activate a virtual environment

  ```sh
  python -m venv venv
  venv\Scripts\activate      # Windows
  source venv/bin/activate   # Linux/Mac
  ```

- Install Django and the packages this project depends on (`django-crispy-forms` is used later to render forms with Bootstrap styling)

  ```sh
  pip install django crispy-forms crispy-bootstrap5
  ```

- Create the project

  ```sh
  django-admin startproject Bikram_2025_CaloryCounter
  cd Bikram_2025_CaloryCounter
  ```

- Create the app

  ```sh
  py manage.py startapp CalorieCounter
  ```

- Register the app and the crispy-forms packages in [settings.py](./Bikram_2025_CaloryCounter/settings.py)

  ```py
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'CalorieCounter',
      'crispy_forms',
      'crispy_bootstrap5',
  ]

  CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
  CRISPY_TEMPLATE_PACK = "bootstrap5"
  ```

---
[⬆️ Go to Context](#context)

## Custom User Model (AbstractUser)

- This project doesn't use Django's built-in `User` model directly. Instead, it extends it with `AbstractUser`, so it's possible to add extra fields or behavior to the user later without breaking anything
- Created in [CalorieCounter/models.py](./CalorieCounter/models.py)

  ```py
  from django.db import models
  from django.contrib.auth.models import AbstractUser


  class User(AbstractUser):

      def __str__(self):
          return f"{self.username}"
  ```

> [!IMPORTANT]
> `AbstractUser` must be connected in `settings.py` using `AUTH_USER_MODEL` **before** the very first migration — see [Connect Custom User Model](#connect-custom-user-model-auth_user_model). Switching to a custom user model after the database already has data is painful, so it's done right at the start of the project.

---
[⬆️ Go to Context](#context)

## BasicInfoModel — Name, Age, Gender, Height, Weight

- Stores personal details for the logged-in user: `name`, `age`, `gender`, `height`, `weight`
- Linked to `User` with a `OneToOneField` — meaning **each user can have exactly one** `BasicInfoModel` record (a user can't have two profiles)

  ```py
  class BasicInfoModel(models.Model):

      GENDER_TYPE = [
          ("Male", "Male"),
          ("Female", "Female")
      ]

      user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info', null=True)
      name = models.CharField(max_length=100, null=True)
      age = models.PositiveIntegerField(null=True)
      gender = models.CharField(choices=GENDER_TYPE, max_length=10, null=True)
      height = models.FloatField(null=True)
      weight = models.FloatField(null=True)

      def __str__(self):
          return f"{self.name} - {self.age}"
  ```

- Field notes:

  | Field    | Type                    | Notes                                                     |
  | -------- | ------------------------ | ------------------------------------------------------------ |
  | `user`   | `OneToOneField(User)`     | `related_name='user_info'` → access via `user.user_info`      |
  | `age`    | `PositiveIntegerField`    | Only accepts 0 or positive numbers                             |
  | `gender` | `CharField` + `choices`   | Dropdown limited to `Male` / `Female`                          |
  | `height`, `weight` | `FloatField`     | Decimal numbers allowed (e.g. `170.5` cm, `65.2` kg)            |

---
[⬆️ Go to Context](#context)

## ConsumedCalories Model

- Every time a user logs a food item, one row is stored here: `item_name`, `calorie`, and the date it was logged
- Linked to `User` with a `ForeignKey` (not `OneToOne`) — because **one user can log many food items**, but each food entry belongs to only one user

  ```py
  class ConsumedCalories(models.Model):

      item_name = models.CharField(max_length=200, null=True)
      calorie = models.FloatField(null=True)
      created_at = models.DateField(auto_now_add=True, null=True)
      consumed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_calorie')

      def __str__(self):
          return f'{self.item_name} - {self.consumed_by.username}'
  ```

- `auto_now_add=True` on `created_at` automatically stamps today's date the moment the record is created — no need to set it manually in the view

> [!NOTE]
> `OneToOneField` vs `ForeignKey` — this is the key difference between the two models above:
> - `BasicInfoModel.user` → `OneToOneField` → 1 user = 1 profile
> - `ConsumedCalories.consumed_by` → `ForeignKey` → 1 user = many calorie entries

---
[⬆️ Go to Context](#context)

## Register Models In Admin

- All three models are registered together using a list, in [CalorieCounter/admin.py](./CalorieCounter/admin.py)

  ```py
  from django.contrib import admin
  from CalorieCounter.models import *


  admin.site.register([
      User,
      BasicInfoModel,
      ConsumedCalories
  ])
  ```

---
[⬆️ Go to Context](#context)

## Connect Custom User Model (`AUTH_USER_MODEL`)

- By default, Django uses its own built-in `auth.User`. Since we created a custom `User` model, Django must be told to use **that one instead**
- Add this single line in [settings.py](./Bikram_2025_CaloryCounter/settings.py)

  ```py
  AUTH_USER_MODEL = "CalorieCounter.User"
  ```

  Format is always `"<app_name>.<ModelName>"`.

---
[⬆️ Go to Context](#context)

## Migrations

- Now that all 3 models exist and `AUTH_USER_MODEL` is set, generate and apply migrations

  ```sh
  py manage.py makemigrations
  py manage.py migrate
  ```

- Create a superuser to access the admin panel

  ```sh
  py manage.py createsuperuser
  ```

---
[⬆️ Go to Context](#context)

## Registration Form (`forms.py`)

- Django already provides a ready-made form for user signup: `UserCreationForm`. Instead of writing a registration form from scratch, we extend it and just customize which fields to show
- Created in [CalorieCounter/forms.py](./CalorieCounter/forms.py)

  ```py
  from django import forms
  from CalorieCounter.models import *
  from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


  class RegisterationForm(UserCreationForm):
      class Meta:
          model = User
          fields = ['username', 'email', 'password1', 'password2']
  ```

- `UserCreationForm` already handles password hashing and the "confirm password" match check internally — we don't have to write that logic ourselves

---
[⬆️ Go to Context](#context)

## Login Form (`forms.py`)

- Same idea — Django's built-in `AuthenticationForm` already validates username + password against the database, so we simply reuse it as-is

  ```py
  class LoginForm(AuthenticationForm):
      pass
  ```

---
[⬆️ Go to Context](#context)

## Master Templates Setup

- Create a shared `master` template folder with 4 files, so every page (register, login, dashboard) reuses the same layout instead of repeating HTML

  ```txt
  📁 templates
  ├── 📁 master
  │   ├── 🌐 base.html          # main layout + navbar + Bootstrap CDN
  │   ├── 🌐 base-form.html      # shared layout for register + login forms
  │   ├── 🌐 nav.html             # navbar
  │   └── 🌐 message.html         # flash/success messages block
  └── 🌐 dashboard.html
  ```

- [master/base.html](./CalorieCounter/templates/master/base.html) — the root layout every page extends

  ```html
  <!doctype html>
  <html lang="en">
    <head>
      <meta charset="utf-8">
      <title>Calorie Counter</title>
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
      {% include 'master/nav.html' %}
      {% block body %}
      {% endblock body %}
      <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>
    </body>
  </html>
  ```

- [master/nav.html](./CalorieCounter/templates/master/nav.html) — a standard Bootstrap navbar, included in `base.html` via `{% include %}` so it appears on every page automatically

---
[⬆️ Go to Context](#context)

## Shared Form Template (`base-form.html`)

- Instead of writing two separate templates for the register page and the login page (which would look almost identical), **one reusable form template** is built. The view decides what title/button text/form object to pass in
- Uses `{% load crispy_forms_tags %}` and the `|crispy` filter so the form renders with full Bootstrap styling automatically, without manually writing `<input>` tags for every field

  ```html
  {% extends 'master/base.html' %}
  {% load crispy_forms_tags %}

  {% block body %}
  <div class="container">
      <h1>{{form_title}}</h1>
      {% include 'master/message.html' %}
    <form method="post" enctype="multipart/form-data">
      {% csrf_token %}
      {{ form_data|crispy }}
      <button type="submit" class="btn btn-primary">{{form_btn}}</button>
    </form>
  </div>
  {% endblock body %}
  ```

---
[⬆️ Go to Context](#context)

## Passing `form_data` To The Template

- `base-form.html` expects 3 dynamic variables from the view's `context`: `form_data`, `form_title`, `form_btn`
- This is what makes the **same template** work for both Register and Login pages:

  | Variable     | Register page value      | Login page value       |
  | ------------ | -------------------------- | ------------------------- |
  | `form_data`  | `RegisterationForm()`       | `LoginForm()`              |
  | `form_title` | `"User Register Form"`      | `"User Login Form"`        |
  | `form_btn`   | `"Register"`                 | `"Login"`                   |

---
[⬆️ Go to Context](#context)

## App-Level URLs

- Created in [CalorieCounter/urls.py](./CalorieCounter/urls.py)

  ```py
  from django.urls import path
  from CalorieCounter.views import *


  urlpatterns = [
      path('', register_page, name='register_page'),
      path('login/', login_page, name='login_page'),
      path('dashboard/', dashboard_page, name='dashboard_page'),
  ]
  ```

---
[⬆️ Go to Context](#context)

## Connect App URLs To Project URLs

- Included in the project's [urls.py](./Bikram_2025_CaloryCounter/urls.py) using `include()`

  ```py
  from django.contrib import admin
  from django.urls import path, include

  urlpatterns = [
      path('admin/', admin.site.urls),
      path('', include('CalorieCounter.urls')),
  ]
  ```

---
[⬆️ Go to Context](#context)

## Disabling Django's Default Password Validators

- By default Django enforces strong-password rules (minimum length, not too common, not all numeric, not similar to username). For faster local testing during development, these were commented out in [settings.py](./Bikram_2025_CaloryCounter/settings.py)

  ```py
  # AUTH_PASSWORD_VALIDATORS = [
  #     {
  #         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  #     },
  #     {
  #         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  #     },
  #     {
  #         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  #     },
  #     {
  #         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  #     },
  # ]
  ```

> [!IMPORTANT]
> This is fine for a class project / local testing, but should be **re-enabled before deploying to production** — otherwise users can register with weak passwords like `1234`.

---
[⬆️ Go to Context](#context)

## Registration View — Full Logic

- Full logic in [CalorieCounter/views.py](./CalorieCounter/views.py)

  ```py
  def register_page(request):

      if request.method == "POST":
          form_data = RegisterationForm(request.POST)
          if form_data.is_valid():
              form_data.save()
              messages.success(request, 'Registeration successfully')
              return redirect('login_page')

      form_data = RegisterationForm()

      context = {
          "form_data": form_data,
          "form_title": "User Register Form",
          "form_btn": "Register"
      }

      return render(request, "master/base-form.html", context)
  ```

- Step-by-step what happens:
  1. **GET request** (page first loads) → skips the `if` block → shows an **empty** registration form
  2. **POST request** (user submits form) → data is bound to `RegisterationForm(request.POST)`
  3. `.is_valid()` checks: passwords match, username isn't taken, email is a valid format, etc.
  4. If valid → `.save()` creates the user in the database → shows a success message → **redirects** to the login page (so the same form can't be submitted twice by refreshing)
  5. If invalid → falls through to `render()` again, showing the same form **with error messages** next to the invalid fields

---
[⬆️ Go to Context](#context)

## Flash Messages (`message.html`)

- Django's `messages` framework is used to show one-time success/info banners (like "Registeration successfully")
- [master/message.html](./CalorieCounter/templates/master/message.html) loops through any pending messages and displays them as Bootstrap alerts

  ```html
  {% if messages %}
  {% for message in messages %}
  <div class="alert alert-primary" role="alert">
    {{message}}
  </div>
  {% endfor %}
  {% endif %}
  ```

- This partial is included in both `base-form.html` and `dashboard.html`, so messages show up right after redirect (e.g. after successful registration or login)

---
[⬆️ Go to Context](#context)

## Login View — Full Logic

  ```py
  def login_page(request):

      if request.method == "POST":
         form_data = LoginForm(request, request.POST)
         if form_data.is_valid():
             user = form_data.get_user()
             login(request, user)
             messages.success(request, 'Login successfully')
             return redirect("dashboard_page")

      form_data = LoginForm()
      context = {
          "form_data": form_data,
          "form_title": "User Login Form",
          "form_btn": "Login"
      }

      return render(request, "master/base-form.html", context)
  ```

- Difference from the registration view: `AuthenticationForm` needs the `request` object passed in as its first argument (`LoginForm(request, request.POST)`) — this is required internally by Django to check session/login throttling
- `form_data.get_user()` retrieves the actual authenticated `User` object once credentials are verified
- `login(request, user)` creates the session — this is the line that actually **logs the user in**
- On success → redirected to `dashboard_page`

---
[⬆️ Go to Context](#context)

## Dashboard Page

- The final destination after login — a protected-feeling landing page that greets the logged-in user by username

  ```py
  def dashboard_page(request):
      return render(request, 'dashboard.html')
  ```

- [dashboard.html](./CalorieCounter/templates/dashboard.html)

  ```html
  {% extends 'master/base.html' %}

  {% block body %}
  <div class="container">
      {% include 'master/message.html' %}
      <h1>
          Welcome, {{ request.user.username}}
      </h1>
  </div>
  {% endblock body %}
  ```

- `{{ request.user.username }}` works directly in the template — Django automatically attaches the logged-in user to every `request` object via the `AuthenticationMiddleware`

> [!NOTE]
> As of this commit, `dashboard_page` doesn't yet check `if request.user.is_authenticated` — so technically anyone can visit `/dashboard/` directly without logging in first. Adding `@login_required` (or a manual check + redirect) is a natural next step for this project.

---
[⬆️ Go to Context](#context)

## Project Structure

```txt
Bikram_2025_CaloryCounter/
├── Bikram_2025_CaloryCounter/
│   ├── settings.py            # AUTH_USER_MODEL, crispy_forms, INSTALLED_APPS
│   ├── urls.py                 # project-level routing
│   ├── asgi.py
│   └── wsgi.py
├── CalorieCounter/
│   ├── models.py                # User (AbstractUser), BasicInfoModel, ConsumedCalories
│   ├── admin.py                  # all 3 models registered
│   ├── forms.py                    # RegisterationForm, LoginForm
│   ├── views.py                     # register_page, login_page, dashboard_page
│   ├── urls.py                       # app-level routing
│   ├── migrations/
│   └── templates/
│       ├── master/
│       │   ├── base.html
│       │   ├── base-form.html
│       │   ├── nav.html
│       │   └── message.html
│       └── dashboard.html
├── db.sqlite3
└── manage.py
```

---
[⬆️ Go to Context](#context)

## Final Output

- `http://127.0.0.1:8000/` → Registration page (`register_page`)
- `http://127.0.0.1:8000/login/` → Login page (`login_page`)
- `http://127.0.0.1:8000/dashboard/` → Welcome dashboard after login (`dashboard_page`)
- `http://127.0.0.1:8000/admin/` → Admin panel — manage `User`, `BasicInfoModel`, `ConsumedCalories`

**Flow:** Register → redirected to Login → Login → redirected to Dashboard → greeted by username

---
[⬆️ Go to Context](#context)
