"""Cleaning services offered on the public site. Illustrative demo data."""

SERVICES = (
    {
        "id": "buero",
        "name": "Büroreinigung",
        "summary": "Regelmäßige Reinigung von Arbeitsplätzen, Besprechungsräumen und Sozialflächen.",
        "tasks": ["Schreibtische und Kontaktflächen", "Böden saugen und wischen", "Sanitärbereiche", "Küche und Müll"],
    },
    {
        "id": "treppenhaus",
        "name": "Treppenhausreinigung",
        "summary": "Pflege von Eingängen, Treppen und Gemeinschaftsflächen in Wohn- und Geschäftshäusern.",
        "tasks": ["Stufen und Podeste", "Geländer", "Eingangsbereich", "Briefkastenanlage"],
    },
    {
        "id": "praxis",
        "name": "Praxis- und Gewerbereinigung",
        "summary": "Reinigung für Praxen, Kanzleien und andere gewerbliche Räume mit festem Ablauf.",
        "tasks": ["Warte- und Behandlungsbereiche", "Empfang", "Sanitär", "Bodenpflege"],
    },
    {
        "id": "fenster",
        "name": "Fensterreinigung",
        "summary": "Rahmen- und Glasreinigung für erreichbare Fenster in Büros und Gewerberäumen.",
        "tasks": ["Glasflächen innen", "Rahmen und Fensterbänke", "Sichtprüfung", "Abstimmung zur Erreichbarkeit"],
    },
    {
        "id": "grund",
        "name": "Grundreinigung",
        "summary": "Gründliche Reinigung außerhalb des laufenden Unterhalts, zum Beispiel vor einem Einzug.",
        "tasks": ["Hartnäckige Beläge", "Ecken und Kanten", "Sanitär und Küche", "Böden"],
    },
    {
        "id": "individuell",
        "name": "Individuelle Reinigungsleistungen",
        "summary": "Ein Ablauf, der zu Objekt, Zeiten und Umfang passt, wenn keine Standardleistung greift.",
        "tasks": ["Besichtigung oder Beschreibung", "Leistungsverzeichnis", "Terminabstimmung", "Festlegung der Intervalle"],
    },
)

SERVICE_IDS = {item["id"] for item in SERVICES}
PROPERTY_TYPES = ("buero", "praxis", "treppenhaus", "wohnung", "sonstiges")
STATUSES = ("neu", "kontaktiert", "angebot_erstellt", "abgeschlossen", "abgelehnt")
PRIVACY_VERSION = "2026-10-01"
