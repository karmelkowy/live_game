gra w życie
===========

wymagania:
---------
* python >= 2.7
* biblioteka wxpython (sudo apt-get install python-wxgtk2.8)

funkcje:
---------
* losowe poruszanie się potworków po mapie
* wykrywanie kolizji z innymi potworkami i omijanie się albo rozmnażanie
* potworki mają określoną długość życia (zmienna globalna live)
* można zmienić ilość i zarazem wielkość pojedyńczych pól (zmienna globalna size)
* można określiś kilka innych dodatkowych parametrów na początku kodu
* potworki umierają
* potworki zmieniają kolor w zależności od fazy życia (różowy - dziecko; czerwony, zielony - dorosły; szzart - starzec)
* możliwość zatrzymywania animacji (spacja albo przycisk na dole)
* możliwość zminay ilość cykli na sekundę ( wyrażona w odstępach pomiędzy cyklami w ms)
* prawy klawisz to gumka ( w przyszłości dowolne narzędnie)
* funkcje lewego klawisza wybiera się przez przyciski na dole
* z prawej strony wyświetlają się podstawowe statystyki 
* podział na gridy w których zmienna jest szansa na rozmnożenie
* losowe śmieci w przypodku zbyt dużego zagęszczenia
* można stawiać ściany blokujące ruch
* pędzel ma zmienny rozmiar (scroll albo slider z prawej)
* pędzel ma zmienne krycie  ( slider po prawej ) od 100% dla wartości 0 do 1% dla wartości 100
* wyświetlenie pędzla na panelu

TODO:
--------
* rozwiązać problem z evt_leave_window - odpowiedzialny za znikanie pędzla
* wyprowadzić jeszcze kilka zmiennych na wieszch
* możliwość edycji niektórych zmiennych podczas trwania animacji

* eksport do exe'ka


Dodatkowo:
-----------

* zamiast kolorków jakieś bitmapy
* anomalie?
* klęski?
* zapysywanie i przewijanie symulacji
* "zadania" z ograniczeniami - masz ileś tego ileś tego, zrób kolonie
