function sendPatch(event, noteDate) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const url = window.EDIT_NOTE_URL.replace("__NOTE_DATE__", noteDate);

    fetch(url, {
        method: "PATCH",
        body: formData,
        credentials: "include",
    })
        .then((response) => {
            if (!response.redirected) return;
            window.location.href = response.url;
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Ошибка при обновлении записи");
        });

    return false;
}

function showEditForm(noteDate, weekIndex, dayIndex, wentToBed, fellAsleep, wokeUp, gotUp, noSleep) {
    const editForm = document.getElementById(`edit-form-${weekIndex}-${dayIndex}`);
    const button = event.target;

    if (editForm.style.display === "none") {
        editForm.style.display = "block";
        button.textContent = "Скрыть форму";
    } else {
        editForm.style.display = "none";
        button.textContent = "Редактировать";
    }
}

function hideEditForm(weekIndex, dayIndex) {
    const editForm = document.getElementById(`edit-form-${weekIndex}-${dayIndex}`);
    const button = editForm.parentElement.querySelector(".btn-warning");

    editForm.style.display = "none";
    button.textContent = "Редактировать";
}
