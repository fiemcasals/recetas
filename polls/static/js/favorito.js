// Función que maneja la acción de marcar o desmarcar un favorito
function marcarFavorito(event, recetaId) {
    // Prevenir el comportamiento por defecto del formulario (enviar la solicitud)
    event.preventDefault(); // Evita el envío del formulario

    // Seleccionamos el formulario que contiene el botón de favorito, utilizando el ID dinámico de la receta
    const formulario = document.querySelector(`#favorito-form-${recetaId}`);
    
    // Obtenemos el token CSRF necesario para la validación de seguridad del formulario
    const csrfToken = formulario.querySelector('[name=csrfmiddlewaretoken]').value;

    // Realizamos una solicitud POST al servidor para marcar o desmarcar la receta como favorito
    fetch(`/marcar_favorito/${recetaId}/`, {
        method: 'POST',  // Indicamos que es una solicitud POST
        headers: {
            "Content-Type": "application/json",  // El tipo de contenido que estamos enviando es JSON
            "X-CSRFToken": csrfToken  // Incluir el token CSRF en los encabezados para la seguridad
        }
    })
    // Procesamos la respuesta del servidor
    .then(response => response.json())  // Convertimos la respuesta a formato JSON
    .then(data => {
        // Verificamos si la respuesta contiene el estado del nuevo favorito
        if (data.nuevo_estado !== undefined) {
            // Seleccionamos el ícono del favorito y el texto correspondiente a la receta
            const icono = document.querySelector(`#icono-favorito-${recetaId}`);
            const texto = document.querySelector(`#texto-favorito-${recetaId}`);

            // Verificamos que el nuevo estado sea un valor booleano (true o false)
            const nuevoEstado = Boolean(data.nuevo_estado);  // Convertimos el estado a un booleano

            // Si el estado es verdadero (favorito seleccionado)
            if (nuevoEstado) {
                // Cambiamos la clase del ícono para mostrar un corazón lleno (rojo)
                icono.classList.remove('fa-heart-o', 'green');  // Eliminamos las clases anteriores (corazón vacío y verde)
                icono.classList.add('fa-heart', 'red');  // Añadimos las clases para corazón lleno y color rojo
                texto.textContent = "¡Seleccionado como Favorito!";  // Actualizamos el texto al mensaje de favorito
            } else {
                // Si el estado es falso (favorito desmarcado)
                icono.classList.remove('fa-heart', 'red');  // Eliminamos las clases anteriores (corazón lleno y rojo)
                icono.classList.add('fa-heart-o', 'green');  // Añadimos las clases para corazón vacío y color verde
                texto.textContent = "¿Favorito?";  // Actualizamos el texto a la pregunta original
            }
        }
    })
    // Si ocurre algún error en la solicitud, lo mostramos en la consola
    .catch(error => console.error('Error al marcar como favorito:', error));  // Mostramos el error si algo sale mal
}
