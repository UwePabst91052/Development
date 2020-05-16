# Beispiel 12.1
#
# Eine einfaches Beispiel zum Experimentieren
#
import Auto


def main():
    # Hauptprogramm
    auto_eins = Auto.Auto("Kia", "Silber", 50, 3)

    print("\nDaten von Auto eins:")
    auto_eins.zeige_daten()

    print("\nDie Autos fahren ein wenig durch die Gegend...")

    auto_eins.strecke_fahren(64)

    print("Kilometerstand des ersten Autos:", auto_eins.kilometerstand)


main()
