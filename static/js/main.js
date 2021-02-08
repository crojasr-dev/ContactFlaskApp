const btnDelete = document.querySelectorAll('.btn-delete')

if (btnDelete) {
    const btn_array = Array.from(btnDelete);
    btn_array.forEach((btn) => {
        btn.addEventListener('click', (e) => {
            if (!confirm('estas seguro?')) {
                e.preventDefault();
            }
        })
    });
}