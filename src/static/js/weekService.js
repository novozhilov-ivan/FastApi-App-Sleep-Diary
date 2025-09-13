const loadedWeeks = new Set();

function loadWeekDays(button) {
    const weekStart = button.getAttribute("data-week-start");
    const weekIndex = button.getAttribute("data-week-index");
    const contentDiv = document.getElementById(`week-content-${weekIndex}`);

    if (loadedWeeks.has(weekIndex)) {
        return;
    }

    loadedWeeks.add(weekIndex);

    fetch(`/api/weeks/${weekStart}`, {
        method: "GET",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        credentials: "include",
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            try {
                renderWeekDays(contentDiv, data, weekIndex);
            } catch (error) {
                contentDiv.innerHTML = `
                <div class="alert alert-danger">
                    <h6>Ошибка обработки данных</h6>
                    <p>Данные получены, но произошла ошибка при отображении.</p>
                </div>
            `;
                loadedWeeks.delete(weekIndex);
            }
        })
        .catch((error) => {
            contentDiv.innerHTML = `
            <div class="alert alert-danger">
                <h6>Ошибка загрузки данных</h6>
                <p>Не удалось загрузить данные за неделю. Попробуйте обновить страницу.</p>
                <button class="btn btn-sm btn-outline-danger" onclick="retryLoadWeek('${weekStart}', '${weekIndex}')">
                    Попробовать снова
                </button>
            </div>
        `;
            loadedWeeks.delete(weekIndex);
        });
}

function retryLoadWeek(weekStart, weekIndex) {
    loadedWeeks.delete(weekIndex);
    const button = document.querySelector(`[data-week-index="${weekIndex}"]`);
    loadWeekDays(button);
}
