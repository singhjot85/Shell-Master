def repeat(str; n):
    if n <= 0 then
        ""
    else
        str + repeat(
            str;
            n - 1
        )
    end;

def nested(level):
    if level == 0 then
        {value: "end"}
    else
        {
            level: level,
            child: nested(
                level - 1
            ),
            array: [
                range(0; level)
            ],
            object: {
                key1: "value1",
                key2: level,
                key3: [true, false, null]
            }
        }
    end;

def conditional_test(x):
    if x < 0 then
        "negative"
    elif x == 0 then
        "zero"
    elif x < 10 then
        "small"
    else
        "large"
    end;

{
    meta: {
        name: "JQ Pretty Printer Test",
        version: "1.0",
        description: "Complex JSON structure",
        timestamp: now
    },
    simple_values: {
        string: "hello world",
        number: 12345,
        float: 123.456,
        boolean_true: true,
        boolean_false: false,
        null_value: null
    },
    arrays: {
        empty: [],
        numbers: [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10
        ],
        mixed: [
            1,
            "two",
            true,
            null,
            {a: 1}
        ],
        nested_arrays: [
            [1, 2],
            [3, 4],
            [
                5,
                [6, 7]
            ]
        ]
    },
    objects: {
        empty: {},
        simple: {a: 1, b: 2},
        nested: {
            a: {
                b: {
                    c: {d: "deep"}
                }
            }
        }
    },
    generated_nested: nested(5),
    conditions: [
        conditional_test(-1),
        conditional_test(0),
        conditional_test(5),
        conditional_test(20)
    ],
    repeated_strings: [
        repeat("a"; 1),
        repeat("b"; 2),
        repeat("c"; 3),
        repeat("d"; 4),
        repeat("e"; 5)
    ],
    large_array: [
        range(0; 50)
    ],
    matrix: [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ],
    edge_cases: {
        empty_string: "",
        large_number: 123456789012345678901234567890,
        special_chars: "!@#$%^&*()_+-=[]{}|;":,.<>/?"
    },
    deep_mix: {
        a: [
            {
                b: [1, 2, 3]
            },
            {
                c: {
                    d: [
                        4,
                        5,
                        {e: "test"}
                    ]
                }
            }
        ]
    },
    booleans: [
        true,
        false,
        true,
        false
    ],
    nulls: [null, null, null],
    alternating: [
        {id: 1, val: "a"},
        {id: 2, val: "b"},
        {id: 3, val: "c"}
    ],
    computation: {
        squares: [
            range(0; 10)
            | . * .
        ],
        evens: [
            range(0; 20)
            | select(
                . % 2 == 0
            )
        ],
        odds: [
            range(0; 20)
            | select(
                . % 2 == 1
            )
        ]
    },
    flatten_test: [
        [1, 2],
        [3, 4],
        [5, 6]
    ]
    | flatten,
    map_test: [
        1,
        2,
        3,
        4,
        5
    ]
    | map(
        . * 10
    ),
    reduce_test: [
        1,
        2,
        3,
        4,
        5
    ]
    | reduce .[] as $i (
        0;
        . + $i
    ),
    sort_test: [
        5,
        3,
        1,
        4,
        2
    ]
    | sort,
    reverse_test: [
        1,
        2,
        3,
        4,
        5
    ]
    | reverse,
    tostring_test: 12345
    | tostring,
    tonumber_test: "6789"
    | tonumber
}