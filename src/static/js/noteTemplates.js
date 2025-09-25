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
                        <button onclick="showEditForm('${note.bedtime_date}', ${weekIndex}, ${dayIndex}, '${formatTime(note.went_to_bed)}', '${formatTime(note.fell_asleep)}', '${formatTime(note.woke_up)}', '${formatTime(note.got_up)}', '${formatTime(note.no_sleep)}')" class="btn btn-sm btn-warning">
                            Редактировать
                        </button>
                    </div>
                    <div id="edit-form-${weekIndex}-${dayIndex}" style="display: none;" class="mt-3">
                        <hr>
                        <h6>Редактировать запись</h6>
                        <form onsubmit="return sendPatch(event, '${note.bedtime_date}')">
                            <div class="row justify-content-center mb-3">
                                <div class="col-6 col-lg-2 mb-3">
                                    <label class="form-label fw-bold small">Лег в кровать</label>
                                    <input required type="time" name="went_to_bed" class="form-control text-center" value="${formatTime(note.went_to_bed)}" />
                                </div>
                                <div class="col-6 col-lg-2 mb-3">
                                    <label class="form-label fw-bold small">Уснул в</label>
                                    <input required type="time" name="fell_asleep" class="form-control text-center" value="${formatTime(note.fell_asleep)}" />
                                </div>
                                <div class="col-6 col-lg-2 mb-3">
                                    <label class="form-label fw-bold small">Проснулся в</label>
                                    <input required type="time" name="woke_up" class="form-control text-center" value="${formatTime(note.woke_up)}" />
                                </div>
                                <div class="col-6 col-lg-2 mb-3">
                                    <label class="form-label fw-bold small">Встал с кровати</label>
                                    <input required type="time" name="got_up" class="form-control text-center" value="${formatTime(note.got_up)}" />
                                </div>
                                <div class="col-6 col-lg-2 mb-3">
                                    <label class="form-label fw-bold small">Время без сна</label>
                                    <input required type="time" name="no_sleep" class="form-control text-center" value="${formatTime(note.no_sleep)}" />
                                </div>
                            </div>
                            <div class="row justify-content-center">
                                <div class="col-md-6 text-center">
                                    <button type="submit" class="btn btn-warning me-2">Обновить запись</button>
                                    <button type="button" onclick="hideEditForm(${weekIndex}, ${dayIndex})" class="btn btn-outline-secondary">Отмена</button>
                                </div>
                            </div>
                        </form>
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
                    <form method="post" action="${window.ADD_NOTE_URL}">
                        <input type="hidden" name="bedtime_date" value="${dateStr}" />
                        <div class="row justify-content-center mb-3">
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small">Лег в кровать</label>
                                <input required type="time" name="went_to_bed" class="form-control text-center" value="23:00" />
                            </div>
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small">Уснул в</label>
                                <input required type="time" name="fell_asleep" class="form-control text-center" value="23:30" />
                            </div>
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small">Проснулся в</label>
                                <input required type="time" name="woke_up" class="form-control text-center" value="07:00" />
                            </div>
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small">Встал с кровати</label>
                                <input required type="time" name="got_up" class="form-control text-center" value="07:30" />
                            </div>
                            <div class="col-6 col-lg-2 mb-3">
                                <label class="form-label fw-bold small">Время без сна</label>
                                <input required type="time" name="no_sleep" class="form-control text-center" value="00:00" />
                            </div>
                        </div>
                        <div class="row justify-content-center">
                            <div class="col-md-6 text-center">
                                <button type="submit" class="btn btn-success me-2">Сохранить запись</button>
                                <button type="reset" class="btn btn-outline-secondary">Очистить</button>
                            </div>
                        </div>
                    </form>
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
