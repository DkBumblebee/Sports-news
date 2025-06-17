function editTask(taskId, taskDescription) {
    // This function is called when the "Edit" button is clicked.
    // It populates the edit form with the task's ID and description
    // and shows the edit form while hiding the add task form.

    document.getElementById('editTaskId').value = taskId;
    document.getElementById('editTaskDescription').value = taskDescription;
    document.getElementById('taskForm').style.display = 'none'; // Hides the addTask form
    document.getElementById('editTaskForm').style.display = 'block'; // Shows the editTask form 
}

function cancelEdit() {
    // This function is called when the "Cancel" button in the edit form is clicked.
    // It hides the edit form and shows the add task form.
    document.getElementById('taskForm').style.display = 'block';
    document.getElementById('editTaskForm').style.display = 'none';
}

function deleteTask(taskId) {
    // This function is called when the "Delete" button is clicked.
    // It confirms the deletion with the user and then sends a POST request
    // to the server to delete the task from the database.
    if (confirm("Are you sure you want to delete this task?")) {
        fetch('/delete_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'task_id=' + taskId,
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Error deleting task:', response.status);
                alert("Error deleting task. Please try again.");
            }
        })
        .catch(error => {
            console.error('Error deleting task:', error);
            alert("An error occurred. Please try again later.");
        });
    }
}

document.getElementById("addTaskForm").addEventListener("submit", function(event) {
    // This event listener is attached to the "Add Task" form's submit event.
    // It prevents the default form submission behavior (page reload) and
    // instead submits the form data using JavaScript (via AJAX or similar).("Hope you under stand this part...")


    event.preventDefault(); // Prevent default form submission
    const newTaskInput = document.getElementById("newTask");
    const newTask = newTaskInput.value;

    if (newTask.trim() !== "") { // Check if the task is not empty or just whitespace
        this.submit(); // Submit the form if the task is valid
        newTaskInput.value = ""; // Clear the input field
    } else {
        alert("Please enter a task."); // Alert the user to enter a task
    }
});
