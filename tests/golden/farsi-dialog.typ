#import "@local/dpurge-langnote:0.0.1": (
  LangNote,
  Lesson,
  Vocabulary,
  Models,
  Text,
  Dialog,
  Questions,
  Exercise,
  Instruction,
  TitlePage,
  TableOfContents,
)

#show: LangNote.with(
  title: "Krótka rozmowa",
  author: none,
  native-lang: "pol",
  foreign-lang: "fas",
  foreign-script: "arab",
)

#TitlePage()

#Lesson(
  date: datetime(year: 2026, month: 7, day: 4),
)[

#Vocabulary[
  - خانه {N} [xāne] = dom
  - کجا {Pron} [kojā] = dokąd; gdzie
]

#Models(title: "Modele")[
  - سلام [salām] = cześć
  - اسم من … است [esm-e man … ast] = moje imię to …
]

#Dialog(title: "Krótka rozmowa")[
  - Dwoje znajomych spotyka się na ulicy.
  - Aḥmad: Marḥabā! Kayfa ḥāluka?
  - Sārah: Ahlan wa-sahlan.
  - — Pauza w tle.
]

#Text(title: "Transkrypcja")[
  Aḥmad: Marḥabā! Sārah: Ahlan wa-sahlan.
]

#Dialog(title: "Tłumaczenie")[
  - Dwoje znajomych spotyka się na ulicy.
  - Ahmad: Cześć! Jak się masz?
  - Sara: Witam serdecznie.
  - — Pauza w tle.
]
]

#TableOfContents()
