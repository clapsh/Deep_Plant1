from datetime import datetime
"""
DATA SETTING CONFIG
"""
species = ["cattle", "pig"]
cattleLarge = [
    "tenderloin",
    "sirloin",
    "striploin",
    "chuck",
    "blade",
    "round",
    "bottom_round",
    "brisket",
    "shank",
    "rib",
]
pigLarge = [
    "tenderloin",
    "loin",
    "boston_shoulder",
    "picnic_shoulder",
    "spare_ribs",
    "belly",
    "ham",
]
cattleSmall = {
    0: ["tenderloin"],
    1: [
        "chuck_roll",
        "ribeye_roll",
        "lower sirloin",
        "chuck_flap_tail",
    ],
    2: ["strip_loin"],
    3: ["chuck"],
    4: [
        "chuck_tender",
        "top_blade_muscle",
        "blade",
        "blade_meat",
        "top_blade_meat",
    ],
    5: [
        "inside_round",
        "eye_of_round",
    ],
    6: [
        "rump_round",
        "top_sirloin",
        "top_sirloin_cap",
        "knuckle",
        "tri_tip",
    ],
    7: [
        "brisket",
        "brisket_point",
        "plate",
        "inside_skirt",
        "flank",
        "flap_meat",
        "apron",
    ],
    8: [
        "fore_shank",
        "hind_shank",
        "heel_muscle",
    ],
    9: [
        "chuck_short_rib",
        "boneless_short_rib",
        "short_rib",
        "interconstal",
        "tirmmed_rib",
        "hanging_tender",
        "outside_skirt",
        "neck_chain",
    ],
}
pigSmall = {
    0: ["tenderloin"],
    1: [
        "loin",
        "sirloin",
    ],
    2: ["boston_shoulder"],
    3: [
        "picnic_shoulder",
        "foreshank",
        "pork_jowl",
        "chuck_tender",
        "top_blade_muscle",
        "spatula_meat",
    ],
    4: ["rib", "ribs", "tirmmed_rib"],
    5: [
        "belly",
        "skirt_meat",
        "back_rib",
        "hanging_tender",
        "odol_belly",
    ],
    6: [
        "buttok",
        "top_sirloin",
        "knuckle",
        "eye_of_round",
        "rump_round",
        "hind_shank",
    ],
}
usrType = {0: "Normal", 1: "Researcher", 2: "Manager", 3: None}
sexType = {0: "Male", 1: "Female", 2: None}
gradeNum = {0: "1++", 1: "1+", 2: "1", 3: "2", 4: "3", 5: None}
CATTLE = 0
PIG = 1
def safe_float(val):
    """
    Safe Float 변환
    """
    try:
        return float(val)
    except (ValueError, TypeError):
        return None


def safe_str(val):
    """
    safe STR 반환
    """
    try:
        return str(val)
    except Exception:
        return None


def safe_int(val):
    """
    Safe Float 변환
    """
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def safe_bool(val):
    """
    Safe Float 변환
    """
    try:
        return bool(val)
    except (ValueError, TypeError):
        return None

def convert2datetime(date_string, format):
    """
    String -> Datetime
    Params
    1. date_string: 날짜/시간 문자열
    2. format: date_string의 포맷 인덱스(1 or 2,,,)
    """
    if date_string == None:
        return date_string
    if format == 1:
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    elif format == 2:
        return datetime.strptime(date_string, "%Y%m%d")
    else:
        return date_string
    
def convert2string(date_object, format):
    """
    Datetime -> String
    Params
    1. date_object: datetime object
    2. format: desired string format (1 or 2)
    """
    if date_object is None:
        return date_object
    if format == 1:
        return date_object.strftime("%Y-%m-%dT%H:%M:%S")
    elif format == 2:
        return date_object.strftime("%Y%m%d")
    else:
        return str(date_object)

def item_encoder(data_dict, item, input_data = None):
    datetime1_cvr = ["createdAt", "loginAt", "updatedAt"]
    datetime2_cvr = ["butcheryYmd", "birthYmd","date"]
    str_cvr = [
        "id",
        "userId",
        "traceNum",
        "farmAddr",
        "farmerNm",
        "name",
        "company",
        "jobTitle",
        "homeAddr",
    ]
    int_cvr = ["period","minute","seqno"]
    float_cvr = [
        "marbling",
        "color",
        "texture",
        "surfaceMoisture",
        "overall",
        "flavor",
        "juiciness",
        "tenderness",
        "umami",
        "palability",
        "L",
        "a",
        "b",
        "DL",
        "CL",
        "RW",
        "ph",
        "WBSF",
        "cardepsin_activity",
        "MFI",
        "Collagen",
        "sourness",
        "bitterness",
        "richness",
    ]
    bool_cvr = ["alarm"]
    if item in datetime1_cvr:
        data_dict[item] = convert2datetime(data_dict.get(item), 1)
    elif item in datetime2_cvr:
        data_dict[item] = convert2datetime(data_dict.get(item), 2)
    elif item in str_cvr:
        data_dict[item] = safe_str(data_dict.get(item))
    elif item in int_cvr:
        data_dict[item] = safe_int(data_dict.get(item))
    elif item in float_cvr:
        data_dict[item] = safe_float(data_dict.get(item))
    elif item in bool_cvr:
        data_dict[item] = safe_bool(data_dict.get(item))
    else:
        data_dict[item] = input_data

def to_dict(model_instance, query_instance=None):
    if hasattr(model_instance, '__table__'):
        return {c.name: getattr(model_instance, c.name) for c in model_instance.__table__.columns}
    else:
        cols = query_instance.column_descriptions
        return { cols[i]['name'] : model_instance[i] for i in range(len(cols)) }