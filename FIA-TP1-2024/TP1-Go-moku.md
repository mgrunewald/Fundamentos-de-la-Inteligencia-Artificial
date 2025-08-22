# Trabajo Práctico 1: Engine de Go-moku

## Introducción

[Go-moku](https://es.wikipedia.org/wiki/Go-moku) es un juego de tablero estratégico tradicional. Se juega con piedras negras y blancas en un tablero de Go. El objetivo del juego es ser el primero en alinear cinco de sus propias piedras verticalmente, horizontalmente o diagonalmente.

## Objetivo

El objetivo de este trabajo práctico es desarrollar un agente inteligente capaz de jugar al Go-moku. Se evaluará la eficiencia del agente en términos de su rendimiento durante las partidas de prueba y su habilidad para implementar estrategias de juego avanzadas.

## Rating

Para evaluar el desempeño de los agentes, utilizaremos el sistema de rating Trueskill. Este sistema asigna una puntuación a cada agente en base a los enfrentamientos de cada agente contra los demás participantes.

## Recomendaciones

Antes de comenzar con la implementación de su agente, recomendamos realizar pruebas con un tablero más pequeño para facilitar la identificación y corrección de errores. Por ejemplo un tablero de 3x3 y `num_in_row=3` equivale al tatetí que es fácil debuggear, y tableros más pequeños como 9x9 suelen funcionar mucho mas rápido que uno de 15x15.

## Forma de trabajo

La forma de trabajo para este trabajo práctico será la siguiente:

1. Hacer un fork del repositorio del trabajo práctico en GitHub. Esto creará una copia del repositorio en tu cuenta de GitHub.
1. Clonar el repositorio _forked_ en tu entorno local.
1. Desarrollar el código del agente en tu entorno local.
1. Realiza commits y pushs frecuentes a tu repositorio forked para mantener un registro de tus cambios.
1. Cuando hayas terminado, realiza un pull request desde tu repositorio forked hacia el repositorio original. Esto enviará tu código para su revisión y evaluación.

**Nota:**  La rama que se intente _mergear_ mediante el pull request debe contener exclusivamente el código fuente del agente y ningún otro archivo más. Cualquier _merge conflict_ o archivo extra será calificado negativamente.

## Entregables

El entregable para cada fase será el código del agente desarrollado en Python 3.11 . Asegúrese de que su código esté bien comentado y sea fácil de entender. No es necesario un informe, pero se espera que cualquier decisión de diseño o implementación importante esté claramente explicada en los docstrings y comentarios del código.

### Checkpoint 0: Comprendiendo las interfaces del juego

Para el checkpoint, es necesario demostrar que se han entendido las interfaces de juego provistas por la cátedra. Su agente deberá ser capaz de interactuar con la interfaz de juego de [OpenAI Gym/Gymnasium](https://gymnasium.farama.org/) para realizar movimientos válidos al azar en el tablero, es decir movimientos que no impliquen poner una piedra en una posición ocupada. El agente se debe ajustar al tamaño del tablero que se esté utilizando en el momento de la ejecución.

**Fecha de control**: Domingo 10 de Marzo a las 23:59

### Entrega Final: Agente Avanzado

Para la entrega final se espera un agente que tenga comportamientos avanzados y como mínimo sea capaz de ganarle a todos los agentes de ejemplo provistos por la cátedra sin problemas.
**Fecha de entrega**: Domingo 14 de Abril a las 23:59

### Entregas continuas

Durante el desarrollo del trabajo práctico, el repositorio estará disponible para hacer entregas continuas de los agentes mediante PRs para que sean evaluados periódicamente contra los demás agentes. Esto permitirá evaluar el desempeño de los agentes y realizar ajustes en el código para mejorar su rendimiento.

## Especificaciones

### Interfaz de juego

Se debe crear una carpeta con el apellido del alumno, por ejemplo para el alumno de apellido "turing" sería `scripts/agents/turing`. Dentro de esta carpeta se debe crear un archivo `turingAgent.py` que contenga la implementación del agente descrita a continuación. En esa misma carpeta se pueden agregar otros archivos que contengan código auxiliar.

Se debe implementar una clase con al menos los siguientes métodos:

```python
agent.action(obs)
agent.name() # Diccionario con nombre apellido y legajo del alumno
agent.__str__() # Nombre del agente (elija lo que quiera)
```

Estos métodos se utilizarán de la siguiente manera:

```python
import gymnasium as gym
import gomoku_udesa
from agents.turing.turingAgent import TuringAgent # remplazar turing por SU apellido

env = gym.make('gomoku_udesa/Gomoku-v0', render_mode='human')
board,info = env.reset()
agent = TuringAgent()
print(agent.name())
print(str(agent))
```

```sh
>> {nombre:'Alan', apellido:'Turing', legajo:123456}
>> Tree-Runner 2049
```

```python
terminated, truncated = False, False
while not terminated and not truncated:
    action = agent.action(board)
    board, reward, terminated, truncated, info = env.step(action)
```
**Nota:** Se pondrá un límite duro al tiempo de ejecución de cada movimiento de 5 segundos, lo mismo para el constructor del agente. Si el agente no devuelve un movimiento dentro de ese tiempo, perderá la partida.

## Evaluación

El trabajo será evaluado en tres dimensiones:

1. **Correctitud de las implementaciones**: Verificación de que las implementaciones se ajustan a las especificaciones y realizan las tareas requeridas, ademas se evaluará que se hayan implementado optimizaciones para arboles adversariales como las vistas en clase.
2. **Rendimiento del agente**: Durante el torneo organizado por la cátedra, se le asignará un rating a los agentes basado en su desempeño. El rating será calculado utilizando el sistema [TrueSkill](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) en un torneo de tipo suizo.
3. **Calidad del código y documentación**: Se evaluará la legibilidad, modularidad y calidad general del código, así como la documentación adjunta en forma de comentarios.


El primer checkpoint debe estar aprobado para poder entregar el TP. Si no lo cumplieran en tiempo se restará entre 0 y 1 punto de la nota final. 

La nota final será calculada utilizando la siguiente fórmula:

$`
Nota = min(2 \times \text{implementaciones} + 2 \times \text{calidad\_y\_documentacion} +  min(6 \times \frac{(\text{Rating} - \text{Rating\_min})}{20.85},8), 10)
`$

Donde `Rating` es el rating del su agente, `Rating_min` es el rating del mejor agente de ejemplo provisto por la cátedra.

Se proporcionarán más detalles durante las clases. Este trabajo debe ser realizado individualmente. ¡Buena suerte!
