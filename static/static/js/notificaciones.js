document.addEventListener("DOMContentLoaded", () => { //espera que se cargue la pagina
    document.getElementById("boton").addEventListener("click", () => { //mantiene en escucha el elemento con el id
        const notificacionId = document.getElementById("boton").getAttribute("data-id");//levanta el valor de la etiqueta data-id
        fetch(`/notificaciones/marcar_leida/${notificacionId}/`, {//llama a un html con un dato variable "notificaionID, el %=$ los concatena"
            method: 'POST',
            headers: {
                "Content-Type": "application/json", //indica que hay datos en formato json
                "X-CSRFToken": getCSRFToken()  // Obtén el token CSRF desde el meta tag
            }
        })
        .then(response => response.json()) //then da lugar a atender la respuesta de la solicitud fetch, response, es la respuesta y response.json se transforma en js para usarlo como un objeto
        .then(data => { //es el objeto json producto de response.json, variable propia de segundo .then
            if (data.nuevo_estado === undefined) {
                return console.error("Error: Respuesta inesperada del servidor", data);
            }

            // Cambiar el estado del botón y la notificación según el nuevo estado
            const boton = document.getElementById("boton");
            if (data.nuevo_estado) {
                boton.classList.replace("btn-leer", "btn-leido");
                boton.textContent = "Leído";
            } else {
                boton.classList.replace("btn-leido", "btn-leer");
                boton.textContent = "Leer";
            }
        })
        .catch(error => console.error('Error al actualizar notificación:', error));
    });
});
