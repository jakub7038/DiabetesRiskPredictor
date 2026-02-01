export interface Persona {
  id: string;
  name: string;
  model: string;
  title: string;
  description: string;
  strengths: string[];
  whenToListen: string;
  limitations: string;
}

export const ML_PERSONAS: Record<string, Persona> = {
  logistic: {
    id: 'logistic',
    name: 'Dr. Andrzej',
    model: 'Regresja Logistyczna',
    title: 'Głos rozsądku',
    description: 'Jest tym lekarzem, który zawsze trzyma się sprawdzonych procedur i medycznych podręczników. Nie szuka dziury w całym, bo uważa, że najważniejsze sygnały są zawsze widoczne gołym okiem. Jednak trzeba pamiętać, że jego podejście liniowe może przeoczyć subtelne, nieliniowe wzorce ukryte w danych pacjenta.',
    strengths: [
      'Dba o to, żeby wyniki nie były przekombinowane.',
      'Jeśli pacjent ma świetne wyniki, pilnuje, by kolumna „Brak cukrzycy" była solidnie wypełniona.',
      'Jest fundamentem zespołu - udziela jasnych, bezpośrednich odpowiedzi, które można wytłumaczyć pacjentowi.'
    ],
    whenToListen: 'Gdy szukasz jasnej odpowiedzi: „Dlaczego wynik jest taki, a nie inny?". Ale jeśli pozostali lekarze mocno się z nim nie zgadzają - może przeoczyć złożone wzorce.',
    limitations: 'W niektórych przypadkach może nie uchwycić całego obrazu. Zawsze warto porównać z innymi opinami.'
  },
  random_forest: {
    id: 'random_forest',
    name: 'Dr. Jolanta',
    model: 'Random Forest',
    title: 'Głos cierpliwości',
    description: 'To lekarka, która nigdy nie wydaje diagnozy w pośpiechu. Jej siła drąży w tym, że potrafi spojrzeć na pacjenta z tysiąca różnych stron jednocześnie i wyciągnąć z tego średnią. Jej ostrożność - rozkład wyników „po równo" gdy dane są niepewne - jest w rzeczywistości zaletą w medycynie, gdzie przesada pewności może nikomu nie pomóc.',
    strengths: [
      'Dba o stabilność wyników - nie daje falsywych nadziei ani niepotrzebnych alarmów.',
      'Jej procenty w kolumnach „Zdrowy", „Przedcukrzyca" i „Cukrzyca" rzadko skaczą gwałtownie - można jej ufać.',
      'Jeśli dane są niepewne, uczciwą pokazuje niepewność - to właśnie czego pragnie lekarz w klinice.'
    ],
    whenToListen: 'Gdy dane pacjenta są niekompletne lub chaotyczne – ona się w tym nie zgubi. Jej ostrożność to zaleta, nie wada.',
    limitations: 'Jej podejście bywa bardzo ostrożne. Czasami może być zbyt konserwatywna w swoich wnioskach.'
  },
  gradient_boost: {
    id: 'gradient_boost',
    name: 'Dr. Paweł',
    model: 'Gradient Boosting',
    title: 'Głos intuicji',
    description: 'Jest tym lekarzem, który siedzi nad wynikami po godzinach, bo lubi wyłapywać subtelne wzorce. Nie jest lepszy od reszty – jest po prostu bardziej dociekliwy tam, gdzie inni widzą tylko statystykę. Jego złożoność ma cenę: trudniej wytłumaczyć pacjentowi dlaczego mówi to co mówi, ale kiedy ma rację, to naprawdę ma rację.',
    strengths: [
      'Dba o detale i wyłapuje subtelne wzorce, które pozostali mogą przeoczyć.',
      'Potrafi „wyczuć" ryzyko u kogoś, kto na pierwszy rzut oka wygląda na zdrowego, ale ma specyficzny zestaw objawów.',
      'Doskonały w identyfikacji bardzo wczesnych sygnałów choroby - jego precyzja w brzegowych przypadkach nie ma równych.'
    ],
    whenToListen: 'Gdy zależy Ci na wyłapaniu bardzo wczesnych sygnałów choroby. Ale jeśli on samotnie się wyróżnia - zweryfikuj wynik, bo może zawyżyć ocenę ryzyka.',
    limitations: 'Jego wyniki mogą być trudne do interpretacji. Warto sprawdzić jego rekomendacje z perspektywą pozostałych opinii.'
  }
};
