# PARCIAL 3 PROGRAMACION I

## Sistema de Gestión de Encuestas

 ![Fondo](https://www.cimec.es/wp-content/uploads/2023/11/Tipo-de-encuestas-retocada.jpg)

## Descripción

Este sistema permite la creación, gestión y análisis de encuestas para optimizar procesos de recopilación de datos en estudios. Facilita la automatización de tareas como la carga de participantes, segmentación, envío de invitaciones y generación de informes. Está diseñado para ser escalable y adaptable a las necesidades de diferentes usuarios. El sistema utiliza una interfaz gráfica desarrollada con **Tkinter** para ofrecer una experiencia de usuario intuitiva.

## Requerimientos Funcionales

### Gestión de Usuarios

* Autenticación mediante usuario y contraseña.
* Gestión de roles: coordinador de estudios y analista de resultados.
* Escalabilidad para admitir más usuarios sin afectar el rendimiento.

### Creación y Gestión de Encuestas

* Creación de encuestas a partir de un banco de preguntas predefinidas.
* Personalización de preguntas (texto, tipo de respuesta, etc.).
* Versionado para control de cambios.
* Guardar encuestas como borradores y publicarlas posteriormente.

### Carga y Segmentación de Participantes

* Cargar participantes desde archivos CSV con datos como:
  * Nombre, correo electrónico, celular, edad, género, dirección, ciudad, cargo, empresa y rango salarial.
* Segmentación según criterios específicos como edad, género o ubicación.
* Integración con CRM para obtener participantes.

### Distribución de Encuestas

* Envío de invitaciones por correo electrónico con enlaces únicos.
* Envío de recordatorios automáticos para encuestados que no respondan.
* Configuración de fecha de cierre para las encuestas.

### Análisis y Reporte de Resultados

* Generación automática de informes con:
  * Tasa de respuesta, distribución de respuestas, análisis estadísticos básicos.
* Exportación de datos crudos en formato CSV.
* Descarga de informes en formato PDF.

## Requerimientos No Funcionales

* **Interfaz Gráfica**: Utiliza **Tkinter** para una experiencia visual y amigable.
* Persistencia de datos en memoria durante la ejecución.
* Compatibilidad con archivos CSV para carga de datos y exportación.
* Escalabilidad y eficiencia para manejar múltiples encuestas y participantes.

\#

# Instalación


1. Clona el Repositorio:

   Si estás utilizando Git, clona el repositorio a tu máquina local:

```bash
git clone  https://github.com/DanielChavezV/PARCIAL-FINAL-PROG.git
```


2. Crear y activar el entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```


3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

# Ejecución

Para ejecutar el proyecto, usa el siguiente comando:

```bash
python main.py
```

# Autor

**Daniel Steven Chavez Valdes y Juan Sebastian Castañeda**

**Ingeniería de Sistemas 4 Semestre**
**Universidad Libre Seccional Cali**
