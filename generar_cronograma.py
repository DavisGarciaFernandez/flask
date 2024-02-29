import numpy as np
import pandas as pd
import numpy_financial as npf

def calcular_cronograma(monto, plazo, valor_comision, valor_tasa, tipo_cronograma):
    monto_total = np.round(monto * (1 + valor_comision), 2)
    cronograma = []
    saldo = monto_total

    # Calcular cuota mensual para CUOTA FIJA
    cuota_mensual_fija = np.round(npf.pmt(valor_tasa, plazo, -monto_total, monto), 2) if tipo_cronograma == "CUOTA FIJA" else 0



    lista_fecha_pago = []
    lista_monto_reembolsar = []
    lista_intereses_pactados = [] 
    lista_amortizacion = []
    lista_cuota_mensual = []

    for i in range(1, plazo + 1):
        intereses_pactados = np.round(saldo * valor_tasa, 2)

        if tipo_cronograma == "CUOTA FLEXIBLE":
            cuota_mensual = np.round(npf.pmt(valor_tasa, plazo-i+1, -saldo), 2) if i < plazo else np.round(saldo + intereses_pactados, 2)
        elif tipo_cronograma == "CUOTA FIJA":
            cuota_mensual = cuota_mensual_fija
        elif tipo_cronograma == "CUOTA MIXTA":
            cuota_mensual = cuota_mensual_fija if i < plazo else np.round(saldo + intereses_pactados, 2)

        amortizacion = np.round(cuota_mensual - intereses_pactados, 2)
        monto_reembolsar = np.round(saldo - amortizacion, 2)
        saldo = monto_reembolsar

        
        lista_fecha_pago.append(f"MES {i}")
        lista_monto_reembolsar.append(monto_reembolsar if i > 1 else monto_total)
        lista_intereses_pactados.append(intereses_pactados)
        lista_amortizacion.append(amortizacion)
        lista_cuota_mensual.append(cuota_mensual)

        cronograma.append({
            'fecha_pago': f'MES {i}',
            'monto_reembolsar': monto_reembolsar if i > 1 else monto_total,
            'intereses_pactados': intereses_pactados,
            'amortizacion': amortizacion,
            'cuota_mensual': cuota_mensual
        })

    # modificaciones a ultimos valores de la lista
    if tipo_cronograma == "CUOTA FLEXIBLE":
        lista_cuota_mensual[len(lista_cuota_mensual)-1] = cuota_mensual+monto
    if tipo_cronograma == "CUOTA FIJA":
        lista_cuota_mensual[len(lista_cuota_mensual)-1] = cuota_mensual
    if tipo_cronograma == "CUOTA MIXTA":
        lista_cuota_mensual[len(lista_cuota_mensual)-1] = monto_total+sum(lista_intereses_pactados)


    return lista_fecha_pago, lista_monto_reembolsar, lista_intereses_pactados, lista_amortizacion, lista_cuota_mensual

monto, plazo, valor_comision, valor_tasa, tipo_cronograma = 20000,12,0.2,0.1,"CUOTA FLEXIBLE"
lista_fecha_pago, lista_monto_reembolsar, lista_intereses_pactados, lista_amortizacion, lista_cuota_mensual = calcular_cronograma(monto, plazo, valor_comision, valor_tasa, tipo_cronograma)


# Crear un DataFrame con los datos
data = {
    'Fecha de Pago': lista_fecha_pago,
    'Monto a Reembolsar': lista_monto_reembolsar,
    'Intereses Pactados': lista_intereses_pactados,
    'Amortización': lista_amortizacion,
    'Cuota Mensual': lista_cuota_mensual
}
df = pd.DataFrame(data)

# Escribir el DataFrame en un archivo Excel
nombre_archivo = 'datos_financieros.xlsx'
df.to_excel(nombre_archivo, index=False)

print(f"Los datos se han guardado en el archivo '{nombre_archivo}' correctamente.")
