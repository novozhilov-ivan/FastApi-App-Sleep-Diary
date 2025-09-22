function saveSleepEntry() {
    const formData = getFormData();

    fetch("/notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
    })
        .then(handleApiResponse)
        .then((data) => {
            alert("Запись успешно сохранена!");
            clearForm();
            location.reload();
        })
        .catch(handleApiError);
}

function updateSleepEntry() {
    const noteDate = document.getElementById("calendar_date").value;
    const formData = getFormData();

    fetch(`/notes/${noteDate}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
    })
        .then(handleApiResponse)
        .then((data) => {
            alert("Запись успешно обновлена!");
            window.location.href = "/weeks";
        })
        .catch(handleApiError);
}

function deleteSleepEntry() {
    if (!confirm("Вы уверены, что хотите удалить эту запись?")) {
        return;
    }

    const noteDate = document.getElementById("calendar_date").value;

    fetch(`/notes/${noteDate}`, {
        method: "DELETE",
        headers: {
            Accept: "application/json",
        },
        credentials: "include",
    })
        .then(handleApiResponse)
        .then((data) => {
            alert("Запись успешно удалена!");
            window.location.href = "/weeks";
        })
        .catch(handleApiError);
}

function getFormData() {
    return {
        bedtime_date: document.getElementById("calendar_date").value,
        went_to_bed: document.getElementById("bedtime").value,
        fell_asleep: document.getElementById("asleep").value,
        woke_up: document.getElementById("awake").value,
        got_up: document.getElementById("rise").value,
        no_sleep: document.getElementById("without_sleep").value,
    };
}

function clearForm() {
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("calendar_date").value = today;
    document.getElementById("bedtime").value = "23:00";
    document.getElementById("asleep").value = "23:30";
    document.getElementById("awake").value = "07:00";
    document.getElementById("rise").value = "07:30";
    document.getElementById("without_sleep").value = "00:00";
}

function saveInlineEntry(date, weekIndex, dayIndex) {
    const formData = {
        bedtime_date: date,
        went_to_bed: document.getElementById(`bedtime_${weekIndex}_${dayIndex}`).value,
        fell_asleep: document.getElementById(`asleep_${weekIndex}_${dayIndex}`).value,
        woke_up: document.getElementById(`awake_${weekIndex}_${dayIndex}`).value,
        got_up: document.getElementById(`rise_${weekIndex}_${dayIndex}`).value,
        no_sleep: document.getElementById(`without_sleep_${weekIndex}_${dayIndex}`).value,
    };

    fetch("/ui/notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
        },
        credentials: "include",
        body: JSON.stringify(formData),
    })
        .then(handleApiResponse)
        .then((data) => {
            alert("Запись успешно сохранена!");
            location.reload();
        })
        .catch(handleApiError);
}

function clearInlineForm(weekIndex, dayIndex) {
    document.getElementById(`bedtime_${weekIndex}_${dayIndex}`).value = "23:00";
    document.getElementById(`asleep_${weekIndex}_${dayIndex}`).value = "23:30";
    document.getElementById(`awake_${weekIndex}_${dayIndex}`).value = "07:00";
    document.getElementById(`rise_${weekIndex}_${dayIndex}`).value = "07:30";
    document.getElementById(`without_sleep_${weekIndex}_${dayIndex}`).value = "00:00";
}

function handleApiResponse(response) {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
}

function handleApiError(error) {
    console.error("Error:", error);
    alert("Произошла ошибка при выполнении операции");
}
