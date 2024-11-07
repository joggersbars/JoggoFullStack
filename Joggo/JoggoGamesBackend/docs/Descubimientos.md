### Anotaciones ###
Si te conectas muchas veces al frontend y al backend en windows y no cierras bien todo, esas conexiones se quedan abiertas, por tanto si creas muchas luego no te podrás conectar porque está sobresaturado de peticiones el servidor del backend. Hay que programar manejadores de señales como ctrl+c, para que borre las conexiones y que éstas se cierren, para evitar sobrecarga.

Si en el frontend envías un json, el orden de las claves a veces no se mantiene, para ello es mejpr usar este tipo de estructura:
```javascript
`{
    "id_partida": ${id_partida}, // Suponiendo que el ID de partida esté guardado en localStorage
    "apodo_jugador": ${apodo_jugador},
    "frase_juego": ${frase},
    "respuesta_jugador": ${respuesta}
}`

```