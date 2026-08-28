const API_BASE = "http://127.0.0.1:5000/api";

let token = localStorage.getItem("taskflow_token");
let username = localStorage.getItem("taskflow_username");

let currentBoardId = null;
let currentTaskId = null;
let currentTaskListId = null;

let authMode = "login";
let draggedTaskId = null;


// =========================
// DOM ELEMENTS
// =========================

const authPage = document.getElementById("authPage");
const appPage = document.getElementById("appPage");

const loginTab = document.getElementById("loginTab");
const registerTab = document.getElementById("registerTab");

const authForm = document.getElementById("authForm");
const authButton = document.getElementById("authButton");
const authMessage = document.getElementById("authMessage");

const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const fullNameInput = document.getElementById("fullName");
const emailInput = document.getElementById("email");
const confirmPasswordInput = document.getElementById("confirmPassword");

const fullNameField = document.getElementById("fullNameField");
const emailField = document.getElementById("emailField");
const confirmPasswordField = document.getElementById("confirmPasswordField");

const currentUser = document.getElementById("currentUser");

const boardsList = document.getElementById("boardsList");

const emptyState = document.getElementById("emptyState");
const boardView = document.getElementById("boardView");

const boardTitle = document.getElementById("boardTitle");
const listsContainer = document.getElementById("listsContainer");

const boardModal = document.getElementById("boardModal");
const boardNameInput = document.getElementById("boardNameInput");

const listModal = document.getElementById("listModal");
const listNameInput = document.getElementById("listNameInput");

const taskModal = document.getElementById("taskModal");
const taskModalTitle = document.getElementById("taskModalTitle");

const taskTitleInput = document.getElementById("taskTitleInput");
const taskDescriptionInput = document.getElementById("taskDescriptionInput");

const deleteTaskBtn = document.getElementById("deleteTaskBtn");


// =========================
// API HELPER
// =========================

async function apiRequest(endpoint, method = "GET", data = null) {

    const options = {
        method: method,
        headers: {
            "Content-Type": "application/json"
        }
    };

    if (token) {
        options.headers["Authorization"] = `Bearer ${token}`;
    }

    if (data) {
        options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE}${endpoint}`, options);

    const result = await response.json();

    if (!response.ok) {
        throw new Error(result.error || "Something went wrong");
    }

    return result;
}


// =========================
// AUTH
// =========================

  // =========================
// AUTH
// =========================


// LOGIN TAB

loginTab.addEventListener("click", () => {

    authMode = "login";

    loginTab.classList.add("active");
    registerTab.classList.remove("active");

    fullNameField.classList.add("hidden");
    emailField.classList.add("hidden");
    confirmPasswordField.classList.add("hidden");

    fullNameInput.value = "";
    emailInput.value = "";
    confirmPasswordInput.value = "";

    authButton.textContent = "Login";

    authMessage.textContent = "";
    authMessage.style.color = "#c0392b";

});


// SIGN UP TAB

registerTab.addEventListener("click", () => {

    authMode = "register";

    registerTab.classList.add("active");
    loginTab.classList.remove("active");

    fullNameField.classList.remove("hidden");
    emailField.classList.remove("hidden");
    confirmPasswordField.classList.remove("hidden");

    authButton.textContent = "Sign Up";

    authMessage.textContent = "";
    authMessage.style.color = "#c0392b";

});


// AUTH FORM SUBMIT

authForm.addEventListener("submit", async (event) => {

    event.preventDefault();


    const fullName = fullNameInput.value.trim();
    const email = emailInput.value.trim();

    const user = usernameInput.value.trim();

    const password = passwordInput.value;

    const confirmPassword =
        confirmPasswordInput.value;


    authMessage.textContent = "";

    authMessage.style.color = "#c0392b";


    // =========================
    // LOGIN VALIDATION
    // =========================

    if (authMode === "login") {

        if (!user) {

            authMessage.textContent =
                "Please enter your username.";

            return;

        }


        if (!password) {

            authMessage.textContent =
                "Please enter your password.";

            return;

        }

    }


    // =========================
    // SIGN UP VALIDATION
    // =========================

    if (authMode === "register") {

        if (!fullName) {

            authMessage.textContent =
                "Please enter your full name.";

            return;

        }


        if (!email) {

            authMessage.textContent =
                "Please enter your email address.";

            return;

        }


        if (!email.includes("@")) {

            authMessage.textContent =
                "Please enter a valid email address.";

            return;

        }


        if (!user) {

            authMessage.textContent =
                "Please enter a username.";

            return;

        }


        if (user.length < 3) {

            authMessage.textContent =
                "Username must be at least 3 characters.";

            return;

        }


        if (!password) {

            authMessage.textContent =
                "Please enter a password.";

            return;

        }


        if (password.length < 4) {

            authMessage.textContent =
                "Password must be at least 4 characters.";

            return;

        }


        if (password !== confirmPassword) {

            authMessage.textContent =
                "Passwords do not match.";

            return;

        }

    }


    try {

        const endpoint =
            authMode === "login"
                ? "/login"
                : "/register";


        let requestData;


        // LOGIN DATA

        if (authMode === "login") {

            requestData = {

                username: user,

                password: password

            };

        }


        // SIGN UP DATA

        else {

            requestData = {

                full_name: fullName,

                email: email,

                username: user,

                password: password

            };

        }


        authButton.disabled = true;

        authButton.textContent =
            authMode === "login"
                ? "Logging in..."
                : "Creating account...";


        const result = await apiRequest(

            endpoint,

            "POST",

            requestData

        );


        // =========================
        // REGISTRATION SUCCESS
        // =========================

        if (authMode === "register") {

            authMessage.textContent =
                "Registration successful! Please login.";

            authMessage.style.color =
                "#198754";


            // Switch to Login

            authMode = "login";


            loginTab.classList.add("active");

            registerTab.classList.remove("active");


            fullNameField.classList.add("hidden");

            emailField.classList.add("hidden");

            confirmPasswordField.classList.add("hidden");


            fullNameInput.value = "";

            emailInput.value = "";

            passwordInput.value = "";

            confirmPasswordInput.value = "";


            authButton.textContent =
                "Login";

            authButton.disabled = false;


            usernameInput.focus();


            return;

        }


        // =========================
        // LOGIN SUCCESS
        // =========================

        token = result.token;

        username =
            result.username || user;


        localStorage.setItem(

            "taskflow_token",

            token

        );


        localStorage.setItem(

            "taskflow_username",

            username

        );


        authButton.disabled = false;

        authButton.textContent =
            "Login";


        showApp();


    } catch (error) {


        authMessage.textContent =
            error.message;


        authMessage.style.color =
            "#c0392b";


        authButton.disabled = false;

        authButton.textContent =
            authMode === "login"
                ? "Login"
                : "Sign Up";

    }

});


// =========================
// SHOW APP
// =========================

function showApp() {

    authPage.classList.add("hidden");
    appPage.classList.remove("hidden");

    currentUser.textContent = username;

    loadBoards();

}


// =========================
// LOGOUT
// =========================

document
    .getElementById("logoutBtn")
    .addEventListener("click", () => {

        localStorage.removeItem("taskflow_token");
        localStorage.removeItem("taskflow_username");

        token = null;
        username = null;

        currentBoardId = null;

        appPage.classList.add("hidden");
        authPage.classList.remove("hidden");

        usernameInput.value = "";
        passwordInput.value = "";

    });


// =========================
// LOAD BOARDS
// =========================

async function loadBoards() {

    try {

        const boards = await apiRequest("/boards");

        boardsList.innerHTML = "";

        if (boards.length === 0) {

            currentBoardId = null;

            emptyState.classList.remove("hidden");
            boardView.classList.add("hidden");

            return;

        }

        boards.forEach((board) => {

            const button = document.createElement("button");

            button.className = "board-item";

            if (board.id === currentBoardId) {
                button.classList.add("active");
            }

            button.textContent = board.name;

            button.addEventListener("click", () => {
                openBoard(board.id);
            });

            boardsList.appendChild(button);

        });

        if (!currentBoardId) {
            openBoard(boards[0].id);
        }

    } catch (error) {

        console.error(error);

        if (
            error.message.includes("Token") ||
            error.message.includes("token")
        ) {

            localStorage.removeItem("taskflow_token");
            localStorage.removeItem("taskflow_username");

            location.reload();

        }

    }

}


// =========================
// OPEN BOARD
// =========================

async function openBoard(boardId) {

    try {

        currentBoardId = boardId;

        const board = await apiRequest(
            `/boards/${boardId}`
        );

        emptyState.classList.add("hidden");
        boardView.classList.remove("hidden");

        boardTitle.textContent = board.name;

        renderLists(board.lists);

        loadBoards();

    } catch (error) {

        alert(error.message);

    }

}


// =========================
// RENDER LISTS
// =========================

function renderLists(lists) {

    listsContainer.innerHTML = "";

    lists.forEach((list) => {

        const listElement =
            document.createElement("div");

        listElement.className = "task-list";

        listElement.innerHTML = `
            <div class="list-header">

                <h3>${escapeHTML(list.name)}</h3>

                <div class="list-actions">

                    <button
                        class="rename-list-btn"
                        data-list-id="${list.id}"
                        data-list-name="${escapeAttribute(list.name)}"
                    >
                        ✏
                    </button>

                    <button
                        class="delete-list-btn"
                        data-list-id="${list.id}"
                    >
                        🗑
                    </button>

                </div>

            </div>

            <div
                class="tasks"
                data-list-id="${list.id}"
            ></div>

            <button
                class="add-task-btn"
                data-list-id="${list.id}"
            >
                + Add Task
            </button>
        `;

        const tasksContainer =
            listElement.querySelector(".tasks");

        list.tasks.forEach((task) => {

            const taskElement =
                document.createElement("div");

            taskElement.className = "task-card";

            taskElement.draggable = true;

            taskElement.dataset.taskId = task.id;

            taskElement.innerHTML = `
                <h4>${escapeHTML(task.title)}</h4>

                ${
                    task.description
                        ? `<p>${escapeHTML(task.description)}</p>`
                        : ""
                }
            `;

            taskElement.addEventListener(
                "click",
                () => openEditTask(task)
            );

            taskElement.addEventListener(
                "dragstart",
                () => {

                    draggedTaskId = task.id;

                    taskElement.classList.add("dragging");

                }
            );

            taskElement.addEventListener(
                "dragend",
                () => {

                    draggedTaskId = null;

                    taskElement.classList.remove("dragging");

                    document
                        .querySelectorAll(".tasks")
                        .forEach((container) => {

                            container.classList.remove(
                                "drag-over"
                            );

                        });

                }
            );

            tasksContainer.appendChild(taskElement);

        });


        // ADD TASK

        listElement
            .querySelector(".add-task-btn")
            .addEventListener("click", () => {

                openCreateTask(list.id);

            });


        // RENAME LIST

        listElement
            .querySelector(".rename-list-btn")
            .addEventListener("click", async () => {

                const newName = prompt(
                    "Enter new list name:",
                    list.name
                );

                if (
                    newName &&
                    newName.trim()
                ) {

                    try {

                        await apiRequest(
                            `/lists/${list.id}`,
                            "PUT",
                            {
                                name: newName.trim()
                            }
                        );

                        openBoard(currentBoardId);

                    } catch (error) {

                        alert(error.message);

                    }

                }

            });


        // DELETE LIST

        listElement
            .querySelector(".delete-list-btn")
            .addEventListener("click", async () => {

                const confirmed = confirm(
                    `Delete "${list.name}" and all its tasks?`
                );

                if (!confirmed) return;

                try {

                    await apiRequest(
                        `/lists/${list.id}`,
                        "DELETE"
                    );

                    openBoard(currentBoardId);

                } catch (error) {

                    alert(error.message);

                }

            });


        // DRAG EVENTS

        tasksContainer.addEventListener(
            "dragover",
            (event) => {

                event.preventDefault();

                tasksContainer.classList.add(
                    "drag-over"
                );

            }
        );


        tasksContainer.addEventListener(
            "dragleave",
            () => {

                tasksContainer.classList.remove(
                    "drag-over"
                );

            }
        );


        tasksContainer.addEventListener(
            "drop",
            async (event) => {

                event.preventDefault();

                tasksContainer.classList.remove(
                    "drag-over"
                );

                if (!draggedTaskId) return;

                try {

                    await apiRequest(
                        `/tasks/${draggedTaskId}`,
                        "PUT",
                        {
                            list_id: list.id
                        }
                    );

                    openBoard(currentBoardId);

                } catch (error) {

                    alert(error.message);

                }

            }
        );


        listsContainer.appendChild(
            listElement
        );

    });

}


// =========================
// CREATE BOARD
// =========================

function openBoardModal() {

    boardNameInput.value = "";

    boardModal.classList.remove("hidden");

    boardNameInput.focus();

}


document
    .getElementById("newBoardBtn")
    .addEventListener("click", openBoardModal);


document
    .getElementById("emptyCreateBoard")
    .addEventListener("click", openBoardModal);


document
    .getElementById("createBoardConfirm")
    .addEventListener("click", async () => {

        const name =
            boardNameInput.value.trim();

        if (!name) {

            alert("Please enter a board name");

            return;

        }

        try {

            const board = await apiRequest(
                "/boards",
                "POST",
                {
                    name: name
                }
            );

            boardModal.classList.add("hidden");

            currentBoardId = board.id;

            await loadBoards();

            openBoard(board.id);

        } catch (error) {

            alert(error.message);

        }

    });


// =========================
// DELETE BOARD
// =========================

document
    .getElementById("deleteBoardBtn")
    .addEventListener("click", async () => {

        if (!currentBoardId) return;

        const confirmed = confirm(
            "Are you sure you want to delete this board?"
        );

        if (!confirmed) return;

        try {

            await apiRequest(
                `/boards/${currentBoardId}`,
                "DELETE"
            );

            currentBoardId = null;

            await loadBoards();

        } catch (error) {

            alert(error.message);

        }

    });


// =========================
// CREATE LIST
// =========================

document
    .getElementById("addListBtn")
    .addEventListener("click", () => {

        listNameInput.value = "";

        listModal.classList.remove("hidden");

        listNameInput.focus();

    });


document
    .getElementById("createListConfirm")
    .addEventListener("click", async () => {

        const name =
            listNameInput.value.trim();

        if (!name) {

            alert("Please enter a list name");

            return;

        }

        try {

            await apiRequest(
                "/lists",
                "POST",
                {
                    board_id: currentBoardId,
                    name: name
                }
            );

            listModal.classList.add("hidden");

            openBoard(currentBoardId);

        } catch (error) {

            alert(error.message);

        }

    });


// =========================
// TASK MODAL
// =========================

function openCreateTask(listId) {

    currentTaskId = null;

    currentTaskListId = listId;

    taskModalTitle.textContent =
        "Create Task";

    taskTitleInput.value = "";

    taskDescriptionInput.value = "";

    deleteTaskBtn.classList.add("hidden");

    taskModal.classList.remove("hidden");

    taskTitleInput.focus();

}


function openEditTask(task) {

    currentTaskId = task.id;

    currentTaskListId = task.list_id;

    taskModalTitle.textContent =
        "Edit Task";

    taskTitleInput.value = task.title;

    taskDescriptionInput.value =
        task.description || "";

    deleteTaskBtn.classList.remove("hidden");

    taskModal.classList.remove("hidden");

}


// =========================
// SAVE TASK
// =========================

document
    .getElementById("saveTaskBtn")
    .addEventListener("click", async () => {

        const title =
            taskTitleInput.value.trim();

        const description =
            taskDescriptionInput.value.trim();

        if (!title) {

            alert("Task title is required");

            return;

        }

        try {

            if (currentTaskId) {

                await apiRequest(
                    `/tasks/${currentTaskId}`,
                    "PUT",
                    {
                        title: title,
                        description: description
                    }
                );

            } else {

                await apiRequest(
                    "/tasks",
                    "POST",
                    {
                        list_id: currentTaskListId,
                        title: title,
                        description: description
                    }
                );

            }

            taskModal.classList.add("hidden");

            openBoard(currentBoardId);

        } catch (error) {

            alert(error.message);

        }

    });


// =========================
// DELETE TASK
// =========================

deleteTaskBtn.addEventListener(
    "click",
    async () => {

        if (!currentTaskId) return;

        const confirmed = confirm(
            "Delete this task?"
        );

        if (!confirmed) return;

        try {

            await apiRequest(
                `/tasks/${currentTaskId}`,
                "DELETE"
            );

            taskModal.classList.add("hidden");

            openBoard(currentBoardId);

        } catch (error) {

            alert(error.message);

        }

    }
);


// =========================
// CLOSE MODALS
// =========================

document
    .querySelectorAll("[data-close]")
    .forEach((button) => {

        button.addEventListener(
            "click",
            () => {

                const modalId =
                    button.dataset.close;

                document
                    .getElementById(modalId)
                    .classList.add("hidden");

            }
        );

    });


// =========================
// ESCAPE HTML
// =========================

function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;

}


function escapeAttribute(text) {

    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/"/g, "&quot;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");

}


// =========================
// AUTO LOGIN
// =========================

if (token && username) {

    showApp();

}