# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

# Dados das plantas
plantas_data = [
    {"id": 1, "nome_popular": "Ipê-Amarelo", "nome_cientifico": "Handroanthus spp.", "altura_media_metros": "8 - 15", "epoca_floracao": "Jul/Set (Inverno/Primavera)", "sugestao_volume_agua_litros": "15 - 20", "frequencia_rega_geral": "A cada 7-10 dias (adulta)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/f/f7/Handroanthus_serratifolius.jpg"},
    {"id": 2, "nome_popular": "Pau-Brasil", "nome_cientifico": "Paubrasilia echinata", "altura_media_metros": "10 - 15", "epoca_floracao": "Set/Out (Primavera)", "sugestao_volume_agua_litros": "15 - 25", "frequencia_rega_geral": "A cada 7 dias (adulta)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/%C3%81rvore_pau-brasil_%28Paubrasilia_echinata%29_por_Jani_Pereira.jpg/1536px-%C3%81rvore_pau-brasil_%28Paubrasilia_echinata%29_por_Jani_Pereira.jpg"},
    {"id": 3, "nome_popular": "Ipê-Roxo", "nome_cientifico": "Handroanthus impetiginosus", "altura_media_metros": "5 - 15", "epoca_floracao": "Jun/Ago (Inverno)", "sugestao_volume_agua_litros": "15 - 20", "frequencia_rega_geral": "A cada 7-10 dias (adulta)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Flores_de_ip%C3%AA-roxo_em_Coronel_Fabriciano_MG.JPG"},
    {"id": 4, "nome_popular": "Jatobá", "nome_cientifico": "Hymenaea courbaril", "altura_media_metros": "15 - 20", "epoca_floracao": "Set/Nov (Primavera)", "sugestao_volume_agua_litros": "20 - 30", "frequencia_rega_geral": "A cada 10 dias (adulta, muito resistente)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/5/5c/Hymenaea_courbaril_1.jpg"},
    {"id": 5, "nome_popular": "Copaíba", "nome_cientifico": "Copaifera spp.", "altura_media_metros": "15 - 25", "epoca_floracao": "Set/Nov (Primavera)", "sugestao_volume_agua_litros": "20 - 30", "frequencia_rega_geral": "A cada 10 dias (adulta)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Copaicaaclimacao.JPG/1200px-Copaicaaclimacao.JPG"},
    {"id": 6, "nome_popular": "Açaí", "nome_cientifico": "Euterpe oleracea", "altura_media_metros": "15 - 25", "epoca_floracao": "Set/Dez (Primavera/Verão)", "sugestao_volume_agua_litros": "30 - 40", "frequencia_rega_geral": "A cada 2 dias (solo encharcado é a preferência)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/2/20/Acapalms.jpg"},
    {"id": 7, "nome_popular": "Pitangueira", "nome_cientifico": "Eugenia uniflora", "altura_media_metros": "2 - 4", "epoca_floracao": "Ago/Nov (Primavera)", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 3-4 dias", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Pitangueira_%28do_tupi_%27ybapytanga%29_jovem%2C_em_muda._%28Eugenia_uniflora%29_05.jpg/250px-Pitangueira_%28do_tupi_%27ybapytanga%29_jovem%2C_em_muda._%28Eugenia_uniflora%29_05.jpg"},
    {"id": 8, "nome_popular": "Manacá-da-Serra", "nome_cientifico": "Tibouchina pulchra", "altura_media_metros": "3 - 6", "epoca_floracao": "Ano todo", "sugestao_volume_agua_litros": "10 - 15", "frequencia_rega_geral": "A cada 2-3 dias (gosta de umidade)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Manacasdaserras.JPG"},
    {"id": 9, "nome_popular": "Araucária", "nome_cientifico": "Araucaria angustifolia", "altura_media_metros": "20 - 50", "epoca_floracao": "Não floresce (Gimnosperma)", "sugestao_volume_agua_litros": "15 - 25", "frequencia_rega_geral": "A cada 7 dias (adulta)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/2/2b/Itaimbezinho_-_Parque_Nacional_Aparados_da_Serra_32.JPG"},
    {"id": 10, "nome_popular": "Embaúba", "nome_cientifico": "Cecropia spp.", "altura_media_metros": "8 - 15", "epoca_floracao": "Variável", "sugestao_volume_agua_litros": "10 - 15", "frequencia_rega_geral": "A cada 4-5 dias (cresce rápido, precisa de água)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Emba%C3%BAba_002MG.jpg/250px-Emba%C3%BAba_002MG.jpg"},
    {"id": 11, "nome_popular": "Mangueira", "nome_cientifico": "Mangifera indica", "altura_media_metros": "15 - 30", "epoca_floracao": "Set/Jan (Primavera/Verão)", "sugestao_volume_agua_litros": "20 - 30", "frequencia_rega_geral": "A cada 7 dias (adulta, resiste à seca)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Mango_tree_Kerala_in_full_bloom.jpg/250px-Mango_tree_Kerala_in_full_bloom.jpg"},
    {"id": 12, "nome_popular": "Cajueiro", "nome_cientifico": "Anacardium occidentale", "altura_media_metros": "5 - 10", "epoca_floracao": "Jul/Nov (Inverno/Primavera)", "sugestao_volume_agua_litros": "10 - 15", "frequencia_rega_geral": "A cada 5-7 dias (adulta, muito resistente)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/da/Cashew_Brazil_tree.jpg/250px-Cashew_Brazil_tree.jpg"},
    {"id": 13, "nome_popular": "Goiabeira", "nome_cientifico": "Psidium guajava", "altura_media_metros": "3 - 6", "epoca_floracao": "Ano todo", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 3-4 dias", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Goiabeira.JPG"},
    {"id": 14, "nome_popular": "Quaresmeira", "nome_cientifico": "Tibouchina granulosa", "altura_media_metros": "8 - 12", "epoca_floracao": "Fev/Mai e Ago/Nov", "sugestao_volume_agua_litros": "10 - 15", "frequencia_rega_geral": "A cada 4-5 dias", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/a/ac/Quaresmeirasbicolores.jpg"},
    {"id": 15, "nome_popular": "Jerivá", "nome_cientifico": "Syagrus romanzoffiana", "altura_media_metros": "8 - 15", "epoca_floracao": "Variável", "sugestao_volume_agua_litros": "15 - 25", "frequencia_rega_geral": "A cada 4 dias", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Jeriv%C3%A1_%28do_tupi_iara%27yb%C3%A1%29_no_Rio_Grande_do_Sul_02.jpg"},
    {"id": 16, "nome_popular": "Palmeira Juçara", "nome_cientifico": "Euterpe edulis", "altura_media_metros": "8 - 15", "epoca_floracao": "Set/Dez (Primavera/Verão)", "sugestao_volume_agua_litros": "20 - 30", "frequencia_rega_geral": "A cada 2-3 dias (não tolera seca)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/6/66/Palmera_palmito_Parque_nacional_Iguaz%C3%BA.JPG"},
    {"id": 17, "nome_popular": "Paineira", "nome_cientifico": "Ceiba speciosa", "altura_media_metros": "10 - 20", "epoca_floracao": "Jan/Mai (Verão/Outono)", "sugestao_volume_agua_litros": "15 - 25", "frequencia_rega_geral": "A cada 7-10 dias (adulta)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Ceiba_speciosa_IMG_1753.jpg/250px-Ceiba_speciosa_IMG_1753.jpg"},
    {"id": 18, "nome_popular": "Sapucaia", "nome_cientifico": "Lecythis pisonis", "altura_media_metros": "10 - 20", "epoca_floracao": "Out/Nov (Primavera)", "sugestao_volume_agua_litros": "15 - 25", "frequencia_rega_geral": "A cada 7 dias (adulta)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/90/Lecythis_marcgraaviana_Miers_%2811684873315%29.jpg/330px-Lecythis_marcgraaviana_Miers_%2811684873315%29.jpg"},
    {"id": 19, "nome_popular": "Ingá", "nome_cientifico": "Inga spp.", "altura_media_metros": "6 - 15", "epoca_floracao": "Variável", "sugestao_volume_agua_litros": "15 - 20", "frequencia_rega_geral": "A cada 3-4 dias (gosta de áreas úmidas)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e8/Pacay_%28Inga_feuillei%29.jpg/960px-Pacay_%28Inga_feuillei%29.jpg"},
    {"id": 20, "nome_popular": "Pata-de-Vaca", "nome_cientifico": "Bauhinia forficata", "altura_media_metros": "4 - 6", "epoca_floracao": "Ago/Nov (Primavera)", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 4-5 dias", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Bauhinia_forficata_cezar.jpg"},
    {"id": 21, "nome_popular": "Sibipiruna", "nome_cientifico": "Cenostigma pluviosum", "altura_media_metros": "6 - 12", "epoca_floracao": "Set/Nov (Primavera)", "sugestao_volume_agua_litros": "10 - 15", "frequencia_rega_geral": "A cada 5-7 dias", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/0/0b/Copasibipirunafrutos.jpg"},
    {"id": 22, "nome_popular": "Oiti", "nome_cientifico": "Licania tomentosa", "altura_media_metros": "8 - 15", "epoca_floracao": "Ago/Set (Inverno/Primavera)", "sugestao_volume_agua_litros": "10 - 15", "frequencia_rega_geral": "A cada 5-7 dias (muito resistente)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/0/06/Licania_tomentosa.JPG"},
    {"id": 23, "nome_popular": "Candeia", "nome_cientifico": "Gochnatia polymorpha", "altura_media_metros": "3 - 6", "epoca_floracao": "Jul/Nov (Inverno/Primavera)", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 7 dias (resistente à seca)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/5/56/Plathymenia_foliolosa.jpg"},
    {"id": 24, "nome_popular": "Aroeira", "nome_cientifico": "Myracrodruon urundeuva", "altura_media_metros": "10 - 20", "epoca_floracao": "Set/Nov (Primavera)", "sugestao_volume_agua_litros": "10 - 15", "frequencia_rega_geral": "A cada 7-10 dias (muito resistente)", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Schinus_terebinthifolius_fruits.JPG"},
    {"id": 25, "nome_popular": "Cumaru", "nome_cientifico": "Dipteryx alata", "altura_media_metros": "10 - 20", "epoca_floracao": "Set/Nov (Primavera)", "sugestao_volume_agua_litros": "15 - 20", "frequencia_rega_geral": "A cada 7 dias", "categoria": "Arbustos e Árvores", "imagem": "https://upload.wikimedia.org/wikipedia/commons/e/ea/Cumaru-nordestino.JPG"},
    {"id": 26, "nome_popular": "Antúrio", "nome_cientifico": "Anthurium andraeanum", "altura_media_metros": "0.3 - 0.6", "epoca_floracao": "Ano todo", "sugestao_volume_agua_litros": "0.5 - 1.0", "frequencia_rega_geral": "A cada 2-3 dias (solo úmido)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Anthurium_eggersii_1.jpg/500px-Anthurium_eggersii_1.jpg"},
    {"id": 27, "nome_popular": "Pacová", "nome_cientifico": "Philodendron bipinnatifidum", "altura_media_metros": "1 - 2", "epoca_floracao": "Não relevante", "sugestao_volume_agua_litros": "1.0 - 2.0", "frequencia_rega_geral": "A cada 3 dias (solo úmido, mas não encharcado)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/9/93/Philodendron-Martianum_sp.jpg"},
    {"id": 28, "nome_popular": "Orquídea", "nome_cientifico": "Cattleya spp.", "altura_media_metros": "0.2 - 0.6", "epoca_floracao": "Variável (Primavera)", "sugestao_volume_agua_litros": "0.1 - 0.3", "frequencia_rega_geral": "A cada 2-4 dias (substrato secar)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Orchis_militaris_flowers.jpg"},
    {"id": 29, "nome_popular": "Samambaia", "nome_cientifico": "Polypodiaceae spp.", "altura_media_metros": "0.5 - 1.5", "epoca_floracao": "Não floresce", "sugestao_volume_agua_litros": "1.0 - 2.0", "frequencia_rega_geral": "A cada 2 dias (solo e ar úmidos)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Polypodiopsida_Fern_02.jpg/500px-Polypodiopsida_Fern_02.jpg"},
    {"id": 30, "nome_popular": "Begônia", "nome_cientifico": "Begonia spp.", "altura_media_metros": "0.3 - 0.6", "epoca_floracao": "Ano todo", "sugestao_volume_agua_litros": "0.5 - 0.8", "frequencia_rega_geral": "A cada 3 dias", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Begonia-6.jpg/330px-Begonia-6.jpg"},
    {"id": 31, "nome_popular": "Renda Portuguesa", "nome_cientifico": "Davallia fejeensis", "altura_media_metros": "0.3 - 0.5", "epoca_floracao": "Não floresce", "sugestao_volume_agua_litros": "0.8 - 1.2", "frequencia_rega_geral": "A cada 2 dias (alta umidade)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/DidzialapisSakys.JPG/330px-DidzialapisSakys.JPG"},
    {"id": 32, "nome_popular": "Hortênsia", "nome_cientifico": "Hydrangea macrophylla", "altura_media_metros": "1 - 2", "epoca_floracao": "Out/Jan (Primavera/Verão)", "sugestao_volume_agua_litros": "2.0 - 4.0", "frequencia_rega_geral": "A cada 2 dias (muita água)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/5/5f/Mudas_de_Hydrangea_macrophylla_%28hort%C3%AAnsia%29_3.jpg"},
    {"id": 33, "nome_popular": "Cróton", "nome_cientifico": "Codiaeum variegatum", "altura_media_metros": "1 - 3", "epoca_floracao": "Variável", "sugestao_volume_agua_litros": "1.0 - 2.0", "frequencia_rega_geral": "A cada 3-4 dias", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Colpfl05.jpg"},
    {"id": 34, "nome_popular": "Zamioculca", "nome_cientifico": "Zamioculcas zamiifolia", "altura_media_metros": "0.6 - 1.0", "epoca_floracao": "Rara", "sugestao_volume_agua_litros": "0.5 - 1.0", "frequencia_rega_geral": "A cada 7-10 dias (muito resistente à seca)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/d/d6/Zamioculcas.jpg"},
    {"id": 35, "nome_popular": "Espada-de-São-Jorge", "nome_cientifico": "Dracaena trifasciata", "altura_media_metros": "0.5 - 1.2", "epoca_floracao": "Rara", "sugestao_volume_agua_litros": "0.5 - 1.0", "frequencia_rega_geral": "A cada 10-15 dias (resistente à seca)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/e/e8/Sansevieria_trifasciata_Closeup_2448px.jpg"},
    {"id": 36, "nome_popular": "Jiboia", "nome_cientifico": "Epipremnum pinnatum", "altura_media_metros": "Trepadeira", "epoca_floracao": "Rara", "sugestao_volume_agua_litros": "0.8 - 1.5", "frequencia_rega_geral": "A cada 3-4 dias", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fe/Epipremnum_aureum_as_Pothos_aureus.jpg/330px-Epipremnum_aureum_as_Pothos_aureus.jpg"},
    {"id": 37, "nome_popular": "Peperômia", "nome_cientifico": "Peperomia spp.", "altura_media_metros": "0.1 - 0.3", "epoca_floracao": "Variável", "sugestao_volume_agua_litros": "0.3 - 0.5", "frequencia_rega_geral": "A cada 4-5 dias (semelhante a suculenta)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/7/76/Peperomia_pellucida_%28Mindanao%2C_Philippines%29.jpg"},
    {"id": 38, "nome_popular": "Lírio-da-Paz", "nome_cientifico": "Spathiphyllum wallisii", "altura_media_metros": "0.3 - 0.6", "epoca_floracao": "Ano todo", "sugestao_volume_agua_litros": "0.5 - 1.0", "frequencia_rega_geral": "A cada 2-3 dias (avisa quando precisa)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/5/54/SpathiphyllumWallisii.jpg"},
    {"id": 39, "nome_popular": "Maria-sem-Vergonha", "nome_cientifico": "Impatiens walleriana", "altura_media_metros": "0.2 - 0.4", "epoca_floracao": "Ano todo", "sugestao_volume_agua_litros": "0.5 - 0.8", "frequencia_rega_geral": "Diariamente/A cada 2 dias (gosta muito de água)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/5/57/Impatiens_Glandulifera.jpg"},
    {"id": 40, "nome_popular": "Bromélia", "nome_cientifico": "Bromeliaceae spp.", "altura_media_metros": "0.3 - 1.5", "epoca_floracao": "Variável", "sugestao_volume_agua_litros": "0.1 - 0.3", "frequencia_rega_geral": "A cada 4-7 dias (manter o \"copo\" com água)", "categoria": "Ervas e Plantas de Vaso", "imagem": "https://upload.wikimedia.org/wikipedia/commons/f/f7/Bromelia_karatas2.jpg"},
    {"id": 41, "nome_popular": "Mandacaru", "nome_cientifico": "Cereus jamacaru", "altura_media_metros": "5 - 10", "epoca_floracao": "Primavera/Verão", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 15-30 dias (muito resistente)", "categoria": "Cactos e Suculentas", "imagem": "https://upload.wikimedia.org/wikipedia/commons/e/e2/Cereus_jamacaru.JPG"},
    {"id": 42, "nome_popular": "Palma Forrageira", "nome_cientifico": "Opuntia ficus-indica", "altura_media_metros": "1 - 3", "epoca_floracao": "Primavera/Verão", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 15 dias (extremamente resistente)", "categoria": "Cactos e Suculentas", "imagem": "https://upload.wikimedia.org/wikipedia/commons/e/e2/Flor_del_nopal_de_la_cochinilla_%28Opuntia_cochenillifera%29%2C_GTOMX.jpg"},
    {"id": 43, "nome_popular": "Flor-de-Maio", "nome_cientifico": "Schlumbergera truncata", "altura_media_metros": "0.1 - 0.3", "epoca_floracao": "Out/Dez (Outono/Inverno)", "sugestao_volume_agua_litros": "0.1 - 0.3", "frequencia_rega_geral": "A cada 7-10 dias", "categoria": "Cactos e Suculentas", "imagem": "https://upload.wikimedia.org/wikipedia/commons/5/58/P1050545.JPG"},
    {"id": 44, "nome_popular": "Maracujá", "nome_cientifico": "Passiflora edulis", "altura_media_metros": "Trepadeira", "epoca_floracao": "Ano todo (depende da espécie)", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 2-3 dias (solo úmido)", "categoria": "Trepadeiras e Outras", "imagem": "https://upload.wikimedia.org/wikipedia/commons/9/91/Passiflora_edulis_forma_flavicarpa.jpg"},
    {"id": 45, "nome_popular": "Guaraná", "nome_cientifico": "Paullinia cupana", "altura_media_metros": "1 - 3", "epoca_floracao": "Set/Nov (Primavera)", "sugestao_volume_agua_litros": "2 - 5", "frequencia_rega_geral": "A cada 3-4 dias", "categoria": "Trepadeiras e Outras", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Guaran%C3%A1_06.jpg/330px-Guaran%C3%A1_06.jpg"},
    {"id": 46, "nome_popular": "Chuva-de-Ouro", "nome_cientifico": "Oncidium spp.", "altura_media_metros": "0.3 - 0.6", "epoca_floracao": "Variável", "sugestao_volume_agua_litros": "0.1 - 0.3", "frequencia_rega_geral": "A cada 2-4 dias (Orquídea, substrato secar)", "categoria": "Trepadeiras e Outras", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Cassia_fistula.jpg/330px-Cassia_fistula.jpg"},
    {"id": 47, "nome_popular": "Caetê (Banana-do-Mato)", "nome_cientifico": "Heliconia spp.", "altura_media_metros": "1 - 4", "epoca_floracao": "Ano todo", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 2-3 dias (gosta de solo úmido)", "categoria": "Trepadeiras e Outras", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heliconia_rostrata1.jpg/330px-Heliconia_rostrata1.jpg"},
    {"id": 48, "nome_popular": "Jasmim-Manga", "nome_cientifico": "Plumeria rubra", "altura_media_metros": "3 - 6", "epoca_floracao": "Verão", "sugestao_volume_agua_litros": "5 - 10", "frequencia_rega_geral": "A cada 5-7 dias (resistente à seca)", "categoria": "Trepadeiras e Outras", "imagem": "https://upload.wikimedia.org/wikipedia/commons/5/5f/White_Five_Petal_Star_2.JPG"},
    {"id": 49, "nome_popular": "Alamanda", "nome_cientifico": "Allamanda cathartica", "altura_media_metros": "1 - 3", "epoca_floracao": "Verão/Outono", "sugestao_volume_agua_litros": "5 - 8", "frequencia_rega_geral": "A cada 3-4 dias", "categoria": "Trepadeiras e Outras", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Bright_yellow_flower.jpg/1200px-Bright_yellow_flower.jpg"},
    {"id": 50, "nome_popular": "Sete-Copas", "nome_cientifico": "Terminalia catappa", "altura_media_metros": "15 - 25", "epoca_floracao": "Verão", "sugestao_volume_agua_litros": "15 - 25", "frequencia_rega_geral": "A cada 7 dias (adulta, resiste bem)", "categoria": "Trepadeiras e Outras", "imagem": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/KetapangGreenLeaves.jpg/1200px-KetapangGreenLeaves.jpg"}
]

# Rota principal
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "mensagem": "API de Plantas Brasileiras",
        "endpoints": {
            "GET /plantas": "Lista todas as plantas",
            "GET /plantas/<id>": "Busca planta por ID",
            "GET /plantas/buscar?nome=<nome>": "Busca planta por nome popular",
            "GET /categorias": "Lista todas as categorias disponíveis",
            "GET /categorias/<categoria>": "Lista plantas por categoria"
        }
    })

# Listar todas as plantas
@app.route('/plantas', methods=['GET'])
def listar_plantas():
    return jsonify({
        "total": len(plantas_data),
        "plantas": plantas_data
    })

# Buscar planta por ID
@app.route('/plantas/<int:id>', methods=['GET'])
def buscar_planta_id(id):
    planta = next((p for p in plantas_data if p['id'] == id), None)
    if planta:
        return jsonify(planta)
    return jsonify({"erro": "Planta não encontrada"}), 404

# Buscar planta por nome
@app.route('/plantas/buscar', methods=['GET'])
def buscar_planta_nome():
    nome = request.args.get('nome', '').lower()
    if not nome:
        return jsonify({"erro": "Parâmetro 'nome' é obrigatório"}), 400
    
    resultados = [p for p in plantas_data if nome in p['nome_popular'].lower()]
    
    if resultados:
        return jsonify({
            "total": len(resultados),
            "plantas": resultados
        })
    return jsonify({"erro": "Nenhuma planta encontrada"}), 404

# Listar categorias disponíveis
@app.route('/categorias', methods=['GET'])
def listar_categorias():
    categorias = list(set(p['categoria'] for p in plantas_data))
    return jsonify({
        "total": len(categorias),
        "categorias": categorias
    })

# Buscar plantas por categoria
@app.route('/categorias/<string:categoria>', methods=['GET'])
def buscar_por_categoria(categoria):
    plantas_categoria = [p for p in plantas_data if p['categoria'].lower() == categoria.lower()]
    
    if plantas_categoria:
        return jsonify({
            "categoria": categoria,
            "total": len(plantas_categoria),
            "plantas": plantas_categoria
        })
    return jsonify({"erro": "Categoria não encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)