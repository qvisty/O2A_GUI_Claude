# Dokumentationsretningslinjer

Formålet med disse filer er at holde Ole løbende orienteret om projektets tilstand, ændringer og beslutninger i et fast og forudsigeligt format.

Retningslinjerne her er udledt af den eksisterende praksis i `docs/`-mappen og skal følges ved fremtidigt arbejde i repoet.

---

## Grundregel

Ved enhver ændring, analyse eller afklaring i projektet skal det vurderes, om `docs/` også skal opdateres. Dokumentation er ikke valgfri sideaktivitet, men en del af leverancen.

Hvis arbejdet efterlader ny viden, et nyt valg, en ny risiko eller en ny status, skal det skrives ned i den relevante fil i `docs/`.

## Filer og formål

### `WORK_LOG.md`

Bruges til en kronologisk arbejdslog.

Opdateres når:

- der er gennemført analysearbejde
- der er lavet kodeændringer
- der er rettet fejl
- der er gennemført refaktorering
- der er afsluttet en afgrænset arbejdssession med ny projektviden

Regler:

- nye indgange tilføjes øverst
- hver indgang dateres
- hver indgang skal kort beskrive hvad der blev gjort, hvad der blev fundet, og hvad det betyder for videre arbejde

### `DECISIONS.md`

Bruges til tekniske beslutninger, som ikke er selvindlysende.

Opdateres når:

- der vælges én løsning frem for en anden
- en arkitektonisk eller teknisk retning fastlægges
- et tradeoff accepteres bevidst
- gammel adfærd bevares eller fjernes af en begrundet årsag

Regler:

- brug stigende beslutningsnumre
- beskriv kontekst, valg, begrundelse, alternativer og konsekvenser
- skriv kun beslutninger der er værd at genfinde senere

### `ISSUES.md`

Bruges til kendte fejl, begrænsninger og teknisk gæld.

Opdateres når:

- en ny fejl identificeres
- en eksisterende fejl får bedre forklaring eller prioritet
- ny teknisk gæld opdages
- en begrænsning dokumenteres som kendt men ikke planlagt rettet nu

Regler:

- beskriv symptom, årsag, berørte filer og planlagt løsning hvis kendt
- vær tydelig om prioritet og konsekvens
- hold fokus på problemer der er relevante for fremtidigt arbejde

### `PROJECT_OVERVIEW.md`

Bruges til den samlede forklaring af systemet til en fremtidig vedligeholder eller bruger, herunder Ole.

Opdateres når:

- systemets faktiske virkemåde ændres
- centrale begrænsninger ændres
- mappestruktur eller aktive komponenter ændres væsentligt
- opsætning eller kørsel ændres

Regler:

- skriv forklarende og ikke kun internt for udviklere
- dokumentet skal kunne læses uden at kende hele kodebasen
- beskriv den aktuelle virkelighed, ikke ønsket fremtidstilstand

## Praktisk arbejdsgang

Efter hver væsentlig opgave skal følgende gennemgås:

1. Skal `WORK_LOG.md` have en ny indgang?
2. Blev der truffet en beslutning som skal i `DECISIONS.md`?
3. Blev der fundet eller ændret et problem som skal i `ISSUES.md`?
4. Har ændringen påvirket forståelsen af systemet i `PROJECT_OVERVIEW.md`?

Hvis svaret er ja til et punkt, opdateres filen som en del af samme arbejde.

## Skriveprincipper

- skriv kort, konkret og genfindeligt
- skriv på dansk som i de eksisterende `docs`-filer
- foretræk forklaring af konsekvenser frem for kun aktivitet
- undgå pynt og generelle formuleringer; dokumentationen skal kunne bruges senere som beslutnings- og vedligeholdelsesgrundlag

## Fremadrettet regel

Fremtidigt arbejde i dette repo skal følge disse retningslinjer, medmindre brugeren udtrykkeligt beder om noget andet.
