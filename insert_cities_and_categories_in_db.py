from api.services.city_service import city_service
from api.services.category_service import category_service
from api.services.level_service import level_service
from api.services.place_service import place_service
from models import City
from schemas.category_schema import CategoryCreate
from schemas.city_schema import CityCreate
from sqlalchemy.orm import Session
from database import SessionLocal
from models.organizer import Organizer
from models.user_organizer import user_organizer
from models.level import Level
from models.place import Place
from schemas.level_schema import LevelCreate
from schemas.place_schema import PlaceCreate

correct_cities = {'Ábalos': {'code': 26339, 'lat': 42.5663460958579, 'long': -2.7034943374},
                  'Agoncillo': {'code': 26160, 'lat': 42.4362228354874, 'long': -2.2788383532},
                  'Aguilar del Río Alhama': {'code': 26530, 'lat': 41.9536806059926, 'long': -1.9926018698},
                  'Ajamil de Cameros': {'code': 26133, 'lat': 0, 'long': 0},
                  'Albelda de Iregua': {'code': 26120, 'lat': 42.3652087121677, 'long': -2.4705590378},
                  'Alberite': {'code': 26141, 'lat': 42.4000988625693, 'long': -2.4096007466},
                  'Alcanadre': {'code': 26509, 'lat': 42.4042978479629, 'long': -2.1517406543},
                  'Aldeanueva de Ebro': {'code': 26559, 'lat': 42.2291365184681, 'long': -1.9095509798},
                  'Alesanco': {'code': 26324, 'lat': 42.4239310584127, 'long': -2.8187652436},
                  'Alesón': {'code': 26315, 'lat': 42.4076250619403, 'long': -2.6706871818},
                  'Alfaro': {'code': 26540, 'lat': 42.159620809149, 'long': -1.82434230161},
                  'Almarza de Cameros': {'code': 26111, 'lat': 42.2261819365028, 'long': -2.5905467066},
                  'Anguciana': {'code': 26210, 'lat': 42.5754139174408, 'long': -2.9063688464},
                  'Anguiano': {'code': 26322, 'lat': 42.2509713543766, 'long': -2.7983743493},
                  'Arenzana de Abajo': {'code': 26311, 'lat': 42.3808925396522, 'long': -2.7176400739},
                  'Arenzana de Arriba': {'code': 26312, 'lat': 42.374238544551, 'long': -2.68634985729},
                  'Arnedillo': {'code': 26589, 'lat': 42.2153974306128, 'long': -2.2361404735},
                  'Arnedo': {'code': 26580, 'lat': 42.2214660084789, 'long': -2.0928397047},
                  'Arrúbal': {'code': 26151, 'lat': 42.4285206632771, 'long': -2.2526572875},
                  'Ausejo': {'code': 26513, 'lat': 42.3524652340104, 'long': -2.135227057},
                  'Autol': {'code': 26560, 'lat': 42.2082301769762, 'long': -1.9710936698},
                  'Azofra': {'code': 26323, 'lat': 42.4385845190338, 'long': -2.7978709938},
                  'Badarán': {'code': 26310, 'lat': 42.3618856739874, 'long': -2.802085684},
                  'Bañares': {'code': 26257, 'lat': 42.4736206831463, 'long': -2.8883326121},
                  'Baños de Río Tobía': {'code': 26320, 'lat': 42.3430593665927, 'long': -2.7564729255},
                  'Baños de Rioja': {'code': 26241, 'lat': 42.5136609827223, 'long': -2.9491648931},
                  'Berceo': {'code': 26327, 'lat': 42.3291482093304, 'long': -2.8695445041},
                  'Bergasa': {'code': 26588, 'lat': 42.2660101845995, 'long': -2.1530620079},
                  'Bergasillas Bajera': {'code': 26588, 'lat': 42.2506801404284, 'long': -2.1650826072},
                  'Bezares': {'code': 26312, 'lat': 42.3658189369826, 'long': -2.6692798714},
                  'Bobadilla': {'code': 26321, 'lat': 42.3183673907055, 'long': -2.7567546253},
                  'Brieva de Cameros': {'code': 26322, 'lat': 42.1793991149214, 'long': -2.7926186067},
                  'Briñas': {'code': 26290, 'lat': 42.6039860769164, 'long': -2.8318039238},
                  'Briones': {'code': 26330, 'lat': 42.5240684236217, 'long': -2.7859777951},
                  'Cabezón de Cameros': {'code': 26135, 'lat': 42.1864583823243, 'long': -2.5179706471},
                  'Calahorra': {'code': 26500, 'lat': 42.307869084608, 'long': -1.95261811526},
                  'Camprovín': {'code': 26311, 'lat': 42.3557343859451, 'long': -2.7186478806},
                  'Canales de la Sierra': {'code': 26329, 'lat': 42.1818161333813, 'long': -3.0824681337},
                  'Canillas de Río Tuerto': {'code': 26325, 'lat': 42.3975611299978, 'long': -2.8319112761},
                  'Cañas': {'code': 26325, 'lat': 42.3949124722046, 'long': -2.8530221082},
                  'Cárdenas': {'code': 26311, 'lat': 42.3745623270071, 'long': -2.7664815967},
                  'Casalarreina': {'code': 26230, 'lat': 42.5473655679105, 'long': -2.905370377},
                  'Castañares de Rioja': {'code': 26240, 'lat': 42.5132277804401, 'long': -2.9214958059},
                  'Castroviejo': {'code': 26315, 'lat': 42.3287926947192, 'long': -2.6556475534},
                  'Cellorigo': {'code': 26212, 'lat': 42.6237349419408, 'long': -3.001187041},
                  'Cenicero': {'code': 26350, 'lat': 42.4793401851368, 'long': -2.6450279797},
                  'Cervera del Río Alhama': {'code': 26520, 'lat': 42.0313213115163, 'long': -1.9660351248},
                  'Cidamón': {'code': 26291, 'lat': 42.4850778032649, 'long': -2.8558342852},
                  'Cihuri': {'code': 26210, 'lat': 42.5787454428988, 'long': -2.9210575006},
                  'Cirueña': {'code': 26258, 'lat': 42.4244987501371, 'long': -2.8776634292},
                  'Clavijo': {'code': 26130, 'lat': 42.3501521107654, 'long': -2.4284464099},
                  'Cordovín': {'code': 26311, 'lat': 42.3883897225054, 'long': -2.8085357294},
                  'Corera': {'code': 26144, 'lat': 42.3540815888504, 'long': -2.2145637018},
                  'Cornago': {'code': 26526, 'lat': 42.0664425892735, 'long': -2.1027286414},
                  'Corporales': {'code': 26259, 'lat': 42.4217034099617, 'long': -3.0062943017},
                  'Cuzcurrita de Río Tirón': {'code': 26214, 'lat': 42.5507366690794, 'long': -2.9665987939},
                  'Daroca de Rioja': {'code': 26373, 'lat': 42.3585033026039, 'long': -2.5930698423},
                  'Enciso': {'code': 26586, 'lat': 42.139771238006, 'long': -2.24938132387},
                  'Entrena': {'code': 26375, 'lat': 42.3957954781069, 'long': -2.5151438685},
                  'Estollo': {'code': 26328, 'lat': 42.3207194262645, 'long': -2.8441499088},
                  'Ezcaray': {'code': 26280, 'lat': 42.2632528627069, 'long': -3.023839979},
                  'Foncea': {'code': 26211, 'lat': 42.6119695530579, 'long': -3.0422377156},
                  'Fonzaleche': {'code': 26211, 'lat': 42.589710205357, 'long': -3.00067125681},
                  'Fuenmayor': {'code': 26360, 'lat': 42.4748305758632, 'long': -2.5842047984},
                  'Galbárruli': {'code': 26212, 'lat': 42.6208995345344, 'long': -2.9572233569},
                  'Galilea': {'code': 26144, 'lat': 42.3634408919726, 'long': -2.2309856978},
                  'Gallinero de Cameros': {'code': 26122, 'lat': 42.1747862789859, 'long': -2.6119312518},
                  'Gimileo': {'code': 26221, 'lat': 42.5535057324179, 'long': -2.8955422108},
                  'Grañón': {'code': 26259, 'lat': 42.5070606590734, 'long': -2.8999689315},
                  'Grávalos': {'code': 26587, 'lat': 0, 'long': 0},
                  'Haro': {'code': 26200, 'lat': 42.5665431693139, 'long': -2.8690706501},
                  'Herce': {'code': 26584, 'lat': 42.2297004411065, 'long': -2.1708500468},
                  'Herramélluri': {'code': 26213, 'lat': 42.5029436390292, 'long': -3.0130398755},
                  'Hervías': {'code': 26257, 'lat': 42.4501602843016, 'long': -2.855648421},
                  'Hormilla': {'code': 26323, 'lat': 42.4540010101185, 'long': -2.7783462571},
                  'Hormilleja': {'code': 26223, 'lat': 42.4637573560773, 'long': -2.7294201043},
                  'Hornillos de Cameros': {'code': 26133, 'lat': 42.212465838362, 'long': -2.40323291675},
                  'Hornos de Moncalvillo': {'code': 26372, 'lat': 42.3973352780627, 'long': -2.5789128875},
                  'Huércanos': {'code': 26314, 'lat': 42.4320364267258, 'long': -2.6675309918},
                  'Igea': {'code': 26525, 'lat': 42.0528316309918, 'long': -2.0263592501},
                  'Jalón de Cameros': {'code': 26134, 'lat': 42.2135462397888, 'long': -2.4926787549},
                  'Laguna de Cameros': {'code': 26135, 'lat': 42.1639712318572, 'long': -2.540238188},
                  'Lagunilla del Jubera': {'code': 26131, 'lat': 42.3268777644748, 'long': -2.345139903},
                  'Lardero': {'code': 26140, 'lat': 42.4140906991708, 'long': -2.4720644516},
                  'Ledesma de la Cogolla': {'code': 26321, 'lat': 42.3185040396705, 'long': -2.7042727116},
                  'Leiva': {'code': 26213, 'lat': 42.508890719051, 'long': -3.04404257768},
                  'Leza de Río Leza': {'code': 26132, 'lat': 42.3361972838805, 'long': -2.4081349444},
                  'Logroño': {'code': 26001, 'lat': 42.4671213247137, 'long': -2.4454133612},
                  'Lumbreras de Cameros': {'code': 26126, 'lat': 0, 'long': 0},
                  'Manjarrés': {'code': 26315, 'lat': 42.3916280148364, 'long': -2.6618651429},
                  'Mansilla de la Sierra': {'code': 26329, 'lat': 42.1119435586792, 'long': -2.9063983997},
                  'Manzanares de Rioja': {'code': 26258, 'lat': 42.3819635256435, 'long': -2.9047043149},
                  'Matute': {'code': 26321, 'lat': 42.2928877233593, 'long': -2.7931509702},
                  'Medrano': {'code': 26374, 'lat': 42.3899570168005, 'long': -2.558175328},
                  'Munilla': {'code': 26586, 'lat': 42.1981754173837, 'long': -2.3258655889},
                  'Murillo de Río Leza': {'code': 26143, 'lat': 42.4074310816256, 'long': -2.3083786887},
                  'Muro de Aguas': {'code': 26587, 'lat': 42.1292692853894, 'long': -2.1229521868},
                  'Muro en Cameros': {'code': 26134, 'lat': 42.2208698946984, 'long': -2.5385617796},
                  'Nájera': {'code': 26300, 'lat': 42.4244023325867, 'long': -2.7339858072},
                  'Nalda': {'code': 26190, 'lat': 42.3323129233651, 'long': -2.4880427984},
                  'Navajún': {'code': 26533, 'lat': 41.9683867883856, 'long': -2.0831289392},
                  'Navarrete': {'code': 26370, 'lat': 42.4281220151845, 'long': -2.5638104829},
                  'Nestares': {'code': 26110, 'lat': 42.286215475242, 'long': -2.60525222268},
                  'Nieva de Cameros': {'code': 26124, 'lat': 42.2201002494892, 'long': -2.6704972636},
                  'Ochánduri': {'code': 26213, 'lat': 42.5259448309644, 'long': -3.0009411438},
                  'Ocón': {'code': 26148, 'lat': 42.3056122024014, 'long': -2.1972770612},
                  'Ojacastro': {'code': 26270, 'lat': 42.348457585384, 'long': -2.98790253824},
                  'Ollauri': {'code': 26220, 'lat': 42.5418473556152, 'long': -2.8280759821},
                  'Ortigosa de Cameros': {'code': 26124, 'lat': 42.1614536407818, 'long': -2.711549259},
                  'Pazuengos': {'code': 26261, 'lat': 42.3034923037593, 'long': -2.9304572754},
                  'Pedroso': {'code': 26321, 'lat': 42.2948554713857, 'long': -2.7001900445},
                  'Pinillos': {'code': 26111, 'lat': 42.1920748056327, 'long': -2.5971002506},
                  'Pradejón': {'code': 26510, 'lat': 42.3268365766514, 'long': -2.0422523719},
                  'Pradillo': {'code': 26122, 'lat': 42.1871082191828, 'long': -2.640565848},
                  'Préjano': {'code': 26589, 'lat': 42.1626187909597, 'long': -2.183787215},
                  'Quel': {'code': 26570, 'lat': 42.2055534009365, 'long': -2.044482052},
                  'Rabanera': {'code': 26133, 'lat': 42.1829540533377, 'long': -2.4764421662},
                  'Rasillo de Cameros, El': {'code': 26124, 'lat': 42.1963077536721, 'long': -2.7135825706},
                  'El Redal': {'code': 26146, 'lat': 42.3474607139224, 'long': -2.1999975057},
                  'Ribafrecha': {'code': 26130, 'lat': 42.3582796851427, 'long': -2.3687963645},
                  'Rincón de Soto': {'code': 26550, 'lat': 42.2376951026978, 'long': -1.8476961887},
                  'Robres del Castillo': {'code': 26131, 'lat': 42.2567733401141, 'long': -2.2922206545},
                  'Rodezno': {'code': 26222, 'lat': 42.5128155703588, 'long': -2.8303174103},
                  'Sajazarra': {'code': 26212, 'lat': 42.5953271789872, 'long': -2.9430591012},
                  'San Asensio': {'code': 26340, 'lat': 42.5075007267059, 'long': -2.7403433215},
                  'San Millán de la Cogolla': {'code': 26326, 'lat': 42.3059721284563, 'long': -2.8931192345},
                  'San Millán de Yécora': {'code': 26216, 'lat': 42.5481308173249, 'long': -3.0993079603},
                  'San Román de Cameros': {'code': 26133, 'lat': 42.2174980465943, 'long': -2.456867666},
                  'San Torcuato': {'code': 26291, 'lat': 42.4804983075003, 'long': -2.8588371435},
                  'San Vicente de la Sonsierra': {'code': 26338, 'lat': 42.5612794580491, 'long': -2.7468534501},
                  'Santa Coloma': {'code': 26315, 'lat': 42.3584221433302, 'long': -2.6368155841},
                  'Santa Engracia del Jubera': {'code': 26131, 'lat': 42.3083011147031, 'long': -2.3084117481},
                  'Santa Eulalia Bajera': {'code': 26585, 'lat': 42.2234051576032, 'long': -2.1902327028},
                  'Santo Domingo de la Calzada': {'code': 26250, 'lat': 42.42846789843, 'long': -2.95550071067},
                  'Santurde de Rioja': {'code': 26260, 'lat': 42.389925027679, 'long': -2.99503059394},
                  'Santurdejo': {'code': 26261, 'lat': 42.3632123259631, 'long': -2.9426512202},
                  'Sojuela': {'code': 26376, 'lat': 42.3551135188113, 'long': -2.5576228302},
                  'Sorzano': {'code': 26191, 'lat': 42.3462085476356, 'long': -2.5213721123},
                  'Sotés': {'code': 26371, 'lat': 42.3907563237756, 'long': -2.6053986368},
                  'Soto en Cameros': {'code': 26132, 'lat': 42.2761183607792, 'long': -2.4312144949},
                  'Terroba': {'code': 26132, 'lat': 42.2566874510665, 'long': -2.4305291287},
                  'Tirgo': {'code': 26211, 'lat': 42.5460683505785, 'long': -2.9386034165},
                  'Tobía': {'code': 26321, 'lat': 42.2748781012845, 'long': -2.8608572487},
                  'Tormantos': {'code': 26213, 'lat': 42.5007168377115, 'long': -3.0663924058},
                  'Torre en Cameros': {'code': 26134, 'lat': 42.2450224487012, 'long': -2.5233220994},
                  'Torrecilla en Cameros': {'code': 26100, 'lat': 42.2622868193718, 'long': -2.6181287207},
                  'Torrecilla sobre Alesanco': {'code': 26224, 'lat': 42.4156488094624, 'long': -2.8411629004},
                  'Torremontalbo': {'code': 26359, 'lat': 42.4868363012607, 'long': -2.6973784481},
                  'Treviana': {'code': 26215, 'lat': 42.5583277903957, 'long': -3.0455628778},
                  'Tricio': {'code': 26312, 'lat': 42.3993958158496, 'long': -2.7100014791},
                  'Tudelilla': {'code': 26512, 'lat': 42.2934933378534, 'long': -2.1173490181},
                  'Uruñuela': {'code': 26313, 'lat': 42.4557175258418, 'long': -2.6997529986},
                  'Valdemadera': {'code': 26532, 'lat': 41.9878300687755, 'long': -2.0591471883},
                  'Valgañón': {'code': 26288, 'lat': 42.3254405195395, 'long': -3.0778449797},
                  'Ventosa': {'code': 26371, 'lat': 42.4034976677652, 'long': -2.6294063724},
                  'Ventrosa': {'code': 26329, 'lat': 42.1762297810747, 'long': -2.8379604752},
                  'Viguera': {'code': 26121, 'lat': 42.3054183153732, 'long': -2.5388429197},
                  'Villalba de Rioja': {'code': 26292, 'lat': 42.6101761063184, 'long': -2.8941050675},
                  'Villalobar de Rioja': {'code': 26256, 'lat': 42.4904727689994, 'long': -2.9674380093},
                  'Villamediana de Iregua': {'code': 26142, 'lat': 42.4330153212515, 'long': -2.4078029947},
                  'Villanueva de Cameros': {'code': 26123, 'lat': 42.156581747155, 'long': -2.64153702097},
                  'Villar de Arnedo': {'code': 26511, 'lat': 42.3138273948547, 'long': -2.0779118043},
                  'Villar de Torre': {'code': 26325, 'lat': 42.3667411018816, 'long': -2.8659477494},
                  'Villarejo': {'code': 26325, 'lat': 42.3672392101918, 'long': -2.8925575947},
                  'Villarroya': {'code': 26587, 'lat': 42.1383826444042, 'long': -2.0633760794},
                  'Villarta-Quintana': {'code': 26259, 'lat': 42.4059672824955, 'long': -3.0591258163},
                  'Villavelayo': {'code': 26329, 'lat': 42.1688020535952, 'long': -2.9877152854},
                  'Villaverde de Rioja': {'code': 26321, 'lat': 42.3218275380717, 'long': -2.813712911},
                  'Villoslada de Cameros': {'code': 26125, 'lat': 42.0709036099867, 'long': -2.699498066},
                  'Viniegra de Abajo': {'code': 26329, 'lat': 42.1259853892287, 'long': -2.8811104511},
                  'Viniegra de Arriba': {'code': 26329, 'lat': 42.0811898298983, 'long': -2.8246748474},
                  'Zarratón': {'code': 26291, 'lat': 42.5187754869971, 'long': -2.8712470265},
                  'Zarzosa': {'code': 26586, 'lat': 42.1789994353009, 'long': -2.357815936},
                  'Zorraquín': {'code': 26288, 'lat': 0, 'long': 0}}

categories = [
    {"name": "Vino"},
    {"name": "Deporte"},
    {"name": "Coche"},
    {"name": "Moto"},
    {"name": "Paseo"},
    {"name": "Senderismo"},
    {"name": "Ciclismo"},
    {"name": "Pesca"},
    {"name": "Caza"},
    {"name": "Aventura"},
    {"name": "Agroturismo"},
    {"name": "Equitación"},
    {"name": "Observación de aves"},
    {"name": "Camping"},
    {"name": "Escalada"},
    {"name": "Navegación"},
    {"name": "Fotografía rural"},
    {"name": "Relax"},
    {"name": "Trekking"},
    {"name": "Gastronomía local"},
    {"name": "Recolección de setas"},
    {"name": "Arte y cultura local"},
    {"name": "Vía ferrata"},
    {"name": "Rutas en 4x4"},
    {"name": "Turismo rural"},
    {"name": "Caballos"},
    {"name": "Conducción en la naturaleza"},
    {"name": "Talleres artesanales"},
    {"name": "Rutas gastronómicas"},
    {"name": "Termalismo"},
    {"name": "Relax en la naturaleza"},
    {"name": "Degustación de vinos"},
    {"name": "Cata de aceites"},
    {"name": "Talleres de cocina tradicional"},
    {"name": "Mercados locales"},
    {"name": "Fiestas populares"},
    {"name": "Rutas de queso"},
    {"name": "Recogida de frutas"},
    {"name": "Catas de productos locales"},
    {"name": "Visitas a bodegas"},
    {"name": "Rutas de miel"},
    {"name": "Jornadas de caza y pesca"},
    {"name": "Festivales rurales"},
    {"name": "Senderismo en la naturaleza"},
    {"name": "Visita a granjas"},
    {"name": "Arte rural"},
    {"name": "Días de campo"},
    {"name": "Excursiones en tractor"},
    {"name": "Rutas en quad"},
    {"name": "Paseos en carro"},
    {"name": "Actividades en granja"},
    {"name": "Fiestas de la cosecha"},
    {"name": "Escapadas rurales"},
    {"name": "Rutas en bici de montaña"},
    {"name": "Convivencia con animales de granja"},
    {"name": "Rutas por los campos"},
    {"name": "Observación de estrellas"},
    {"name": "Fiestas de tradiciones locales"},
    {"name": "Jornadas de intercambio cultural"},
    {"name": "Ruta de los embutidos"},
    {"name": "Catas de cerveza artesanal"},
    {"name": "Talleres de cerámica"},
    {"name": "Recreación histórica"},
    {"name": "Rutas por caminos rurales"},
    {"name": "Vuelta en carreta tirada por caballos"},
    {"name": "Visitas a museos rurales"},
    {"name": "Talleres de cestería"},
    {"name": "Escuelas de oficios tradicionales"},
    {"name": "Rutas de pastores"},
    {"name": "Rutas por viñedos"},
    {"name": "Caminos del vino"},
    {"name": "Convivencia en aldeas"}
]

levels = [
    {"name": "Semilla", "range_min": 0, "range_max": 20},
    {"name": "Brote Verde", "range_min": 21, "range_max": 40},
    {"name": "Planta Joven", "range_min": 41, "range_max": 60},
    {"name": "Campo en Flor", "range_min": 61, "range_max": 80},
    {"name": "Recolector/a", "range_min": 81, "range_max": 100},
    {"name": "Cultivador/a", "range_min": 101, "range_max": 120},
    {"name": "Granjero/a", "range_min": 121, "range_max": 140},
    {"name": "Capataz de Campos", "range_min": 141, "range_max": 160},
    {"name": "Terrateniente", "range_min": 161, "range_max": 180},
    {"name": "Hacendado/a", "range_min": 181, "range_max": 200},
    {"name": "Señor/a de la Naturaleza", "range_min": 201, "range_max": 500}
]

db: Session = SessionLocal()


def insert_cities_in_db():
    for city_name, city_info in correct_cities.items():
        city_create = CityCreate(
            name=city_name,
            latitude=float(city_info['lat']),
            longitude=float(city_info['long']),
            location_url=f"https://www.google.com/maps?q={city_info['lat']},{city_info['long']}",
            cp=str(city_info['code']),
        )

        city_service.create_city(db=db, city_create=city_create)


def insert_categories_in_db():
    for category_info in categories:
        category_create = CategoryCreate(
            name=category_info['name'],
        )

        category_service.create_category(db=db, category_create=category_create)


def insert_levels_in_db():
    levels_instances = [LevelCreate(**level) for level in levels]

    for level_instance in levels_instances:
        level_service.create_level(db=db, level_create=level_instance)


def insert_places_in_db():
    cities: list[City] = city_service.get_all_cities(db=db)

    for city in cities:
        place = PlaceCreate(name="Plaza", city_id=city.id, location_url=city.location_url)
        place_service.create_place(db=db, place_create=place)

if __name__ == '__main__':
    insert_cities_in_db()
    insert_categories_in_db()
    insert_levels_in_db()
    insert_places_in_db()