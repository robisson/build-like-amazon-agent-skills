# Links Fixture — A

A link that does not resolve: [missing page](./nope.md). Expect
`FALHA [link-broken]` and exit 1.

A link that does resolve, to prove the walker is not simply failing everything:
[the sibling](sub/b.md).

A link the checker must ignore: [the homepage](https://example.invalid/), a
[mail link](mailto:nobody@example.invalid) and a [pure fragment](#links-fixture--a).

A target inside a code span must not be checked: `[not a link](./also-nope.md)`.
