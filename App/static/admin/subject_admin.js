document.addEventListener('DOMContentLoaded', function() {
    const courseSelect = document.getElementById('id_course');
    const semesterSelect = document.getElementById('id_semester');

    courseSelect.addEventListener('change', function() {
        const courseId = this.value;
        fetch(`admin/get_semesters/?course_id=${courseId}`)
            .then(response => response.json())
            .then(data => {
                semesterSelect.innerHTML = '';
                data.semesters.forEach(semester => {
                    const option = document.createElement('option');
                    option.value = semester.id;
                    option.textContent = `Semester ${semester.number}`;
                    semesterSelect.appendChild(option);
                });
            });
    });
});