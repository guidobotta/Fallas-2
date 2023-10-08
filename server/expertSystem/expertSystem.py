#from experta import Fact, KnowledgeEngine, L, Rule
from ..customRuleEngine import Condition as L, ComparableElement as Fact, RuleEngine as KnowledgeEngine, Rule

# Possible beers
CREAM_ALE = "Cream Ale"
BALTIC_PORTER = "Baltic Porter"
KOLSCH = "Kolsch"
WHITE_IPA = "Ipa Blanca"
CZECH_AMBER_LAGER = "Lager Ambar Checa"
NATALIA_NATALIA = "No es posible realizar una birra con estos atributos"

class BeerProperty:
    def __init__(self):
        self.property = set({})
        self.property_amount = 0
        self.name = ""

class BeerAttributes(Fact):
    pass

class BeerRules(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.candidateBeers = []
        self.cantidateProperties = []

    @Rule(
        BeerAttributes(intensity=L("baja") | L("media") | L("*")),
        BeerAttributes(color=L("palido") | L("*")),
        BeerAttributes(bitterness=L("bajo") | L("medio") | L("*")),
        BeerAttributes(hop=L("nuevo mundo") | L("*")),
        BeerAttributes(fermentation=L("media") | L("*")),
        BeerAttributes(yeast=L("ale") | L("*")),
    )
    def creamAle(self):
        self.candidateBeers.append(CREAM_ALE)
        self.cantidateProperties.append({
            "intensity": set({"baja", "media"}),
            "color": set({"palido"}),
            "bitterness": set({"bajo", "medio"}),
            "hop": set({"nuevo mundo"}),
            "fermentation": set({"media"}),
            "yeast": set({"ale"}),
        })

    @Rule(
        BeerAttributes(intensity=L("alta") | L("*")),
        BeerAttributes(color=L("oscuro") | L("*")),
        BeerAttributes(bitterness=L("medio") | L("*")),
        BeerAttributes(hop=L("viejo mundo") | L("*")),
        BeerAttributes(fermentation=L("media") | L("*")),
        BeerAttributes(yeast=L("lager") | L("*")),
    )
    def balticPorter(self):
        self.candidateBeers.append(BALTIC_PORTER)
        self.cantidateProperties.append({
            "intensity": set({"alta"}),
            "color": set({"oscuro"}),
            "bitterness": set({"medio"}),
            "hop": set({"viejo mundo"}),
            "fermentation": set({"media"}),
            "yeast": set({"lager"}),
        })

    @Rule(
        BeerAttributes(intensity=L("media") | L("*")),
        BeerAttributes(color=L("palido") | L("*")),
        BeerAttributes(bitterness=L("bajo") | L("medio") | L("*")),
        BeerAttributes(hop=L("viejo mundo") | L("*")),
        BeerAttributes(fermentation=L("alta") | L("*")),
        BeerAttributes(yeast=L("ale") | L("*")),
    )
    def kolsch(self):
        self.candidateBeers.append(KOLSCH)
        self.cantidateProperties.append({
            "intensity": set({"media"}),
            "color": set({"palido"}),
            "bitterness": set({"bajo", "medio"}),
            "hop": set({"viejo mundo"}),
            "fermentation": set({"alta"}),
            "yeast": set({"ale"}),
        })

    @Rule(
        BeerAttributes(intensity=L("alta") | L("*")),
        BeerAttributes(color=L("palido") | L("*")),
        BeerAttributes(bitterness=L("alto") | L("medio") | L("*")),
        BeerAttributes(hop=L("nuevo mundo") | L("*")),
        BeerAttributes(fermentation=L("alta") | L("*")),
        BeerAttributes(yeast=L("ale") | L("*")),
    )
    def whiteIPA(self):
        self.candidateBeers.append(WHITE_IPA)
        self.cantidateProperties.append({
            "intensity": set({"alta"}),
            "color": set({"palido"}),
            "bitterness": set({"alto", "medio"}),
            "hop": set({"nuevo mundo"}),
            "fermentation": set({"alta"}),
            "yeast": set({"ale"}),
        })

    @Rule(
        BeerAttributes(intensity=L("media") | L("*")),
        BeerAttributes(color=L("ambar") | L("oscuro") | L("*")),
        BeerAttributes(bitterness=L("bajo") | L("medio") | L("*")),
        BeerAttributes(hop=L("viejo mundo") | L("*")),
        BeerAttributes(fermentation=L("baja") | L("*")),
        BeerAttributes(yeast=L("lager") | L("*")),
    )
    def czechAmberLager(self):
        self.candidateBeers.append(CZECH_AMBER_LAGER)
        self.cantidateProperties.append({
            "intensity": set({"media"}),
            "color": set({"ambar", "oscuro"}),
            "bitterness": set({"bajo", "medio"}),
            "hop": set({"viejo mundo"}),
            "fermentation": set({"baja"}),
            "yeast": set({"lager"}),
        })

    def reset_state(self):
        self.context = set()
        self.candidateBeers = []
        self.cantidateProperties = []

def getCandidateBeers(data):
    engine = BeerRules()
    engine.reset_state()
    engine.declare(
        BeerAttributes(
            intensity=data["intensity"],
            color=data["color"],
            bitterness=data["bitterness"],
            hop=data["hop"],
            fermentation=data["fermentation"],
            yeast=data["yeast"],
        )
    )
    engine.run()
    print(data)

    if not engine.candidateBeers:
        return {
            "candidateBeers": engine.candidateBeers,
            "nextQuestion": "null",
        }

    definedProperties = list(filter(lambda key: data[key] != "*", data.keys()))
    storedCantidateProperties = {}

    for candidateProperty in engine.cantidateProperties:
        for key in candidateProperty.keys():
            if key in definedProperties:
                continue

            storedCandidateProperty = storedCantidateProperties.get(key, BeerProperty())
            storedCandidateProperty.property = storedCandidateProperty.property.union(candidateProperty[key])
            storedCandidateProperty.property_amount += len(candidateProperty[key])
            storedCandidateProperty.name = key
            storedCantidateProperties[key] = storedCandidateProperty

    next_quesiton = max(list(storedCantidateProperties.values()), key=lambda x: (len(x.property), -x.property_amount)).name
    print(next_quesiton)

    return {
        "candidateBeers": engine.candidateBeers,
        "nextQuestion": next_quesiton,
    }


engine = BeerRules()
engine.reset()
engine.declare(
    BeerAttributes(
        intensity="media",
        color="palido",
        bitterness="bajo",
        hop="nuevo mundo",
        fermentation="media",
        yeast="ale",
    )
)
engine.run()
print(f"Diagnostico: {engine.candidateBeers}")
