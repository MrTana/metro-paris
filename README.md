# Metro París en vivo

Pantalla de horarios del metro de París en tiempo real, estilo pantallas del metro.

- `index.html`: la aplicación.
- `_worker.js`: proxy para Cloudflare Pages (reenvía `/api/*` a la API de PRIM).
- `servidor.py`: alternativa local para usarla en un PC (`python servidor.py`).

Se publica con Cloudflare Pages conectado a este repositorio. La clave (jeton) de PRIM se guarda solo en el navegador.
