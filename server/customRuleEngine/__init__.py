"""
Custom Rule Engine

Definiciones:
    - Motor de Reglas: Evalua un conjunto de reglas contra un elemento
    - Reglas: Evalua un conjunto de condiciones contra un elemento
    - Condiciones: Establece las propiedades que debe cumplir el elemento

Como "facilidad" se hace abuso del Elemento a comparar y las evaluaciones de python
    donde `x == y` el que tiene a cargo la evaluación es la instancia de x.
    Uno de los elementos comparables en sus atributos va a tener condiciones, y el otro poseera los literales
    a comparar
    Ejemplo
        cmp1= Comparable1(color=Condicion('negro') | Condicion('blanco'))
        cmp2= Comparable2(color='gris'

        result = cmp1 == cmp2

    Esto es porque tiene sentido que una condición sepa evaluar un literal, pero no vice-versa.
"""


class Condition(object):
    """
    A condition is the simplest object that can be compared to another object.
    If joined by another condition through a logical operator (or, and), it will
    return a ChainedCondition object containing both conditions.
    """
    def __init__(self, value):
        self.value = value

    def __and__(self, other):
        return ANDCC(self, other)

    def __or__(self, other):
        return ORCC(self, other)

    def __eq__(self, other):
        return self.value == other

    def matches(self, other):
        return self == other


class ChainedCondition(object):
    """
    A chained condition is a condition that contains other conditions.
    These conditions are linked via logical operators (or, and).
    """
    def __init__(self, *args):
        self.conditions = args

    def __and__(self, other):
        return ANDCC(self, other)

    def __or__(self, other):
        return ORCC(self, other)

    def matches(self, other):
        raise NotImplemented


class ORCC(ChainedCondition):
    """
    ORCC: OR Chained Condition
    Return True if any of the conditions matches
    """
    def matches(self, other):
        matches = False
        for condition in self.conditions:
            _matches = condition.matches(other)
            matches = matches or _matches
        return matches


class ANDCC(ChainedCondition):
    """
    ANDCC: AND Chained Condition
    Return True if all of the conditions matches
    """
    def matches(self, other):
        matches = False
        for condition in self.conditions:
            _matches = condition.matches(other)
            matches = matches and _matches
        return matches


class ComparableElement(dict):
    """
    A comparable element is an object that will be used for making comparissons
    Will
    """
    def __init__(self, **kargs):
        super().__init__(**kargs)

    def matches(self, other):
        for key, comparator in self.items():
            if key not in other or not comparator.matches(other[key]):
                return False
        return True


class Rule(object):
    def __init__(self, *args):
        self.comparables = args

    def __call__(self, original_method):
        def wrapped(instance, other, *args, **kwargs):
            if self.matches(other):
                return original_method(instance, *args, **kwargs)

        return wrapped

    def matches(self, element: ComparableElement):
        return all(comparable.matches(element) for comparable in self.comparables)


class RuleEngine(object):
    def __init__(self):
        self.other = None
        self.rules = self._set_rules()

    def _set_rules(self):
        _rules = []
        callables = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        return [callable for callable in callables if not callable.startswith('_') and callable not in ('declare', 'run')]

    def declare(self, other):
        self.other = other

    def run(self):
        for rule in self.rules:
            getattr(self, rule)(self.other)



class MyRuleEngine(RuleEngine):
    def __init__(self):
        self.candidate_beers = []
        super().__init__()

    @Rule(ComparableElement(color=Condition('blanco')))
    def r1_blanco(self):
        self.candidate_beers.append('cerveza_blanca')

    @Rule(ComparableElement(color=Condition('negro'), amargor=Condition('fuerte')))
    def r2_negro(self):
        self.candidate_beers.append('cerveza_negra')

    @Rule(
        ComparableElement(intensity=Condition("media") | Condition("*")),
        ComparableElement(color=Condition("palido") | Condition("*")),
        ComparableElement(bitterness=Condition("bajo") | Condition("medio") | Condition("*")),
        ComparableElement(hop=Condition("viejo mundo") | Condition("*")),
        ComparableElement(fermentation=Condition("alta") | Condition("*")),
        ComparableElement(yeast=Condition("ale") | Condition("*")),
    )
    def r3_suave(self):
        self.candidate_beers.append('kolsh')


"""
x = Condition("foo") | Condition("aaa") & Condition("bbb")
y = ComparableElement(x='foo', y='baar')

myrule = Rule(ComparableElement(color=Condition('blanco') | Condition('negro') | Condition('fuxia')))

myelement = ComparableElement(color='azul')

result = myrule.matches(myelement)
print(result)
"""

#cmp_1 = ComparableElement(color=Condition('negro'), amargor=Condition('fuerte'))
#cmp_2 = ComparableElement(color='negro', amargor='fuerte')

#assert cmp_1.matches(cmp_2)

"""
eng = MyRuleEngine()
eng.declare(ComparableElement(color='palido', bitterness='bajo', intensity='*', hop='*', fermentation='*', yeast='*'))
eng.run()

eng.declare(ComparableElement(color='AAAA', bitterness='bajo', intensity='*', hop='*', fermentation='*', yeast='*'))
eng.run()
print(f"Cervezas Candidatas: {eng.candidate_beers}")
"""
