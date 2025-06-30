import re

from .extractors.breastcancernow_org import (
    extract_full_text as extract_breastcancernow_org_full_text,
)
from .extractors.www_breastcancer_org import (
    extract_full_text as extract_breastcancer_org_full_text,
)
from .extractors.www_curetoday_com import (
    extract_full_text as extract_curetoday_com_full_text,
)
from .extractors.www_nature_com import extract_full_text as extract_nature_com_full_text
from .extractors.www_news_medical_net import (
    extract_full_text as extract_news_medical_net_full_text,
)
from .extractors.www_webmd_com import extract_full_text as extract_webmd_com_full_text

EXTRACTOR_REGISTRY = {
    r"www\.breastcancer\.org": extract_breastcancer_org_full_text,
    r"breastcancernow\.org": extract_breastcancernow_org_full_text,
    r"www\.curetoday\.com": extract_curetoday_com_full_text,
    r"www\.nature\.com": extract_nature_com_full_text,
    r"www\.news-medical\.net": extract_news_medical_net_full_text,
    r"www\.webmd\.com": extract_webmd_com_full_text,
    # Add more extractors as needed
}


def get_extractor_for_domain(domain: str):
    """
    Recorre EXTRACTOR_REGISTRY y devuelve la función extractora
    cuya clave (patrón regex) coincide con el dominio.
    Si no hay coincidencia, retorna None.
    """
    for pattern, extractor_fn in EXTRACTOR_REGISTRY.items():
        if re.search(pattern, domain):
            return extractor_fn
    return None
