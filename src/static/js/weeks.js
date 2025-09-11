// Объект для отслеживания загруженных недель
const loadedWeeks = new Set();

function loadWeekDays(button) {
    const weekStart = button.getAttribute("data-week-start");
    const weekIndex = button.getAttribute("data-week-index");
    const contentDiv = document.getElementById(`week-content-${weekIndex}`);

    // Если данные уже загружены, не загружаем повторно
    if (loadedWeeks.has(weekIndex)) {
        return;
    }

    // Отмечаем как загружаемую
    loadedWeeks.add(weekIndex);

    // Выполняем AJAX запрос для получения дней недели
    fetch(`/api/weeks/${weekStart}/days`, {
        method: "GET",
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
        },
        credentials: "include", // Включаем куки для авторизации
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then((data) => {
            // Рендерим полученные данные
            renderWeekDays(contentDiv, data, weekIndex);
        })
        .catch((error) => {
            console.error("Ошибка загрузки данных недели:", error);
            // Показываем ошибку пользователю
            contentDiv.innerHTML = `
            <div class="alert alert-danger">
                <h6>Ошибка загрузки данных</h6>
                <p>Не удалось загрузить данные за неделю. Попробуйте обновить страницу.</p>
                <button class="btn btn-sm btn-outline-danger" onclick="retryLoadWeek('${weekStart}', '${weekIndex}')">
                    Попробовать снова
                </button>
            </div>
        `;
            // Убираем из загруженных, чтобы можно было попробовать снова
            loadedWeeks.delete(weekIndex);
        });
}

function retryLoadWeek(weekStart, weekIndex) {
    loadedWeeks.delete(weekIndex);
    const button = document.querySelector(`[data-week-index="${weekIndex}"]`);
    loadWeekDays(button);
}

function renderWeekDays(container, weekData, weekIndex) {
    if (!weekData.days || weekData.days.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <p class="mb-0">За эту неделю записей пока нет</p>
            </div>
        `;
        return;
    }

    let daysHtml = `
        <div class="row">
            <div class="col-md-8">
                <div class="accordion" id="days-accordion-${weekIndex}">
    `;

    weekData.days.forEach((day, dayIndex) => {
        daysHtml += `
            <div class="accordion-item">
                <div class="accordion-header">
                    <button class="accordion-button collapsed"
                            type="button"
                            data-bs-toggle="collapse"
                            data-bs-target="#day-${weekIndex}-${dayIndex}">
                        <div class="d-flex justify-content-between w-100">
                            <span><strong>${day.calendar_date}</strong></span>
                            <span class="badge bg-info me-3">${day.sleep_efficiency}%</span>
                        </div>
                    </button>
                </div>
                <div id="day-${weekIndex}-${dayIndex}"
                     class="accordion-collapse collapse"
                     data-bs-parent="#days-accordion-${weekIndex}">
                    <div class="accordion-body">
                        <div class="row">
                            <div class="col-sm-6">
                                <p><strong>Лег в:</strong> ${day.bedtime}</p>
                                <p><strong>Уснул в:</strong> ${day.asleep}</p>
                                <p><strong>Проснулся в:</strong> ${day.awake}</p>
                                <p><strong>Встал в:</strong> ${day.rise}</p>
                            </div>
                            <div class="col-sm-6">
                                <p><strong>Время сна:</strong> ${day.sleep_duration}</p>
                                <p><strong>Время в кровати:</strong> ${day.in_bed_duration}</p>
                                <p><strong>Не спал:</strong> ${day.without_sleep} мин</p>
                                <p><strong>Эффективность:</strong> ${day.sleep_efficiency}%</p>
                            </div>
                        </div>
                        <div class="mt-3">
                            <a href="/sleep/update/${day.calendar_date}" class="btn btn-sm btn-success">
                                Редактировать
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    daysHtml += `
                </div>
            </div>
            <div class="col-md-4">
                <div class="card">
                    <div class="card-header">
                        <h6>Статистика за неделю</h6>
                    </div>
                    <div class="card-body">
                        <p><strong>Средняя эффективность:</strong><br>
                           <span class="h4">${weekData.stats.average_sleep_efficiency}%</span></p>
                        <p><strong>Среднее время сна:</strong><br>
                           <span class="h5">${weekData.stats.average_sleep_duration}</span></p>
                        <p><strong>Среднее время в кровати:</strong><br>
                           <span class="h5">${weekData.stats.average_time_in_bed}</span></p>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = daysHtml;
}
