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

## Debugger:
