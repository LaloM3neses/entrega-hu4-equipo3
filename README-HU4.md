# HU-4 — Consulta y seguimiento de incidencias (Equipo 3)

Entregable para el Sprint 1 según el cronograma (Pruebas: 13 sep, Entrega: 14 sep).

## Qué incluye

**Backend** (`backend/` → va dentro de `trabajo-colaborativo-backend/`):
- `app/models/report.py` — tabla `reports`.
- `app/schemas/report.py` — DTOs (JSON en camelCase para que calce con el frontend).
- `app/services/report.py` — lógica de negocio.
- `app/routers/report.py` — `POST /reports/`, `GET /reports/`, `GET /reports/{folio}`.
- `app/urls.py` — reemplaza al actual (ya trae el router de reports registrado).
- `alembic/env.py` — reemplaza al actual (importa el modelo `Report`).
- `alembic/versions/d4e5f6a7b8c9_create_reports.py` — migración nueva.

**Frontend** (`frontend/` → va dentro de `trabajo-colaborativo-frontend/`):
- `src/app/data/reports-api.service.ts` — llama al backend real (nuevo).
- `src/app/folio-search/` — pantalla de "Buscar por folio" (nueva).
- `src/app/app.routes.ts` — reemplaza al actual, agrega la ruta `/inicio/buscar`.
- `src/app/home/home.ts` y `home.html` — reemplazan a los actuales, solo se agregó el link "Buscar por folio".

## Decisiones importantes a comunicarle al equipo

1. **`campusLabel` / `spaceLabel` como texto libre.** Equipo 1 (HU-03) aún no entrega el catálogo de Campus/Space en el backend, así que el modelo `Report` guarda el campus y la ubicación como texto en vez de una FK real. Cuando ellos entreguen su catálogo, hay que migrar estos dos campos a `campus_id` / `space_id`.
2. **`POST /reports/` es una versión mínima.** El formulario completo de alta (HU-05/06) es de Equipo 1. Este POST solo existe para poder meter datos de prueba y que la consulta (HU-4) sea demostrable hoy. Avisen a Equipo 1 para no duplicar el endpoint cuando ellos conecten su formulario.
3. **"Folio" = el `id` autoincremental del backend** (un número, ej. `1`, `2`...). No es el mismo tipo de id que usa el mock del frontend (`"rep-banos-sucios"`). Por eso se creó `ApiReport` como tipo separado de `Report` en el frontend — no se tocó el modelo mock existente, así que no debería romper el resto de las pantallas (técnico, responsable, etc.) que siguen usando datos mock.

## Cómo aplicarlo

### Backend
1. Copia el contenido de `backend/` dentro de tu clon de `trabajo-colaborativo-backend`, respetando las rutas (sobrescribe `app/urls.py` y `alembic/env.py`).
2. Levanta los contenedores si no están corriendo:
   ```bash
   docker compose up -d
   ```
3. Aplica la migración:
   ```bash
   docker compose exec api alembic upgrade head
   ```
4. Verifica en Swagger: http://localhost:8000/docs — deberías ver la sección **Reports**.

### Frontend
1. Copia el contenido de `frontend/` dentro de tu clon de `trabajo-colaborativo-frontend`, respetando las rutas (sobrescribe `app.routes.ts`, `home/home.ts`, `home/home.html`).
2. `npm install` si hace falta, luego `ng serve`.
3. Entra a `/inicio/buscar` (o dale clic a "Buscar por folio" desde la pantalla de Reportante).

## Cómo probar (lo que pide el cronograma: "búsqueda por folio y visualización del estado inicial")

1. Regístrate / inicia sesión (endpoints de Equipo 1, ya existen: `POST /auth/register`, `POST /auth/login`) para obtener un `access_token`.
2. Crea un reporte de prueba:
   ```bash
   curl -X POST http://localhost:8000/reports/ \
     -H "Authorization: Bearer TU_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Aire acondicionado sin enfriar",
       "description": "El aula CC04-304 está demasiado caliente desde ayer.",
       "campusLabel": "Campus Central",
       "spaceLabel": "CC04 - 304"
     }'
   ```
   La respuesta trae `"id": 1` (ese `1` es el folio) y `"status": "creado"`.
3. Consulta por folio:
   ```bash
   curl http://localhost:8000/reports/1 -H "Authorization: Bearer TU_ACCESS_TOKEN"
   ```
4. En el frontend, en `/inicio/buscar`, escribe `1` en el campo Folio y dale "Buscar" — debe mostrar el título, la ubicación y la línea de tiempo con el primer punto ("Creado") activo, que es justo el estado inicial "Reportada" que pide probar el cronograma.

## Pendiente para después del Sprint 1

- Migrar `campus_label`/`space_label` a FKs reales cuando exista el catálogo (HU-03).
- Coordinarse con Equipo 1 para que `POST /reports/` sea uno solo (probablemente el de ellos, con imagen y catálogo real).
- Sumar filtros de búsqueda adicionales si el equipo lo pide (por estado, por campus, etc.) — no estaba en el alcance de HU-4 para este sprint.
