# Finance Management App

<div align="justify">
The project focuses on building a Finance Management application using Flask as the backend framework and PostgreSQL as the database. The application provides a web-based interface powered by HTML, CSS, and JavaScript, with Bootstrap used for responsive and structured layouts. Users can track and analyze their total expenses, manage loans, and monitor insurance premiums. Category-wise expense insights are visualized using the Plotly library, enabling interactive and intuitive data analysis. The system is designed to simplify personal finance tracking by combining robust backend logic with clean and user-friendly dashboards.
<br><br>
</div>


## Setup
<h3>
<div>
<img src="img/env.png"; width=20> <b>Environment</b>
</div>
</h3>

*Note - The app is written using Python virtual environment version **3.13.5** and supports the latest Python versions. However, lower Python versions may offer more stability compared to the latest ones. Below setup will focus Windows system. And commands to setup may vary for macOS or Linux.*

<div>
1. Move to folder (CLI commands)

```bash
# If you downloaded the file, just navigate to folder
# Then press Shift (in Windows) + Left Mouse click
# Choose Open PowerShell window here option and move on to creating virtual environment
cd household_finances_app
```
</div>

<div>
2. Create a python virtual environment using -

```bash
# Path to installation of particular version of python  may vary
# I have installed more than one version of python in pyver directory
# Refer the resources section, for youtube video to install multiple versions of python
C:\Users\<username>\pyver\py3121\python -m venv housevenv
```
</div>

<div>
3. Activate the virtual environment using -

```bash
housevenv\Scripts\activate
```
</div>

<div>
4. Install python packages using - 

```bash
pip install -r requirements.txt
```
</div>

<div>
<h3>
<img src="img/postgres.png"; width=20> <b>PostgreSQL</b>
</h3>
</div>

<div>
1. Install PostgreSQL from <a href="https://www.enterprisedb.com/downloads/postgres-postgresql-downloads">here</a>
</div><br>

<div>
2. Please refer the <b>resource</b> section for PostgreSQL setup to get the database up and ready.
</div><br>

<div>
3. After installation is successful, open pgAdmin 4 <img src="img/pg-resource/pgAdmin.png"> 
</div><br>

<div>
4. Now to connect the PostgreSQL server, enter database password (it will be same password, that was choosen while installing PostgreSQL) <img src="img/pg-resource/pgLogin.png"> 
</div><br>

<div>
5. After connecting to server, the left pane gives an overview of available and <i>running up servers</i>. I had created 3 other databases, but by default the Postgres provides with <i>postgres</i> database <img src="img/pg-resource/pgData.png">
</div><br>

<div>
6. We can navigate down to know more about current database.<img src="img/pg-resource/pgSchema.png">
</div><br>

<div>
7. Create database by right clicking on <b>database</b>, and then choose <b>Create > Database...</b> <img src="img/pg-resource/pgDb.png"> 
</div><br>

<div>
8. A window shall pop-up asking for <b><i>Database name</b></i>. Enter <b>finance_db</b>. <i>Since above app has finance_db database connection. You may independently try changing the name of database, by updating references to finance_db in above application, with desired database name. </i>
</div><br>

<div>
9. In <a href="configs.py">configs.py</a> file, update the database <i>password</i> at

```bash
SQLALCHEMY_DB = postgresql://postgres:password@localhost/finance_db
```
</div>

<div>
11. Create a <b>.env</b> file in <i>current directory</i>, from <b>env.example.txt</b> to save the <i>secret credentials</i> that will be created in upcoming steps.
</div><br>

<div>
12. We need an endpoint for sending email based <i>otp for login verification</i> into app. We will use Google Account's App Password to authenticate ourselves, for sending verified and encrypted emails. 
</div><br>

<div>
13. Navigate to <b><i>Google Accounts section</b></i>, and then choose Security tab and search for <i>App passwords</i>. <img src="img/pg-resource/pgPw.png"> 
</div><br>

<div>
14. Create an app with name that can used now and referenced later. <img src="img/pg-resource/pgApp.png"> 
</div><br>

<div>
15. Copy the App password to newly created <b>.env</b> file at <b>MAIL_PASSWORD</b>.
</div><br>

<div>
16. Change the <b>MAIL_USERNAME</b> and <b>MAIL_DEFAULT_SENDER</b> with the Google Account e-mail id used to create the App password. <i>You may get error in authentication of APP password, so try without enclosing it in quotes, that's what I was able to do.</i>
</div><br>

<div>
17. Congratulations! You have successfully completed the setup.
</div><br>

<div>
18. To learn more about PostgreSQL, please refer <b>resource</b> section to get reference to learning resources. <i>Having an idea of basic queries will help understand the purpose  at various instances of the application.</i>
</div>

## Execute
This section explains how to run the application, the folder structure involved, and the different features available once the app is running.

**Project Overview**
<ul>
<li>

`temaplates` folder contains HTML files for rendering dynamic content with Flask
</li>
</ul>

<ul>
<li>

`routes` folder holds Python-based routes for page redirection, dashboard categories, and schema declarations.
</li>
</ul>

<ul>
<li>

`seeders` folder includes custom seeders to populate the PostgreSQL database with fake data for testing.
</li>
</ul>

<ul>
<li>

`app.py` The main entry point of the application. Running this file initializes the backend, creates schema in pgAdmin 4, and connects routes with templates.
</li>
</ul>

<ul>
<li>

`logger` folder keeps track of steps that execute on the interface or application.
</li>
</ul>

**Steps to run**

<div>
1. Run the app using below command (before running please activate the virtual environment)

``` bash
python app.py
``` 
</div>

<div>
2. Register as a New User

<ul>
    <li>Navigate to the registration page.</li>
    <li>Enter your details.</li>
    <li>An OTP will be sent to your registered email via Google Account Gateway.</li>
    <li>Verify OTP to activate login.</li>
</ul>
</div>

<div>
3.  Login and access features
<ul>
<li>Once verified, log in with your credentials.</li>
<li>Use filters, add data, and explore charts.</li>
</ul>
</div>

**Features**
<ul>
<li>

*Filter buttons* - Filter out data by category and date range.
</li>
</ul>

<ul>
<li>

*More Info buttons* - View database-related details for each schema.
</li>
</ul>

<ul>
<li>

*Add data{schema name}* - Add new records into the database by choosing the appropriate schema (with input fields & dropdowns for better visualization).
</li>
</ul>

<ul>
<li>

*Dynamic Charts* - Auto-updated charts that can be filtered by categories/date range.
</li>
</ul>

<ul>
<li>

*Enlarge Charts* - Use the View Larger Chart button for a detailed view.
</li>
</ul>

<ul>
<li>

*Forget Password* - If a user forgets their password, they can reset it from the login page. An OTP will be sent to the registered email to ensure only the verified user can reset credentials. The updated password is securely stored in the database.
</li>
</ul>


## Resources
**Python Version Setup**
<ul>
<li>https://www.youtube.com/watch?v=28eLP22SMTA&t=99s</li>
</ul>

**PostgreSQL Setup**
<ul>
<li>https://www.w3schools.com/postgresql/postgresql_install.php</li>
</ul>

**Learn PostgreSQL**
<ul>
<li>(Beginners Introduction) https://www.w3schools.com/postgresql/index.php</li>
<li>(Official website) https://www.postgresql.org/docs/17/sql.html</li>
</ul>

**Document Object Model (HTML/CSS/JS)**
<ul>
<li>https://developer.mozilla.org/en-US/docs/Web/API/Document_Object_Model</li>
<li>https://developer.mozilla.org/en-US/docs/Web/API/Document</li>
<li>https://developer.mozilla.org/en-US/docs/Web/API/Element</li>
</ul>
