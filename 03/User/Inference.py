from typing import List

from ExpertSystem.Business.UserFramework import IInference, ActionBaseCaller
from ExpertSystem.Structure.Enums import LogicalOperator, Operator
from ExpertSystem.Structure.RuleBase import Rule, Fact, ExpressionNode, Expression


class Inference(IInference):
    """
    | User definition of the inference. You can define here you inference method (forward or backward).
      You can have here as many functions as you want, but you must implement interfere with same signature

    |
    | `def interfere(self, knowledge_base: List[Fact], rules: List[Rule], action_base: ActionBase):`
    |

    | Method `interfere` will be called each turn or manually with `Inference` button.
    | Class have no class parameters, you can use only inference parameters

    """
    knowledge_base: List[Fact]
    action_base: ActionBaseCaller
    unc = []
    op = None

    def infere(self, knowledge_base: List[Fact], rules: List[Rule], action_base: ActionBaseCaller) -> None:
        """
        User defined inference

        :param knowledge_base: - list of Fact classes defined in  KnowledgeBase.create_knowledge_base()
        :param rules:  - list of rules trees defined in rules file.
        :param action_base: - instance of ActionBaseCaller for executing conclusions

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!    TODO: Write implementation of your inference mechanism definition HERE    !!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        """
        self.knowledge_base = knowledge_base
        self.action_base = action_base
        evall = 0.38

        for rule in rules:
            condition = self.rule_evaluation(rule.condition)
            print(condition)
            if rule.uncertainty:
                uncertainty = rule.uncertainty
            else:
                uncertainty = 1
            if self.op == LogicalOperator.AND and uncertainty and len(self.unc):
                uncertainty *= min(self.unc)
            elif self.op == LogicalOperator.OR and uncertainty and len(self.unc):
                uncertainty *= max(self.unc)

            if condition and uncertainty and uncertainty >= evall:
                self.conclusion_evaluation(rule.conclusion)
                self.unc.clear()
                break
            elif condition and not rule.uncertainty:
                self.conclusion_evaluation(rule.conclusion)
                self.unc.clear()
                break


    def rule_evaluation(self, root_node: ExpressionNode) -> float:
        """
        Example of rule tree evaluation. This implementation did not check comparision operators and uncertainty.
        For usage in inference extend this function

        :param root_node: root node of the rule tree
        :return: True if rules is satisfiable, False in case of not satisfiable or missing Facts
        """

        if root_node.operator == LogicalOperator.AND:
            left = self.rule_evaluation(root_node.left)
            right = self.rule_evaluation(root_node.right)
            self.op = LogicalOperator.AND
            return left and right


        elif root_node.operator == LogicalOperator.OR:
            left = self.rule_evaluation(root_node.left)
            right = self.rule_evaluation(root_node.right)
            self.op = LogicalOperator.OR
            return left or right

        elif root_node.operator == Operator.MORE_THEN:
            left = self.rule_evaluation(root_node.left)
            right = self.rule_evaluation(root_node.right)
            return left > right


        elif isinstance(root_node.value, Expression):
            if root_node.value.uncertainty:
                print(f'Expression {root_node.value.name} has {root_node.value.uncertainty} uncertainty')
                self.unc.append(root_node.value.uncertainty)
            try:
                return self.knowledge_base[self.knowledge_base.index(root_node.value.name)](*root_node.value.args)
            except ValueError:
                return False

        else:
            return bool(root_node.value)

    def conclusion_evaluation(self, root_node: ExpressionNode):
        if self.action_base.has_method(root_node.value):
            self.action_base.call(root_node.value)
