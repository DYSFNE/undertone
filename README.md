# undertone

A build tool that turns a small set of design tokens into a complete,
accessible Obsidian theme.

**Status: early** This repository is the project skeleton. Do not install it.

---

## The idea

Most Obsidian themes are hand-written CSS. A colour is picked, pasted in
several places, and checked by eye. When the palette changes, every value
must be found and edited again, and contrast is never verified.

This project treats the theme as **compiled output**:

```
tokens.toml  ->  undertone  ->  theme.css
```

You define the intent — a base hue, a contrast target, a type scale. The
compiler produces the hundreds of CSS variables Obsidian expects, and it
refuses to emit a theme that fails contrast rules.

## How it will work

| Stage | Input | Output |
|---|---|---|
| Parse | `tokens.toml` | token tree |
| Generate | token tree | OKLCH colour ramps |
| Verify | ramps + pairings | contrast report |
| Emit | verified tokens | `theme.css` |

Colour work is done in OKLCH so that lightness steps are perceptually
even. Contrast is computed, not estimated.

## Install

Not ready. When it is:

```bash
pip install undertone
```

## Usage

Planned interface:

```bash
undertone build tokens.toml -o theme.css
undertone check theme.css
```

## Layout

```
undertone/          package source
tests/              tests
tokens/             example token files
docs/               notes on the design decisions
pyproject.toml      metadata and tool config
```

## Contributing

Commits follow [Conventional Commits](https://www.conventionalcommits.org).
One commit for each logical change.

## Roadmap

- [ ] Token file format
- [ ] OKLCH ramp generation
- [ ] Contrast verification
- [ ] CSS variable emitter
- [ ] Print stylesheet
- [ ] Table and Bases styling

## License

MIT. See [LICENSE](LICENSE).
