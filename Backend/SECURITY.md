# 🔐 Guía de Seguridad - Perseus Backend

## ⚠️ ADVERTENCIA IMPORTANTE

Este documento contiene información crítica sobre la seguridad de tu aplicación.

---

## 🔑 Tokens y Credenciales

### ✅ Configuración Actual

Tu archivo `.env` contiene los siguientes tokens:

- **HuggingFace Token**: Configurado ✓
- **OpenAI API Key**: Configurado ✓
- **Groq API Key**: Configurado ✓

### 🚨 NUNCA COMPARTAS ESTOS TOKENS

Los tokens de API son como contraseñas. Si alguien los obtiene, puede:
- Usar tus créditos de OpenAI/Groq
- Acceder a tus modelos privados
- Realizar acciones en tu nombre

---

## 🛡️ Protección de Tokens

### 1. Git Ignore

El archivo `.gitignore` está configurado para **NUNCA** subir `.env` a Git:

```gitignore
.env
.env.local
Backend/.env
```

### 2. Verificación

Antes de hacer commit, **SIEMPRE** verifica:

```bash
git status
```

Si ves `.env` en la lista, **NO HAGAS COMMIT**. Ejecuta:

```bash
git reset .env
```

### 3. Si Accidentalmente Expusiste un Token

**INMEDIATAMENTE:**

1. **HuggingFace**:
   - Ve a https://huggingface.co/settings/tokens
   - Revoca el token expuesto
   - Genera uno nuevo

2. **OpenAI**:
   - Ve a https://platform.openai.com/api-keys
   - Revoca la clave expuesta
   - Genera una nueva

3. **Groq**:
   - Ve a https://console.groq.com/keys
   - Revoca la clave expuesta
   - Genera una nueva

4. **Cambia el token en `.env`**

5. **Limpia el historial de Git** (si fue commiteado):
   ```bash
   # Esto es complejo - busca ayuda si es necesario
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch Backend/.env" \
   --prune-empty --tag-name-filter cat -- --all
   ```

---

## 📝 Mejores Prácticas

### ✅ HACER

- Usar `.env` para todos los secretos
- Mantener `.env.example` SIN tokens reales
- Usar variables de entorno en producción
- Rotar tokens regularmente (cada 3-6 meses)
- Usar tokens con permisos mínimos necesarios

### ❌ NO HACER

- Hardcodear tokens en el código
- Compartir tu archivo `.env`
- Subir `.env` a Git
- Usar el mismo token en múltiples proyectos
- Compartir screenshots con tokens visibles

---

## 🔒 Producción

Cuando despliegues a producción (DigitalOcean, AWS, etc.):

1. **NO copies el archivo `.env`**
2. Usa el panel de control del servicio para configurar variables de entorno
3. O usa servicios de gestión de secretos:
   - AWS Secrets Manager
   - HashiCorp Vault
   - DigitalOcean App Platform Environment Variables

---

## 📊 Monitoreo de Uso

Revisa regularmente el uso de tus APIs:

- **OpenAI**: https://platform.openai.com/usage
- **HuggingFace**: https://huggingface.co/settings/tokens
- **Groq**: https://console.groq.com/

Si ves uso inusual, **revoca inmediatamente** tus tokens.

---

## 🆘 Contacto de Emergencia

Si crees que tus tokens fueron comprometidos:

1. Revoca TODOS los tokens inmediatamente
2. Revisa el uso de las APIs
3. Contacta al soporte del servicio si hay cargos no autorizados
4. Cambia contraseñas si es necesario

---

## ✅ Checklist de Seguridad

Antes de cada commit:

- [ ] Verificar que `.env` está en `.gitignore`
- [ ] Ejecutar `git status` y confirmar que `.env` NO aparece
- [ ] No hay tokens hardcodeados en el código
- [ ] `.env.example` NO contiene tokens reales

Antes de desplegar:

- [ ] Variables de entorno configuradas en el servidor
- [ ] No se copió `.env` al servidor
- [ ] CORS configurado correctamente
- [ ] Solo origenes permitidos pueden acceder a la API

---

**Recuerda: La seguridad es responsabilidad de todos. Mantén tus tokens seguros.** 🔐
