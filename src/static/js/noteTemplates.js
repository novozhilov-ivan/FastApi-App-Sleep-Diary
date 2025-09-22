const NOTE_TEMPLATES = {
    dayWithNote: (note, weekIndex, dayIndex, dayName, efficiency, formatTime) => `
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
                        <a href="/sleep/edit/${note.bedtime_date}" class="btn btn-sm btn-warning">
                            Редактировать
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `,

    dayWithoutNote: (dayName, dateStr, weekIndex, dayIndex) => `
        <div class="accordion-item">
            <div class="accordion-header">
                <button class="accordion-button collapsed"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#day-${weekIndex}-${dayIndex}">
                    <div class="d-flex justify-content-between align-items-center w-100">
                        <span class="text-muted"><strong>${dayName}</strong> - Запись отсутствует</span>
                        <span class="badge bg-secondary">Добавить</span>
                    </div>
                </button>
            </div>
            <div id="day-${weekIndex}-${dayIndex}"
                 class="accordion-collapse collapse"
                 data-bs-parent="#days-accordion-${weekIndex}">
                <div class="accordion-body">
                    <div class="alert alert-info">
                        <h6>Добавить запись за ${dayName} (${dateStr})</h6>
                    </div>
                    <div class="sleep-form-container">
                        <div class="row justify-content-center mb-3">
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small" for="bedtime_${weekIndex}_${dayIndex}">Лег в кровать</label>
                                <input required
                                       type="time"
                                       id="bedtime_${weekIndex}_${dayIndex}"
                                       class="form-control text-center"
                                       value="23:00" />
                            </div>
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small" for="asleep_${weekIndex}_${dayIndex}">Уснул в</label>
                                <input required
                                       type="time"
                                       id="asleep_${weekIndex}_${dayIndex}"
                                       class="form-control text-center"
                                       value="23:30" />
                            </div>
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small" for="awake_${weekIndex}_${dayIndex}">Проснулся в</label>
                                <input required
                                       type="time"
                                       id="awake_${weekIndex}_${dayIndex}"
                                       class="form-control text-center"
                                       value="07:00" />
                            </div>
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small" for="rise_${weekIndex}_${dayIndex}">Встал с кровати</label>
                                <input required
                                       type="time"
                                       id="rise_${weekIndex}_${dayIndex}"
                                       class="form-control text-center"
                                       value="07:30" />
                            </div>
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small" for="without_sleep_${weekIndex}_${dayIndex}">Время без сна</label>
                                <input required
                                       type="time"
                                       id="without_sleep_${weekIndex}_${dayIndex}"
                                       class="form-control text-center"
                                       value="00:00" />
                            </div>
                        </div>
                        <div class="row justify-content-center">
                            <div class="col-md-6 text-center">
                                <button type="button" onclick="saveInlineEntry('${dateStr}', ${weekIndex}, ${dayIndex})" class="btn btn-success me-2">
                                    Сохранить запись
                                </button>
                                <button type="button" onclick="clearInlineForm(${weekIndex}, ${dayIndex})" class="btn btn-outline-secondary">
                                    Очистить
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `,

    weekStats: () => `
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
    `,

    noDataAlert: () => `
        <div class="alert alert-info">
            <p class="mb-0">За эту неделю записей пока нет</p>
        </div>
    `,

    loadingSpinner: () => `
        <div class="text-center p-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Загружаем записи за неделю...</span>
            </div>
            <p class="mt-2 text-muted">Загружаем записи за неделю...</p>
        </div>
    `,

    errorAlert: (weekStart, weekIndex) => `
        <div class="alert alert-danger">
            <h6>Ошибка загрузки данных</h6>
            <p>Не удалось загрузить данные за неделю. Попробуйте обновить страницу.</p>
            <button class="btn btn-sm btn-outline-danger" onclick="retryLoadWeek('${weekStart}', '${weekIndex}')">
                Попробовать снова
            </button>
        </div>
    `,
};
