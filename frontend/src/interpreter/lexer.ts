export const TokenType = {
  IDENTIFIER: 'IDENTIFIER',
  DOT: 'DOT',
  LPAREN: 'LPAREN',
  RPAREN: 'RPAREN',
  NEWLINE: 'NEWLINE',
  EOF: 'EOF',
} as const;

export type TokenType = (typeof TokenType)[keyof typeof TokenType];

export interface Token {
  type: TokenType;
  value: string;
  line: number;
}

export function createLexer(input: string) {
  let pos = 0;
  let line = 1;
  const tokens: Token[] = [];

  function isWhitespace(char: string): boolean {
    return /\s/.test(char);
  }

  function isAlpha(char: string): boolean {
    return /[a-zA-Z_]/.test(char);
  }

  function readIdentifier(): string {
    const start = pos;
    while (pos < input.length && /[a-zA-Z0-9_]/.test(input[pos])) {
      pos++;
    }
    return input.slice(start, pos);
  }

  function tokenize(): Token[] {
    pos = 0;
    line = 1;
    tokens.length = 0;

    while (pos < input.length) {
      const char = input[pos];

      if (isWhitespace(char)) {
        if (char === '\n') {
          tokens.push({ type: TokenType.NEWLINE, value: '\n', line });
          line++;
        }
        pos++;
        continue;
      }

      if (char === '.') {
        tokens.push({ type: TokenType.DOT, value: '.', line });
        pos++;
        continue;
      }

      if (char === '(') {
        tokens.push({ type: TokenType.LPAREN, value: '(', line });
        pos++;
        continue;
      }

      if (char === ')') {
        tokens.push({ type: TokenType.RPAREN, value: ')', line });
        pos++;
        continue;
      }

      if (isAlpha(char)) {
        const identifier = readIdentifier();
        tokens.push({ type: TokenType.IDENTIFIER, value: identifier, line });
        continue;
      }

      throw new Error(`Unexpected character '${char}' at line ${line}`);
    }

    tokens.push({ type: TokenType.EOF, value: '', line });
    return tokens;
  }

  return { tokenize };
}
