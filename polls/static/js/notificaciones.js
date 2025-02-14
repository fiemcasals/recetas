document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".btn-toggle-notificacion").forEach(button => {
        button.addEventListener("click", function () {
            const notificacionId = this.dataset.id;

            fetch(`/notificaciones/marcar_leida/${notificacionId}/`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.nuevo_estado !== undefined) {
                    const item = document.querySelector(`#notificacion-${notificacionId}`);
                    const boton = item.querySelector("button");

                    if (data.nuevo_estado) {
                        item.classList.remove("nueva");
                        item.classList.add("leida");
                        boton.textContent = "Marcar como Nueva";
                    } else {
                        item.classList.remove("leida");
                        item.classList.add("nueva");
                        boton.textContent = "Marcar como Leída";
                    }
                }
            })
            .catch(error => console.error('Error al actualizar notificación:', error));
        });
    });
});
