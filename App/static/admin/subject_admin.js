document.addEventListener('DOMContentLoaded', function() {
    const courseSelect = document.getElementById('id_course');
    const semesterSelect = document.getElementById('id_semester');

    if (courseSelect) {
        courseSelect.addEventListener('change', function() {
            const courseId = this.value;
            console.log(`Course selected: ${courseId}`); // Debugging step
            fetch(`/admin/get_semesters/?course_id=${courseId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Semesters fetched:', data); // Debugging step
                    semesterSelect.innerHTML = '';
                    data.semesters.forEach(semester => {
                        const option = document.createElement('option');
                        option.value = semester.id;
                        option.textContent = `Semester ${semester.number}`;
                        semesterSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error); // Debugging step
                });
        });
    } else {
        console.error('Course select element not found'); // Debugging step
    }
});