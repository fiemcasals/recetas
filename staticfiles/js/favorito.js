document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".favorito").forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault(); // Evita la recarga de la página
            event.stopPropagation(); // Evita que el navegador siga el enlace JSON

            var recetaId = this.dataset.recetaId;
            var csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute("content");

            fetch(`/marcar_favorito/${recetaId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/json"
                },
                credentials: 'same-origin', 
                body: JSON.stringify({})
            })
            .then(response => response.json()) 
            .then(data => {
                if (data.status === "success") {
                    // Aquí verificamos el estado del favorito y cambiamos el icono
                    var icon = this.querySelector('i'); // Encontramos el ícono en el botón
                    if (data.new_state) {
                        icon.classList.remove('fa-heart-o'); // Removemos el corazón vacío
                        icon.classList.add('fa-heart'); // Agregamos el corazón lleno
                        icon.style.color = 'red'; // Cambiamos el color a rojo
                    } else {
                        icon.classList.remove('fa-heart'); // Removemos el corazón lleno
                        icon.classList.add('fa-heart-o'); // Agregamos el corazón vacío
                        icon.style.color = ''; // Reseteamos el color
                    }
                }
            })
            .catch(error => console.error("Error:", error));
        });
    });
});
