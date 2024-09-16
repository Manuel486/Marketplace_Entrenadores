-- Base de datos full_ventas_portal

-- Insertar datos en la tabla Especialidad
INSERT INTO `Especialidad` (`Nombre`, `Estado`, `FechaCreacion`, `FechaActualizacion`) VALUES
('Cardio', 'Activo', '2024-01-01', '2024-01-01'),
('Fuerza', 'Activo', '2024-01-01', '2024-01-01'),
('Flexibilidad', 'Activo', '2024-01-01', '2024-01-01');

-- Insertar datos en la tabla TipoDeRutina
INSERT INTO `TipoDeRutina` (`Nombre`, `Descripcion`, `EspecialidadID`) VALUES
('Entrenamiento de Resistencia', 'Rutina enfocada en aumentar la resistencia cardiovascular.', 1),
('Entrenamiento de Fuerza Muscular', 'Rutina enfocada en el desarrollo de masa muscular.', 2),
('Entrenamiento de Flexibilidad', 'Rutina enfocada en mejorar la flexibilidad y el rango de movimiento.', 3);

-- Insertar datos en la tabla Local
INSERT INTO `Local` (`Nombre`, `Direccion`, `Telefono`) VALUES
('Gym Central', 'Calle Falsa 123, Ciudad', '123456789'),
('Fitness Club', 'Avenida Principal 456, Ciudad', '987654321');

-- Insertar datos en la tabla Instructor
INSERT INTO `Instructor` (`Nombres`, `Apellidos`, `Email`, `Edad`, `Sexo`, `FechaNacimiento`, `LocalID`) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', 30, 'M', '1994-05-15', 1),
('Ana', 'Gómez', 'ana.gomez@example.com', 28, 'F', '1996-07-20', 2),
('Carlos', 'Mendoza', 'carlos.mendoza@example.com', 35, 'M', '1989-12-01', 1);

-- Insertar datos en la tabla InformacionPersonalInstructor
INSERT INTO `InformacionPersonalInstructor` (`InstructorID`, `PreferenciaHorario`) VALUES
(1, 'Mañana'),
(2, 'Tarde'),
(3, 'Noche');

-- Insertar datos en la tabla Usuario
INSERT INTO `Usuario` (`Username`, `Password`, `Email`, `Nombre`, `Apellido`, `Tipo`) VALUES
('cliente1', 'password123', 'cliente1@example.com', 'Laura', 'Martínez', 'Cliente'),
('instructor1', 'password123', 'instructor1@example.com', 'David', 'Rodríguez', 'Instructor');

-- Insertar datos en la tabla Cliente
INSERT INTO `Cliente` (`ClienteID`, `Talla`, `PorcentajeGrasaCorporal`, `NivelCondicionFisica`, `ObjetivoPrincipal`, `HistorialLesiones`, `EnfermedadesPreexistentes`, `PreferenciasEntrenamiento`, `FechaRegistro`) VALUES
(1, 1.75, 20.5, 'Intermedio', 'Perder peso', 'Ninguna', 'Ninguna', 'Entrenamientos HIIT', '2024-01-10');

-- Insertar datos en la tabla Rutina
INSERT INTO `Rutina` (`Nombre`, `TipoID`, `Descripcion`, `Frecuencia`, `FechaInicio`, `FechaFin`, `Imagen`, `HorasRecomendadas`, `Objetivos`, `InstructorID`, `ClienteID`) VALUES
('Rutina de Cardio Avanzada', 1, 'Una rutina avanzada de entrenamiento cardiovascular.', '3 veces por semana', '2024-01-15', '2024-03-15', NULL, '1 hora', 'Mejorar la resistencia cardiovascular', 1, 1),
('Rutina de Fuerza Total', 2, 'Entrenamiento completo para desarrollar masa muscular.', '4 veces por semana', '2024-01-15', '2024-04-15', NULL, '1.5 horas', 'Desarrollo muscular y fuerza', 2, NULL);

-- Insertar datos en la tabla MedidasCorporales
INSERT INTO `MedidasCorporales` (`Estado`, `Bicep`, `Tricep`, `Pectorales`, `Dorsales`, `Cintura`, `Gluteos`, `Cuello`, `RutinaID`) VALUES
('B', 30.0, 25.0, 40.0, 35.0, 80.0, 95.0, 40.0, 1),
('O', 32.0, 26.0, 42.0, 36.0, 78.0, 94.0, 41.0, 2);
