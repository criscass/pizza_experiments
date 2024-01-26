# Pizza Diary

![pizza diary logo, a cartoonish agenda that lloks like a pizza slice](static/images/pizza-diary-logo-sm.png)

#### Video Demo: https://www.youtube.com/watch?v=mh57fLK06lw&t=112s

#### Live Demo: https://pizza-diary.onrender.com/

**_Wait a bit in case server needs waking up._**

#### Attention:

**_If you want to clone the project and run it locally you should complete the .env file._**

#### Description:

Pizza Diary is an app that lets you track your dough-making experiments.

It features an in-app calculator that helps you determine the right amounts of flour, water, and salt needed for a specific number of pizza balls, usually weighing 250 grams each. You can start a "new experiment" by entering the ingredients and procedure, along with a final comment and rating for the result. The only mandatory ingredients for creating a new experiment are flour and water; the rest are optional. Your new experiment will then appear on the list of experiments on the home page, where you can view, edit, or delete it in full detail. Access to all pages, except for the calculator, requires logging in.

Both the registration and login pages incorporate server-side and client-side validation. For example, a user cannot register with an email or username that's already in use. Additionally, the email must be valid, and the password should be at least 8 characters long.

The app is developed using Flask and Bootstrap for styling, and it incorporates various libraries including WTForms, SQLAlchemy, Flask-Login, and Flask-Bcrypt. Initially, I used SQLite for the database, but I later switched to PostgreSQL to take advantage of free hosting services available for it.

Because I've used SQLAlchemy, I'm defining some classes in the "app.py" file that represent the tables in the database. I could have written these classes in a separate file and then imported them into the main app file, but I didn't because the project is not so large, after all. In the future, if I introduce new functionalities, I'll definitely refactor this part.
The same is valid for the forms, which are also defined in the "app.py" file, since I'm using the library "WTForms".

The login and permissions are managed through Flask-Login.

The environmental variables include the secret_key, used throughout the app, the database_url, and edit_url.
The database_url variable needs to be set according to the database used. In my case, I use an instance on ElephantSQL, both for my local development and production.
The edit_url is needed because I had to hardcode an "href" address to be able to redirect through JavaScript when in the "edit experiment" session. All these variables are kept private by not including them in my GitHub repository. In production, the variables are managed by the hosting servers.

Although I'm more experienced with JavaScript than Python, having used it before taking CS50, I enjoyed working with Flask and wanted to build something using it. This led me to use some JavaScript in areas where I found Python or Jinja challenging.

#### Future Enhancements:

1. Improve the app's styling to make it more colorful.
2. Enable automatic login when a user registers a new account.
3. Allow creation of a new experiment directly from the calculator, with main ingredients pre-filled.
4. Introduce the option to use different types of flour in a mix.
5. Add alternative measurement units, such as ounces and Fahrenheit.
6. Introduce a community section where users can share and discuss their experiments, offer tips, and provide feedback on others' creations.
