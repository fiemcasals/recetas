class Cocinado {
    constructor(recetaId) {
        this.recetaId = recetaId;
        this.button = document.querySelector(`#cocinado-btn-${recetaId}`);
        this.texto = document.querySelector(`#texto-cocinado-${recetaId}`);
        this.csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    }

    marcarCocinado(event) {
        event.preventDefault(); // Evita que el formulario se envíe

        // Cambiar el color del botón y el texto
        this.button.style.backgroundColor = "green";
        this.texto.textContent = "¡Receta Cocinada!";

        // Hacer la solicitud para registrar el cocinado
        this.registrarCocinado();
    }

    registrarCocinado() {
        fetch(`/receta/${this.recetaId}/cocinado/`, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": this.csrfToken
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.mensaje) {
                // Esperar 10 segundos y luego volver al estado original
                setTimeout(() => {
                    this.button.style.backgroundColor = ""; // Restaurar el fondo
                    this.texto.textContent = "Marcar como Cocinado"; // Restaurar el texto
                }, 10000); // Esperar 10 segundos antes de volver a la normalidad
            }
        })
        .catch(error => console.error('Error al registrar el cocinado:', error));
    }
}
