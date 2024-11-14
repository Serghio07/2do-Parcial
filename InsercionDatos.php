<?php
// InsercionDatos.php

// Configuración de conexión a la base de datos
$servername = "localhost";
$username = "tu_usuario";       // Reemplaza con tu usuario de MySQL
$password = "tu_contraseña";     // Reemplaza con tu contraseña de MySQL
$dbname = "bd_ejercicios";

// Crear conexión
$conn = new mysqli($servername, $username, $password, $dbname);

// Verificar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Obtener datos JSON del cuerpo de la solicitud
$data = json_decode(file_get_contents('php://input'), true);

// Verificar si los datos están correctamente recibidos
if (!isset($data['joysticks']) || !isset($data['timestamp'])) {
    die("Datos incompletos recibidos.");
}

// Insertar datos en la tabla Sesiones (por ejemplo, creando una sesión con un ID ficticio o real)
$idUsuario = 1;  // Suponemos que el idUsuario es conocido o proporcionado por alguna lógica externa
$fechaSesion = date('Y-m-d');  // Fecha actual
$duracion = 60;  // Duración de la sesión en segundos (ajustar según tus necesidades)
$tipoEjercicio = "Prueba Joystick";  // Definir tipo de ejercicio

$sqlSesion = "INSERT INTO Sesiones (idUsuario, Fecha_sesion, Duracion, Tipo_ejercicio) 
              VALUES ($idUsuario, '$fechaSesion', $duracion, '$tipoEjercicio')";

// Ejecutar la inserción de sesión
if ($conn->query($sqlSesion) !== TRUE) {
    die("Error al insertar sesión: " . $conn->error);
}

// Obtener el ID de la sesión recién insertada
$idSesion = $conn->insert_id;

// Variables para calcular el progreso
$totalFuerza = 0;
$totalMovilidadHorizontal = 0;
$totalMovilidadVertical = 0;
$totalPrecisiónDiagonal = 0;
$lecturasCount = 0;

// Insertar las lecturas de los joysticks
foreach ($data['joysticks'] as $joystick) {
    $joystickId = $joystick['joystick_id'];
    $ejeX = $joystick['x_val'];
    $ejeY = $joystick['y_val'];
    $nivelX = $joystick['x_nivel'];
    $nivelY = $joystick['y_nivel'];
    $boton = ($joystick['boton'] == "Presionado") ? 1 : 0;  // Convertir a booleano
    $direccion = $joystick['x_direccion'] . ", " . $joystick['y_direccion'];  // Dirección combinada
    $diagonal = $joystick['diagonal'];

    // Calcular la fuerza promedio (puedes ajustar este cálculo según tus necesidades)
    $fuerza = sqrt(pow($ejeX, 2) + pow($ejeY, 2));  // Fuerza como magnitud del vector (ejemplo básico)

    // Calcular movilidad horizontal y vertical
    $movilidadHorizontal = abs($ejeX);  // Usamos el valor absoluto para movilidad en X
    $movilidadVertical = abs($ejeY);    // Usamos el valor absoluto para movilidad en Y

    // Calcular precisión diagonal
    // Aquí podrías implementar una fórmula o medida que indique la precisión diagonal
    $precisionDiagonal = abs($ejeX - $ejeY);  // Solo un ejemplo de cálculo básico

    // Sumar valores para el cálculo del progreso
    $totalFuerza += $fuerza;
    $totalMovilidadHorizontal += $movilidadHorizontal;
    $totalMovilidadVertical += $movilidadVertical;
    $totalPrecisiónDiagonal += $precisionDiagonal;
    $lecturasCount++;

    // Sentencia SQL para insertar los datos de lectura en la tabla Lecturas
    $sqlLectura = "INSERT INTO Lecturas (idSesion, Joytstick_numero, Eje_x, Eje_y, Nivel_x, Nivel_y, Boton, Direccion, Diagonal)
                   VALUES ($idSesion, $joystickId, $ejeX, $ejeY, $nivelX, $nivelY, $boton, '$direccion', '$diagonal')";

    // Ejecutar la inserción de lectura
    if ($conn->query($sqlLectura) !== TRUE) {
        die("Error al insertar lectura: " . $conn->error);
    }
}

// Calcular el progreso promedio para la sesión
$promFuerza = $lecturasCount ? $totalFuerza / $lecturasCount : 0;
$promMovilidadHorizontal = $lecturasCount ? $totalMovilidadHorizontal / $lecturasCount : 0;
$promMovilidadVertical = $lecturasCount ? $totalMovilidadVertical / $lecturasCount : 0;
$promPrecisiónDiagonal = $lecturasCount ? $totalPrecisiónDiagonal / $lecturasCount : 0;

// Calcular mejora en la fuerza (esto podría basarse en datos de sesiones anteriores, se puede ajustar)
$mejoraFuerza = $promFuerza;  // Puedes hacer una comparación con la fuerza de sesiones anteriores para determinar la mejora

// Insertar el progreso en la tabla Progreso
$sqlProgreso = "INSERT INTO Progreso (idUsuario, Fecha_calculo, Fuerza_promedio, Movilidad_horizontal, Movilidad_vertical, Precision_diagonal, Mejora_fuerza)
                VALUES ($idUsuario, '$fechaSesion', $promFuerza, $promMovilidadHorizontal, $promMovilidadVertical, $promPrecisiónDiagonal, $mejoraFuerza)";

// Ejecutar la inserción de progreso
if ($conn->query($sqlProgreso) !== TRUE) {
    die("Error al insertar progreso: " . $conn->error);
}

// Respuesta al cliente
echo "Datos insertados correctamente.";

// Cerrar conexión
$conn->close();
?>
