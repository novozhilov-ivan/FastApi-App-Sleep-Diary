function renderWeekDays(container, weekData, weekIndex) {
    if (!weekData.week_notes || weekData.week_notes.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <p class="mb-0">За эту неделю записей пока нет</p>
            </div>
        `;
        return;
    }

    const daysOfWeek = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"];
    const notesByWeekday = {};

    weekData.week_notes.forEach((note) => {
        const date = new Date(note.bedtime_date);
        const weekday = (date.getDay() + 6) % 7;
        notesByWeekday[weekday] = note;
    });

    let daysHtml = `
        <div class="row">
            <div class="col-md-8">
                <div class="accordion" id="days-accordion-${weekIndex}">
    `;

    for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
        const dayName = daysOfWeek[dayIndex];
        const note = notesByWeekday[dayIndex];

        if (note) {
            const efficiency = (note.statistics_sleep_efficiency * 100).toFixed(1);
            const formatTime = (timeStr) => timeStr.substring(0, 5);

            daysHtml += `
                <div class="accordion-item">
                    <div class="accordion-header">
                        <button class="accordion-button collapsed"
                                type="button"
                                data-bs-toggle="collapse"
                                data-bs-target="#day-${weekIndex}-${dayIndex}">
                            <div class="d-flex justify-content-between w-100">
                                <span><strong>${dayName} ${note.bedtime_date}</strong></span>
                                <span class="badge bg-info me-3">${efficiency}%</span>
                            </div>
                        </button>
                    </div>
                    <div id="day-${weekIndex}-${dayIndex}"
                         class="accordion-collapse collapse"
                         data-bs-parent="#days-accordion-${weekIndex}">
                        <div class="accordion-body">
                            <div class="row">
                                <div class="col-sm-6">
                                    <p><strong>Лег в:</strong> ${formatTime(note.went_to_bed)}</p>
                                    <p><strong>Уснул в:</strong> ${formatTime(note.fell_asleep)}</p>
                                    <p><strong>Проснулся в:</strong> ${formatTime(note.woke_up)}</p>
                                    <p><strong>Встал в:</strong> ${formatTime(note.got_up)}</p>
                                </div>
                                <div class="col-sm-6">
                                    <p><strong>Время сна:</strong> ${formatTime(note.statistics_sleep)}</p>
                                    <p><strong>Время в кровати:</strong> ${formatTime(note.statistics_in_bed)}</p>
                                    <p><strong>Не спал:</strong> ${formatTime(note.no_sleep)}</p>
                                    <p><strong>Эффективность:</strong> ${efficiency}%</p>
                                </div>
                            </div>
                            <div class="mt-3">
                                <a href="/weeks/${note.bedtime_date}" class="btn btn-sm btn-success">
                                    Редактировать
                                </a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } else {
            daysHtml += `
                <div class="accordion-item">
                    <div class="accordion-header">
                        <div class="accordion-button collapsed bg-light">
                            <div class="d-flex justify-content-between align-items-center w-100">
                                <span class="text-muted"><strong>${dayName}</strong> - Запись отсутствует</span>
                                <button class="btn btn-outline-primary btn-sm" disabled>
                                    Добавить запись
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }
    }

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
                           <span class="h4">В разработке</span></p>
                        <p><strong>Среднее время сна:</strong><br>
                           <span class="h5">В разработке</span></p>
                        <p><strong>Среднее время в кровати:</strong><br>
                           <span class="h5">В разработке</span></p>
                    </div>
                </div>
            </div>
        </div>
    `;

    container.innerHTML = daysHtml;
}
