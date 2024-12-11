function verImagem(event) {
    const reader = new FileReader();
    reader.onload = function () {
        const preview = document.getElementById('preview');
        preview.src = reader.result;
        preview.classList.remove('d-none');
    };
    reader.readAsDataURL(event.target.files[0]);
}