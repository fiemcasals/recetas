#se crea un .py de apps para cada aplicacion que se tenga, en este caso solo polls
#se repite todo menos el prefico Polls...que es cambiado por el nombre de la app nueva
#permite ciertas configuraciones obtenidas en appconfig

from django.apps import AppConfig


class PollsConfig(AppConfig):
    name = 'polls'
