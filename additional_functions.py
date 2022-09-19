from datetime import datetime

def open_file(config):
    """
    Funkcja otwierająca strumień do pliku.

    Parameters
    ----------
    config : ConfigParser
        Zmienna z danymi konfiguracyjnymi.

    Returns
    -------
    file : TextIOWrapper
        Otwarty stream do pliku.

    """
    file = None
    now = datetime.now()
    now = now.strftime("%d_%m_%Y_%H_%M_%S")
    name = 'data'
    path = config.load_value_from_config_str('file_dir', 'data')
    file = open(f"{path}/{name}_{now}.csv", "w+", encoding="utf-8")
    file.write("Data,Czas,Time_Stamp,X,Y,Z,M1,M2,G\n")
    file.flush()
    return file

def close_file(file):
    """
    Funkcja zamykająca stream do pliku.

    Parameters
    ----------
    file : TextIOWrapper
        Otwarty stream do pliku.

    """
    if file is not None:
        file.close()
    file = None
    return file

def write_to_file(file, data):
    """
    Funkcja zapisująca informacje do pliku

    Parameters
    ----------
    file : TextIOWrapper
        Otwarty stream do pliku.
    data : list
        Lista wyników do zapisania.

    """
    file.write("".join(str(x) for x in data if x is not None))
    file.flush()