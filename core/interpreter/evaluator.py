"""
Expression evaluator for the B-Bot script interpreter.
Evaluates AST expressions including constants, variables, and operations.
"""
import ast
from typing import Any, Dict
from core.interpreter.exceptions import ScriptValidationError
from core.interpreter.data_types import BotList


class ExpressionEvaluator:
    """Evaluates AST expressions to their runtime values."""
    
    def evaluate(self, node: ast.AST, scope: Dict[str, Any]) -> Any:
        """
        Evaluate an AST expression node.
        
        Args:
            node: The AST node to evaluate
            scope: Current variable scope dictionary
            
        Returns:
            The evaluated value (int, bool, etc.)
            
        Raises:
            ScriptValidationError: If evaluation fails
        """
        if isinstance(node, ast.Constant):
            return node.value
        
        elif isinstance(node, ast.Name):
            if node.id in scope:
                return scope[node.id]
            else:
                raise ScriptValidationError(f"Variable '{node.id}' is not defined")
        
        elif isinstance(node, ast.List):
            return self._evaluate_list(node, scope)
        
        elif isinstance(node, ast.Subscript):
            return self._evaluate_subscript(node, scope)
        
        elif isinstance(node, ast.Call):
            return self._evaluate_call(node, scope)
        
        elif isinstance(node, ast.Compare):
            return self._evaluate_comparison(node, scope)
        
        elif isinstance(node, ast.BinOp):
            return self._evaluate_binary_op(node, scope)
        
        elif isinstance(node, ast.BoolOp):
            return self._evaluate_bool_op(node, scope)
        
        elif isinstance(node, ast.UnaryOp):
            return self._evaluate_unary_op(node, scope)
        
        else:
            raise ScriptValidationError(f"Unsupported expression type: {type(node).__name__}")
    
    def _evaluate_list(self, node: ast.List, scope: Dict[str, Any]) -> BotList:
        """
        Evaluate a list literal.
        
        Args:
            node: The AST List node
            scope: Current variable scope dictionary
            
        Returns:
            BotList containing evaluated elements
        """
        items = []
        for elt in node.elts:
            items.append(self.evaluate(elt, scope))
        return BotList(items)
    
    def _evaluate_subscript(self, node: ast.Subscript, scope: Dict[str, Any]) -> Any:
        """
        Evaluate a subscript operation (list indexing).
        
        Args:
            node: The AST Subscript node
            scope: Current variable scope dictionary
            
        Returns:
            Value at the specified index
        """
        value = self.evaluate(node.value, scope)
        
        if not isinstance(value, BotList):
            raise ScriptValidationError("Can only index lists")
        
        # Evaluate the index
        if isinstance(node.slice, ast.Index):  # Python 3.8 and earlier
            index = self.evaluate(node.slice.value, scope)
        elif isinstance(node.slice, ast.Constant):  # Python 3.9+
            index = node.slice.value
        else:
            raise ScriptValidationError("Only constant integer indices are supported")
        
        if not isinstance(index, int):
            raise ScriptValidationError("Index must be an integer")
        
        return value[index]
    
    def _evaluate_call(self, node: ast.Call, scope: Dict[str, Any]) -> Any:
        """
        Evaluate a function call (built-in functions like len).
        
        Args:
            node: The AST Call node
            scope: Current variable scope dictionary
            
        Returns:
            Result of the function call
        """
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            
            # Handle built-in functions
            if func_name == 'len':
                if len(node.args) != 1:
                    raise ScriptValidationError("len() requires exactly 1 argument")
                value = self.evaluate(node.args[0], scope)
                if not isinstance(value, (BotList, list)):
                    raise ScriptValidationError("len() requires a list")
                return len(value)
            
            elif func_name == 'append':
                # This is a method call, should be handled differently
                raise ScriptValidationError("append() is a method, use list.append(value)")
        
        raise ScriptValidationError(f"Unsupported function call: {func_name}")
    
    def _evaluate_comparison(self, node: ast.Compare, scope: Dict[str, Any]) -> bool:
        """
        Evaluate a comparison expression.
        
        Args:
            node: The AST Compare node
            scope: Current variable scope dictionary
            
        Returns:
            Boolean result of the comparison
        """
        left = self.evaluate(node.left, scope)
        
        for op, comparator in zip(node.ops, node.comparators):
            right = self.evaluate(comparator, scope)
            
            if isinstance(op, ast.Eq):
                result = left == right
            elif isinstance(op, ast.NotEq):
                result = left != right
            elif isinstance(op, ast.Lt):
                result = left < right
            elif isinstance(op, ast.LtE):
                result = left <= right
            elif isinstance(op, ast.Gt):
                result = left > right
            elif isinstance(op, ast.GtE):
                result = left >= right
            else:
                raise ScriptValidationError(f"Unsupported comparison operator: {type(op).__name__}")
            
            # For chained comparisons, use the right value as the next left
            left = right
            
            # If any comparison is False, the whole chain is False
            if not result:
                return False
        
        return True
    
    def _evaluate_binary_op(self, node: ast.BinOp, scope: Dict[str, Any]) -> Any:
        """
        Evaluate a binary operation (arithmetic).
        
        Args:
            node: The AST BinOp node
            scope: Current variable scope dictionary
            
        Returns:
            Result of the operation
        """
        left = self.evaluate(node.left, scope)
        right = self.evaluate(node.right, scope)
        
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ScriptValidationError("Division by zero")
            return left // right  # Integer division
        elif isinstance(node.op, ast.Mod):
            if right == 0:
                raise ScriptValidationError("Modulo by zero")
            return left % right
        else:
            raise ScriptValidationError(f"Unsupported binary operator: {type(node.op).__name__}")
    
    def _evaluate_bool_op(self, node: ast.BoolOp, scope: Dict[str, Any]) -> bool:
        """
        Evaluate a boolean operation (and/or).
        
        Args:
            node: The AST BoolOp node
            scope: Current variable scope dictionary
            
        Returns:
            Boolean result of the operation
        """
        if isinstance(node.op, ast.And):
            # Short-circuit evaluation
            for value in node.values:
                if not self.evaluate(value, scope):
                    return False
            return True
        
        elif isinstance(node.op, ast.Or):
            # Short-circuit evaluation
            for value in node.values:
                if self.evaluate(value, scope):
                    return True
            return False
        
        else:
            raise ScriptValidationError(f"Unsupported boolean operator: {type(node.op).__name__}")
    
    def _evaluate_unary_op(self, node: ast.UnaryOp, scope: Dict[str, Any]) -> Any:
        """
        Evaluate a unary operation (not, -).
        
        Args:
            node: The AST UnaryOp node
            scope: Current variable scope dictionary
            
        Returns:
            Result of the operation
        """
        operand = self.evaluate(node.operand, scope)
        
        if isinstance(node.op, ast.Not):
            return not operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise ScriptValidationError(f"Unsupported unary operator: {type(node.op).__name__}")
