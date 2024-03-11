import random
import json
import datetime

# Get user input
# taxi_app = input("Enter the taxi app name: ")
# taxi_model = input("Enter the taxi model name: ")
# taxi_plate_field_name = input("Enter the field plate name: ")
# trajectory_app = input("Enter the trajectory app name: ")
# trajectory_model = input("Enter the trajectory model name: ")
# trajectory_taxi_field_name = input("Enter the taxi field name: ")
# trajectory_datetime_field_name = input("Enter the datetime field name: ")
# trajectory_longitude_field_name = input("Enter the longitude field name: ")
# trajectory_latitude_field_name = input("Enter the latitude field name: ")

taxi_app = "taxis"
taxi_model = "taxi"
taxi_plate_field_name = "plate"
trajectory_app = "taxis"
trajectory_model = "trajectory"
trajectory_taxi_field_name = "taxi"
trajectory_datetime_field_name = "date"
trajectory_longitude_field_name = "longitude"
trajectory_latitude_field_name = "latitude"


taxi_list = [
    (10026, "FFNJ-9813"),
    (10133, "PAOF-6727"),
    (1017, "MIFO-1824"),
    (10206, "INHN-2688"),
    (10207, "JLDK-4535"),
    (10247, "OBEF-5861"),
    (10293, "POOD-6790"),
    (1049, "BHNL-4225"),
    (1065, "GHDN-9291"),
    (108, "LNGK-1108"),
    (1139, "MFEF-8699"),
    (1364, "EGFM-5153"),
    (1475, "KJDM-6267"),
    (15, "FNHK-3772"),
    (165, "HKNN-8042"),
    (167, "IIJB-4867"),
    (1806, "HGIJ-7345"),
    (1963, "NBNI-1458"),
    (1999, "MOCP-7556"),
    (21, "NNEL-8793"),
    (2112, "GHNJ-1555"),
    (2153, "KHGM-2815"),
    (2179, "MKFF-1845"),
    (2183, "MKMJ-7264"),
    (2210, "FGMG-3071"),
    (2211, "FHID-7265"),
    (2230, "LOFJ-3431"),
    (2270, "GJGE-8317"),
    (2351, "FIPC-8785"),
    (2353, "DIFO-4571"),
    (252, "LAHG-7611"),
    (2522, "LGBJ-0156"),
    (2542, "DOHO-6151"),
    (2611, "EGOA-2654"),
    (2677, "PGDC-1949"),
    (2692, "NEIJ-5872"),
    (2717, "LBOK-2444"),
    (2719, "BKAM-8657"),
    (2761, "CFBG-2755"),
    (2783, "LIEL-8257"),
    (280, "IHIH-1812"),
    (2816, "AFOI-1144"),
    (2886, "AIGG-5536"),
    (2925, "BADO-1416"),
    (296, "CGEF-7101"),
    (3029, "MBDM-1187"),
    (3082, "BDFM-5551"),
    (3282, "MDDB-5497"),
    (3300, "NBAC-4573"),
    (3335, "EHMB-5718"),
    (3379, "MPNJ-7725"),
    (3458, "GGDE-3387"),
    (3492, "OKCA-5223"),
    (3510, "FEHJ-7325"),
    (3560, "GJCC-2787"),
    (3572, "GFHP-7928"),
    (3663, "DOKF-7876"),
    (376, "DDNG-0487"),
    (3812, "AAML-9871"),
    (3859, "GPGM-7365"),
    (3900, "EIED-2133"),
    (3942, "JLBH-4071"),
    (3979, "IEMK-7327"),
    (4028, "HNHM-3476"),
    (4055, "KPKO-3451"),
    (4056, "CIKI-8122"),
    (4105, "MLGC-5558"),
    (4145, "LGHO-2055"),
    (4242, "LGEF-9081"),
    (4397, "EGDN-3052"),
    (4416, "KHIE-6756"),
    (4449, "JGIE-0333"),
    (4453, "DNCM-7790"),
    (4485, "LLEL-9271"),
    (4728, "DABK-9431"),
    (4787, "NGKN-4357"),
    (4831, "FHCI-2846"),
    (4910, "GDEE-7052"),
    (515, "EHCE-5183"),
    (5170, "FCBN-3511"),
    (5210, "IPGK-3957"),
    (5224, "KMDK-1502"),
    (5240, "COIO-8354"),
    (5256, "HMMN-0507"),
    (5270, "BDLP-4643"),
    (5370, "HBJH-8671"),
    (5540, "OHAE-8815"),
    (5561, "FKOH-3490"),
    (56, "JIMF-2287"),
    (5610, "KOGN-4837"),
    (570, "AMGF-6934"),
    (5803, "HNMB-4988"),
    (5838, "MBND-8204"),
    (6031, "HFND-4178"),
    (6056, "BJFI-7501"),
    (6058, "JBKB-1428"),
    (609, "PNCB-3390"),
    (6118, "IBNE-0418"),
    (6129, "FLGH-8619"),
    (6163, "PEPP-9872"),
    (624, "FKLI-9441"),
    (6247, "KMGB-7305"),
    (626, "ECFG-9397"),
    (6286, "MLHK-7222"),
    (6298, "DCFM-2125"),
    (6374, "KCGK-4346"),
    (6418, "GHGH-1458"),
    (655, "NOGG-5935"),
    (6598, "FHLB-7962"),
    (6642, "DKOK-3814"),
    (6643, "KJDE-7135"),
    (6680, "MCCI-5437"),
    (6700, "BLMO-4997"),
    (6737, "DLEP-5452"),
    (6768, "FCPJ-0116"),
    (6772, "NOCB-3788"),
    (6782, "KOFG-2986"),
    (6790, "MGMA-6670"),
    (6841, "MGKK-5876"),
    (6899, "KACP-6171"),
    (7027, "OGHL-0787"),
    (7088, "HDBL-4695"),
    (71, "CLLD-1805"),
    (7131, "OKAL-8398"),
    (7150, "DNCJ-7132"),
    (7169, "CKEH-6725"),
    (7189, "DKFB-4482"),
    (7215, "JJNC-1645"),
    (7217, "IELF-5280"),
    (7218, "MNBE-4846"),
    (7219, "LPJA-3471"),
    (7249, "CNCJ-2997"),
    (7262, "FDAP-3298"),
    (7300, "HHJP-8573"),
    (7302, "KDJI-8221"),
    (7397, "DHFJ-3563"),
    (7493, "MOJF-6958"),
    (7534, "MICH-4553"),
    (7613, "FCKB-6558"),
    (7646, "FOFM-3206"),
    (7716, "IAMG-2604"),
    (7779, "KGHD-5576"),
    (7813, "FFGI-2329"),
    (7834, "GKGI-7231"),
    (7934, "PCKL-3328"),
    (7938, "HLBO-2375"),
    (7956, "CCKF-1601"),
    (7957, "BAJW-7971"),
    (8011, "FJEC-3215"),
    (804, "CDBJ-7875"),
    (8150, "BBJC-1672"),
    (8230, "CDKL-3488"),
    (8251, "GOAJ-6841"),
    (8300, "EDOF-2862"),
    (8305, "GIBC-2378"),
    (8311, "GNGM-2252"),
    (8320, "OOMH-5539"),
    (8362, "GPGD-1746"),
    (8377, "LPOM-8373"),
    (8410, "GNDO-6910"),
    (8433, "IGMB-9195"),
    (8466, "GGHB-2669"),
    (8484, "FHEE-8646"),
    (8491, "BNJE-8175"),
    (8585, "MDEF-7585"),
    (8604, "HOMH-4581"),
    (8715, "NFJM-6129"),
    (8716, "EONJ-3377"),
    (8733, "GMGM-1378"),
    (8751, "GMEC-3019"),
    (8776, "MDDJ-5215"),
    (8825, "HBEE-6337"),
    (8869, "HINB-4821"),
    (8935, "GAJG-2446"),
    (8974, "CKNH-1553"),
    (9018, "MOJL-7377"),
    (9061, "NPGE-7240"),
    (9098, "MIHI-5177"),
    (9217, "MJDD-8286"),
    (923, "IBIJ-5577"),
    (9238, "LLOD-8718"),
    (9271, "JDOL-5035"),
    (9275, "ENPB-7532"),
    (9298, "EMOJ-3697"),
    (9300, "KEJH-7652"),
    (9328, "EHBL-7645"),
    (9357, "BLFH-6860"),
    (9406, "EIGN-5732"),
    (9408, "CHGM-2476"),
    (9440, "FDCH-3572"),
    (9451, "MLMM-3869"),
    (9452, "KEBK-7570"),
    (9513, "FNHL-5802"),
    (9557, "BOIG-0354"),
    (9643, "GHDD-1743"),
    (9654, "ENKO-4271"),
    (9678, "FLPG-1136"),
    (974, "FNDF-2678"),
    (9836, "FHGJ-5518"),
    (9916, "BLDG-3162"),
]


def get_taxis_fixture_object(pk, plate):
    return {"model": f"{taxi_app}.{taxi_model.lower()}", "pk": pk, "fields": {taxi_plate_field_name: plate}}


def get_trajectory_fixture_object(pk, taxi_id, datetime, longitude, latitude):
    return {
        "model": f"{trajectory_app}.{trajectory_model.lower()}",
        "pk": pk,
        "fields": {
            trajectory_taxi_field_name: taxi_id,
            trajectory_datetime_field_name: datetime,
            trajectory_longitude_field_name: longitude,
            trajectory_latitude_field_name: latitude,
        },
    }


taxi_fixture = []


for taxi in taxi_list:
    taxi_fixture.append(get_taxis_fixture_object(taxi[0], taxi[1]))


taxi_fixture_json = json.dumps(taxi_fixture, indent=4)


with open("taxi_fixture.json", "w") as file:
    file.write(taxi_fixture_json)


trajectory_fixture = []

for taxi in taxi_list:
    initial_date = datetime.datetime.now(datetime.timezone.utc)
    for day in range(0, 10):
        initial_latitude = 40.741895
        initial_longitude = -73.989308
        day_date = initial_date + datetime.timedelta(days=day)
        for i in range(0, 10):
            latitude = initial_latitude + random.uniform(-0.0005, 0.0005)
            longitude = initial_longitude + random.uniform(-0.0005, 0.0005)
            date = day_date + datetime.timedelta(minutes=i)
            trajectory_fixture.append(
                get_trajectory_fixture_object(
                    len(trajectory_fixture) + 1, taxi[0], date.isoformat(), longitude, latitude
                )
            )


trajectory_fixture_json = json.dumps(trajectory_fixture, indent=4)


with open("trajectory_fixture.json", "w") as file:
    file.write(trajectory_fixture_json)
