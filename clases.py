from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField, TimeField, IntegerField, FloatField, DateField
from alternativas import *
from funciones import *

class MyForm_Comision(FlaskForm):
    monto = StringField('Monto:')
    monto_unidad = SelectField('Moneda:', choices=monto_unidades)
    esquema = SelectField('Esquema:', choices=esquemas)
    pago_puntual = SelectField('¿Pago puntual?:', choices=pagos_puntuales)
    compra_venta = SelectField('¿Operación compra venta?:', choices=compras_ventas)
    con_hipoteca = SelectField('¿Con hipoteca?:', choices=con_hipotecas)
    num_propiedad = IntegerField('Número de propiedades:')
    opcion_broker = SelectField('¿Tiene Broker?:', choices=opciones_brokers)
    tipo_pagador = SelectField('¿Tipo pagador?:', choices=tipo_pagadores)
    submit = SubmitField('Enviar datos de Comision')


class MyForm_Tasa(FlaskForm):
    plazo = StringField('Plazo(meses):')
    tasa_particular = SelectField('Tasa particular:', choices=tasas_particulares)
    comision_particular = SelectField('Comisión particular:', choices=comisiones_particulares)
    cuota_puente = SelectField('Cuota Puente:', choices=cuotas_puentes)
    
    distrito_1 = SelectField('Distrito:', choices=distritos)
    tipo_propiedad_1 = SelectField('Tipo de propiedad:', choices=tipos_propiedades)
    nivel_riesgo_1 = SelectField('Nivel de riesgo:', choices=niveles_de_riesgos)
    tipo_deuda_1 = SelectField('Tipo de deuda:', choices=tipos_de_deudas)

    distrito_2 = SelectField('Distrito:', choices=distritos)
    tipo_propiedad_2 = SelectField('Tipo de propiedad:', choices=tipos_propiedades)
    nivel_riesgo_2 = SelectField('Nivel de riesgo:', choices=niveles_de_riesgos)
    tipo_deuda_2 = SelectField('Tipo de deuda:', choices=tipos_de_deudas)

    distrito_3 = SelectField('Distrito:', choices=distritos)
    tipo_propiedad_3 = SelectField('Tipo de propiedad:', choices=tipos_propiedades)
    nivel_riesgo_3 = SelectField('Nivel de riesgo:', choices=niveles_de_riesgos)
    tipo_deuda_3 = SelectField('Tipo de deuda:', choices=tipos_de_deudas)
    
    

    submit = SubmitField('Enviar datos de Tasa')


class MyForm_Cronograma(FlaskForm):
    tasa_final = StringField('Tasa final:')
    comision_total = StringField('Comisión total:')
    tipo_cronograma = SelectField('Tipo Cronograma: ', choices=tipos_cronogramas)

    submit = SubmitField('Enviar datos de Cronograma')            