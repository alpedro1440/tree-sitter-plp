; Kata kunci logika dan operator pencarian
["and" "or" "not" "in" "contains"] @keyword

; Operator perbandingan
["=" "!=" ">" "<" ">=" "<="] @operator

; Literal
(string) @string
(number) @number
(boolean) @constant.builtin

; Nama field pada setiap bentuk ekspresi
(comparison field: (identifier) @property)
(in_expression field: (identifier) @property)
(contains_expression field: (identifier) @property)
