import type { Token, TokenType } from './lexer';

export interface ASTNode {
  type: 'CallExpression';
  object: string;
  method: string;
  line: number;
}

export function createParser(tokens: Token[]) {
  let pos = 0;

  function current(): Token {
    return tokens[pos];
  }

  function advance(): Token {
    return tokens[pos++];
  }

  function expect(type: TokenType): Token {
    const token = advance();
    if (token.type !== type) {
      throw new Error(`Expected ${type} but got ${token.type} at line ${token.line}`);
    }
    return token;
  }

  function parseCallExpression(): ASTNode {
    const identifier = expect('IDENTIFIER');
    expect('DOT');
    const method = expect('IDENTIFIER');
    expect('LPAREN');
    expect('RPAREN');

    return {
      type: 'CallExpression',
      object: identifier.value,
      method: method.value,
      line: identifier.line,
    };
  }

  function parse(): ASTNode[] {
    const nodes: ASTNode[] = [];

    while (current().type !== 'EOF') {
      if (current().type === 'NEWLINE') {
        advance();
        continue;
      }

      nodes.push(parseCallExpression());

      if (current().type === 'NEWLINE') {
        advance();
      }
    }

    return nodes;
  }

  return { parse };
}
