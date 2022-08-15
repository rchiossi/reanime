# ReAnime

Command line tool for finding duplicate anime in big collections.

### Modes

##### Direct
Direct mode will create a title string for the series by stripping common used markers (e.g '[]', 1080p, 720p) and use it to compare againts the generated title for other series found. This mode will find most duplicates

##### Fuzzy
Fuzzy mode will use the same clean title from direct mode but calculate the fuzzy distance between two titles instead of direct comparing them. This mode will find related series, like different seasons from the same series or spin offs.

