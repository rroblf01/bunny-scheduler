## Bunny Scheduler

Este proyecto es un ejemplo rápido de una aplicación de reservas, desarrollado en Django y en menos de 2 horas. Su objetivo es demostrar cómo implementar un sistema básico de gestión de reservas con las siguientes características:

- Permite múltiples usuarios.
- Los usuarios pueden ver sus propias reservas y las de otros usuarios.
- Es posible solicitar el intercambio de reservas entre usuarios.

### Generación de CSS

Para generar el CSS utilizando Tailwind, ejecuta el siguiente comando:

```
deno run  --unstable-detect-cjs -A npm:tailwindcss@3 -i ./static/input.css -o ./static/output.css --minify
```

Esto compilará los estilos definidos en `input.css` y generará el archivo optimizado `output.css` en la carpeta `static/`.

---
Este proyecto es solo un ejemplo y no está pensado para producción.
