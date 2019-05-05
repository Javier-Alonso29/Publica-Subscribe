# Arquitecturas Publica-Suscribe

## Sistema de Monitoreo de Adultos Mayores (SMAM)

Existe un asilo llamado Divina Providencia en el que viven un grupo de adultos mayores. Parte del personal que trabaja en el asilo, entre otras tareas, se dedica a atender las necesidades de los adultos mayores y a monitorear su estado de salud.

La fundación Catalina Huffmann, que es una fundación altruista en la región, decidió, a manera de donación, desarrollarle al asilo un sistema de cómputo para realizar las actividades de monitoreo del estado de salud de los adultos mayores de forma (semi-)automática. Para ello, la fundación utilizó un conjunto de dispositivos “wearables” que portan cada uno de los adultos mayores. Mediante el envío de información sobre ritmo cardiaco, presión arterial y temperatura, estos dispositivos “wearables” permiten monitorear en tiempo real a cada uno de los adultos mayores y de esta forma ser más eficientes en la prevención de incidencias.

En la siguiente figura se muestra el diseño de la propuesta de solución del departamento de desarrollo para el SMAM.

![Vista de contenedores del SMAM](docs/diagrama_contenedores_capitulo_4.png)

## Prerrequisitos

Para poner en marcha el SMAM se requiere instalar algunas dependencias. Podrás encontrar estas dependencias en el archivo `requirements.txt`. También puedes instalar éstas dependencias con el comando:

```shell
pip install -r requirements.txt
```

**Nota:** se asume que el gestor de dependencias `pip` se ha instalado previamente.

## Ejecución

Actualmente el SMAM cuenta con dos versiones, una que puedes poner en marcha de forma local y otra que puedes poner en marcha de forma distribuida. Dentro del directorio `smam` se encuentran las instrucciones para poner en marcha cualquier versión del SMAM.

## Versión

2.0.2 - Mayo 2019

## Autores

* **Perla Velasco**
* **Yonathan Martínez**