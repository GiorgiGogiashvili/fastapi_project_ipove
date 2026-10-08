from app.schemas.request import Language, RequestAnalysis


KEYWORDS = {
    "dentist": [
        "зуб",
        "стоматолог",
        "кариес",
        "tooth",
        "dentist",
        "cavity",
        "კბილი",
        "სტომატოლოგი",
        "კარიესი",
    ],
    "laboratory": [
        "анализ",
        "кровь",
        "лаборатория",
        "test",
        "blood",
        "laboratory",
        "ანალიზი",
        "სისხლი",
        "ლაბორატორია",
    ],
    "legal": [
        "договор",
        "документ",
        "заявление",
        "contract",
        "document",
        "application",
        "ხელშეკრულება",
        "დოკუმენტი",
        "განცხადება",
    ],
}


TRANSLATIONS = {
    "dentist": {
        "ru": ("Медицина", "Стоматолог"),
        "en": ("Healthcare", "Dentist"),
        "ka": ("მედიცინა", "სტომატოლოგი"),
    },
    "laboratory": {
        "ru": ("Медицина", "Лабораторная диагностика"),
        "en": ("Healthcare", "Laboratory diagnostics"),
        "ka": ("მედიცინა", "ლაბორატორიული დიაგნოსტიკა"),
    },
    "legal": {
        "ru": ("Документы", "Юрист или консультант"),
        "en": ("Documents", "Lawyer or consultant"),
        "ka": ("დოკუმენტები", "იურისტი ან კონსულტანტი"),
    },
    "unknown": {
        "ru": ("Не определено", "Нужна дополнительная информация"),
        "en": ("Unknown", "More information is needed"),
        "ka": ("უცნობია", "საჭიროა დამატებითი ინფორმაცია"),
    },
}


def detect_service(
    text: str,
    language: Language,
) -> RequestAnalysis:
    normalized_text = text.lower()
    detected_service = "unknown"

    for service_code, words in KEYWORDS.items():
        if any(word in normalized_text for word in words):
            detected_service = service_code
            break

    category, service = TRANSLATIONS[detected_service][language]

    urgency = "medium"

    if detected_service == "unknown":
        urgency = "low"

    return RequestAnalysis(
        category=category,
        service=service,
        service_code=detected_service,
        urgency=urgency,
    )