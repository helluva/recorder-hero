## Songs

Songs are specified as a list of notes `<note>,<measures>` and rests `rest,<measures>`.

This is basically a CSV representation of sheet music. `<note>` can be any note playable by our recorder (from lower E `e1` to upper C `c3`). `<measures>` is a floating point representation of things like quarter notes `0.25`, eight notes `0.125`, and half notes `0.5`. `rest` indicates a pause.

Notes can also have an additional `,short` signifier that will cause them to be played as a single "puff of air" instead of being sustained until the next note or rest.