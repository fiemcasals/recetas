function marcarFavorito(event, recetaId) {
    event.preventDefault(); // Evita el envío del formulario

    const formulario = document.querySelector(`#favorito-form-${recetaId}`);
    const csrfToken = formulario.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/marcar_favorito/${recetaId}/`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.nuevo_estado !== undefined) {
            const icono = document.querySelector(`#icono-favorito-${recetaId}`);
            const texto = document.querySelector(`#texto-favorito-${recetaId}`);

            if (data.nuevo_estado) {
                icono.classList.remove('fa-heart-o', 'green');
                icono.classList.add('fa-heart', 'red');
                texto.textContent = "¡Seleccionado como Favorito!";
            } else {
                icono.classList.remove('fa-heart', 'red');
                icono.classList.add('fa-heart-o', 'green');
                texto.textContent = "¿Favorito?";
            }
        }
    })
    .catch(error => console.error('Error al marcar como favorito:', error));
}
