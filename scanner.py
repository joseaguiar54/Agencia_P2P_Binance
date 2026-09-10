import requests

def probar_conexion_binance():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    
    # Buscamos las órdenes de VENTA de USDT en VES (Donde nosotros vamos a comprar)
    payload = {
        "fiat": "VES",
        "page": 1,
        "rows": 5,
        "tradeType": "SELL", 
        "asset": "USDT",
        "payTypes": ["Banesco"],
        "publisherType": None
    }
    
    print("Iniciando conexión con Binance P2P (Banesco VES)...")
    
    try:
        response = requests.post(url, json=payload)
        datos = response.json()
        
        if datos['code'] == '000000':
            print("¡Conexión Exitosa! Aquí están los 3 precios más baratos de la tabla:\n")
            anuncios = datos['data'][:3]
            for anuncio in anuncios:
                precio = anuncio['adv']['price']
                anunciante = anuncio['advertiser']['nickName']
                print(f"- Anunciante: {anunciante} | Precio: {precio} VES")
        else:
            print("Hubo un error al leer los datos.")
            
    except Exception as e:
        print(f"Error de conexión: {e}")

if __name__ == "__main__":
    probar_conexion_binance()