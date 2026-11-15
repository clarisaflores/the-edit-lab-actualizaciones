# The Edit Lab · actualizaciones

Aquí viven las versiones nuevas de The Edit Lab. Cada lab de las clientas revisa `ultima.json` cada 6 horas y, cuando hay una versión más nueva, la descarga, revisa que sea la original (huella sha256), guarda un respaldo de la anterior y la instala sola.

- `ultima.json`: la versión más nueva, sus novedades, el enlace al paquete y su huella.
- `noticias.json`: noticias que aparecen en la campanita de todas las clientas (`{"noticias": [{"id": "...", "fecha": "...", "titulo": "...", "texto": "...", "titulo_en": "...", "texto_en": "..."}]}`).
- `paquetes/`: los paquetes de cada versión.
- `publicar.py`: prepara una versión nueva.
