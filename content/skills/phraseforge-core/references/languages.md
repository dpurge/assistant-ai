# Language and script codes

`lang` is **ISO 639-3** (3 letters, lowercase).
`script` is **ISO 15924** (4 letters, lowercase).

## Common languages used in the repo

| Language    | `lang` | Default `script` |
| ----------- | ------ | ---------------- |
| Polish      | `pol`  | `latn`           |
| English     | `eng`  | `latn`           |
| German      | `deu`  | `latn`           |
| Spanish     | `spa`  | `latn`           |
| French      | `fra`  | `latn`           |
| Italian     | `ita`  | `latn`           |
| Portuguese  | `por`  | `latn`           |
| Dutch       | `nld`  | `latn`           |
| Romanian    | `ron`  | `latn`           |
| Czech       | `ces`  | `latn`           |
| Hungarian   | `hun`  | `latn`           |
| Finnish     | `fin`  | `latn`           |
| Swedish     | `swe`  | `latn`           |
| Norwegian   | `nor`  | `latn`           |
| Danish      | `dan`  | `latn`           |
| Lithuanian  | `lit`  | `latn`           |
| Indonesian  | `ind`  | `latn`           |
| Vietnamese  | `vie`  | `latn`           |
| Turkish     | `tur`  | `latn`           |
| Swahili     | `swa`  | `latn`           |
| Esperanto   | `epo`  | `latn`           |
| Latin       | `lat`  | `latn`           |
| Russian     | `rus`  | `cyrl`           |
| Ukrainian   | `ukr`  | `cyrl`           |
| Bulgarian   | `bul`  | `cyrl`           |
| Serbian     | `srp`  | `cyrl`           |
| Mongolian   | `mon`  | `cyrl`           |
| Kazakh      | `kaz`  | `cyrl`           |
| Uzbek       | `uzb`  | `cyrl`           |
| Tatar       | `tat`  | `cyrl`           |
| Tajik       | `tgk`  | `cyrl`           |
| Greek       | `ell`  | `grek`           |
| Ancient Greek | `grc` | `grek`          |
| Arabic      | `arb`  | `arab`           |
| Persian     | `fas`  | `arab`           |
| Uyghur      | `uig`  | `arab`           |
| Hebrew      | `heb`  | `hebr`           |
| Yiddish     | `yid`  | `hebr`           |
| Mandarin (Simplified)  | `cmn` | `hans` |
| Mandarin (Traditional) | `cmn` | `hant` |
| Japanese    | `jpn`  | `jpan`           |
| Korean      | `kor`  | `kore`           |
| Hindi       | `hin`  | `deva`           |

## Scripts supported by the components

Recognized script codes (must be one of these, in lowercase):
`latn`, `cyrl`, `grek`, `arab`, `hans`, `hant`, `hebr`, `kore`,
`jpan`, `armn`, `geor`, `syrc`, `mong`.

Unknown scripts will not get correct direction / sizing — pick the
nearest match.

## Right-to-left scripts

`arab`, `hebr`, `syrc` render right-to-left. The components handle
this automatically — you just set `script` correctly.

## Scripts that need a transcription section

Any script other than `latn`, `cyrl`, `grek`. The exact romanization system
(e.g. DIN 31635 for Arabic, Hanyu Pinyin for Mandarin, Hepburn for Japanese,
Revised Romanization for Korean) is specified by the matching
`phraseforge-lang-<iso>` skill.
