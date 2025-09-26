function renderWeekDays(container, weekData, weekIndex) {
    if (!weekData.week_notes || weekData.week_notes.length === 0) {
        container.innerHTML = NOTE_TEMPLATES.noDataAlert();
        return;
    }

    const daysOfWeek = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"];
    const notesByWeekday = {};

    let weekStartDate;
    if (weekData.week_start_date) {
        weekStartDate = new Date(weekData.week_start_date);
    } else if (weekData.week_notes && weekData.week_notes.length > 0) {
        const firstNoteDate = new Date(weekData.week_notes[0].bedtime_date);
        const dayOfWeek = (firstNoteDate.getDay() + 6) % 7;
        weekStartDate = new Date(firstNoteDate);
        weekStartDate.setDate(firstNoteDate.getDate() - dayOfWeek);
    } else {
        weekStartDate = new Date();
        const dayOfWeek = (weekStartDate.getDay() + 6) % 7;
        weekStartDate.setDate(weekStartDate.getDate() - dayOfWeek);
    }

    weekData.week_notes.forEach((note) => {
        const date = new Date(note.bedtime_date);
        const weekday = (date.getDay() + 6) % 7;
        notesByWeekday[weekday] = note;
    });

    const formatTime = (timeStr) => timeStr.substring(0, 5);

    let daysHtml = `
        <div class="row">
            <div class="col-12">
                <div class="accordion" id="days-accordion-${weekIndex}">
    `;

    for (let dayIndex = 0; dayIndex < 7; dayIndex++) {
        const dayName = daysOfWeek[dayIndex];
        const note = notesByWeekday[dayIndex];

        if (note) {
            const efficiency = (note.statistics_sleep_efficiency * 100).toFixed(1);
            daysHtml += NOTE_TEMPLATES.dayWithNote(note, weekIndex, dayIndex, dayName, efficiency, formatTime);
        } else {
            const currentDate = new Date(weekStartDate);
            currentDate.setDate(weekStartDate.getDate() + dayIndex);
            const dateStr = currentDate.toISOString().split("T")[0];
            daysHtml += NOTE_TEMPLATES.dayWithoutNote(dayName, dateStr, weekIndex, dayIndex);
        }
    }

    daysHtml += `
                </div>
            </div>
        </div>
    `;

    container.innerHTML = daysHtml;
}
