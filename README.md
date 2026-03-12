# Wizz Life — Task Manager API

API REST para gestión de tareas de equipo, desarrollada con **FastAPI** y **PostgreSQL**.

## Stack tecnológico

- **FastAPI** — framework web
- **SQLAlchemy** — ORM
- **PostgreSQL** — base de datos
- **passlib + bcrypt** — hash de contraseñas
- **python-jose** — autenticación JWT
- **uvicorn** — servidor ASGI

## Endpoints

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| `POST` | `/signup/` | No | Registrar usuario |
| `POST` | `/signin/` | No | Iniciar sesión, retorna JWT |
| `GET` | `/tasks/` | Si | Listar tareas (filtros, paginación, ordenamiento) |
| `POST` | `/tasks/` | Si | Crear tarea |
| `GET` | `/tasks/{id}/` | Si | Detalle de una tarea |
| `PATCH` | `/tasks/{id}/` | Si | Actualizar tarea parcialmente |
| `DELETE` | `/tasks/{id}/` | Si | Eliminar tarea |

Los endpoints protegidos requieren header: `Authorization: Bearer <token>`

### Parámetros de `GET /tasks/`

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `status` | string | — | Filtrar: `pending`, `in_progress`, `done` |
| `skip` | int | `0` | Registros a saltar (paginación) |
| `limit` | int | `20` | Máximo de registros (máx: 100) |
| `order_by` | string | `created_at` | Campo de ordenamiento: `created_at`, `updated_at`, `title` |

## Cómo ejecutar localmente

### 1. Clonar el repositorio

```bash
git clone https://github.com/CrstnG/wizz-backend.git
cd wizz-backend
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con nuevo DATABASE_URL y SECRET_KEY
```

### 4. Tener PostgreSQL corriendo y la base de datos creada

```bash
createdb wizzlife 
```

### 5. Iniciar el servidor

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`
Documentación interactiva (Swagger): `http://localhost:8000/docs`

## Cómo levantar con Docker

### Solo el contenedor de la API

```bash
docker build -t wizz-backend .
docker run -p 8000:8000 --env-file .env wizz-backend
```

Requiere que `DATABASE_URL` en `.env` apunte a un PostgreSQL accesible desde el contenedor.

## Decisiones técnicas relevantes

### Separación de capas
El proyecto sigue una arquitectura de capas explícita:
- **Routers** → solo manejo HTTP (códigos de estado, excepciones)
- **Services** → lógica de negocio pura
- **Models** → definición de tablas (SQLAlchemy ORM)
- **Schemas** → validación de datos de entrada/salida (Pydantic)

Esto facilita el testing unitario de la lógica sin levantar un servidor HTTP.

### PATCH semántico
El endpoint `PATCH /tasks/{id}/` usa `model_dump(exclude_unset=True)` para actualizar **únicamente** los campos enviados en el request, sin pisar los campos no incluidos.

### Seguridad
- Las contraseñas se almacenan como hash `bcrypt` (nunca en texto plano)
- El JWT se firma con `HS256` y expira en 30 minutos (configurable)
- Los errores de autenticación siempre dicen "Credenciales inválidas" (no especifica si el email o la contraseña es lo incorrecto)
- Cada usuario solo puede ver y modificar sus propias tareas

### Creación de tablas
Se usa `Base.metadata.create_all()` al inicio de la app para simplicidad.
