CREATE TABLE TIPO_CITA(
    codTc INT AUTO_INCREMENT NOT NULL,
    nomTc   VARCHAR(20),
    PRIMARY KEY (codTc)
);

CREATE TABLE BOX(
    codBox INT NOT NULL,
    codPm  INT,
    PRIMARY KEY (codBox)
);

CREATE TABLE TURNOS(
    codTur INT NOT NULL,
    codPm  INT,
    dia_T     VARCHAR(20),
    hora_iT  TIME,
    hora_fT  TIME,
    PRIMARY KEY (codTur)
);


CREATE TABLE CITA(
    codCit INT AUTO_INCREMENT PRIMARY KEY,
    rut_P INT,
    codBox INT,
    codTc  INT,
    codPm  INT,
    codRep INT,
    fecha  DATE,
    hora   TIME
);

CREATE TABLE MEDICO(
    codPm INT AUTO_INCREMENT NOT NULL,
    codTra INT,
    funcion VARCHAR(30),
    PRIMARY KEY (codPm)
);

CREATE TABLE DISPONIBILIDAD(
    codDis INT NOT NULL,
    codPm   INT,
    dia     VARCHAR(20),
    hora_iD TIME,
    hora_fD TIME,
    PRIMARY KEY(codDis)
);

CREATE TABLE ATENCION(
    codAte INT AUTO_INCREMENT PRIMARY KEY,
    codPm INT,
    rut_P  INT,
    tratamiento VARCHAR(500),
    receta VARCHAR(200),
    descripcion VARCHAR(300),
    diagnostico VARCHAR(100),
    fecha_a DATE
);


CREATE TABLE PACIENTE(
    rut_P INT,
    nombre_P VARCHAR(20),
    direccion_P VARCHAR(20),
    comuna_P VARCHAR(50),
    telefono_P VARCHAR(20),
    email_P VARCHAR(50),
    PRIMARY KEY(rut_P)
    
);

CREATE TABLE RECEPCIONISTA(
    codRep INT NOT NULL,
    codTra INT,
    PRIMARY KEY(codRep)
);


CREATE TABLE TRABAJADOR(
    codTra INT AUTO_INCREMENT,
    rut_T INT,
    nombre_T VARCHAR(30),
    direccion_T VARCHAR(50),
    telefono_T VARCHAR(20),
    email_T VARCHAR(20),
    PRIMARY KEY(codTra)
);

CREATE TABLE TIPO_ESPECIALIDAD(
    codEsp INT NOT NULL,
    codPm  INT
    
);

CREATE TABLE ESPECIALIDAD(
    codEsp INT,
    nombre VARCHAR(30),
    PRIMARY KEY(codEsp)
);

CREATE TABLE USUARIO(
    codU INT NOT NULL,
    codTra INT,
    codPer INT,
    pass VARCHAR(30),
    PRIMARY KEY(codU)
);

CREATE TABLE PERFIL(
    codPer INT NOT NULL,
    nombre_Perfil VARCHAR(15),
    PRIMARY KEY(codPer)
);

CREATE TABLE FARMACEUTICO(
    codFar INT AUTO_INCREMENT NOT NULL,
    codTra INT,
    PRIMARY KEY(codFar)
);

CREATE TABLE REGISTRO_BODEGA(
    codMov INT AUTO_INCREMENT PRIMARY KEY,
    codTipoM INT,
    codFar INT,
    codIns INT,
    fecIns DATE,
    fecVec DATE,
    lote   INT,
    stock  INT
);

CREATE TABLE TIPO_MOVIMIENTO(
    codTipoM INT NOT NULL,
    nombre_tm VARCHAR(20),
    PRIMARY KEY(codTipoM)
);

CREATE TABLE INSUMO(
    codIns INT NOT NULL,
    codTipoI INT,
    codUbi INT,
    nombre_in VARCHAR(20),
    stock INT,
    PRIMARY KEY (codIns)
);

CREATE TABLE TIPO_INSUMO(
    codTipoI INT,
    nombre_ti VARCHAR(20),
    PRIMARY KEY(codTipoI)
);

CREATE TABLE UBICACION_BODEGA(
    codUbi INT NOT NULL,
    nombre_ub VARCHAR(20),
    PRIMARY KEY(codUbi)
);

CREATE TABLE ACEPTACION(
  RESPUESTA VARCHAR(2) PRIMARY KEY
);



ALTER TABLE TURNOS
ADD FOREIGN KEY (codPm) REFERENCES MEDICO(codPm);


ALTER TABLE DISPONIBILIDAD
ADD FOREIGN KEY (codPm) REFERENCES MEDICO(codPm);

ALTER TABLE MEDICO 
ADD FOREIGN KEY (codTra) REFERENCES TRABAJADOR(codTra);

ALTER TABLE TIPO_ESPECIALIDAD 
ADD FOREIGN KEY (codEsp) REFERENCES ESPECIALIDAD(codEsp);

ALTER TABLE TIPO_ESPECIALIDAD
ADD FOREIGN KEY(codPm) REFERENCES MEDICO(codPm);

ALTER TABLE BOX
ADD FOREIGN KEY(codPm) REFERENCES MEDICO(codPm);


ALTER TABLE CITA
ADD FOREIGN KEY(codBox) REFERENCES BOX(codBox);


ALTER TABLE CITA
ADD FOREIGN KEY(codTc) REFERENCES TIPO_CITA(codTc);


ALTER TABLE CITA
ADD FOREIGN KEY(codPm) REFERENCES MEDICO(codPm);

ALTER TABLE CITA
ADD FOREIGN KEY(rut_P) REFERENCES PACIENTE(rut_P);

ALTER TABLE CITA
ADD FOREIGN KEY(codRep) REFERENCES RECEPCIONISTA(codRep);


ALTER TABLE RECEPCIONISTA
ADD FOREIGN KEY(codTra) REFERENCES TRABAJADOR(codTra);

ALTER TABLE ATENCION
ADD FOREIGN KEY(codPm) REFERENCES MEDICO(codPm);

ALTER TABLE ATENCION
ADD FOREIGN KEY(rut_P) REFERENCES PACIENTE(rut_P);

ALTER TABLE FARMACEUTICO
ADD FOREIGN KEY(codFar) REFERENCES TRABAJADOR(codTra);

ALTER TABLE REGISTRO_BODEGA
ADD FOREIGN KEY(codTipoM) REFERENCES TIPO_MOVIMIENTO(codTipoM);

ALTER TABLE REGISTRO_BODEGA
ADD FOREIGN KEY(codFar) REFERENCES FARMACEUTICO(codFar);

ALTER TABLE REGISTRO_BODEGA
ADD FOREIGN KEY(codIns) REFERENCES INSUMO(codIns);

ALTER TABLE INSUMO
ADD FOREIGN KEY(codTipoI) REFERENCES TIPO_INSUMO(codTipoI);

ALTER TABLE INSUMO
ADD FOREIGN KEY(codUbi) REFERENCES UBICACION_BODEGA(codUbi);

ALTER TABLE USUARIO
ADD FOREIGN KEY(codTra) REFERENCES TRABAJADOR(codTra);


ALTER TABLE USUARIO
ADD FOREIGN KEY(codPer) REFERENCES PERFIL(codPer);


INSERT INTO PACIENTE VALUES(123456789,'JUAN PÉREZ','ALMIRANTE 123','SANTIAGO',912345678,'juan@example.com'),
  (987654321,'ANA LÓPEZ','AVENIDA CENTRAL 456','SAN MIGUEL',987654321,'ana@example.com'),
  (567890123,'PEDRO RAMÍREZ','PUNTA ARENAS 789','LA FLORIDA',956789012,'pedro@example.com'),
  (321098765,'MARÍA FERNÁNDEZ','CALLE SECUNDARIA 321','MACUL',932109876,'maria@example.com'),
  (654321098,'CARLOS GÓMEZ','AUXILIADORA 987','MAIPU',965432109,'carlos@example.com');


INSERT INTO TRABAJADOR VALUES(1,123456789,'MARÍA GONZÁLEZ','CALLE PRINCIPAL 123',912345678,'m.gonzalez@kill.cl'),
  (2,987654321,'JUAN TORRES','AVENIDA CENTRAL 456',987654321,'j.torres@kill.cl'),
  (3,56789013,'CARLOS RAMÍREZ','PLAZA MAYOR 789',956789012,'c.ramirez@kill.cl'),
  (4,321098765,'LAURA FERNÁNDEZ','CALLE SECUNDARIA 321',932109876,'l.fernandez@kill.cl'),
  (5,654321098,'ANDRÉS GÓMEZ','AV. PRINCIPAL 987',965432109,'a.gomez@kill.cl'),
  (6,112233445,'ANA LÓPEZ','CALLE DEL SOL 456',911223344,'a.lopez@kill.cl'),
  (7,556677889,'RICARDO SILVA','AVENIDA CENTRAL 789',955667788,'r.silva@kill.cl'),
(8,998877665,'SANDRA TORRES','PLAZA PRINCIPAL 123',999887766,'s.torres@kill.cl'),
  (9,443322110,'DIEGO ROJAS','CALLE DEL MAR 456',944332211,'d.rojas@kill.cl'),
  (10,223344556,'ANA CÁCERES','AV PRINCIPAL 789',922334455,'a.caceres@kill.cl'),
  (11,778899002,'DANIEL MORALES','CALLE DEL SOL 123',977889900,'d.morales@kill.cl'),
  (12,152358466,'CLAUDIA SALAZAR','AVENIDA CENTRAL 456',900112233,'c.salazar@kill.cl'),
  (13,334455667,'ANDRÉS ESPINOZA','PLAZA MAYOR 789',933445566,'a.espinoza@kill.cl'),
  (14,889900118,'KARLA MENDOZA','CALLE PRINCIPAL 321',988990011,'k.mendoza@kill.cl'),
  (15,265123685,'RICARDO VALENZUELA','AVENIDA DEL SOL 9',955667788,'r.valenzuela@kill.cl'),
  (16,123344577,'LAURA SÁNCHEZ','CALLE PRINCIPAL 654',922336455,'l.sanchez@kill.cl');



INSERT INTO MEDICO VALUES(1,1,'MEDICINA'),
  (2,2,'PEDIATRÍA'),
  (3,3,'OTORRINOLOGIA'),
  (4,4,'CARDIOLOGÍA'),
  (5,5,'DERMATOLOGÍA');


INSERT INTO DISPONIBILIDAD VALUES(1,1,'LUNES','08:00:00','17:00:00'),
  (2,1,'MARTES','08:00:00','17:00:00'),
  (3,1,'MIERCOLES','08:00:00','17:00:00'),
  (4,1,'JUEVES','08:00:00','17:00:00'),
  (5,1,'VIERNES','08:00:00','17:00:00');

  INSERT INTO TURNOS VALUES(1,1,'LUNES','08:00:00','17:00:00'),
  (2,1,'MARTES','08:00:00','17:00:00'),
  (3,1,'MIERCOLES','08:00:00','17:00:00'),
  (4,1,'JUEVES','08:00:00','17:00:00'),
  (5,1,'VIERNES','08:00:00','17:00:00');


INSERT INTO ESPECIALIDAD VALUES(1,'MEDICINA GENERAL'),
  (2,'PEDIATRIA'),
  (3,'OTORRINOLOGIA'),
  (4,'CARDIOLOGIA'),
  (5,'DERMATOLOGIA');

INSERT INTO TIPO_ESPECIALIDAD VALUES(1,1),
  (2,1),
  (1,2),
  (5,2),
  (5,3);

INSERT INTO BOX VALUES(1,1),
  (2,2),
  (3,3),
  (4,4),
  (5,5);


INSERT INTO TIPO_CITA VALUES(1,'CONSULTA GENERAL'),
  (2,'EXAMEN'),
  (3,'PROCEDIMIENTO'),
  (4,'ESPECIALIDAD'),
  (5,'CIRUGIA');

INSERT INTO RECEPCIONISTA VALUES(1,6),
  (2,7),
  (3,8),
  (4,9),
  (5,10);


INSERT INTO CITA VALUES
(1,123456789,1,1,1,1,'2023-05-05','09:10:00'),
  (2,987654321,1,1,1,2,'2023-05-10','10:25:00'),
  (3,567890123,1,1,1,3,'2023-05-17','11:30:00'),
  (4,321098765,1,1,1,4,'2023-05-22','12:55:00'),
  (5,654321098,1,1,1,5,'2023-05-29','09:45:00');


INSERT INTO ATENCION VALUES(1,1,123456789,'Descansar, hidratarse, tomar paracetamol para la fiebre y el malestar, usar descongestionantes nasales y hacer gárgaras con agua tibia y sal.','paracetamol cada 8 hrs','Paciente presenta congestión nasal, estornudos frecuentes y malestar general, sin fiebre ni dificultad respiratoria','resfriado comun','2023-05-05'),
  (2,1,987654321,'Descansar, hidratarse, evitar alimentos sólidos, tomar líquidos claros como caldo de pollo, bebidas isotónicas y medicamentos antidiarreicos bajo supervisión médica.','viadil cada 8 hrs','Paciente experimenta náuseas, vómitos y diarrea, acompañados de dolor abdominal y malestar generalizado.','gastroenteritis','2023-05-10'),
  (3,1,567890123,'Dieta baja en sodio, ejercicio regular, medicamentos antihipertensivos y seguimiento de la presión arterial.','consultar especialista cardiologia','Paciente muestra lecturas consistentemente elevadas de presión arterial en múltiples visitas,  falta de síntomas aparentes','Hipertensión arterial','2023-05-17'),
  (4,1,321098765,'Dieta equilibrada, control de carbohidratos, actividad física regular, medicamentos antidiabéticos y monitoreo de glucosa en sangre.','consultar especialista nutricionista','Paciente presenta niveles altos de azúcar en sangre (hiperglucemia) junto con síntomas como sed excesiva, aumento de la micción y fatiga persistente.','Diabetes tipo 2','2023-05-22'),
  (5,1,654321098,'escansar, hidratarse, medicamentos para aliviar la tos y la congestión, evitar irritantes respiratorios y realizar inhalaciones de vapor o usar un humidificador.','salbutamol','presenta tos persistente con expectoración y dificultad para respirar, síntomas de infección respiratoria como fiebre y malestar general.','Bronquitis aguda','2023-05-29');



INSERT INTO FARMACEUTICO VALUES(1,11),
  (2,12),
  (3,13),
  (4,14),
  (5,15);


INSERT INTO PERFIL VALUES(1,'ADMINISTRADOR'),
  (2,'MEDICO'),
  (3,'RECEPCIONISTA'),
  (4,'FARMACEUTICO'),
    (5,'INACTIVO');


INSERT INTO USUARIO VALUES
  (123456789,1,2,'medico123'),
  (987654321,2,2,'medico123'),
  (123344577,16,1,'admin123'),
  (112233445,6,3,'rep123'),
  (778899002,11,4,'far123');


INSERT INTO UBICACION_BODEGA VALUES(1,'BODEGA 1'),
  (2,'BODEGA 2'),
  (3,'REFRIGERADOR 1'),
  (4,'REFRIGERADOR 2'),
  (5,'GABINETE 1');


INSERT INTO TIPO_INSUMO VALUES(1,'MEDICAMENTOS'),
  (2,'MATERIAL QUIRÚRGICO'),
  (3,'EQUIPOS MÉDICOS'),
  (4,'PARA LABORATORIO'),
  (5,'CONSUMIBLES MÉDICOS');


INSERT INTO INSUMO VALUES(1,1,5,'PARACETAMOL',20),
  (2,1,5,'IBUPROFENO',30),
  (3,1,5,'AMOXICILINA',15),
  (4,1,5,'OMEPRAZOL',60),
  (5,1,5,'ATORVASTATINA',25),
  (6,2,1,'GASA ESTÉRIL',100),
  (7,2,1,'TIJERAS DE CURVA',8),
  (8,2,1,'AGUJA HIPODÉRMICA',25),
  (9,2,1,'VENDA ADHESIVA',40),
  (10,2,1,'ESPARADRAPO',20),
  (11,3,1,'ESTETOSCOPIO',3),
  (12,3,1,'TERMÓMETRO',12),
  (13,3,1,'DESFIBRILADOR',2),
  (14,3,1,'ESFIGMOMANÓMETRO',6),
  (15,3,1,'OXÍMETRO DE PULSO',5),
  (16,4,2,'MICROSCOPIO',4),
  (17,4,2,'TUBOS DE ENSAYO',50),
  (18,4,2,'PIPETA GRADUADA',20),
  (19,4,2,'BALANZA ANALÍTICA',2),
  (20,4,2,'AGITADOR MAGNÉTICO',6),
  (21,5,1,'ALGODÓN',30),
  (22,5,1,'GUANTES DE LÁTEX',100),
  (23,5,1,'MASCARILLAS',50),
  (24,5,1,'JERINGAS',40),
  (25,5,4,'BOLSAS DE SUERO',15);

  INSERT INTO TIPO_MOVIMIENTO VALUES(1,'RETIRO'),
  (2,'INGRESO'),
  (3,'DESECHADO'),
  (4,'REVISION'),
  (5,'RE-UBICACIÓN');


INSERT INTO REGISTRO_BODEGA VALUES(1,1,1,1,'2023-05-05','2024-05-05',123456,20),
  (2,1,2,2,'2023-05-10','2024-05-10',234569,30),
  (3,1,3,3,'2023-05-17','2024-05-17',597562,15),
  (4,1,4,4,'2023-05-22','2024-05-22',125632,60),
  (5,1,5,5,'2023-05-29','2024-05-29',85245,25),
  (6,1,1,1,'2023-06-01','2023-07-01',789012,15),
  (7,1,2,2,'2023-06-05','2023-06-30',346587,25),
  (8,1,3,3,'2023-06-10','2023-06-30',124578,10),
  (9,1,4,4,'2023-06-15','2023-07-05',369874,30),
  (10,1,5,5,'2023-06-20','2023-07-10',965874,20);

INSERT INTO ACEPTACION VALUES("NO");