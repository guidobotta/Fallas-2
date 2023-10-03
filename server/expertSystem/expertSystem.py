from experta import Fact, KnowledgeEngine, L, Rule

# Possible beers
CREAM_ALE = "Cream Ale"
BALTIC_PORTER = "Baltic Porter"
KOLSCH = "Kolsch"
WHITE_IPA = "Ipa Blanca"
CZECH_AMBER_LAGER = "Lager Ambar Checa"
NATALIA_NATALIA = "No es posible realizar una birra con estos atributos"

QUESTION_LIST = [
    "intensity",
    "color",
    "bitterness",
    "hop",
    "fermentation",
    "yeast",
    "null",
]


class BeerAttributes(Fact):
    pass


class BeerRules(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.candidateBeers = []

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


def getCandidateBeers(data):
    engine = BeerRules()
    engine.reset()
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
    next_quesiton_index = len(list(filter(lambda x: x != "*", data.values())))
    print(next_quesiton_index)
    return {
        "candidateBeers": engine.candidateBeers,
        "nextQuestion": QUESTION_LIST[next_quesiton_index],
    }
