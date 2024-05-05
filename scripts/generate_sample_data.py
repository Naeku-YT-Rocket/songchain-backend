import requests
import random

sample_emails = [
    "daniel@ytrocket.com",
    "jose@ytrocket.com",
    "rober@ytrocket.com",
    "laura@ytrocket.com",
    "cano@ytrocket.com",
    "roa@ytrocket.com",
    "valeria@ytrocket.com",
    "diego@ytrocket.com",
    "juan@ytrocket.com"
]

sample_digital_assets = [
    {
        "name": "Vibras",
        "owner_email": "jose@ytrocket.com",
        "cover_art_uri": "https://example.com/vibras.jpg",
        "available_partitions": 3,
        "artist_name": "J Balvin"
    },
    {
        "name": "Échame La Culpa",
        "owner_email": "laura@ytrocket.com",
        "cover_art_uri": "https://example.com/echamela-culpa.jpg",
        "available_partitions": 3,
        "artist_name": "Luis Fonsi, Demi Lovato"
    },
    {
        "name": "X",
        "owner_email": "cano@ytrocket.com",
        "cover_art_uri": "https://example.com/x.jpg",
        "available_partitions": 3,
        "artist_name": "Nicky Jam, J Balvin"
    },
    {
        "name": "Aura",
        "owner_email": "diego@ytrocket.com",
        "cover_art_uri": "https://example.com/aura.jpg",
        "available_partitions": 3,
        "artist_name": "Ozuna"
    },
    {
        "name": "Clandestino",
        "owner_email": "rober@ytrocket.com",
        "cover_art_uri": "https://example.com/clandestino.jpg",
        "available_partitions": 3,
        "artist_name": "Shakira, Maluma"
    },
    {
        "name": "Odisea",
        "owner_email": "juan@ytrocket.com",
        "cover_art_uri": "https://example.com/odisea.jpg",
        "available_partitions": 3,
        "artist_name": "Ozuna"
    },
    {
        "name": "Bailando",
        "owner_email": "valeria@ytrocket.com",
        "cover_art_uri": "https://example.com/bailando.jpg",
        "available_partitions": 3,
        "artist_name": "Enrique Iglesias, Descemer Bueno, Gente de Zona"
    },
    {
        "name": "Calma",
        "owner_email": "daniel@ytrocket.com",
        "cover_art_uri": "https://example.com/calma.jpg",
        "available_partitions": 3,
        "artist_name": "Pedro Capó, Farruko"
    },
    {
        "name": "Taki Taki",
        "owner_email": "roa@ytrocket.com",
        "cover_art_uri": "https://example.com/taki-taki.jpg",
        "available_partitions": 3,
        "artist_name": "DJ Snake, Selena Gomez, Ozuna, Cardi B"
    },
    {
        "name": "La La La (Brazil 2014)",
        "owner_email": "jose@ytrocket.com",
        "cover_art_uri": "https://example.com/la-la-la.jpg",
        "available_partitions": 3,
        "artist_name": "Shakira"
    },
    {
        "name": "Felices los 4",
        "owner_email": "cano@ytrocket.com",
        "cover_art_uri": "https://example.com/felices-los-4.jpg",
        "available_partitions": 3,
        "artist_name": "Maluma"
    },
    {
        "name": "Dura",
        "owner_email": "laura@ytrocket.com",
        "cover_art_uri": "https://example.com/dura.jpg",
        "available_partitions": 3,
        "artist_name": "Daddy Yankee"
    },
    {
        "name": "Despacito",
        "owner_email": "diego@ytrocket.com",
        "cover_art_uri": "https://example.com/despacito.jpg",
        "available_partitions": 3,
        "artist_name": "Luis Fonsi, Daddy Yankee"
    },
    {
        "name": "Ella Quiere Beber",
        "owner_email": "rober@ytrocket.com",
        "cover_art_uri": "https://example.com/ella-quiere-beber.jpg",
        "available_partitions": 3,
        "artist_name": "Anuel AA"
    },
    {
        "name": "Te Boté (Remix)",
        "owner_email": "valeria@ytrocket.com",
        "cover_art_uri": "https://example.com/te-bote-remix.jpg",
        "available_partitions": 3,
        "artist_name": "Casper Mágico, Nio García, Darell, Nicky Jam, Bad Bunny, Ozuna"
    },
    {
        "name": "China",
        "owner_email": "juan@ytrocket.com",
        "cover_art_uri": "https://example.com/china.jpg",
        "available_partitions": 3,
        "artist_name": "Anuel AA, Daddy Yankee, Karol G, Ozuna, J Balvin"
    },
    {
        "name": "Con Calma",
        "owner_email": "daniel@ytrocket.com",
        "cover_art_uri": "https://example.com/con-calma.jpg",
        "available_partitions": 3,
        "artist_name": "Daddy Yankee, Snow"
    },
    {
        "name": "Tusa",
        "owner_email": "roa@ytrocket.com",
        "cover_art_uri": "https://example.com/tusa.jpg",
        "available_partitions": 3,
        "artist_name": "Karol G, Nicki Minaj"
    },
    {
        "name": "Mia",
        "owner_email": "diego@ytrocket.com",
        "cover_art_uri": "https://example.com/mia.jpg",
        "available_partitions": 3,
        "artist_name": "Bad Bunny, Drake"
    },
    {
        "name": "Adan y Eva",
        "owner_email": "jose@ytrocket.com",
        "cover_art_uri": "https://example.com/adan-y-eva.jpg",
        "available_partitions": 3,
        "artist_name": "Paulo Londra"
    }
]


sample_partition_prices = [15, 20, 70, 80, 200, 500, 1000, 2000, 3000]
sample_balances = [8000, 9000, 10000, 50000]

for email in sample_emails:

    response = requests.post("http://localhost:8000/wallet", json={"owner_email": email})

    wallet_creation_response = response.json()

    print("WALLET CREATED STATUS: ", response.status_code)

    # Increase balance

    sample_balance = random.choice(sample_balances)

    print(sample_balance)

    update_wallet_response = requests.patch(f"http://localhost:8000/wallet/{wallet_creation_response['id']}", json={"balance": sample_balance})

    print("UPDATE WALLET STATUS: ", update_wallet_response.status_code)


for digital_asset in sample_digital_assets:

    response = requests.post("http://localhost:8000/digital_asset", json=digital_asset)

    digital_asset_created = response.json()

    print("DIGITAL ASSET CREATED STATUS: ", response.status_code)

    sample_price = random.choice(sample_partition_prices)

    for i in range(digital_asset["available_partitions"]):

        wallets = requests.get(f"http://localhost:8000/wallet?owner_email={digital_asset['owner_email']}")

        wallet_id = wallets.json()[0]["id"]

        partition_creation_data = {
            "price": sample_price,
            "wallet": {
                "id": wallet_id
            },
            "digital_asset": {
                "id": digital_asset_created["id"]
            }
        }

        partition_creation_response = requests.post("http://localhost:8000/partition", json=partition_creation_data)

        print("PARTITION CREATED STATUS: ", partition_creation_response.status_code)