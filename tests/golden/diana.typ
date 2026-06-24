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
  title: "Bogini łowów Diana",
  author: none,
  native-lang: "pol",
  foreign-lang: "lat",
  foreign-script: "latn",
)

#TitlePage()

#Lesson(
  date: datetime(year: 2026, month: 6, day: 22),
)[

#Vocabulary[
  - Diana {N f} = Diana
  - dea {N f} = bogini
  - silva {N f} = las; puszcza
]

#Models(title: "Modele")[
  - Diana est dea. = Diana jest boginią.
  - Diana silvas amat. = Diana kocha lasy.
]

#Text(title: "Tekst")[
  Diana est dea silvarum et venationis.
]

#Text(title: "Tłumaczenie")[
  Diana to bogini lasów i łowów.
]

#Questions(title: "Pytania")[
  + Quis est Diana?
]

#Exercise(number: "1")[
  #Instruction[Przetłumacz na polski:]
  - Diana est dea.
  - Diana silvas amat.
]
]

#TableOfContents()
