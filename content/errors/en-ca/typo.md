# A Field Name With A Typo

This page's own sidecar states `titel` instead of `title`. Nothing above declared a kind for `titel`, so it should be reported as a field with no declared kind, rather than silently treated as a new local field.
