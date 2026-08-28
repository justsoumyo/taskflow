\# 🚀 TaskFlow



TaskFlow is a full-stack task management and project organization application inspired by Kanban-style boards.



Users can create an account, log in securely, create boards, organize lists, and manage tasks.



PS C:\\Users\\Soumyadeep Mondal\\Desktop\\taskflow\\taskflow> C:\\Users\\Soumyadeep Mondal\\Desktop\\taskflow\\taskflow

C:\\Users\\Soumyadeep : The term 'C:\\Users\\Soumyadeep' is not recognized as the name of a

cmdlet, function, script file, or operable program. Check the spelling of the name, or if a

path was included, verify that the path is correct and try again.

At line:1 char:1



\* C:\\Users\\Soumyadeep Mondal\\Desktop\\taskflow\\taskflow

\* ```

&#x20;   + CategoryInfo          : ObjectNotFound: (C:\\Users\\Soumyadeep:String) \[], CommandNotFound 

&#x20;  Exception

&#x20;   + FullyQualifiedErrorId : CommandNotFoundException

&#x20; ```



PS C:\\Users\\Soumyadeep Mondal\\Desktop\\taskflow\\taskflow>



\## ✨ Features



\* 🔐 User Registration

\* 🔑 User Login with JWT Authentication

\* 👤 Full Name and Email Registration

\* 📋 Create Multiple Boards

\* 📌 Create and Manage Lists

\* 📝 Create Tasks

\* ✏️ Edit Tasks

\* 🗑️ Delete Tasks

\* 🗂️ Delete Boards

\* 📱 Responsive User Interface

\* 🔒 User-specific Boards and Tasks

\* ❤️ REST API Backend



\## 🛠️ Technologies Used



\### Frontend



\* HTML

\* CSS

\* JavaScript



\### Backend



\* Python

\* Flask

\* Flask-CORS

\* PyJWT



\### Database



\* SQLite



\## 📂 Project Structure



```text

taskflow/

│

├── backend/

│   ├── app.py

│   ├── requirements.txt

│   └── taskflow.db

│

├── frontend/

│   ├── index.html

│   ├── style.css

│   └── app.js

│

└── README.md

```



\## ⚙️ Installation



\### 1. Clone the repository



```bash

git clone https://github.com/justsoumyo/taskflow.git

```



\### 2. Go to the backend folder



```bash

cd taskflow/backend

```



\### 3. Install dependencies



```bash

pip install -r requirements.txt

```



\### 4. Run the server



```bash

python app.py

```



The backend server will run at:



```text

http://127.0.0.1:5000

```



\## 🌐 API Health Check



Open:



```text

http://127.0.0.1:5000/health

```



Expected response:



```json

{

&#x20; "status": "ok",

&#x20; "message": "TaskFlow API is running"

}

```



\## 🔗 API Endpoints



| Method | Endpoint                 | Description           |

| ------ | ------------------------ | --------------------- |

| POST   | `/api/register`          | Create a new account  |

| POST   | `/api/login`             | User login            |

| GET    | `/api/boards`            | Get user boards       |

| POST   | `/api/boards`            | Create a board        |

| GET    | `/api/boards/<board\_id>` | Get board details     |

| DELETE | `/api/boards/<board\_id>` | Delete a board        |

| POST   | `/api/lists`             | Create a list         |

| PUT    | `/api/lists/<list\_id>`   | Update a list         |

| DELETE | `/api/lists/<list\_id>`   | Delete a list         |

| POST   | `/api/tasks`             | Create a task         |

| PUT    | `/api/tasks/<task\_id>`   | Update or move a task |

| DELETE | `/api/tasks/<task\_id>`   | Delete a task         |



\## 📱 Mobile Support



TaskFlow has a responsive interface and can be accessed from other devices on the same Wi-Fi network when the Flask server is running with:



```python

app.run(host="0.0.0.0", port=5000, debug=True)

```



\## 👨‍💻 Developer



\*\*Soumyadeep Mondal\*\*



GitHub: https://github.com/justsoumyo



\---



⭐ If you like this project, consider giving it a star!



