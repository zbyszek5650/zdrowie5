import streamlit as st
import pandas as pd

# Aktywacja Dark Mode (wymaga ustawienia w konfiguracji Streamlit, ale tutaj symulujemy to przez CSS i odpowiednie formatowanie)
st.set_page_config(page_title="Sztab Kryzysowy", layout="wide", page_icon="🚨")

# --- CUSTOM CSS DLA DARK MODE I KART KPI ---
st.markdown("""
    <style>
    /* Ukrycie standardowego górnego paska i stopki */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Stylizacja sekcji nagłówka i przycisku */
    .header-bar {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 8px;
        border-bottom: 2px solid #333;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    /* Stylizacja Kart KPI */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 15px;
        margin-bottom: 30px;
    }
    .kpi-card {
        background-color: #262730;
        border: 1px solid #444;
        border-radius: 8px;
        padding: 15px;
        flex: 1;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .kpi-title {
        font-size: 14px;
        font-weight: bold;
        color: #A0AEC0;
        text-transform: uppercase;
        margin-bottom: 5px;
    }
    .kpi-status-green { color: #48BB78; font-weight: bold; font-size: 18px; margin-bottom: 10px;}
    .kpi-status-yellow { color: #ECC94B; font-weight: bold; font-size: 18px; margin-bottom: 10px;}
    .kpi-status-red { color: #F56565; font-weight: bold; font-size: 18px; margin-bottom: 10px; animation: blinker 1s linear infinite;}
    
    @keyframes blinker {
      50% { opacity: 0; }
    }
    
    .progress-bg {
        background-color: #4A5568;
        border-radius: 4px;
        height: 12px;
        width: 100%;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
    }
    
    /* Stylizacja Sekcji Raportu Sytuacyjnego */
    .sitrep-box {
        background-color: #1A202C;
        border-left: 5px solid #3182CE;
        padding: 20px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 20px;
        font-size: 18px;
        line-height: 1.6;
    }
    .sitrep-title {
        color: #63B3ED;
        font-weight: bold;
        text-transform: uppercase;
        margin-bottom: 10px;
        font-size: 14px;
    }
    
    /* Stylizacja Alertów */
    .alert-box {
        background-color: #2D3748;
        border: 1px solid #DD6B20;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 30px;
        color: #E2E8F0;
    }
    .alert-title {
        color: #DD6B20;
        font-weight: bold;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    /* Stylizacja Sekcji Decyzyjnej */
    .decision-header {
        border-bottom: 2px solid #4A5568;
        padding-bottom: 10px;
        margin-bottom: 20px;
        color: #E2E8F0;
        font-size: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- STAN GRY ---
@st.cache_resource
def get_game_state():
    return {
        "round": 0, 
        "teams": {}, 
        "active_scenario": "Wariant A: Ransomware i paraliż HIS (3 Rundy)" 
    }

state = get_game_state()

# --- BAZA SCENARIUSZY (5 WARIANTÓW) ---
ALL_SCENARIOS = {
    "Wariant A: Ransomware i paraliż HIS (3 Rundy)": {
        1: {
            "title": "🔴 FAZA OPERACYJNA: ETAP 1 - PIERWSZE SYMPTOMY INFEKCJI",
            "desc": "Godzina 14:00. Lekarze na Szpitalnym Oddziale Ratunkowym (SOR) zgłaszają znaczne spowolnienie systemu HIS. Na komputerach w rejestracji pojawiły się **czarne ekrany**. Tłum w poczekalni gęstnieje.",
            "questions": {
                "IT": {
                    "label": "ZESPÓŁ IT / CYBERBEZPIECZEŃSTWO:",
                    "options": {
                        "Natychmiastowe odcięcie SOR od głównej sieci (Prewencyjny Blackout)": {"pat": 0, "avl": -20, "fin": -5, "comp": +10},
                        "Analiza logów w tle i zdalny restart stacji roboczych": {"pat": -10, "avl": +5, "fin": 0, "comp": -10},
                    }
                },
                "Med": {
                    "label": "PION MEDYCZNY:",
                    "options": {
                        "Wdrożenie procedury 'Downtime': pełne przejście na dokumentację papierową": {"pat": +15, "avl": 0, "fin": -5, "comp": +10},
                        "Wstrzymanie wypisów i przyjęć planowych do czasu powrotu systemu": {"pat": -15, "avl": 0, "fin": -15, "comp": -5},
                    }
                },
                "Dir": {
                    "label": "SZTAB ZARZĄDZAJĄCY (DYREKCJA):",
                    "options": {
                        "Powiadomienie Centrum e-Zdrowia (CeZ) o potencjalnym zagrożeniu krytycznym": {"pat": 0, "avl": 0, "fin": 0, "comp": +15},
                        "Brak eskalacji. Zespół czeka na wewnętrzną diagnozę techniczną": {"pat": 0, "avl": 0, "fin": 0, "comp": -15},
                    }
                }
            }
        },
        2: {
            "title": "🔴 FAZA OPERACYJNA: ETAP 2 - ŻĄDANIE OKUPU I STAN WYJĄTKOWY",
            "desc": "Godzina 16:30. Diagnoza potwierdzona: atak Ransomware na bazy danych pacjentów. **Żądanie 50 Bitcoinów.** Brak wyników z laboratorium, brak dawek leków na oddziałach.",
            "questions": {
                "IT": {
                    "label": "ZESPÓŁ IT / CYBERBEZPIECZEŃSTWO:",
                    "options": {
                        "Twardy reset i odcięcie zasilania serwerów, wezwanie CERT Polska": {"pat": -10, "avl": -30, "fin": -10, "comp": +25},
                        "Próba odzyskania danych z porannych kopii bez zrywania połączeń sieciowych": {"pat": -25, "avl": -10, "fin": -20, "comp": -20},
                    }
                },
                "Med": {
                    "label": "PION MEDYCZNY:",
                    "options": {
                        "Przekierowanie karetek do innych placówek, wypisywanie pacjentów w stanie stabilnym": {"pat": +20, "avl": 0, "fin": -20, "comp": +10},
                        "Próba kontynuacji leczenia 'na ślepo' bazując wyłącznie na wywiadzie ustnym": {"pat": -40, "avl": 0, "fin": 0, "comp": -30},
                    }
                },
                "Dir": {
                    "label": "SZTAB ZARZĄDZAJĄCY (DYREKCJA):",
                    "options": {
                        "Kategoryczna odmowa negocjacji. Powołanie sztabu kryzysowego z Policją": {"pat": 0, "avl": 0, "fin": +10, "comp": +20},
                        "Nawiązanie tajnego kontaktu z napastnikami w celu sondowania negocjacji": {"pat": -10, "avl": 0, "fin": -40, "comp": -25},
                    }
                }
            }
        },
        3: {
            "title": "🔴 FAZA OPERACYJNA: ETAP 3 - REKONWALESCENCJA I KONTROLA",
            "desc": "Dzień 3. Trwa powolne odtwarzanie środowiska informatycznego. Pod placówką parkują wozy transmisyjne. Do administracji zgłasza się kontrola z **Urzędu Ochrony Danych Osobowych (UODO)**.",
            "questions": {
                "IT": {
                    "label": "ZESPÓŁ IT / ARCHITEKTURA:",
                    "options": {
                        "Odbudowa sieci od podstaw z wdrożeniem pełnej mikrosegmentacji (czasochłonne)": {"pat": +10, "avl": -15, "fin": -20, "comp": +20},
                        "Szybkie łatanie luk i powrót do starej architektury w celu przywrócenia usług": {"pat": -20, "avl": +20, "fin": +10, "comp": -25},
                    }
                },
                "Med": {
                    "label": "PION PR I KOMUNIKACJI:",
                    "options": {
                        "Wydanie otwartego komunikatu o wycieku danych medycznych i start infolinii": {"pat": +10, "avl": 0, "fin": -10, "comp": +25},
                        "Zasłanianie się tajemnicą śledztwa i konsekwentna odmowa komentarzy": {"pat": -10, "avl": 0, "fin": -20, "comp": -20},
                    }
                },
                "Dir": {
                    "label": "SZTAB ZARZĄDZAJĄCY (DYREKCJA):",
                    "options": {
                        "Organizacja pilnych szkoleń antyphishingowych dla całego personelu": {"pat": +15, "avl": -5, "fin": -10, "comp": +15},
                        "Wstrzymanie szkoleń. Skupienie winy w mediach na zewnętrznym dostawcy antywirusa": {"pat": -15, "avl": 0, "fin": 0, "comp": -20},
                    }
                }
            }
        }
    },
    # (Poniżej skopiowane pozostałe warianty dla kompletności, struktura danych pozostaje bez zmian)
    "Wariant B: Atak na urządzenia medyczne IoT (3 Rundy)": {
        1: {"title": "🔴 FAZA OPERACYJNA: ETAP 1 - UTRATA SYNCHRONIZACJI APARATURY", "desc": "Godzina 03:00. OiTM. Kardiomonitory nagle tracą łączność z centralą. Dwie pompy infuzyjne zaczynają emitować fałszywe alarmy.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Natychmiastowe odcięcie sieci Wi-Fi dla urządzeń IoT": {"pat": +10, "avl": -20, "fin": -5, "comp": +5}, "Zdalny restart centrali (utrzymanie sieci)": {"pat": -15, "avl": +10, "fin": 0, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Przejście na manualne monitorowanie (100% obłożenia)": {"pat": +25, "avl": 0, "fin": -10, "comp": +10}, "Zignorowanie anomalii jako usterki sprzętu": {"pat": -40, "avl": 0, "fin": 0, "comp": -30}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Skierowanie dodatkowego personelu na OiTM": {"pat": +20, "avl": 0, "fin": -15, "comp": 0}, "Czekanie na raport z porannej zmiany": {"pat": -20, "avl": 0, "fin": 0, "comp": -10}}}}},
        2: {"title": "🔴 FAZA OPERACYJNA: ETAP 2 - SZANTAŻ NA ŻYCIU PACJENTÓW", "desc": "Godzina 05:00. Hakerzy grożą zdalną zmianą dawek leków w pompach infuzyjnych, jeśli nie zostanie wpłacony okup w ciągu 2 godzin.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Fizyczne wyciągnięcie kabli zasilających routery (Air-Gap)": {"pat": +20, "avl": -30, "fin": -5, "comp": +15}, "Próba lokalizacji złośliwego oprogramowania w sieci": {"pat": -30, "avl": -5, "fin": 0, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Odłączenie pomp i podawanie leków manualnie": {"pat": +25, "avl": -10, "fin": -5, "comp": +10}, "Ewakuacja całego OiTM do innego szpitala": {"pat": -15, "avl": -20, "fin": -30, "comp": +5}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Zgłoszenie incydentu do CSIRT GOV w trybie pilnym": {"pat": 0, "avl": 0, "fin": 0, "comp": +30}, "Zatajenie ataku i próba samodzielnej negocjacji": {"pat": -10, "avl": 0, "fin": -30, "comp": -40}}}}},
        3: {"title": "🔴 FAZA OPERACYJNA: ETAP 3 - DOCHODZENIE PO INCYDENCIE", "desc": "Dzień następny. Sieć zabezpieczona. Wykryto luki w oprogramowaniu starych pomp. NFZ grozi wstrzymaniem finansowania.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wydzielenie hermetycznej sieci VLAN dla IoMT": {"pat": +15, "avl": +10, "fin": -15, "comp": +20}, "Podłączenie sprzętu do ogólnej sieci po zmianie haseł": {"pat": -25, "avl": +20, "fin": +5, "comp": -30}}}, "Med": {"label": "PION PR:", "options": {"Zawieszenie ostrego dyżuru i szczera komunikacja": {"pat": +10, "avl": -15, "fin": -15, "comp": +10}, "Komunikowanie usterek technicznych, kontynuacja przyjęć": {"pat": -15, "avl": +10, "fin": +10, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Rozpoczęcie programu wymiany sprzętu medycznego": {"pat": +25, "avl": +10, "fin": -40, "comp": +20}, "Pozwanie producenta pomp o wadliwe oprogramowanie": {"pat": -5, "avl": 0, "fin": +15, "comp": 0}}}}}
    },
    "Wariant C: Zaawansowany Atak APT (5 Rund)": {
         1: {"title": "🔴 FAZA OPERACYJNA: ETAP 1 - NIEWINNE ANOMALIA CZY ZWIAD?", "desc": "Piątek, 09:00. Skargi lekarzy na powolne ładowanie zdjęć PACS. System pocztowy odrzuca hasła. Wykryto dziwny ruch wychodzący z serwera LIS.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Izolacja serwera LIS i reset haseł w administracji": {"pat": 0, "avl": -10, "fin": -5, "comp": +10}, "Tryb głębokiego monitorowania, praca bez przerw": {"pat": -5, "avl": +5, "fin": 0, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Ręczne opisywanie pilnych zdjęć RTG": {"pat": +10, "avl": 0, "fin": -5, "comp": 0}, "Oczekiwanie na stabilizację PACS": {"pat": -10, "avl": 0, "fin": 0, "comp": 0}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Zwołanie wstępnego, niejawnego sztabu kryzysowego": {"pat": +5, "avl": 0, "fin": -5, "comp": +5}, "Uznanie za awarię IT, brak działań zarządczych": {"pat": -10, "avl": 0, "fin": +5, "comp": -5}}}}},
         2: {"title": "🔴 FAZA OPERACYJNA: ETAP 2 - UDERZENIE I LATERAL MOVEMENT", "desc": "Piątek, 21:00. Czarne ekrany i żądanie 2 mln zł okupu. Hakerzy przejęli system BMS. Klimatyzacja na blokach operacyjnych wariuje.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Odcięcie głównego zasilania serwerowni i sieci (Blackout)": {"pat": -10, "avl": -40, "fin": -15, "comp": +20}, "Próba odzyskania kontroli nad BMS bez wyłączania sieci": {"pat": -30, "avl": -10, "fin": -10, "comp": -15}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Ewakuacja bloków operacyjnych, wentylacja ręczna": {"pat": +25, "avl": 0, "fin": -10, "comp": +10}, "Kontynuowanie operacji w niestabilnym środowisku": {"pat": -40, "avl": 0, "fin": -20, "comp": -30}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Zgłoszenie 'Zdarzenia Masowego', przekierowanie karetek": {"pat": +20, "avl": 0, "fin": -25, "comp": +20}, "Zakaz informowania mediów i wojewody": {"pat": -20, "avl": 0, "fin": +10, "comp": -35}}}}},
         3: {"title": "🔴 FAZA OPERACYJNA: ETAP 3 - SZANTAŻ MEDIALNY", "desc": "Sobota, 10:00. Publikacja fragmentu dokumentacji pacjenta VIP na Twitterze. Przed szpitalem wozy transmisyjne i zaniepokojone rodziny.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wynajęcie firmy Incident Response (wysokie koszty)": {"pat": +10, "avl": +15, "fin": -30, "comp": +20}, "Odtwarzanie siłami lokalnych informatyków": {"pat": -10, "avl": -10, "fin": +15, "comp": -10}}}, "Med": {"label": "PION PR:", "options": {"Wysłanie personelu na rozmowy z rodzinami": {"pat": +15, "avl": 0, "fin": -5, "comp": +10}, "Odmawianie dostępu 'ze względów bezpieczeństwa'": {"pat": -15, "avl": 0, "fin": 0, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Konferencja prasowa: przyznanie się do wycieku RODO": {"pat": +5, "avl": 0, "fin": -15, "comp": +25}, "Zablokowanie wypowiedzi, groźby pozwów": {"pat": -5, "avl": 0, "fin": +5, "comp": -30}}}}},
         4: {"title": "🔴 FAZA OPERACYJNA: ETAP 4 - PARALIŻ KLINICZNY", "desc": "Niedziela, 14:00. Skrajne wyczerpanie personelu. Podawanie leków z pamięci. Wkraczają kontrolerzy z MZ i UODO.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Przekazanie serwerów organom śledczym (dowody)": {"pat": -15, "avl": -20, "fin": 0, "comp": +30}, "Priorytet przywrócenia bazy leków (odmowa wydania sprzętu)": {"pat": +25, "avl": +20, "fin": -10, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Powołanie Komisji Etycznej (Triage leków ratujących życie)": {"pat": +15, "avl": 0, "fin": 0, "comp": +10}, "Podawanie leków losowo, unikanie odpowiedzialności": {"pat": -30, "avl": 0, "fin": 0, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Pełna współpraca z MZ i udostępnienie dokumentacji": {"pat": 0, "avl": 0, "fin": 0, "comp": +25}, "Wpuszczenie nadzoru tylko z prawnikami": {"pat": 0, "avl": 0, "fin": -20, "comp": -30}}}}},
         5: {"title": "🔴 FAZA OPERACYJNA: ETAP 5 - POST-MORTEM I ROZLICZENIE", "desc": "Dzień 7. Częściowe odzyskanie danych. Ogromne straty wizerunkowe. Raport końcowy organów nadzoru.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Migracja krytycznych systemów do Chmury Krajowej": {"pat": +10, "avl": +30, "fin": -30, "comp": +20}, "Odbudowa lokalnej serwerowni i zakup 'lepszego antywirusa'": {"pat": -10, "avl": -15, "fin": +15, "comp": -20}}}, "Med": {"label": "SZKOLENIA:", "options": {"Comiesięczne symulacje ataków (Downtime Drills)": {"pat": +20, "avl": 0, "fin": -10, "comp": +15}, "Jednorazowe szkolenie e-learningowe": {"pat": -15, "avl": 0, "fin": +5, "comp": -15}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Dyrektor składa dymisję, ułatwiając negocjacje finansowe": {"pat": 0, "avl": 0, "fin": +20, "comp": +10}, "Zwolnienie Głównego Informatyka jako manewr PR": {"pat": 0, "avl": 0, "fin": -10, "comp": -10}}}}}
    },
    "Wariant D: Niewidzialny Zabójca (Zatrucie Danych - 4 Rundy)": {
         1: {"title": "🔴 FAZA OPERACYJNA: ETAP 1 - PODEJRZANY BŁĄD DANYCH", "desc": "Wtorek, 11:00. Pielęgniarka wstrzymuje transfuzję - system pokazuje złą grupę krwi. Z bazy zniknęła informacja o śmiertelnej alergii pacjenta. Systemy działają płynnie.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Zablokowanie edycji w bazie (Read-Only) i audyt logów": {"pat": +10, "avl": -10, "fin": -5, "comp": +10}, "Restart serwera aplikacyjnego (traktowanie jako błąd)": {"pat": -20, "avl": +5, "fin": 0, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Wstrzymanie operacji do czasu weryfikacji krwi w laboratorium": {"pat": +25, "avl": 0, "fin": -15, "comp": +10}, "Kontynuowanie zabiegów, nakaz 'podwójnego sprawdzania'": {"pat": -30, "avl": 0, "fin": +5, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Poufne zgłoszenie na Policję (podejrzenie sabotażu)": {"pat": 0, "avl": 0, "fin": 0, "comp": +20}, "Czekanie na wewnętrzne wyjaśnienie sprawy": {"pat": 0, "avl": 0, "fin": +5, "comp": -15}}}}},
         2: {"title": "🔴 FAZA OPERACYJNA: ETAP 2 - EPIDEMIA NIEUFNOŚCI", "desc": "Wtorek, 16:00. Ktoś z uprawnieniami modyfikował setki wyników i dawek. Lekarze odmawiają podawania leków. Haker żąda 1 mln zł za listę zmienionych rekordów.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Przywrócenie bazy z backupu (utrata wpisów z ostatnich 48h)": {"pat": +10, "avl": -20, "fin": -10, "comp": +15}, "Próba ręcznego wyśledzenia złośliwych modyfikacji": {"pat": -25, "avl": +10, "fin": 0, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Masowe ponowne pobieranie krwi (gigantyczne koszty)": {"pat": +25, "avl": -10, "fin": -25, "comp": +10}, "Poleganie na starych, papierowych wydrukach z biurek": {"pat": -10, "avl": +5, "fin": +5, "comp": -10}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Transparentne powiadomienie MZ i pacjentów": {"pat": +10, "avl": 0, "fin": -25, "comp": +30}, "Zatajenie manipulacji jako 'awarii technicznej'": {"pat": -10, "avl": 0, "fin": +10, "comp": -40}}}}},
         3: {"title": "🔴 FAZA OPERACYJNA: ETAP 3 - KRET CZY PRZEJĘTE KONTO?", "desc": "Środa, 10:00. Służby informują o użyciu danych logowania ordynatora (brak 2FA, ofiara phishingu). Sprawa wypływa w mediach.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wymuszone natychmiastowe wdrożenie MFA (SMS) dla wszystkich": {"pat": +10, "avl": -15, "fin": -10, "comp": +25}, "Tylko masowy reset haseł na silniejsze": {"pat": -15, "avl": +10, "fin": +5, "comp": -15}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Szkolenie z cyberhigieny dla personelu (opóźnienia na izbie)": {"pat": +15, "avl": -10, "fin": -10, "comp": +15}, "Zostawienie personelu na stanowiskach, instrukcje mailem": {"pat": -10, "avl": +15, "fin": +5, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Ochrona oszukanego ordynatora, nacisk na naprawę procesów": {"pat": 0, "avl": 0, "fin": 0, "comp": +15}, "Zwolnienie ordynatora, zrzucenie winy": {"pat": -5, "avl": 0, "fin": +10, "comp": -15}}}}},
         4: {"title": "🔴 FAZA OPERACYJNA: ETAP 4 - ROZLICZENIE Z ZAUFANIA", "desc": "Czwartek, 12:00. Kryzys opanowany, ale pacjenci wytaczają pozwy zbiorowe o podanie niewłaściwych leków. Nadzór oczekuje wniosków.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wdrożenie systemu DLP i zaawansowanego monitorowania logów": {"pat": +15, "avl": +5, "fin": -25, "comp": +20}, "Brak większych zmian strukturalnych": {"pat": -20, "avl": +10, "fin": +15, "comp": -30}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Darmowe badania kontrolne dla pacjentów ze zmanipulowanej puli": {"pat": +25, "avl": -5, "fin": -30, "comp": +15}, "Oczekiwanie na pozwy, brak działań proaktywnych": {"pat": -10, "avl": +5, "fin": +10, "comp": -20}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Powołanie oficera ds. integralności danych klinicznych": {"pat": +10, "avl": 0, "fin": -10, "comp": +15}, "Wydatkowanie budżetu naprawczego na kampanię PR": {"pat": -10, "avl": 0, "fin": -15, "comp": -20}}}}}
    },
    "Wariant E: Przerwany Łańcuch (Atak na Telemedycynę - 4 Rundy)": {
         1: {"title": "🔴 FAZA OPERACYJNA: ETAP 1 - PARALIŻ ZEWNĘTRZNY", "desc": "Środa, 18:00. Padła zewnętrzna chmura dla radiologii zdalnej i platforma tele-monitoringu pacjentów kardiologicznych. Awaria po stronie dostawcy.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Natychmiastowe zerwanie VPN z chmurą dostawcy (Air-Gap)": {"pat": 0, "avl": -20, "fin": -5, "comp": +15}, "Utrzymanie aktywnych połączeń API w oczekiwaniu na naprawę": {"pat": -15, "avl": +5, "fin": 0, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Wezwanie lokalnych radiologów na nadgodziny do szpitala": {"pat": +20, "avl": +10, "fin": -25, "comp": +5}, "Wstrzymanie opisów planowych, diagnostyka tylko na ratunek życia": {"pat": -15, "avl": -10, "fin": +10, "comp": -5}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Wdrożenie papierowych procedur dla pacjentów z telemonitoringu": {"pat": +15, "avl": 0, "fin": -10, "comp": +10}, "Uznanie to za awarię techniczną dostawcy, brak aktywacji BCP": {"pat": -20, "avl": 0, "fin": +5, "comp": -15}}}}},
         2: {"title": "🔴 FAZA OPERACYJNA: ETAP 2 - ZARAZA PO ŁĄCZACH", "desc": "Środa, 22:00. Dostawca informuje o zainfekowaniu wirusem replikującym się przez API. Wyciekły dane telemetryczne pacjentów kardiologicznych.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Odcięcie całego szpitala od sieci Internet w celu skanowania": {"pat": -10, "avl": -30, "fin": -15, "comp": +25}, "Bieżąca aktualizacja antywirusa i blokowanie IP dostawcy": {"pat": -25, "avl": +15, "fin": 0, "comp": -20}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Wysłanie karetek po pacjentów kardiologicznych wysokiego ryzyka": {"pat": +30, "avl": 0, "fin": -30, "comp": +10}, "Wysłanie SMS-ów do pacjentów z prośbą o zgłaszanie złego samopoczucia": {"pat": -30, "avl": 0, "fin": +10, "comp": -15}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Zgłoszenie do UODO wycieku, przyjęcie roli administratora danych": {"pat": +10, "avl": 0, "fin": -5, "comp": +30}, "Przerzucanie odpowiedzialności na dostawcę, brak zgłoszeń do UODO": {"pat": 0, "avl": 0, "fin": 0, "comp": -35}}}}},
         3: {"title": "🔴 FAZA OPERACYJNA: ETAP 3 - ODPOWIEDZIALNOŚĆ STRON", "desc": "Czwartek, 08:00. Ostra krytyka w mediach dotycząca cięcia kosztów na cyberbezpieczeństwie. Wąskie gardła w radiologii paraliżują placówkę.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Wymóg audytów bezpieczeństwa TLPT od nowego dostawcy chmury": {"pat": +10, "avl": -10, "fin": -15, "comp": +25}, "Podpisanie najtańszej umowy bez audytu celem szybkiego powrotu usług": {"pat": -20, "avl": +25, "fin": +15, "comp": -30}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Osobiste, telefoniczne uspokajanie pacjentów kardiologicznych przez lekarzy": {"pat": +25, "avl": -5, "fin": -15, "comp": +15}, "Wydanie ogólnego oświadczenia na stronie www szpitala": {"pat": -15, "avl": 0, "fin": +5, "comp": -15}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Pozew sądowy o odszkodowanie i rozwiązanie umowy z dostawcą": {"pat": +5, "avl": 0, "fin": +10, "comp": +15}, "Kontynuacja umowy przy rekompensacie 'darmowego roku'": {"pat": -25, "avl": +10, "fin": +25, "comp": -25}}}}},
         4: {"title": "🔴 FAZA OPERACYJNA: ETAP 4 - NOWA ARCHITEKTURA", "desc": "Piątek. Konieczność przedstawienia Ministerstwu Zdrowia planu zarządzania ryzykiem łańcucha dostaw.", "questions": {"IT": {"label": "ZESPÓŁ IT:", "options": {"Strategia Multi-Cloud (wielu dostawców) z systemem Failover": {"pat": +15, "avl": +20, "fin": -35, "comp": +20}, "Wycofanie się do technologii lokalnej (serwery szpitalne)": {"pat": -10, "avl": -15, "fin": -10, "comp": -10}}}, "Med": {"label": "PION MEDYCZNY:", "options": {"Fizyczne plany awaryjne (BCP) dla wdrażanej aparatury cyfrowej": {"pat": +20, "avl": 0, "fin": -10, "comp": +20}, "Redukcja aparatury analogowej dla cięcia kosztów": {"pat": -25, "avl": +10, "fin": +20, "comp": -25}}}, "Dir": {"label": "SZTAB ZARZĄDZAJĄCY:", "options": {"Powołanie Działu Zarządzania Ryzykiem Stron Trzecich (wymóg DORA/NIS2)": {"pat": +15, "avl": 0, "fin": -15, "comp": +25}, "Weryfikacja bezpieczeństwa vendora wyłącznie przez Dział Zakupów": {"pat": -20, "avl": 0, "fin": +15, "comp": -30}}}}}
    }
}

# --- FUNKCJE POMOCNICZE ---
def calculate_score(team_name):
    pat, avl, fin, comp = 100, 100, 100, 100
    active_scenario_data = ALL_SCENARIOS[state["active_scenario"]]
    
    for r in range(1, state["round"] + 1):
        if r in state["teams"][team_name]["decisions"] and r in active_scenario_data:
            for role, choice in state["teams"][team_name]["decisions"][r].items():
                impact = active_scenario_data[r]["questions"][role]["options"][choice]
                pat += impact["pat"]
                avl += impact["avl"]
                fin += impact["fin"]
                comp += impact["comp"]
    return max(0, min(150, pat)), max(0, min(150, avl)), max(0, min(150, fin)), max(0, min(150, comp))

def get_status_text(val, is_critical=False):
    if is_critical:
        if val > 80: return "STABILNY", "kpi-status-green"
        if val > 50: return "OSTRZEŻENIE", "kpi-status-yellow"
        return "KRYTYCZNY", "kpi-status-red"
    else:
        if val > 70: return "W NORMIE", "kpi-status-green"
        if val > 40: return "RYZYKO", "kpi-status-yellow"
        return "ZAGROŻENIE", "kpi-status-red"

def render_kpi_card(icon, label, value, is_critical=False):
    status_text, status_class = get_status_text(value, is_critical)
    # Procent wypełnienia paska
    pct = min((value/150)*100, 100)
    
    # Kolor paska
    bar_color = "#48BB78" if "green" in status_class else "#ECC94B" if "yellow" in status_class else "#F56565"

    html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{icon} {label}</div>
        <div class="{status_class}">{status_text}</div>
        <div class="progress-bg">
            <div class="progress-bar" style="width: {pct}%; background-color: {bar_color};"></div>
        </div>
        <div style="font-size: 12px; color: #A0AEC0; margin-top: 5px;">{value} / 150 PKT</div>
    </div>
    """
    return html

# --- WIDOKI ---
def login_view():
    st.markdown("<div style='text-align: center; margin-top: 50px;'><h1 style='color: #E2E8F0;'>📡 SYSTEM ŁĄCZNOŚCI SZTABOWEJ</h1><p style='color: #A0AEC0; font-size: 18px;'>Autoryzacja dostępu do Centrum Operacyjnego</p></div>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<div style='background-color: #2D3748; padding: 30px; border-radius: 10px; border: 1px solid #4A5568;'>", unsafe_allow_html=True)
        team_name = st.text_input("KRYPTONIM JEDNOSTKI (NAZWA SZPITALA):")
        if st.button("AUTORYZUJ DOSTĘP KRYZYSOWY", use_container_width=True, type="primary"):
            if team_name:
                if team_name not in state["teams"]:
                    state["teams"][team_name] = {"decisions": {}, "ready": False}
                st.session_state["role"] = "team"
                st.session_state["team_name"] = team_name
                st.rerun()
            else:
                st.error("Odmowa. Wprowadź identyfikator.")
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.write("<br><br>", unsafe_allow_html=True)
        with st.expander("🔑 Dostęp Poziomu Administratora (Dowództwo)"):
            admin_pass = st.text_input("Klucz szyfrujący:", type="password")
            if st.button("Uruchom Konsolę Dowodzenia"):
                if admin_pass == "admin":
                    st.session_state["role"] = "admin"
                    st.rerun()

def admin_view():
    st.title("👨‍⚕️ Konsola Dowodzenia (Master Control)")
    
    if state["round"] == 0:
        st.warning("Oczekuj na zalogowanie jednostek.")
        selected = st.selectbox("Wybierz scenariusz kryzysowy:", list(ALL_SCENARIOS.keys()), index=list(ALL_SCENARIOS.keys()).index(state["active_scenario"]))
        if selected != state["active_scenario"]:
            state["active_scenario"] = selected
            st.success(f"Aktywowano: {selected}")
    else:
        st.info(f"Aktywny incydent: **{state['active_scenario']}**")
    
    col1, col2 = st.columns(2)
    with col1:
        total_rounds = len(ALL_SCENARIOS[state["active_scenario"]])
        is_finished = state["round"] > total_rounds
        st.metric("Faza Operacyjna", state["round"] if not is_finished else "Zakończono")
        if not is_finished:
            if st.button("Transmisja: Następny Etap ⏩", type="primary"):
                state["round"] += 1
                for t in state["teams"]: state["teams"][t]["ready"] = False
                st.rerun()
        else:
            if st.button("Zakończ Symulację 🔄"):
                state["round"] = 0
                state["teams"] = {}
                st.rerun()
                
    with col2:
        st.write("### Gotowość Sztabów Lokalnych")
        for t, data in state["teams"].items():
            status = "✅ Zatwierdzono" if data["ready"] else "⏳ Oczekiwanie na decyzje..."
            st.write(f"- **{t}**: {status}")

    st.write("---")
    if state["teams"]:
        scores = []
        for t in state["teams"]:
            p, a, f, c = calculate_score(t)
            scores.append({"Placówka": t, "Pacjenci": p, "Systemy": a, "Finanse": f, "Zgodność": c})
        st.dataframe(pd.DataFrame(scores), use_container_width=True)

def team_view():
    team = st.session_state["team_name"]
    total_rounds = len(ALL_SCENARIOS[state["active_scenario"]])
    
    # 1. Pasek Nagłówka (Top Bar)
    colA, colB = st.columns([3, 1])
    with colA:
        st.markdown(f"<div style='font-size: 24px; font-weight: bold; color: #E2E8F0; padding-top: 5px;'>🏥 SZTAB KRYZYSOWY: {team.upper()}</div>", unsafe_allow_html=True)
    with colB:
        if st.button("📡 SYNCHRONIZUJ DANE", use_container_width=True):
            st.rerun()
            
    st.write("<br>", unsafe_allow_html=True)
    
    # 2. Wskaźniki Krytyczne (KPI Cards)
    p, a, f, c = calculate_score(team)
    
    kpi_html = f"""
    <div class="kpi-container">
        {render_kpi_card("❤️", "PACJENCI", p, is_critical=True)}
        {render_kpi_card("🖥️", "SYSTEMY IT", a)}
        {render_kpi_card("💰", "FINANSE I PR", f)}
        {render_kpi_card("⚖️", "ZGODNOŚĆ PRAWNA", c)}
    </div>
    """
    st.markdown(kpi_html, unsafe_allow_html=True)

    # 3 i 4. Faza Operacyjna i Decyzje
    if state["round"] == 0:
        st.markdown("<div class='sitrep-box'><div class='sitrep-title'>🔴 FAZA OPERACYJNA: ETAP 0 - OCZEKIWANIE</div><span style='color: #E2E8F0;'>Trwa spokojny dyżur. Wszystkie systemy podtrzymywania życia i rejestracji pacjentów funkcjonują prawidłowo. Personel nie zgłasza żadnych anomalii. Sztab w trybie nasłuchu.</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='alert-box'><div class='alert-title'>⚠️ KANAŁ ALERTÓW:</div>[Brak nowych powiadomień krytycznych z oddziałów]</div>", unsafe_allow_html=True)
        
    elif 1 <= state["round"] <= total_rounds:
        r = state["round"]
        scenario = ALL_SCENARIOS[state["active_scenario"]][r]
        
        # Sekcja Sytuacyjna
        st.markdown(f"<div class='sitrep-box'><div class='sitrep-title'>{scenario['title']}</div><span style='color: #E2E8F0;'>{scenario['desc']}</span></div>", unsafe_allow_html=True)
        st.markdown("<div class='alert-box'><div class='alert-title'>⚠️ KANAŁ ALERTÓW:</div>Oczekuję na wytyczne Dowództwa. Konieczne podjęcie skoordynowanych akcji.</div>", unsafe_allow_html=True)
        
        # Sekcja Decyzyjna
        st.markdown("<div class='decision-header'>⚡ WYMAGANE DECYZJE SZTABU</div>", unsafe_allow_html=True)
        
        if state["teams"][team]["ready"]:
            st.success("Rozkazy przekazane do realizacji. Sztab w trybie oczekiwania na rozwój zdarzeń.")
        else:
            with st.form(f"form_r{r}"):
                choices = {}
                # Wyświetlamy decyzje jako bloki, a nie ciasne listy
                for role, q_data in scenario["questions"].items():
                    st.markdown(f"<span style='color: #63B3ED; font-weight: bold;'>{q_data['label']}</span>", unsafe_allow_html=True)
                    choices[role] = st.radio(f"Wybór {role}", list(q_data["options"].keys()), label_visibility="collapsed")
                    st.write("<br>", unsafe_allow_html=True)
                
                if st.form_submit_button("ZATWIERDŹ I WPROWADŹ ROZKAZY DO SYSTEMU 📝", type="primary"):
                    if r not in state["teams"][team]["decisions"]:
                        state["teams"][team]["decisions"][r] = {}
                    state["teams"][team]["decisions"][r] = choices
                    state["teams"][team]["ready"] = True
                    st.rerun()

    elif state["round"] > total_rounds:
        st.markdown("<div class='sitrep-box' style='border-left: 5px solid #48BB78;'><div class='sitrep-title' style='color: #48BB78;'>🟢 FAZA OPERACYJNA: ZAKOŃCZONO</div><span style='color: #E2E8F0;'>Stan wyjątkowy odwołany. Rozpoczyna się faza audytu pokontrolnego.</span></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='decision-header'>📋 WYNIK AUDYTU ORGANÓW NADZORCZYCH</div>", unsafe_allow_html=True)
        if p < 50:
            st.error("Wyrok Prokuratora: ZAGROŻENIE ŻYCIA PACJENTÓW. Oczekuj aktu oskarżenia.")
        elif c < 50:
            st.error("Wyrok Regulatora: KATASTROFA PRAWNA. Nałożono maksymalne kary finansowe (RODO/NIS2).")
        elif p >= 80 and c >= 80:
            st.success("Wyrok: MISTRZOWSKIE ZARZĄDZANIE KRYZYSEM. Infrastruktura i pacjenci zabezpieczeni.")
        else:
            st.warning("Wyrok: SZPITAL PRZETRWAŁ Z DUŻYMI STRATAMI. Decyzje operacyjne wymagały kompromisów.")

if "role" not in st.session_state:
    login_view()
elif st.session_state["role"] == "admin":
    admin_view()
elif st.session_state["role"] == "team":
    team_view()