{"kind":"deck","format":"deez.nut","version":2,"name":"Zig Basics"}
{"kind":"note","note_type":"basic","fields":["What is Zig?","A general-purpose systems programming language focused on robustness, optimality, and maintainability."],"tags_json":"[\"zig\",\"basics\"]"}
{"kind":"note","note_type":"basic","fields":["What does `comptime` mean in Zig?","The value or code is evaluated at compile time rather than runtime."],"tags_json":"[\"zig\",\"comptime\"]"}
{"kind":"note","note_type":"reverse","fields":["Zig optional type syntax","`?T`"],"tags_json":"[\"zig\",\"types\"]"}
{"kind":"note","note_type":"reverse","fields":["Zig error union syntax","`E!T` or `!T` when the error set is inferred"],"tags_json":"[\"zig\",\"errors\"]"}
{"kind":"note","note_type":"basic","fields":["What does `try` do in Zig?","It unwraps a successful error union value, or returns the error from the current function."],"tags_json":"[\"zig\",\"errors\"]"}
{"kind":"note","note_type":"basic","fields":["What does `catch` do in Zig?","It handles the error case of an error union expression."],"tags_json":"[\"zig\",\"errors\"]"}
{"kind":"note","note_type":"basic","fields":["What does `defer` do in Zig?","It schedules an expression to run when the current scope exits."],"tags_json":"[\"zig\",\"control-flow\"]"}
{"kind":"note","note_type":"basic","fields":["What does `errdefer` do in Zig?","It schedules cleanup that runs only when the current scope returns an error."],"tags_json":"[\"zig\",\"errors\"]"}
{"kind":"note","note_type":"reverse","fields":["Zig slice syntax","`[]T`"],"tags_json":"[\"zig\",\"types\"]"}
{"kind":"note","note_type":"reverse","fields":["Zig single-item pointer syntax","`*T`"],"tags_json":"[\"zig\",\"types\"]"}
{"kind":"note","note_type":"basic","fields":["What does `@This()` return in Zig?","The innermost container type in which the builtin is evaluated."],"tags_json":"[\"zig\",\"types\"]"}
{"kind":"note","note_type":"cloze","fields":["Zig uses {{c1::explicit allocators}} instead of hiding memory allocation behind a global allocator.","Memory management"],"tags_json":"[\"zig\",\"memory\"]"}
