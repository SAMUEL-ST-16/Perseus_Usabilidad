# Perseus - Frontend

Sistema web para la extracción automática de requisitos de usabilidad basados en ISO 25010:2023 a partir de comentarios de usuarios de aplicaciones móviles.

## Descripción

Este frontend Angular consume la API del backend FastAPI para procesar comentarios de usuarios y extraer requisitos de usabilidad clasificados según las 8 subcaracterísticas de usabilidad de la norma ISO 25010:2023:

1. **Operabilidad** - Grado en que el producto tiene atributos que facilitan su operación y control
2. **Aprendizabilidad** - Grado en que el producto permite al usuario aprender su uso
3. **Involucración del usuario** - Grado en que el usuario está satisfecho y motivado con el uso del producto
4. **Reconocibilidad de adecuación** - Grado en que los usuarios pueden reconocer si el producto es apropiado para sus necesidades
5. **Protección frente a errores de usuario** - Grado en que el sistema protege a los usuarios contra cometer errores
6. **Inclusividad** - Grado en que el producto puede ser usado por personas con diversas características y capacidades
7. **Auto descriptividad** - Grado en que la interfaz de usuario es auto-explicativa
8. **Asistencia al usuario** - Grado en que el producto proporciona ayuda y soporte al usuario

## Tecnologías

- **Angular 21** - Framework frontend
- **TypeScript 5.7** - Lenguaje de programación
- **RxJS** - Programación reactiva
- **CSS3** - Estilos y diseño responsivo

## Estructura del Proyecto

```
Frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── home/              # Componente principal con las 3 funcionalidades
│   │   │   │   ├── home.ts
│   │   │   │   ├── home.html
│   │   │   │   └── home.css
│   │   │   └── iso25010/          # Página informativa de ISO 25010
│   │   │       ├── iso25010.ts
│   │   │       ├── iso25010.html
│   │   │       └── iso25010.css
│   │   ├── services/
│   │   │   └── api.service.ts     # Servicio para comunicación con backend
│   │   ├── models/
│   │   │   └── requirement.model.ts  # Interfaces TypeScript
│   │   ├── data/
│   │   │   └── iso25010.data.ts   # Datos de referencia ISO 25010
│   │   ├── app.config.ts          # Configuración de la aplicación
│   │   ├── app.routes.ts          # Rutas de la aplicación
│   │   └── app.html               # Plantilla principal
│   ├── styles.css                 # Estilos globales
│   └── index.html                 # Punto de entrada HTML
├── angular.json                   # Configuración de Angular
├── package.json                   # Dependencias del proyecto
└── tsconfig.json                  # Configuración de TypeScript
```

## Requisitos Previos

- **Node.js** >= 18.x
- **npm** >= 9.x
- **Angular CLI** 21.x

Puedes verificar tus versiones con:

```bash
node --version
npm --version
ng version
```

## Instalación

### 1. Instalar Angular CLI globalmente (si no lo tienes)

```bash
npm install -g @angular/cli@21
```

### 2. Instalar dependencias del proyecto

```bash
cd Frontend
npm install
```

## Configuración

### URL del Backend

El frontend está configurado para conectarse al backend en `http://localhost:8000`.

Si necesitas cambiar esta URL, edita el archivo:

**`src/app/services/api.service.ts`**

```typescript
private readonly API_URL = 'http://localhost:8000/api/requirements';
```

## Ejecución

### 1. Asegúrate de que el backend esté corriendo

El backend debe estar ejecutándose en `http://localhost:8000` antes de iniciar el frontend.

```bash
# En otra terminal, desde la carpeta Backend/
cd Backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### 2. Iniciar el servidor de desarrollo

```bash
cd Frontend
ng serve
```

O con opciones específicas:

```bash
ng serve --open --port 4200
```

La aplicación estará disponible en: **http://localhost:4200**

## Funcionalidades

### 1. Procesamiento de Comentario Individual

Permite ingresar un comentario de usuario manualmente y obtener un PDF con el análisis de requisitos de usabilidad encontrados.

**Ubicación:** Tarjeta 1 en la página principal

**Endpoint usado:** `POST /api/requirements/process/single`

### 2. Procesamiento de Archivo CSV

Permite cargar un archivo CSV con múltiples comentarios y obtener un PDF con todos los requisitos extraídos.

**Ubicación:** Tarjeta 2 en la página principal

**Endpoint usado:** `POST /api/requirements/process/csv`

**Formato del CSV esperado:**
```csv
content,score
"Comentario del usuario 1",4.5
"Comentario del usuario 2",3.2
```

### 3. Procesamiento desde Google Play Store

Permite ingresar la URL de una aplicación de Google Play Store para extraer comentarios automáticamente y analizarlos.

**Ubicación:** Tarjeta 3 en la página principal

**Endpoint usado:** `POST /api/requirements/process/playstore`

**Formato de URL esperado:**
```
https://play.google.com/store/apps/details?id=com.ejemplo.app
```

### 4. Página Informativa ISO 25010

Proporciona información detallada sobre la norma ISO 25010:2023 y las 8 subcaracterísticas de usabilidad.

**Ubicación:** `/iso25010` o enlace desde la página principal

## Rutas de la Aplicación

| Ruta | Componente | Descripción |
|------|-----------|-------------|
| `/` | HomeComponent | Página principal con las 3 funcionalidades |
| `/iso25010` | ISO25010Component | Información sobre ISO 25010 |
| `/**` | Redirect | Cualquier ruta no encontrada redirige a `/` |

## Estilos y Tema

El frontend utiliza un tema moderno con paleta de colores profesional:

- **Color primario:** `#667eea`
- **Color secundario:** `#764ba2`
- **Acento (éxito):** `#48bb78`
- **Peligro:** `#f56565`

Todos los estilos globales se encuentran en `src/styles.css` y utilizan CSS Variables para fácil personalización.

## Personalización de Iconos e Imágenes

Los componentes tienen placeholders para iconos que puedes reemplazar:

### Iconos en ISO25010 Component

Actualmente usa emojis como placeholders en `iso25010.html`:

```html
@case (0) { 🔐 }  <!-- Confidencialidad -->
@case (1) { ✓ }   <!-- Integridad -->
@case (2) { 📝 }  <!-- No Repudio -->
@case (3) { 👤 }  <!-- Responsabilidad -->
@case (4) { 🔑 }  <!-- Autenticidad -->
@case (5) { 🛡️ }  <!-- Resistencia -->
```

**Para reemplazar con imágenes:**

1. Coloca tus imágenes en `src/assets/icons/`
2. Actualiza el código HTML:

```html
<img [src]="sub.icon" [alt]="sub.name" />
```

3. Actualiza `src/app/data/iso25010.data.ts` con las rutas correctas:

```typescript
icon: 'assets/icons/confidentiality.svg'
```

## Comandos Útiles

### Desarrollo

```bash
# Iniciar servidor de desarrollo
ng serve

# Iniciar y abrir navegador automáticamente
ng serve --open

# Usar un puerto específico
ng serve --port 4201
```

### Build

```bash
# Build de producción
ng build

# Build con optimizaciones
ng build --configuration production
```

Los archivos compilados estarán en `dist/frontend/`.

### Testing

```bash
# Ejecutar tests unitarios
ng test

# Ejecutar tests e2e
ng e2e
```

### Linting

```bash
# Verificar código
ng lint
```

## Manejo de Errores

El frontend maneja los siguientes tipos de errores:

1. **Errores de red:** Cuando el backend no está disponible
2. **Errores de validación:** Cuando los datos ingresados no son válidos
3. **Errores del servidor:** Cuando el backend retorna un error

Todos los errores se muestran al usuario mediante mensajes en las tarjetas correspondientes.

## Estado de Carga

Cada funcionalidad muestra:

- **Spinner de carga** mientras procesa
- **Mensaje de progreso** con el estado actual
- **Mensaje de éxito** cuando el PDF se descarga
- **Mensaje de error** si algo falla

## Descarga de PDFs

Los PDFs se descargan automáticamente con nombres descriptivos:

- Comentario individual: `requisito_individual.pdf`
- Archivo CSV: `requisitos_csv.pdf`
- Google Play Store: `requisitos_playstore.pdf`

El navegador solicitará permiso para la descarga automática la primera vez.

## Navegadores Soportados

- Chrome (últimas 2 versiones)
- Firefox (últimas 2 versiones)
- Safari (últimas 2 versiones)
- Edge (últimas 2 versiones)

## Solución de Problemas

### El frontend no puede conectarse al backend

**Problema:** Errores de CORS o "Failed to fetch"

**Solución:**
1. Verifica que el backend esté corriendo en `http://localhost:8000`
2. Verifica que el backend tenga CORS habilitado
3. Revisa la consola del navegador para más detalles

### Los PDFs no se descargan

**Problema:** El PDF no se descarga automáticamente

**Solución:**
1. Verifica la configuración de descargas de tu navegador
2. Permite las descargas automáticas para `localhost`
3. Revisa la consola del navegador para errores

### Errores de compilación

**Problema:** Errores al ejecutar `ng serve`

**Solución:**
```bash
# Limpia node_modules y reinstala
rm -rf node_modules package-lock.json
npm install

# Limpia caché de Angular
ng cache clean
```

## Próximas Mejoras

- Añadir gráficos estadísticos de resultados
- Implementar historial de análisis
- Añadir exportación en múltiples formatos (Excel, JSON)
- Implementar preview de PDF antes de descargar
- Añadir modo oscuro

## Contribución

Este proyecto es parte de una tesis de grado. Para contribuciones o sugerencias, contacta al autor.

## Licencia

Proyecto académico - Todos los derechos reservados

---

**Desarrollado con Angular 21**
**Basado en ISO 25010:2023 - Usabilidad**
