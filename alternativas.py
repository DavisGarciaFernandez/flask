# --------------------------------------------- Para Comision ----------------------------------
esquemas = [('-1',""),
            ('0',"CUOTA FIJA"),
            ('1','CUOTA FLEXIBLE'),
            ('2','CUOTA MIXTA'),
            ('10','CUOTA PUENTE')
            ]

monto_unidades = [('-1',""),
                ('0','Soles'),
                ('1','Dolares')
                ]

tipo_pagadores = [('-1',""),
                ('0',"No es cliente Prestamype"),
                ('1',"Mal pagador")]

distritos = [('-1',""),
            ('0','SAN ISIDRO'),
            ('1','MIRAFLORES'),
            ('2','SANTIAGO DE SURCO'),
            ('3','SAN BORJA'),
            ('4','BARRANCO'),
            ('5','ASIA'),
            ('6','CHILCA'),
            ('7','SAN BARTOLO'),
            ('8','PUNTA HERMOSA'),
            ('9','SANTA ROSA'),
            ('10','SANTA MARIA DEL MAR'),
            ('11','PUCUSANA'),
            ('12','MAGDALENA DEL MAR'),
            ('13','PUEBLO LIBRE'),
            ('14','LINCE'),
            ('15','JESUS MARÍA'),
            ('16','SURQUILLO'),
            ('17','SAN MIGUEL'),
            ('18','BREÑA'),
            ('19','CERCADO DE LIMA'),
            ('20','LA VICTORIA'),
            ('21','RIMAC'),
            ('22','SAN LUIS'),
            ('23','CARABAYLLO'),
            ('24','COMAS'),
            ('25','INDEPENDENCIA'),
            ('26','LOS OLIVOS'),
            ('27','PUENTE PIEDRA'),
            ('28','SAN MARTÍN DE PORRES'),
            ('29','CHORRILLOS'),
            ('30','LURIN'),
            ('31','SAN JUAN DE MIRAFLORES'),
            ('32','VILLA EL SALVADOR'),
            ('33','VILLA MARÍA DEL TRIUNFO'),
            ('34','PACHACAMAC'),
            ('35','ATE'),
            ('36','CHACLACAYO'),
            ('37','LURIGANCHO'),
            ('38','LA MOLINA'),
            ('39','SAN JUAN DE LURIGANCHO'),
            ('40','SANTA ANITA'),
            ('41','CALLAO'),
            ('42','VENTANILLA'),
            ('43','BELLAVISTA'),
            ('44','LA PERLA'),
            ('45','CARMEN DE LA LEGUA'),
            ('46','AREQUIPA'),
            ('47','OTROS')
            ]

niveles_de_riesgos = [('-1',""),
                    ('0','Bajo'),
                    ('1','Bajo Medio'),
                    ('2','Moderado'),
                    ('3','Moderado Medio'),
                    ('4','Medio')
                    ]

tipos_propiedades = [('-1',""),
                    ('0','Casa'),
                    ('1','Departamento'),
                    ('2','Edificio'),
                    ('3','Terreno'),
                    ('4','Local')
                    ]

pagos_puntuales = [('-1',""),
                    ('0','No'),
                    ('1','Sí'),
                    ]

compras_ventas = [('-1',""),
                    ('0','No'),
                    ('1','Sí'),
                    ]

con_hipotecas = [('-1',""),
                ('0','No'),
                ('1','Simultaneo'),
                ('2','No simultaneo')
                ]

cuotas_puentes = [('-1',""),
                    ('0','No'),
                    ('1','Sí'),
                    ]



opciones_brokers = [('-1',""),
                    ('0','No'),
                    ('1','Si broker o FUVEX'),
                    ('2','Si True Solutions Buro')
                    ]

def numeroATexto_CuotaPuente(num):
    return dict(cuotas_puentes)[num]

def numeroATexto_TipoPagador(num):
    return dict(tipo_pagadores)[num]

def numeroATexto_Esquema(num):
    return dict(esquemas)[num]
def numeroATexto_MontoUnidades(num):
    return dict(monto_unidades)[num]

def numeroATexto_Distrito(num):
    if type(num) is not list:
        return dict(distritos)[num]
    elif type(num) is list:
        resultado = []
        for i in range(len(num)):
            resultado.append(dict(distritos)[num[i]])
        return resultado



def numeroATexto_NivelDeRiesgo(num):
    if type(num) is not list:
        return dict(niveles_de_riesgos)[num]
    elif type(num) is list:
        resultado = []
        for i in range(len(num)):
            resultado.append(dict(niveles_de_riesgos)[num[i]])
        return resultado

def numeroATexto_TipoPropiedad(num):
    if type(num) is not list:
        return dict(tipos_propiedades)[num]
    elif type(num) is list:
        resultado = []
        for i in range(len(num)):
            resultado.append(dict(tipos_propiedades)[num[i]])
        return resultado

def numeroATexto_PagoPuntual(num):
    return dict(pagos_puntuales)[num]
def numeroATexto_CompraVenta(num):
    return dict(compras_ventas)[num]
def numeroATexto_Hipoteca(num): 
    return dict(con_hipotecas)[num]
def numeroATexto_OpcionBroker(num):
    return dict(opciones_brokers)[num]

# -------------------------------------------Para Tasa------------------------------------

tipos_de_deudas = [('-1',""),
                    ('0','Medio con castigo vigente'),
                    ('1','Medio sin castigo vigente pero historico más de 120 dias y menos de 180 dias'),
                    ('2','Medio sin castigo vigente pero historico más de 180 dias y menos de 360 dias'),
                    ('3','Medio sin castigo vigente pero historico más de 360 dias')
                    ]

def numeroATexto_TipoDeuda(num):
    if type(num) is not list:
        return dict(tipos_de_deudas)[num]
    elif type(num) is list:
        resultado = []
        for i in range(len(num)):
            resultado.append(dict(tipos_de_deudas)[num[i]])
        return resultado

# -------------------------------------------Para Cronograma------------------------------------------
tasas_particulares = [('-1',""),
                ('0','NO'),
                ('1','SI')
                ]
comisiones_particulares = [('-1',""),
                ('0','NO'),
                ('1','SI')
                ]

tipos_cronogramas = [('-1',""),
                ('0',"CUOTA MIXTA"),
                ('1',"CUOTA FIJA"),
                ('2',"CUOTA PUENTE"),
                ('3',"CUOTA FLEXIBLE")
                ]
def numeroATexto_TipoCronograma(num):
    return dict(tipos_cronogramas)[num]         