import json
import os
import math
import openpyxl
import numpy as np
import numpy_financial as npf
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime
from scipy.optimize import fsolve

#-------------------------------------------EXTRAER INFORMACIÓN DE LOS JSON-----------------------------------
def extraer_datos(clave):
    if os.path.exists("datos.json"):
        with open('datos.json', 'r') as file:
            data = json.load(file)
        return data.get(clave, None) 
    else:
        return False


def extraer_datos_fondos(clave):
    if os.path.exists("datos_fondos.json"):
        with open('datos_fondos.json', 'r') as file:
            data = json.load(file)
        return data.get(clave, None) 
    else:
        return False

def agregar_datos(clave, valor):
    if os.path.exists("datos.json"):
        with open('datos.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}

    data[clave] = valor

    with open('datos.json', 'w') as file:
        json.dump(data, file)

    return True

def agregar_datos_fondos(clave, valor):
    if os.path.exists("datos_fondos.json"):
        with open('datos_fondos.json', 'r') as file:
            data = json.load(file)
    else:
        data = {}

    data[clave] = valor

    with open('datos_fondos.json', 'w') as file:
        json.dump(data, file)

    return True

def extraer_calculo_comision(clave):
    if os.path.exists("calculo_comision.json"):
        with open('calculo_comision.json', 'r') as file:
            data = json.load(file)
        return data.get(clave, None) 
    else:
        return True

def extraer_calculo_tasa(clave):
    if os.path.exists("calculo_tasa.json"):
        with open('calculo_tasa.json', 'r') as file:
            data = json.load(file)
        return data.get(clave, None) 
    else:
        return True

def extraer_calculo_cronograma(clave):
    if os.path.exists("calculo_cronograma.json"):
        with open('calculo_cronograma.json', 'r') as file:
            data = json.load(file)
        return data.get(clave, None) 
    else:
        return True



# -------------------------------------- main_comision------------------------------------

def operarComision():
    tabla_distrito = {
            "SAN ISIDRO": 0.00, "MIRAFLORES": 0.00, "SANTIAGO DE SURCO": 0.90, "SAN BORJA": 0.90,
            "BARRANCO": 1.13, "ASIA": 1.13, "CHILCA": 1.13, "SAN BARTOLO": 0.90,
            "PUNTA HERMOSA": 0.90, "SANTA ROSA": 1.35, "SANTA MARIA DEL MAR": 0.90, "PUCUSANA": 1.13,
            "MAGDALENA DEL MAR": 1.35, "PUEBLO LIBRE": 1.58, "LINCE": 1.13, "JESUS MARIA": 1.13,
            "SURQUILLO": 1.35, "SAN MIGUEL": 1.13, "BREÑA": 1.58, "CERCADO DE LIMA": 1.80,
            "LA VICTORIA": 1.80, "RIMAC": 2.25, "SAN LUIS": 1.80, "CARABAYLLO": 2.25,
            "COMAS": 2.03, "INDEPENDENCIA": 2.03, "LOS OLIVOS": 1.58, "PUENTE PIEDRA": 2.25,
            "SAN MARTIN DE PORRES": 2.03, "CHORRILLOS": 1.58, "LURIN": 2.03, "SAN JUAN DE MIRAFLORES": 2.25,
            "VILLA EL SALVADOR": 2.03, "VILLA MARIA DEL TRIUNFO": 2.25, "PACHACAMAC": 2.48, "ATE": 1.80,
            "CHACLACAYO": 2.03, "LURIGANCHO": 2.25, "LA MOLINA": 1.80, "SAN JUAN DE LURIGANCHO": 2.25,
            "SANTA ANITA": 2.03, "CALLAO": 2.25, "VENTANILLA": 2.48, "BELLAVISTA": 2.25,
            "LA PERLA": 2.25, "CARMEN DE LA LEGUA": 2.48, "AREQUIPA": 2.25, "OTROS": 2.475
        }

    tabla_esquema = {
            "CUOTA FIJA": 0.00225,
            "CUOTA FLEXIBLE": 0.00,
            "CUOTA MIXTA": 0.0045,
            "CUOTA PUENTE": 0.0045,
        }


    tabla_riesgo = {
            "Riesgo Bajo": 0.00,
            "Bajo medio": 0.0045,
            "Moderado": 0.009,
            "Moderado Medio": 0.0135,
            "Medio": 0.018,
        }

    tabla_tipo_propiedad = {
            "Casa": 0.00,
            "Departamento": 0.00,
            "Edificio": 0.00,
            "Terreno": 0.01,
            "Local": 0.01,
        }

    tabla_broker_si_broker = {
            0: 1.00,
            300000: 0.85,
            400000: 0.75,
            500000: 0.60,
            750000: 0.50,
            1000001: 0.50,
            2000001: 0.50,
            4000001: 0.50,
            7000001: 0.50,
            10000001: 0.50,
        }

    tabla_broker_si_true = {
            0: 2.25,
            300000: 2.25,
            400000: 2.25,
            500000: 2.25,
            750000: 2.25,
            1000001: 2.50,
            2000001: 2.75,
            4000001: 3.00,
            7000001: 3.00,
            10000001: 3.00,
    }

    tabla_hipoteca_simultaneo = {
            0: 1000,
            20000: 1000,
            25000: 1000+((1500-1000)/(135000-25000))*(float(extraer_datos("monto"))-25000),
            135000: 1500+((2000-1500)/(250000-135000)) * (float(extraer_datos("monto"))-135000),
            250001: 2000,
        }

    tabla_hipoteca_no_simultaneo = {
            0: 1500,
            20000: 1500+((2750-1500)/(135000-20000))*(float(extraer_datos("monto"))-20000),
            25000: 2750+((4000-2750)/(250000-135000)) * (float(extraer_datos("monto"))-135000),
            135000: 2750+((4000-2750)/(250000-135000)) * (float(extraer_datos("monto"))-135000),
            250001: 4000
        }


    tabla10 = {
            0: 1100,
            99999: 1300, 
            199999: 1300,
            299999: 1400
        }


    tabla20 = {
            0: {'Gastos notariales hipoteca': 'Hasta $100,000', 'Costo soles': 450},
            100000: {'Gastos notariales hipoteca': 'Hasta $250,000', 'Costo soles': 550},
            250000: {'Gastos notariales hipoteca': 'Hasta $500,000', 'Costo soles': 650},
        }


    def buscar_valor_por_rango(monto, tabla):
        for rango, valor in sorted(tabla.items(), reverse=True):
            if monto >= rango:
                return valor
        return 0.00

    def buscar_gasto_notarial(monto_ajustado, tabla):
        for limite, info in sorted(tabla.items(), reverse=True):
            if monto_ajustado >= limite:
                return info['Costo soles']
        return 0

    def buscar_valor_en_tabla(monto_ajustado, tabla):
        # Ordena la tabla por sus claves (rangos) en orden descendente
        for limite in sorted(tabla.keys(), reverse=True):
            if monto_ajustado >= limite:
                return tabla[limite]
        return 0


    def calcular_total(monto, moneda, esquema, distrito, riesgo, tipo_propiedad, con_broker, con_hipoteca, tipo_pagador, compra_venta, num_propiedades):


        if monto > 100000:
            if monto > 600000:
                castigo_monto = 0.00
            else:
                castigo_monto = ((600000 - monto) / 10000 )*( 0.00122 / 2)
        else:
            castigo_monto = (600000 - monto) / 10000 * 0.00122

        castigo_esquema = tabla_esquema.get(esquema, 0.00)

        valor_distrito = tabla_distrito.get(distrito, 0.00) / 100

        if monto > 100000:
            valor_riesgo = tabla_riesgo.get(riesgo, 0.00) / (monto / 100000)
        else:
            valor_riesgo = tabla_riesgo.get(riesgo, 0.00)

        valor_tipo_propiedad = tabla_tipo_propiedad.get(tipo_propiedad, 0.00)

        castigo_distrito_riesgo_tipo_propiedad = valor_distrito + valor_riesgo + valor_tipo_propiedad
        
        # Cálculo para castigo_con_broker
        if con_broker == "No":
            castigo_con_broker = 0
        elif con_broker == "Si broker o FUVEX":
            castigo_con_broker = buscar_valor_por_rango(monto, tabla_broker_si_broker) / 100.0
        elif con_broker == "Si True Solutions Buro":
            castigo_con_broker = buscar_valor_por_rango(monto, tabla_broker_si_true) / 100.0
        else:
            castigo_con_broker = "error"


        # Cálculo para castigo_con_hipoteca
        if con_hipoteca == "Simultaneo":
            valor_hipoteca = buscar_valor_por_rango(monto, tabla_hipoteca_simultaneo)
            castigo_con_hipoteca = valor_hipoteca / monto
        elif con_hipoteca == "No simultaneo":
            valor_hipoteca = buscar_valor_por_rango(monto, tabla_hipoteca_no_simultaneo)
            castigo_con_hipoteca = valor_hipoteca / monto
        else:
            castigo_con_hipoteca = 0.00


        # Cálculo para castigo_tipo_pagador
        if tipo_pagador in ["No es cliente Prestamype", "Mal pagador"]:
            castigo_tipo_pagador = 0.003 / (monto / 100000)
        else:
            castigo_tipo_pagador = 0.00

        # Cálculo para castigo_compra_venta
        if compra_venta == "S\u00ed":
            castigo_compra_venta = 1000 / monto
        else:
            castigo_compra_venta = 0.00

        castigo_vri = 0.01 * (0.40 / 0.5)

        margen_bruto = float(castigo_monto) + float(castigo_esquema) + float(castigo_distrito_riesgo_tipo_propiedad) + float(castigo_con_broker) + float(castigo_con_hipoteca) + float(castigo_tipo_pagador) + float(castigo_compra_venta) + float(castigo_vri)


    ################################
        
        def redondear_mas(numero, decimales):
            factor = 10 ** decimales
            return math.ceil(numero * factor) / factor


        # Cálculo de Total Compra de deuda
        if con_hipoteca == "Simultaneo":
            base_calculo = (monto * (1 + redondear_mas((redondear_mas((margen_bruto) * (1 + 0.025), 2) + 0.01) * 1.1, 2)) * 2 / 3.2) * 5
            if base_calculo > 35000:
                total_compra_deuda = 200 + math.ceil(base_calculo / 5000) * 7.5 + 37 * num_propiedades + 300
            else:
                total_compra_deuda = 200 + math.ceil(base_calculo / 5000) * 0.75 + 37 * num_propiedades + 300
        else:
            total_compra_deuda = 0


        # Cálculo de Total Gastos registrales (Inscrip+Lev)
        base_calculo_gr = (monto * (1 + redondear_mas((redondear_mas((margen_bruto) * (1 + 0.025), 2) + 0.01) * 1.1, 2)) * 2 / 3.2) * 5
        if base_calculo_gr > 35000:
            total_gastos_registrales_inscrip_lev = 2 * (math.ceil(math.ceil(base_calculo_gr / 5000) * 7.5) + 37 * num_propiedades) + 600
        else:
            total_gastos_registrales_inscrip_lev = 2 * (math.ceil(math.ceil(base_calculo_gr / 5000) * 0.75) + 37 * num_propiedades) + 600
        #total_gastos_registrales_inscrip_lev = round(total_gastos_registrales_inscrip_lev)


        # Cálculo de Total Gastos registrales (C-V+Hipo)
        base_calculo_gastos_cv_hipo = (((monto * (1 + redondear_mas((redondear_mas((margen_bruto) * (1 + 0.025), 2) + 0.01) * 1.1, 2)) / num_propiedades) * 2 / 3.2) * 5) * 3 / 1000
        total_gastos_registrales_cv_hipo = redondear_mas(base_calculo_gastos_cv_hipo, 0) * num_propiedades + 40 * num_propiedades


        # Cálculo de Total Gastos Notariales (C-V+Hipo)
        monto_ajustado = ((monto * (1 + redondear_mas((redondear_mas((margen_bruto) * (1 + 0.025), 2) + 0.01) * 1.1, 2)) / num_propiedades) * 2 / 3.2) * num_propiedades
        valor_base = buscar_valor_en_tabla(monto_ajustado, tabla10)
        total_gastos_notariales_cv_hipo = valor_base + 300 + 100 + (10 * 1.18) + (48 * 1.18 * num_propiedades)


        # Cálculo de Total Gastos Notariales (Inscrip+Lev)
        monto_ajustado = (monto * (1 + redondear_mas((redondear_mas((margen_bruto) * (1 + 0.025), 2) + 0.01) * 1.1, 2))) * 2 / 3.2
        gastos_notariales_hipoteca = buscar_gasto_notarial(monto_ajustado, tabla20)
        total_gastos_notariales_inscrip_lev = gastos_notariales_hipoteca + 200 + 100 + 50 * (num_propiedades ** 2) + 11.8


        if compra_venta == "S\u00ed":
            total_gastos = (total_gastos_notariales_cv_hipo + total_gastos_registrales_cv_hipo +
                            total_gastos_registrales_inscrip_lev + total_compra_deuda)
        else:
            total_gastos = total_gastos_notariales_inscrip_lev + total_gastos_registrales_inscrip_lev + total_compra_deuda

        
        # Cálculo de total_gastos_broker
        total_gastos_broker = total_gastos # + monto * castigo_con_broker

        # Cálculo de gastos_operativos
        gastos_operativos = total_gastos_broker / monto # + castigo_con_hipoteca

        
        # Cálculo de comisión_total
        comision_total = redondear_mas(redondear_mas((redondear_mas((margen_bruto + gastos_operativos) * (1 + 0.025) * 100, 2) / 100 + 0.015) * 1.1, 2) * 1.3, 2)

        # guardo total gastos
        datos_fondos = {
            "total_gastos":total_gastos
        }
        with open('datos_fondos.json', 'w') as json_file:
            json.dump(datos_fondos, json_file, indent=4)

        agregar_datos_fondos("gastos_operativos_porcentaje",gastos_operativos*100)
        agregar_datos_fondos("gastos_operativos_numero",monto*gastos_operativos)
        agregar_datos_fondos("monto_total",monto + monto*gastos_operativos)
    

        datos_castigo_comision = {
            "castigo monto": castigo_monto,
            "castigo esquema": castigo_esquema,
            "castigo distrito":castigo_distrito_riesgo_tipo_propiedad,
            "castigo broker":castigo_con_broker,
            "castigo hipoteca":castigo_con_hipoteca,
            "castigo tipo pagador":castigo_tipo_pagador,
            "castigo compra venta":castigo_compra_venta,
            "castigo vri":castigo_vri,
            "margen bruto": margen_bruto,
            "total gastos":total_gastos,
            "gastos notariales":total_gastos_notariales_cv_hipo,
            "total gastos registrales":total_gastos_registrales_cv_hipo,
            "total gastos registrales inscrip lev":total_gastos_registrales_inscrip_lev,
            "total compra deuda": total_compra_deuda,
            "total gastos notariables inscrip lev": total_gastos_notariales_inscrip_lev,
            "total gastos broker":total_gastos_broker,
            "gastos operativos":gastos_operativos
        }
        with open('datos_castigo_comision.json', 'w') as json_file:
            json.dump(datos_castigo_comision, json_file, indent=4)

        return comision_total

    monto = float(extraer_datos("monto"))
    moneda = extraer_datos("monto_unidad")
    esquema = extraer_datos("esquema")
    distrito = extraer_datos("lista_distritos")[0]
    riesgo = extraer_datos("lista_niveles_riesgos")[0]
    tipo_propiedad = extraer_datos("lista_tipos_propiedades")[0]
    tipo_pagador = extraer_datos("tipo_pagador")
    compra_venta = extraer_datos("compra_venta")
    con_hipoteca = extraer_datos("con_hipoteca")
    num_propiedades = extraer_datos("nro_propiedades")
    con_broker = extraer_datos("opcion_broker")
    if moneda == "Dolares": monto = 3.6*monto
    comision_total = calcular_total(monto, moneda, esquema, distrito, riesgo, tipo_propiedad, con_broker, con_hipoteca, tipo_pagador, compra_venta, num_propiedades)

    calculo_comision = {
        "comision_total":comision_total
    }
    with open('calculo_comision.json', 'w') as json_file:
        json.dump(calculo_comision, json_file, indent=4)


#--------------------------------------main_tasa--------------------------------------------


def operarTasa():
    tabla_distrito = {
        "SAN ISIDRO": -5.00,"MIRAFLORES": -5.00,"SANTIAGO DE SURCO": -1.00,"SAN BORJA": -1.00,"BARRANCO": 0.00,
        "ASIA": 0.00,"CHILCA": 0.00,"SAN BARTOLO": -1.00,"PUNTA HERMOSA": -1.00,"SANTA ROSA": 1.00,"SANTA MARIA DEL MAR": -1.00,
        "PUCUSANA": 0.00,"MAGDALENA DEL MAR": 1.00,"PUEBLO LIBRE": 2.00,"LINCE": 0.00,"JESUS MARIA": 0.00,
        "SURQUILLO": 1.00,"SAN MIGUEL": 0.00,"BREÑA": 2.00,"CERCADO DE LIMA": 3.00,"LA VICTORIA": 3.00,
        "RIMAC": 5.00,"SAN LUIS": 3.00,"CARABAYLLO": 5.00,"COMAS": 4.00,"INDEPENDENCIA": 4.00,"LOS OLIVOS": 2.00,
        "PUENTE PIEDRA": 5.00,"SAN MARTIN DE PORRES": 4.00,"CHORRILLOS": 2.00,"LURIN": 4.00,"SAN JUAN DE MIRAFLORES": 5.00,
        "VILLA EL SALVADOR": 4.00,"VILLA MARIA DEL TRIUNFO": 5.00,"PACHACAMAC": 6.00,"ATE": 3.00,"CHACLACAYO": 4.00,
        "LURIGANCHO": 5.00,"LA MOLINA": 3.00,"SAN JUAN DE LURIGANCHO": 5.00,"SANTA ANITA": 4.00,"CALLAO": 5.00,
        "VENTANILLA": 6.00,"BELLAVISTA": 5.00,"LA PERLA": 5.00,"CARMEN DE LA LEGUA": 6.00,"AREQUIPA": 5.00,"OTROS": 5.00
    }

    tabla_tipo_propiedad = {
        "Casa": 0,
        "Departamento": 0,
        "Edificio": 0,
        "Terreno": 0.045,
        "Local": 0.045
    }

    tabla_riesgo = {
        "Bajo": 0,
        "Bajo Medio": 1,
        "Moderado": 2,
        "Moderado Medio": 3,
        "Medio": 4
    }

    tabla_okey = {
        "Medio con castigo vigente": 0.03,
        "Medio sin castigo vigente pero historico más de 120 dias y menos de 180 dias": -0.03,
        "Medio sin castigo vigente pero historico más de 180 dias y menos de 360 dias": -0.02,
        "Medio sin castigo vigente pero historico más de 360 dias": 0
    }

    def buscar_valor(clave, tabla):
        return tabla.get(clave, 0)

    def calcular_valor_riesgo(monto, riesgo):
        base_riesgo = 0.09 * (monto / 100000) if monto < 100000 else 0.09 
        return base_riesgo * buscar_valor(riesgo, tabla_riesgo)

    def calcular_valor_okey(riesgo, tipo_deuda):
        return buscar_valor(tipo_deuda, tabla_okey) if riesgo == "Medio" else 0

    def calcular_tasa_final(moneda, monto, plazo, cuota_puente, distrito, tipo_propiedad, riesgo, tipo_deuda):
        valor_monto = monto if moneda == "Soles" else monto * 3.6
        
        if valor_monto > 100000:
            castigo_monto = 1 + (0.018 / (valor_monto / 100000) * ((valor_monto - 20000) / 10000))
            castigo_plazo = 1 + ((plazo - 6) / 6 * 0.008 * 2.5)
        else:
            castigo_monto = 1 + (((valor_monto - 20000) / 10000) * 0.018)
            castigo_plazo = 1 + ((plazo - 6) / 6 * 0.008)
        
        castigo_cuota_puente = 1 + (0.08 if cuota_puente == "Si" else 0)
        
        valor_distrito = buscar_valor(distrito, tabla_distrito) / 100.00

        valor_tipo_propiedad = buscar_valor(tipo_propiedad, tabla_tipo_propiedad)

        valor_riesgo = calcular_valor_riesgo(valor_monto, riesgo)

        valor_okey = calcular_valor_okey(riesgo, tipo_deuda)

        valor_vri = (0.4 / 0.05) * 0.015

        castigo_distrito = 1 + valor_distrito
        castigo_tipo_propiedad = 1 + valor_tipo_propiedad
        castigo_riesgo = 1 + valor_riesgo
        castigo_okey = 1 + valor_okey
        castigo_vri = 1 + valor_vri
        
        total = castigo_monto * castigo_plazo * castigo_distrito * castigo_tipo_propiedad * castigo_riesgo * castigo_okey * castigo_cuota_puente * castigo_vri
        
        tasa_final = round(0.01235 * total, 4)  if moneda == "Soles" else  round(0.01235 * total * 0.70, 4) 
      
      
        datos_castigo_tasa = {
            "castigo_monto": castigo_monto,
            "castigo_plazo":castigo_plazo,
            "castigo_distrito":castigo_distrito,
            "castigo_tipo propiedad":castigo_tipo_propiedad,
            "castigo_riesgo":castigo_riesgo,
            "castigo_okey":castigo_okey,
            "castigo_cuota puente":castigo_cuota_puente,
            "castigo_vri":castigo_vri,
            "total":total
        }
        with open('datos_castigo_tasa.json', 'w') as json_file:
            json.dump(datos_castigo_tasa, json_file, indent=4)


        return tasa_final

    moneda = extraer_datos("monto_unidad")
    monto = float(extraer_datos("monto"))
    plazo = float(extraer_datos("plazo"))
    cuota_puente = extraer_datos("cuota_puente")
    distrito = extraer_datos("lista_distritos")[0]
    tipo_propiedad = extraer_datos("lista_tipos_propiedades")[0]
    riesgo = extraer_datos("lista_niveles_riesgos")[0]
 
    tipo_deuda = extraer_datos("lista_tipos_deudas")[0]


    tasa_final = calcular_tasa_final(moneda, monto, plazo, cuota_puente, distrito, tipo_propiedad, riesgo, tipo_deuda)


    calculo_tasa = {
        "tasa_final": tasa_final
    }
    with open('calculo_tasa.json', 'w') as json_file:
        json.dump(calculo_tasa, json_file, indent=4)


# ------------------------------------ main_cronograma -------------------------------------
def operarCronograma():
    monto = extraer_datos('monto')
    plazo = extraer_datos('plazo')
    comision_particular,tasa_particular = extraer_datos("comision_particular"), extraer_datos("tasa_particular")

    calculo_cronograma = {
        "tasa_interes": tasa_particular,
        "gastos_operativos": comision_particular,
    }
    with open('calculo_cronograma.json', 'w') as json_file:
        json.dump(calculo_cronograma, json_file, indent=4)



# -----------------------------------------------------------CUOTA MENSUAL----------------------------------



def obtener_cuota_mensual(monto, moneda, plazo,valor_comision,valor_tasa,tipo_cronograma):

    monto_total = np.round(monto * (1 + valor_comision), 2)

    if tipo_cronograma == "CUOTA FLEXIBLE":
        cuota_mensual = np.round(npf.pmt(valor_tasa, plazo, -monto_total, monto), 2)
    elif tipo_cronograma == "CUOTA FIJA":
        cuota_mensual = np.round(npf.pmt(valor_tasa, plazo, -monto_total), 2)
    else:
        cuota_mensual = 0.00

    return cuota_mensual,monto_total


# --------------------------------------------------------- Generar Excel --------------------------------------------
def generar_excel(cronograma_data, nombre_archivo):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Cronograma P2P"

    encabezados = ['FECHA DE PAGO', 'MONTO POR REEMBOLSAR', 'INTERESES PACTADOS', 'AMORTIZACION', 'CUOTA MENSUAL']
    sheet.append(encabezados)

    for fila in zip(*cronograma_data):
        sheet.append(fila)

    workbook.save(nombre_archivo)


def generar_excel2(cronograma_data, nombre_archivo):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Cronograma Fondos"

    encabezados = ['FECHA DE PAGO', 'MONTO POR REEMBOLSAR', 'INTERESES PACTADOS', 'AMORTIZACION', 'CUOTA MENSUAL']
    sheet.append(encabezados)

    for fila in zip(*cronograma_data):
        sheet.append(fila)

    workbook.save(nombre_archivo)


def calcular_cronograma(monto, moneda, plazo, valor_comision, valor_tasa, tipo_cronograma):
    

    monto_total = np.round(monto * (1 + valor_comision), 2)
    

    saldo = monto_total

    lista_fecha_pago = []
    lista_monto_reembolsar = [monto_total]  # Inicializa con monto_total como primer valor
    lista_intereses_pactados = [] 
    lista_amortizacion = []
    lista_cuota_mensual = []

    total_intereses = 0

    for i in range(1, plazo + 1):
        intereses_pactados = np.round(saldo * valor_tasa, 2)
        total_intereses += intereses_pactados

        if tipo_cronograma == "CUOTA FLEXIBLE":
            cuota_mensual = np.round(npf.pmt(valor_tasa, plazo-i+1, -saldo, monto), 2)
        elif tipo_cronograma == "CUOTA FIJA":
            cuota_mensual = np.round(npf.pmt(valor_tasa, plazo, -monto_total), 2)
        elif tipo_cronograma == "CUOTA MIXTA":
            cuota_mensual = extraer_datos_fondos("cuota_mixta") 
        else:
            cuota_mensual = 0.00

        amortizacion = np.round(cuota_mensual - intereses_pactados, 2)
        saldo = np.round(saldo - amortizacion, 2)

        lista_fecha_pago.append(f"MES {i}")
        if i < plazo:
            lista_monto_reembolsar.append(saldo)
        lista_intereses_pactados.append(intereses_pactados)
        lista_amortizacion.append(amortizacion)
        lista_cuota_mensual.append(cuota_mensual)

    # modificaciones a ultimos valores de la lista
    if tipo_cronograma == "CUOTA FLEXIBLE":
        lista_cuota_mensual[len(lista_cuota_mensual)-1] = cuota_mensual+monto
        lista_amortizacion[len(lista_cuota_mensual)-1] = cuota_mensual+monto - intereses_pactados
    if tipo_cronograma == "CUOTA FIJA":
        lista_cuota_mensual[len(lista_cuota_mensual)-1] = cuota_mensual
        lista_amortizacion[len(lista_cuota_mensual)-1] = cuota_mensual - intereses_pactados
    if tipo_cronograma == "CUOTA MIXTA":
        lista_cuota_mensual[len(lista_cuota_mensual)-1] = monto_total+sum(lista_intereses_pactados)
        lista_amortizacion[len(lista_cuota_mensual)-1] = monto_total+sum(lista_intereses_pactados) - intereses_pactados

    agregar_datos("lista_intereses_pactados",lista_intereses_pactados)

    agregar_datos_fondos("ultimo_monto_reembolsar",lista_monto_reembolsar[-1])
    agregar_datos_fondos("ultimo_amortizacion", lista_amortizacion[-1])
    agregar_datos_fondos("cuota_mensual", cuota_mensual)

    
    flujo = []
    for i in range(int(plazo)):
        flujo.append(lista_cuota_mensual[i])

    flujo[0] = -monto
    flujo[-1] = lista_monto_reembolsar[-1]-lista_amortizacion[-1]

    agregar_datos_fondos("flujo",flujo)
    agregar_datos_fondos("lista_cuota_mensual",lista_cuota_mensual)
    agregar_datos_fondos("lista_fecha_pago",lista_fecha_pago)



    return lista_fecha_pago, lista_monto_reembolsar, lista_intereses_pactados, lista_amortizacion, lista_cuota_mensual


def calcular_cronograma2(monto, moneda, plazo, valor_comision, valor_tasa, tipo_cronograma):


    monto_total = np.round(monto * (1 + valor_comision), 2)

    saldo = monto_total

    total_gastos = extraer_datos_fondos("total_gastos")

    saldo_final = float(extraer_datos_fondos("ultimo_monto_reembolsar")) - float(extraer_datos_fondos("ultimo_amortizacion"))


    lista_fecha_pago = extraer_datos_fondos("lista_fecha_pago")
    lista_monto_reembolsar = [monto + total_gastos] # Inicializa con monto_total como primer valor
    lista_intereses_pactados = []
    lista_amortizacion = []
    
    lista_cuota_mensual = extraer_datos_fondos("lista_cuota_mensual")



    p = float(extraer_datos("plazo"))
    E = monto + total_gastos
    M = float(extraer_datos_fondos("cuota_mensual"))   # 735.4
    Y = extraer_datos_fondos("lista_cuota_mensual")[-1]

    def equation(X):
        suma_serie = sum((X + 1) ** i for i in range(plazo - 1))
        primer_termino_grande = E * (X + 1) ** (p - 1) - M * suma_serie
        segundo_termino_grande = X * primer_termino_grande
        return primer_termino_grande - Y + segundo_termino_grande - saldo_final

    # Valor inicial estimado para X
    X0 = 0.1

    # Utiliza fsolve para encontrar la raíz de la función
    x, = fsolve(equation, X0)

    for i in range(int(p)):
        lista_intereses_pactados.append(x*lista_monto_reembolsar[i])
        lista_amortizacion.append(M-lista_intereses_pactados[i]) # 735.4 - 569.89
        lista_monto_reembolsar.append(lista_monto_reembolsar[i]-lista_amortizacion[i])

    lista_monto_reembolsar.remove(lista_monto_reembolsar[-1])


    agregar_datos_fondos("x",x)
    agregar_datos_fondos("lista_intereses_pactados",lista_intereses_pactados)
    

    flujo = []
    for i in range(int(p)):
        flujo.append(lista_cuota_mensual[i])

    flujo[0] = -monto
    flujo[-1] = lista_monto_reembolsar[-2]-lista_amortizacion[-1]

    agregar_datos_fondos("flujo2",flujo)


    for i,e in enumerate(lista_monto_reembolsar):
        lista_monto_reembolsar[i]=round(e,2)

    for i,e in enumerate(lista_intereses_pactados):
        lista_intereses_pactados[i]=round(e,2)

    for i,e in enumerate(lista_amortizacion):
        lista_amortizacion[i]=round(e,2)

    for i,e in enumerate(lista_cuota_mensual):
        lista_cuota_mensual[i]=round(e,2)

    lista_amortizacion[-1] = lista_cuota_mensual[-1]-lista_intereses_pactados[-1]

    return lista_fecha_pago, lista_monto_reembolsar, lista_intereses_pactados, lista_amortizacion, lista_cuota_mensual



def enviardatos():
    scope = ['https://www.googleapis.com/auth/spreadsheets', "https://www.googleapis.com/auth/drive"]

    credenciales = ServiceAccountCredentials.from_json_keyfile_name("powerful-star-414914-4302ed1ac12d.json", scope)
    cliente = gspread.authorize(credenciales)

    sheet = cliente.open("BaseDeDatos").sheet1

    with open('datos.json', 'r') as json_file:
        data = json.load(json_file)

    row = [json.dumps(value) if isinstance(value, list) else value for value in data.values()]

    sheet.append_row(row)


def obtener_fecha_actual():
    fecha_actual = datetime.datetime.now()
    fecha_formateada = fecha_actual.strftime("%d/%m/%Y %H:%M:%S")
    return fecha_formateada

