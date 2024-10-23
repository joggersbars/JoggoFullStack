## Implementation Notes
El proyecto se divide en varias carpetas que tienen scripts creados con un determinado objetivo.

- En la carpeta `app.database` encontramos el script `database_configuration.py`
- En la carpeta `app.routers` encontramos el script `users.py`
- En la carpeta `app.util` encontramos los siguientes scritps: `crud.py`, `logging.py`, `model.py`, `schemas.py`. `security.py`:
    * En `model.py` tenemos las siguientes relaciones entre Tablas:
        - `User` → Relación con GamePlayer: Un usuario puede participar en múltiples partidas.
        - `Game` → Relación con GamePlayer y GamePhrase: Una partida puede tener múltiples jugadores y frases.
        - `GamePhrase` → Relación con GameResponse: Una frase puede tener múltiples respuestas de los jugadores.
