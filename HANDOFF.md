\# TaskFlow - Project Handoff



\## 1. Project Overview



TaskFlow is a full-stack task management application based on a Kanban-style board system.



The application allows users to:



\* Create a new account

\* Log in securely

\* Create multiple boards

\* Create lists inside boards

\* Create, edit, move, and delete tasks

\* Organize tasks using lists such as:



&#x20; \* To Do

&#x20; \* In Progress

&#x20; \* Done



The project uses a separate frontend and backend architecture.



\---



\# 2. Project Structure



```text

taskflow/

│

├── backend/

│   ├── app.py

│   ├── app\_backup.py

│   ├── requirements.txt

│   └── taskflow.db

│

├── frontend/

│   ├── index.html

│   ├── style.css

│   └── app.js

│

├── README.md

└── HANDOFF.md

```



\---



\# 3. Technologies Used



\## Frontend



\* HTML

\* CSS

\* JavaScript



\## Backend



\* Python

\* Flask

\* Flask-CORS

\* PyJWT



\## Database



\* SQLite



\## Authentication



\* JWT (JSON Web Token)

\* Password hashing using SHA-256



\---



\# 4. Backend Setup



Open the backend folder:



```powershell

cd backend

```



Install dependencies:



```powershell

pip install -r requirements.txt

```



If required, install packages manually:



```powershell

pip install flask flask-cors pyjwt

```



Start the backend server:



```powershell

python app.py

```



The server runs on:



```text

http://127.0.0.1:5000

```



The health check endpoint is:



```text

http://127.0.0.1:5000/health

```



Expected response:



```json

{

&#x20;   "status": "ok",

&#x20;   "message": "TaskFlow API is running"

}

```



\---



\# 5. Network Access



The Flask application is configured to run using:



```python

app.run(

&#x20;   host="0.0.0.0",

&#x20;   port=5000,

&#x20;   debug=True

)

```



This allows other devices on the same Wi-Fi network to access the backend using the computer's local IP address.



Example:



```text

http://10.16.69.129:5000

```



The IP address may change depending on the network.



\---



\# 6. Authentication Flow



\## Registration



Endpoint:



```text

POST /api/register

```



Expected data:



```json

{

&#x20;   "full\_name": "Example User",

&#x20;   "email": "example@email.com",

&#x20;   "username": "exampleuser",

&#x20;   "password": "password123"

}

```



The backend stores the user information in the SQLite database.



\---



\## Login



Endpoint:



```text

POST /api/login

```



Example:



```json

{

&#x20;   "username": "exampleuser",

&#x20;   "password": "password123"

}

```



Successful login returns a JWT token.



The frontend should store and use this token for authenticated API requests.



\---



\# 7. Main API Endpoints



\## Health Check



```text

GET /health

```



\## Register



```text

POST /api/register

```



\## Login



```text

POST /api/login

```



\## Get Boards



```text

GET /api/boards

```



Requires JWT authentication.



\## Create Board



```text

POST /api/boards

```



Example:



```json

{

&#x20;   "name": "My Project"

}

```



A new board automatically receives the default lists:



\* To Do

\* In Progress

\* Done



\## Get Single Board



```text

GET /api/boards/<board\_id>

```



\## Delete Board



```text

DELETE /api/boards/<board\_id>

```



\## Create List



```text

POST /api/lists

```



Example:



```json

{

&#x20;   "board\_id": 1,

&#x20;   "name": "Testing"

}

```



\## Update List



```text

PUT /api/lists/<list\_id>

```



\## Delete List



```text

DELETE /api/lists/<list\_id>

```



\## Create Task



```text

POST /api/tasks

```



Example:



```json

{

&#x20;   "list\_id": 1,

&#x20;   "title": "Complete TaskFlow",

&#x20;   "description": "Finish frontend and backend integration"

}

```



\## Update or Move Task



```text

PUT /api/tasks/<task\_id>

```



\## Delete Task



```text

DELETE /api/tasks/<task\_id>

```



\---



\# 8. Database



The application currently uses SQLite.



Database file:



```text

backend/taskflow.db

```



Main tables:



\## users



Stores:



\* User ID

\* Full name

\* Email

\* Username

\* Password hash

\* Creation date



\## boards



Stores:



\* Board ID

\* Board name

\* User ID

\* Creation date



\## lists



Stores:



\* List ID

\* List name

\* Board ID

\* Position



\## tasks



Stores:



\* Task ID

\* Title

\* Description

\* List ID

\* Position

\* Creation date



\---



\# 9. Frontend



The frontend files are located in:



```text

frontend/

```



Main files:



```text

index.html

style.css

app.js

```



\## index.html



Contains:



\* Login interface

\* Sign Up interface

\* Sidebar

\* Board interface

\* Create Board modal

\* Create List modal

\* Create/Edit Task modal



\## style.css



Contains:



\* Authentication page styling

\* Login and Sign Up tabs

\* Sidebar styling

\* Board styling

\* Task cards

\* Modal styling

\* Mobile responsive design



\## app.js



Handles:



\* User registration

\* Login

\* JWT token storage

\* Logout

\* Board loading

\* Board creation

\* List creation

\* Task creation

\* Task editing

\* Task deletion

\* Drag and drop task movement



\---



\# 10. GitHub Repository



Repository:



https://github.com/justsoumyo/taskflow



Basic update workflow:



```powershell

git add .

git commit -m "Describe your changes"

git push

```



Check repository status:



```powershell

git status

```



\---



\# 11. Important Notes



\* The current application uses SQLite.

\* The current Flask server uses debug mode.

\* The secret key currently has a development fallback value.

\* The SQLite database file may contain local development data.

\* `app\_backup.py` is kept as a backup file.

\* The backend should be started before using the frontend.



\---



\# 12. Recommended Next Improvements



The following features can be added in future versions:



\* Task due dates

\* Task priority levels

\* Labels and tags

\* Search functionality

\* Task filtering

\* User profile page

\* Profile picture upload

\* Email verification

\* Forgot password functionality

\* Password reset

\* Board sharing

\* Multiple users per board

\* Task comments

\* File attachments

\* Notifications

\* Dark mode

\* Activity history

\* Dashboard statistics

\* PostgreSQL or MySQL database

\* Docker support

\* Production deployment

\* HTTPS

\* Environment variable configuration



\---



\# 13. Production Deployment Checklist



Before deploying the application publicly:



\* Change the development secret key.

\* Store secrets in environment variables.

\* Set `debug=False`.

\* Use a production WSGI server.

\* Configure CORS properly.

\* Move from SQLite to PostgreSQL for larger deployments.

\* Do not upload sensitive database data.

\* Add `.env` to `.gitignore`.

\* Configure HTTPS.

\* Add proper error logging.



\---



\# 14. Handoff Summary



TaskFlow is currently a working full-stack task management application with:



\* User registration

\* User login

\* JWT authentication

\* User-specific boards

\* Default Kanban lists

\* Custom lists

\* Task management

\* Task movement between lists

\* Responsive frontend

\* SQLite database

\* Flask REST API



The project is suitable for further development, deployment, and portfolio improvement.



\---



\## Developer



Soumyadeep Mondal



GitHub:



https://github.com/justsoumyo



\## Repository



https://github.com/justsoumyo/taskflow



