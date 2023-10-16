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
from collections import defaultdict


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

    def jsonify(self):
        return {self.value}


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

    def jsonify(self):
        res = set()
        for condition in self.conditions:
            res = res | condition.jsonify()
        return res


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

    def jsonify(self):
        return {key: value.jsonify() for key, value in self.items()}

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
                instance.append_matching_attributes(self.jsonify())
                return original_method(instance, *args, **kwargs)

        return wrapped

    def matches(self, element: ComparableElement):
        return all(comparable.matches(element) for comparable in self.comparables)

    def jsonify(self):
        res = {}
        for comparable in self.comparables:
            res.update(comparable.jsonify())
        return res

class AttributeInfo():
    def __init__(self):
        self.attribute = set({})
        self.attribute_amount = 0

class RuleEngine(object):
    PUB_ATTRS = ('declare', 'reset', 'run', 'append_matching_attributes', 'get_executed_rules_attribute_variance')

    def __init__(self):
        self.other = None
        self.rules = self._set_rules()
        self.matching_attributes = {}

    def reset(self):
        self.other = None
        self.matching_attributes = {}

    def _set_rules(self):
        _rules = []
        callables = [method_name for method_name in dir(self) if callable(getattr(self, method_name))]
        return [callable for callable in callables if not callable.startswith('_') and callable not in self.PUB_ATTRS]

    def append_matching_attributes(self, attributes):
        for key, value_set in attributes.items():
            attributeInfo = self.matching_attributes.get(key, AttributeInfo())
            attributeInfo.attribute = attributeInfo.attribute.union(value_set)
            attributeInfo.attribute_amount += len(value_set)
            self.matching_attributes[key] = attributeInfo

    def get_executed_rules_attribute_variance(self):
        attribute_variance = []
        for key, attributeInfo in self.matching_attributes.items():
            attribute_variance.append((key, attributeInfo.attribute, attributeInfo.attribute_amount))
        return attribute_variance
    
    def declare(self, other):
        self.other = other

    def run(self):
        for rule in self.rules:
            if(getattr(self, rule)(self.other)):
                return
