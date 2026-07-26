## Summary

One or two sentences. What does this PR change and why?

## Motivation

Link the issue this closes (e.g. `Closes #123`), or describe the design problem.

## Type of change

- [ ] Bug fix (glyph rendering, metric, OpenType feature)
- [ ] New glyph
- [ ] Refactor (no visual change)
- [ ] Documentation
- [ ] Breaking change (e.g. re-encodes a glyph, shifts advance width)

## Checklist

- [ ] I have read [CONTRIBUTING.md](../blob/master/CONTRIBUTING.md)
- [ ] `py src/newell/test_generator.py` passes
- [ ] `fontmake` build succeeds (if UFO sources changed)
- [ ] Glyph count and metrics verified
- [ ] README or OFL credit updated if applicable
- [ ] Commits signed
- [ ] **No AI-attribution trailers** (`Co-Authored-By: Claude`, `Generated-by`, etc.)

## Before / after renderings

For any visual change, attach before and after renderings at display size (≥48px) and body size (~16px).

| | Before | After |
| --- | --- | --- |
| Display (≥48px) | attach | attach |
| Body (~16px) | attach | attach |

## Test plan

How did you verify this works? List the build commands run and the viewers used to spot-check.

```sh
$ py src/newell/test_generator.py
$ fontmake -u source/newell-Regular.ufo -o otf
```