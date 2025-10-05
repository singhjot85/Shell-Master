# Rules / Algo for JQ formatter - Approach devlopment
Algorithm and approach for JQ formatter. Rules would be used to develop an approach, then a pseudocode or algorithm and then final code.

## Parser:
For working with any jq program we need to make sure that its a valid jq program, for that we need to develop a jq parser.  
It will parse the input jq program, convert it into raw string and make it ready for consumption of any program.
1. Take the jq program as a string input.
2. Remove any white-spaces.
3. Remove any newlines.
4. *not sure* Should we remove all special characters??

## Formatter:

### Rules:
1. Find `[], (), {}`
    - newline after open bracket `[`
    - newline before `]`
    - tab before doing this newline
(Replace `[]` with `[\n<indent>\n]`)
2. Exception for 30 chars - skip if the content inside `[]` is <30 chars.
3. `,` -> `<space>,/n`
4. `|` -> `<space>|\n<indent>`
5. For an `if/elif` statement find `then`,`else` and `end` and replace `if<statement>then<statement>else<statement>end` -> `if<space><statement><space>then<newline><statement><newline>else<newline><statement>end`

### Approach
Follow this approach in this sequence only to format the jq program properly.
1. Get an input string and parse it for formatter.
2. find out actual jq program from base level brackets, Ex:
extract jq program from: `({ jq-program }//null)` or `{ jq-program }`.
3. find `,` in the entire jq program and replace with `<space>,/n` this will seperate expressions for us to scan one-by-one. ***not sure how to handle when strings have (,) in them***
4. find `:` and execute formatter for only left side of operator, those would be our tokens for formatting,
    - Save `rate:(.rate_index)//null` as {"rate":"(.rate_index)//null"} and run formatter on each value of hashmap/dict. The value(s) would be our tokens for execution.
5. For each token execute three rules:
    1. `if<statement>then<statement>else<statement>end` -> `if<space><statement><space>then<newline><statement><newline>else<newline><statement>end`.
    3. `[]`or`()`or`{}` -> `[<newline><indent><newline>]` only if chars between brackets are >=30.
    2. `|` -> `<space>|\n<indent>`

## Approach - 2:
High level approach:
1. Break the entire program find `{}, ()` and split in three parts: prefix, root-jq, postfix.
2. Break in tokens for each `{},()` using `: and ,` rule.
3. For each value in tokens run the formatter recursively.

## Approach - 3:
High level approach:
1. Parse to an AST(Abstract Syntax Tree)
    1. Tokenize the given input into keywords, identifiers, literals etc.
    2. Parse the tokens to AST.
2. Walk AST with the rules.
3. Output pretty printed code.
4. [TODO-Req] Handles the comments and whitespace.


## Debugger:
TODO: Develop a debugger to debug the jq, at what line it fails.


## Python Regex (Tutorial):

### Core Functions
- `re.compile(pattern)` → Compile regex for reuse.
- `re.search(pattern, string)` → Find **first** match.
- `re.findall(pattern, string)` → Find **all** matches (list).
- `re.sub(pattern, repl, string)` → Replace matches.
- `re.match(pattern, string)` → Match only at **start** of string.
### Common Regex Tokens
- `\d` → Digit (0–9)  
- `\w` → Word char (letters, digits, underscore)  
- `\s` → Whitespace (space, tab, newline)  
- `.` → Any char except newline  
### Quantifiers
- `+` → One or more  
- `*` → Zero or more  
- `?` → Zero or one  
### Character Sets
- `[abc]` → One of `a`, `b`, `c`  
- `[^abc]` → Not `a`, `b`, or `c`  
- `[0-9]` → Any digit  
- `[a-zA-Z]` → Any letter  
### Anchors
- `^` → Start of string  
- `$` → End of string  


###  Real-World Examples
```python
import re

# Simple
text = "Call me at 9876543210 or 123-456-7890."
phones = re.findall(r"\d{10}|\d{3}-\d{3}-\d{4}", text)
print(phones)  # ['9876543210', '123-456-7890']

# A little Complex
text = "Send to: test.email+alex@domain.co, hello@sub.domain.org"
emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
print(emails)  
# ['test.email+alex@domain.co', 'hello@sub.domain.org']
```
---


## Rough Work:
sbaLoanNumber: .sba_number,
loanStatus: "Is, funded Funded",

Tokenizer No. 1:
```C++
pair<int,int> keyIndices(0,0), valueindices(0,0);
bool isKey=true, isString=true;
map<pair<String,String>> tokens;
for (int i=0, i<s.size(), i++){
    // Handling for strings (just flip the switch)
    if(s[i]=='"') isString= !isString;

    if(s[i]==':'){
        isKey = false;
        keyIndices[1]= i-1;
        valueIndices[0]= i+1;
        tokens.insert({
            s.substr(keyIndices[0],keyIndices[1]),
            ""
        });
    }
    if(s[i]==',' && !isString){
        isKey= true;
        keyIndices[0]= i+1; 
        valueIndices[1]= i-1;
        String key= s.substr(keyIndices[0],keyIndices[1]);
        tokens[key]= s.substr(valueindices[0],valueindices[1]);
    }
}
```
```python
is_key, is_string= (True, False)
key_indices, val_indices= ([0,0],[0,0])
tokens= {}

for i, ch in enumerate(program):
    if ch == '"':
        is_string = not is_string
        continue

    if not is_string:
        if ch == ':':
            is_key = False
            key_indices[1] = i
            key = program[key_indices[0]:key_indices[1]].strip()
            val_indices[0] = i+1

        elif ch == ',':
            is_key = True
            val_indices[1] = i
            tokens[key] = program[val_indices[0]:val_indices[1]].strip()
            key_indices[0] = i+1

if key is not None and val_indices[0] < len(program):
    tokens[key] = program[val_indices[0]:].strip()

```
Problems: break in nested jq's, ex: `{ "a": 1, "b": "x,y", "c": { a: { b: 1 } } }`


