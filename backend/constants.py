from firebase_admin import initialize_app
from firebase_admin.credentials import Certificate

AZUL = 0
PRETO = 1
AMARELO = 2
VERMELHO = 3

CREDENTIALS = Certificate('cred/manvsvirus-2944b63208f8.json')
FIREBASE = initialize_app(CREDENTIALS, {'app': 'manvsvirus'})

COLORS=['Azul', 'Preto', 'Amarelo', 'Vermelho']

CITIES_DATA = (
    ("Atlanta", "Estados Unidos", 4.715, AZUL, (1, 4, 25)),  # 1
    ("Chicago", "Estados Unidos", 9.121, AZUL, (0, 2, 10, 24, 27)),  # 2
    ("São Francisco", "Estados Unidos", 5.864, AZUL, (1, 24, 39, 44)),  # 3
    ("Nova York", "Estados Unidos", 20.464, AZUL, (4, 8, 9, 10)),  # 4
    ("Washington", "Estados Unidos", 4.679, AZUL, (0, 3, 10, 25)),  # 5
    ("São Petersburgo", "Rússia", 4.879, AZUL, (6, 22)),  # 6
    ("Essen", "Alemanha", 0.575, AZUL, (5, 7, 8, 11)),  # 7
    ("Milão", "Itália", 5.232, AZUL, (6, 16)),  # 8
    ("Londres", "Reino Unido", 8.586, AZUL, (3, 6, 9, 11)),  # 9
    ("Madri", "Espanha", 5.427, AZUL, (3, 8, 11, 23, 29)),  # 10
    ("Montreal", "Canadá", 3.429, AZUL, (1, 3, 4)),  # 11
    ("Paris", "França", 10.755, AZUL, (6, 7, 8, 9, 23)),  # 12

    ("Calcutá", "Índia", 14.374, PRETO, (14, 15, 37, 41)),  # 13
    ("Bombaim", "Índia", 16.910, PRETO, (14, 15, 20)),  # 14
    ("Déli", "Índia", 22.242, PRETO, (12, 13, 15, 17, 20)),  # 15
    ("Chennai", "Índia", 8.865, PRETO, (12, 13, 14, 41, 47)),  # 16
    ("Istambul", "Turquia", 13.576, PRETO, (5, 7, 18, 21, 22, 23)),  # 17
    ("Teerã", "Irã", 7.419, PRETO, (14, 18, 20, 22)),  # 18
    ("Bagdá", "Iraque", 6.204, PRETO, (16, 17, 19, 20, 21)),  # 19
    ("Riad", "Arábia Saudita", 5.037, PRETO, (18, 20, 21)),  # 20
    ("Carachi", "Paquistão", 20.711, PRETO, (13, 14, 17, 18, 19)),  # 21
    ("Cairo", "Egito", 14.718, PRETO, (16, 18, 19, 23, 32)),  # 22
    ("Moscou", "Rússia", 15.512, PRETO, (5, 16, 17)),  # 23
    ("Argel", "Argélia", 2.946, PRETO, (9, 11, 16, 21)),  # 24

    ("Los Angeles", "Estados Unidos", 14.900, AMARELO, (1, 2, 27, 45)),  # 25
    ("Miami", "Estados Unidos", 5.582, AMARELO, (0, 4, 27, 30)),  # 26
    ("Lagos", "Nigéria", 11.547, AMARELO, (29, 32)),  # 27
    ("Cidade do México", "México", 19.463, AMARELO, (1, 24, 25, 30, 34)),  # 28
    ("Buenos Aires", "Argentina", 13.639, AMARELO, (29, 30)),  # 29
    ("São Paulo", "Brasil", 20.186, AMARELO, (9, 26, 28, 30)),  # 30
    ("Bogotá", "Colômbia", 8.702, AMARELO, (25, 27, 28, 29, 34)),  # 31
    ("Johannesburgo", "África do Sul", 3.888, AMARELO, (32, 35)),  # 32
    ("Cartum", "Sudão", 4.887, AMARELO, (21, 26, 31, 35)),  # 33
    ("Santiago", "Chile", 6.015, AMARELO, (34,)),  # 34
    ("Lima", "Peru", 9.121, AMARELO, (27, 30)),  # 35
    ("Kinshasa", "República Democrática do Congo", 9.046, AMARELO, (26, 31, 32)),  # 36

    ("Pequim", "República Popular da China", 17.311, VERMELHO, (38, 42)),  # 37
    ("Hong Kong", "República Popular da China", 7.106, VERMELHO, (38, 41, 43, 44, 46)),  # 38
    ("Xangai", "República Popular da China", 13.482, VERMELHO, (36, 37, 39, 42, 43)),  # 39
    ("Tóquio", "Japão", 13.189, VERMELHO, (2, 38, 40, 42)),  # 40
    ("Osaka", "Japão", 2.871, VERMELHO, (39, 43)),  # 41
    ("Bangkok", "Tailândia", 7.151, VERMELHO, (12, 15, 37, 46, 47)),  # 42
    ("Seul", "Coréia do Sul", 22.547, VERMELHO, (36, 38, 39)),  # 43
    ("Taipé", "Taiwan", 8.338, VERMELHO, (37, 38, 40, 44)),  # 44
    ("Manila", "Filipinas", 20.767, VERMELHO, (37, 43, 45, 46)),  # 45
    ("Sydney", "Austrália", 3.785, VERMELHO, (24, 44, 47)),  # 46
    ("Cidade de Ho Chi Minh", "Vietnã", 8.314, VERMELHO, (37, 41, 44, 47)),  # 47
    ("Jacarta", "Indonésia", 26.063, VERMELHO, (15, 41, 45, 46))  # 48
)