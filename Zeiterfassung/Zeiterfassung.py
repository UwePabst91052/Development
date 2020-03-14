import Workpackage as Wp
import datetime as dt
import os
from StoreWorkpackages import write_workpackage
from StoreWorkpackages import open_tag
from StoreWorkpackages import close_tag
from ReadWorkpackes import read_workpackages
from BerichtAusdrucken import report_work_summary
from BerichtAnzeigen import display_report


def select_main_menu():
    print("Bitte wählen Sie.\n")
    print("    1...Arbeitspaket hinzufügen")
    print("    2...Beginne mit Arbeitspaket")
    print("    3...Beende Arbeit")
    print("    4...Was wurde an bestimmten Tag gearbeitet")
    print("    5...Wieviel wurde für Arbeitspaket gearbeitet")
    print("    6...Speichere unter...")
    print("    7...Öffne Datei...")
    print("    8...Bericht nach Arbeitstagen geordnet")
    print("    x...Beenden\n")
    return input("Auswahl: ")


def select_workpackage(workpackages):
    ix = 0
    for wp in workpackages:
        print("{0}. {1}".format(ix, wp.wp_name))
        ix += 1

    return workpackages[int((input("Wählen Sie: ")))]


def select_date(workpackages):
    ix = 0
    dates = []
    for wp in workpackages:
        for wd in wp.workdays:
            print("{0}. {1}".format(ix, str(wd.date)))
            dates.append(str(wd.date))
            ix += 1
    return dates[int(input("Wählen Sie: "))]


def select_file():
    ix = 0
    files = os.listdir('./Dateien')
    for file in files:
        print("{0}. {1}".format(ix, file))
        ix += 1
    return files[int(input("Wählen Siie: "))]


def input_time():
    time_str = dt.datetime.now().strftime("%H:%M:%S")
    time_in = input("Übernehmen Sie {0} mit <Enter> \noder geben Sie eine Zeit ein: ".format(time_str))
    if time_in == "":
        return time_str
    else:
        return time_in


def input_date():
    date_str = dt.date.today().strftime("%d.%m.%Y")
    date_in = input("Übernehmen Sie {0} mit <Enter> \noder geben Sie Datum ein: ".format(date_str))
    if date_in == "":
        return date_str
    else:
        return date_in


def main():
    workpackages = []
    wp_cur = None
    while True:
        cmd = select_main_menu()
        if cmd == '1':
            name = input("Name des Arbeitspaketes: ")
            wp_cur = Wp.Workpackage(name)
            wp_cur.add_workday(dt.date.today().strftime("%d.%m."))
            workpackages.append(wp_cur)
        elif cmd == '2':
            wp_cur = select_workpackage(workpackages)
            print("Sie arbeiten gerade an \"{0}\"".format(wp_cur.wp_name))
            time_str = input_time()
            wp_cur.add_workday(dt.date.today().strftime("%d.%m."))
            wp_cur.begin_working(time_str)
        elif cmd == '3':
            print("Sie arbeiten gerade an \"{0}\"".format(wp_cur.wp_name))
            time_str = input_time()
            wp_cur.finish_working(time_str)
        elif cmd == '4':
            duration = 0
            wpckgs = []
            date_str = select_date(workpackages)
            for wp in workpackages:
                for wd in wp.workdays:
                    if str(wd.date) == date_str:
                        wpckgs.append(wp)
                        duration += wd.get_duration()
            print("Sie haben am {0} {1} Stunden gearbeitet:".format(date_str,
                                                                    Wp.Time.convert_seconds_to_time_string(duration)))
            for wp in wpckgs:
                wp.duration_for_date(date_str)
        elif cmd == '5':
            wp_cur = select_workpackage(workpackages)
            print(wp_cur)
        elif cmd == '6':
            filename = input("Geben Sie den Dateinamen ein: ")
            filename = "Dateien/" + filename + ".xml"
            file = open(filename, "w", encoding="utf-8")
            open_tag(file, "Zeiterfassung")
            for wp in workpackages:
                write_workpackage(file, wp)
            close_tag(file, "Zeiterfassung")
            file.close()
        elif cmd == '7':
            filename = select_file()
            filename = "Dateien/" + filename
            file = open(filename, encoding="utf-8")
            workpackages = read_workpackages(file)
            file.close()
        elif cmd == '8':
            report = report_work_summary( 'Uwe Pabst', workpackages )
            display_report(report)
        else:
            break


main()
