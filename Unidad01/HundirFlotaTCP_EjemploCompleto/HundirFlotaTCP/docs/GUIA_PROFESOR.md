# Guía docente – Hundir la flota con TCP

## Material

Esta carpeta contiene **la solución completa**. Para entregar al alumnado, utiliza **la carpeta/ZIP de alumnado**, no esta.

## Temporalización orientativa (4–6 horas)

1. Repaso de TCP y ejecución de un cliente/servidor simple: 30 min.
2. Comprensión de tableros y realización de disparos (`TODO 1`): 45–60 min.
3. Envío y recepción de líneas (`TODO 2–3`): 45–60 min.
4. Máquina de turnos y protocolo (`TODO 4`): 90–120 min.
5. Conexiones (`TODO 5–6`), pruebas en parejas y entrega: 45–60 min.

## Competencias técnicas

- Diferenciar la función de `bind`/`listen`/`accept` frente a `connect`.
- Utilizar `sendall` y `recv` con `encode`/`decode`.
- Delimitar mensajes sobre un flujo TCP mediante `\n`.
- Coordinar turnos sin hilos ni esperas circulares.
- Comprobar errores y desconexiones.

## Secuencia de la comunicación

```text
SERVIDOR (jugador 1)                    CLIENTE (jugador 2)
listen + accept                         connect
mi_turno=True                           mi_turno=False

DISPARO|B3               -------------> recibe y evalúa su tablero
                         <------------- RESULTADO|AGUA|CONTINUA
espera disparo           <------------- DISPARO|C2
RESULTADO|TOCADO|CONTINUA -------------> espera respuesta
...
RESULTADO|TOCADO|FIN     -------------> ambos terminan (ejemplo)
```

En cada mitad del turno exactamente un extremo espera un disparo y el otro envía ese disparo; luego el atacante espera la respuesta y el atacado la envía. Nadie espera `recv` a la vez indefinidamente si ambos respetan el protocolo.

## Observaciones

- `recibir_mensaje()` usa `recv(1)` intencionadamente porque los mensajes son muy cortos y el alumnado puede comprender la delimitación; no es una solución optimizada para alta carga.
- Las tres naves son de una sola casilla: no se contempla `HUNDIDO` por barco. Solo `TOCADO` o `AGUA`, y `FIN` al acertar el tercer barco.
- Se evita una tercera figura que actúe como árbitro: **el servidor también juega**.
- Se usa un puerto alto (50505) para evitar conflictos comunes con servicios locales.
- En el laboratorio puede haber aislamiento entre clientes Wi-Fi o reglas de cortafuegos. Si no pueden conectarse entre ordenadores, la prueba en dos terminales de un mismo ordenador es válida para el objetivo de TCP.

## Propuesta de valoración (10 puntos)

| Apartado | Puntos |
| --- | ---: |
| Conexión TCP servidor/cliente | 2 |
| Envío/recepción con delimitación de mensajes | 2 |
| Aplicación correcta de los disparos y tableros | 2 |
| Alternancia de turnos y fin de partida | 3 |
| Pruebas y entrega ordenada | 1 |

Esta tabla es una orientación didáctica, **no** una asignación oficial a criterios RA-CE.

## Ejecución

En dos terminales: `python servidor.py` y después `python cliente.py`. En dos ordenadores, actualizar `HOST` en el cliente con la IP privada del servidor. Ambos deben usar el mismo puerto 50505.
