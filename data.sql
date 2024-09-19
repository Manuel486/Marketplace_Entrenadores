-- Insertar datos en la tabla Especialidad
INSERT INTO `Especialidad` (`Nombre`, `Estado`, `FechaCreacion`, `FechaActualizacion`) VALUES
('Cardio', 'Activo', '2024-01-01', '2024-01-01'),
('Fuerza', 'Activo', '2024-01-01', '2024-01-01'),
('Flexibilidad', 'Activo', '2024-01-01', '2024-01-01');

-- Insertar datos en la tabla TipoDeRutina
INSERT INTO `TipoDeRutina` (`Nombre`, `Descripcion`) VALUES
('Entrenamiento de Resistencia', 'Rutina enfocada en aumentar la resistencia cardiovascular.'),
('Entrenamiento de Fuerza Muscular', 'Rutina enfocada en el desarrollo de masa muscular.'),
('Entrenamiento de Flexibilidad', 'Rutina enfocada en mejorar la flexibilidad y el rango de movimiento.');

-- Insertar datos en la tabla TipoDeRutinaEspecialidad
INSERT INTO `TipoDeRutinaEspecialidad` (`TipoDeRutinaID`, `EspecialidadID`) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Insertar datos en la tabla Local
INSERT INTO `Local` (`Nombre`, `Direccion`, `Telefono`) VALUES
('Gym Central', 'Calle Falsa 123, Ciudad', '123456789'),
('Fitness Club', 'Avenida Principal 456, Ciudad', '987654321');

-- Insertar datos en la tabla Usuario
INSERT INTO `Usuario` (`Username`, `Password`, `Email`, `Nombre`, `Apellido`, `Tipo`) VALUES
('administrador', 'administrador', 'laura.martinez@example.com', 'Laura', 'Martínez', 'Administrador'),
('instructor1', 'instructor1', 'david.rodriguez@example.com', 'David', 'Rodríguez', 'Instructor'),
('instructor2', 'instructor2', 'miguel.molina@example.com', 'Miguel', 'Molina', 'Instructor'),
('instructor3', 'instructor3', 'piero.vargas@example.com', 'Piero', 'Vargas', 'Instructor');

-- Insertar datos en la tabla Instructor
INSERT INTO `Instructor` (`Nombres`, `Apellidos`, `Email`, `Edad`, `Sexo`, `FechaNacimiento`, `UsuarioID`, `LocalID`) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', 30, 'M', '1994-05-15', 2, 1),
('Ana', 'Gómez', 'ana.gomez@example.com', 28, 'F', '1996-07-20', 3, 2),
('Carlos', 'Mendoza', 'carlos.mendoza@example.com', 35, 'M', '1989-12-01', 4, 1);

-- Insertar datos en la tabla InformacionPersonalInstructor
INSERT INTO `InformacionPersonalInstructor` (`InstructorID`, `PreferenciaHorario`) VALUES
(1, 'Mañana'),
(2, 'Tarde'),
(3, 'Noche');

-- Insertar datos en la tabla MetaPredeterminada
INSERT INTO `MetaPredeterminada` (`Nombre`, `TipoDeRutinaID`) VALUES
('Meta de Resistencia Avanzada', 1),
('Meta de Fuerza Superior', 2),
('Meta de Flexibilidad Extrema', 3);

-- Insertar datos en la tabla EspecialidadInstructor
INSERT INTO `EspecialidadInstructor` (`InstructorID`, `EspecialidadID`) VALUES
(1, 1),
(2, 2),
(3, 3);

-- Insertar datos en la tabla Cliente
INSERT INTO `Cliente` (`ClienteID`, `Talla`, `PorcentajeGrasaCorporal`, `NivelCondicionFisica`, `ObjetivoPrincipal`, `HistorialLesiones`, `EnfermedadesPreexistentes`, `PreferenciasEntrenamiento`, `FechaRegistro`) VALUES
(1, 1.75, 20.5, 'Intermedio', 'Perder peso', 'Ninguna', 'Ninguna', 'Entrenamientos HIIT', '2024-01-10');

-- Insertar datos en la tabla Rutina
INSERT INTO `Rutina` (`Nombre`, `TipoID`, `Descripcion`, `Frecuencia`, `FechaInicio`, `FechaFin`, `Imagen1`, `Imagen2`, `Objetivos`, `InstructorID`, `ClienteID`) VALUES
('Rutina de Cardio Avanzada', 1, 'Una rutina avanzada de entrenamiento cardiovascular.', '3 veces por semana', '2024-01-15', '2024-03-15', NULL, NULL, 'Mejorar la resistencia cardiovascular', 1, 1),
('Rutina de Fuerza Total', 2, 'Entrenamiento completo para desarrollar masa muscular.', '4 veces por semana', '2024-01-15', '2024-04-15', NULL, NULL, 'Desarrollo muscular y fuerza', 2, NULL);

-- Insertar datos en la tabla Meta
INSERT INTO `Meta` (`Nombre`, `EstadoInicial`, `EstadoFinal`, `RutinaID`) VALUES
('Mejorar la resistencia cardiovascular', 50.0, 40.0, 1),
('Desarrollo muscular y fuerza', 80.0, 70.0, 2);
