## What is Brand?

Brand takes strings as input and evaluates control sequences, replacing them with the result of that evaluation, which often includes LaTeX macros. Control sequences are denoted with square braces. For example, using brand to evaluate `"Roll some dice! [roll 2 6 1]"` would return `"Roll some dice! 8 (2d6 + 1)"`, or `"Make this [bold BOLD!]"` would return `"Make this \textbf{BOLD!}"`.

## What is it Good For?

I originally needed brand to perform arithmetic in ways that LaTeX could not, for example calculating the average result of 2d6 + 1. From there, I expanded it to be something closer to an interface for LaTeX, with commands that simulate LaTeX macros like \textbf or \enumerate.

I currently use it as part of a workflow that turns YAML files into LaTeX, allowing me to separate my data from the data formatting (to some extent).

## How do I Use It?

First, you have to aquire a copy of the program. There is currently a "core" module that contains all the essential functions and a "5e" module that has additional functions that are specifically for creating fifth edition Dungeons & Dragons monster stat blocks. In the releases, there is a file for each module. You can also clone this repository and run the brand_compiler.py file, which will allow you to choose a module to compile.

Once you have a copy of the file, you can include it in a python project and use it to evaluate strings by calling the `eval_string(string, params)` function.

The eval_string function has two parameters: the first one is the string to evaluate, and the second is a dictionary of variables for brand to use. The dictionary is in the form `{"variable name":"value"}`.

### Brand Function Calling
Brand commands are contained in square brackets, and the arguments are separated by spaces. The first word in a command is the function to execute; for example, `[bold this text]` calls the "bold" function with the "this" and "text" arguments. Angular braces or the `[bind *stuff]` command group separate arguments into a single argument.

### Brand Variables
Variables are denoted by the variable name surrounded with square brackets. The actual variable names and associated values are stored in the dictionary passed to the eval_string function. For example, `brand.eval_string("The variable foo is equal to [foo]", {"foo":3})` evaluates to `"The variable foo is equal to 3"`.

Brand has an AUTOMATIC_VARIABLES variable, which is a list of variable names. A variable name that is in AUTOMATIC_VARIABLES is always replaced with its value, even if it is not in square brackets. However, variables are only replaced this way when inside of another command. For example, if "dex" is in AUTOMATIC VARIABLES, `brand.eval_string("dex bonus is equal to [format_bonus dex].", {"dex":2})` evaluates to `dex bonus is equal to +2.`

## Functions

### Core Module

**[articulate capitalize \*name]**\
Returns name with the proper indefinite article. If capitalize is true, the article will be capitalized.\
`[articulate True Alex G.]` -> `An Alex G.`\
`[articulate False goblin]` -> `a goblin`

**[bind \*stuff]**\
Returns the arguments wrapped in angular brackets, making brand treat them as a single argument.\
`[bind this text]` -> `<this text>`

**[bold \*stuff]**\
Returns the arguments wrapped in a \textbf LaTeX macro.\
`[bold my text]` -> `\textbf{my text}`

**[bolditalics \*stuff]**\
the function works in the same way as the `[bold]` command, but makes the text bold and italic instead.

**[bulletlist \*entries]**\
Each entry must be separated by an ampersand. Returns the entries as a LaTeX bulleted list.\
`[bulletlist entry 1 & entry 2]` -> `\\ \begin{itemize} \item entry 1 \item entry 2 \end{itemize}`

**[dicetable size title \*entries]**\
Each entry must be separated by an ampersand. Returns a LaTeX table relating the roll of a die to the entries.\
`[dicetable 4 Result result 1 & result 2 & result 3 & result 4]` -> \
`\bigskip\begin{tabularx}{0.8\columnwidth}{|c|X|} \hline 1d4 & Result \\ [2pt]\hline 1 & result 1 \\ [2pt]\hline 2 & result 2 \\ [2pt]\hline 3 & result 3 \\ [2pt]\hline 4 & result 4 \\\hline\end{tabularx}`

**[format_bonus bonus]**\
Returns the bonus with the proper +/- annotation.\
`[format_bonus 10]` -> `+10`\
`[format_bonus -5]` -> `-5`

**[format_index index]**\
Returns the index with the proper ordinary suffix.\
`[format_index 2]` -> `2nd`\
`[format_index 5]` -> `5th`

**[include type filename]**\
This function relies on the `include_functions` global parameter, which is a dictionary of the form `{type:lambda function}`. Each function must accept one argument. When this function is evaluated, if the `type` parameter is in the include_functions dictionary, it calls the associated function with the `filename` argument and returns the result within a \quote section.

`include_functions["mytest"] = lambda filename : "filename is " + filename`\
`[include mytest go/to/marz]` -> `\begin{quote} filename is go/to/marz \end{quote}`

**[italics \*stuff]**\
This function works in the same way as the `[bold]` command, but makes the text italic instead of bold.

**[monster \*name]**\
Returns the name wrapped in a \textbf macro. This function is used to make sure the formatting of monster names remains consistent throughout a body of work, and can or should be modified by the user.\
`[monster goblin facehaver]` -> `\textbf{goblin facehaver}`

**[numberlist \*entries]**\
This function works in the same way as the `[bulletlist]` command, but uses the enumerate environment to create a numbered list.

**[possessive \*name]**\
Returns the name with the proper possessive ending.\
`[possessive Steve Jones]` -> `Steve Jones'`\
`[possessive grobblink]` -> `grobblink's`

**[roll num size \*bonuses]**\
Returns the average value followed by the dice rolled in parentheses. The function does not require bonuses.\
`[roll 1 6]` -> `3 (1d6)`\
`[roll 2 4 3]` -> `8 (2d4 + 3)`

**[spell \*name]**\
This function is used in the same way as the `[monster]` function, but makes the text italic by default instead of bold.\
`[spell Magic Missile]` -> `\textit{Magic Missile}`

**[sum \*numbers]**\
Returns the sum of all arguments.\
`[sum 2 10 5]` -> `17`

**[table cols \*entries]**\
The first argument specifies the columns of the table (same as the LaTeX tabular environment, but the vertical lines are automatically entered). If there are any X columns, the tabularx environment is used instead with a width of `0.8\columnwidth`. The rest of the arguments form the table entries, which must be separated by ampersands.\
`[table cc Number & Meaning & 12 & 12 is a pretty good number]` ->
`\bigskip\begin{tabular}{|c|c|}\hline Number & Meaning \\ [2pt]\hline 12 & 12 is a pretty good number \\ \hline\end{tabular}`